"""
LLM Client for Jumpchain Engine
Supports: LM Studio (local), OpenRouter (API), Anthropic (API)
"""

import requests
import json
import logging
from typing import Dict, List, Optional, Union
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class LLMResponse:
    """Response from an LLM"""
    content: str
    model: str
    tokens_used: int
    cost_usd: float
    latency_ms: float


@dataclass
class UsageStats:
    """Track LLM usage and costs"""
    model: str
    total_tokens: int
    total_cost_usd: float
    call_count: int


class LLMClient:
    """Universal LLM client for multiple providers"""

    # Cost per 1M tokens (input)
    COSTS = {
        'glm-4-air': 0.0,  # Local, free
        'google/glm-4-plus': 0.002,  # $2/1M via OpenRouter
        'claude-sonnet-4.5': 0.003,  # $3/1M input
        'claude-sonnet-4-5': 0.003,  # Alternative name
    }

    def __init__(self, config):
        """
        Initialize LLM client

        Args:
            config: Config object with LLM endpoints
        """
        self.config = config
        self.usage_stats = {}
        self.load_usage_stats()

    def load_usage_stats(self):
        """Load usage statistics from file"""
        try:
            with open('data/llm_usage.json', 'r') as f:
                data = json.load(f)
                for model, stats in data.items():
                    self.usage_stats[model] = UsageStats(**stats)
        except FileNotFoundError:
            logger.info("No existing usage stats found, starting fresh")

    def save_usage_stats(self):
        """Save usage statistics to file"""
        data = {
            model: {
                'model': stats.model,
                'total_tokens': stats.total_tokens,
                'total_cost_usd': stats.total_cost_usd,
                'call_count': stats.call_count
            }
            for model, stats in self.usage_stats.items()
        }

        with open('data/llm_usage.json', 'w') as f:
            json.dump(data, f, indent=2)

    def call(self,
             model_type: str,
             prompt: str,
             system_prompt: Optional[str] = None,
             max_tokens: int = 1000,
             temperature: float = 0.7) -> LLMResponse:
        """
        Call an LLM

        Args:
            model_type: 'local_fast', 'analytical', or 'master_narrator'
            prompt: User prompt
            system_prompt: Optional system prompt
            max_tokens: Max response tokens
            temperature: Sampling temperature

        Returns:
            LLMResponse object
        """
        import time
        start_time = time.time()

        # Get config for this model type
        llm_config = self.config.get('llm_endpoints', model_type)

        if not llm_config:
            raise ValueError(f"No config found for model type: {model_type}")

        endpoint = llm_config.get('endpoint')
        model = llm_config.get('model')
        api_key = llm_config.get('api_key', '')

        # Determine provider type
        if 'anthropic.com' in endpoint:
            response = self._call_anthropic(
                endpoint, model, api_key, prompt, system_prompt, max_tokens, temperature
            )
        else:
            # OpenAI-compatible (LM Studio, OpenRouter, etc.)
            response = self._call_openai_compatible(
                endpoint, model, api_key, prompt, system_prompt, max_tokens, temperature
            )

        latency_ms = (time.time() - start_time) * 1000

        # Calculate cost
        cost = self._calculate_cost(model, response['tokens_used'])

        # Update usage stats
        self._update_usage(model, response['tokens_used'], cost)

        return LLMResponse(
            content=response['content'],
            model=model,
            tokens_used=response['tokens_used'],
            cost_usd=cost,
            latency_ms=latency_ms
        )

    def _call_openai_compatible(self,
                                endpoint: str,
                                model: str,
                                api_key: str,
                                prompt: str,
                                system_prompt: Optional[str],
                                max_tokens: int,
                                temperature: float) -> Dict:
        """Call OpenAI-compatible API (LM Studio, OpenRouter)"""

        messages = []

        if system_prompt:
            messages.append({
                'role': 'system',
                'content': system_prompt
            })

        messages.append({
            'role': 'user',
            'content': prompt
        })

        headers = {
            'Content-Type': 'application/json'
        }

        if api_key:
            headers['Authorization'] = f'Bearer {api_key}'

        data = {
            'model': model,
            'messages': messages,
            'max_tokens': max_tokens,
            'temperature': temperature
        }

        try:
            response = requests.post(endpoint, headers=headers, json=data, timeout=60)
            response.raise_for_status()
            result = response.json()

            content = result['choices'][0]['message']['content']
            tokens = result.get('usage', {}).get('total_tokens', 0)

            return {
                'content': content,
                'tokens_used': tokens
            }

        except Exception as e:
            logger.error(f"Error calling {model}: {e}")
            raise

    def _call_anthropic(self,
                       endpoint: str,
                       model: str,
                       api_key: str,
                       prompt: str,
                       system_prompt: Optional[str],
                       max_tokens: int,
                       temperature: float) -> Dict:
        """Call Anthropic API (Claude)"""

        headers = {
            'Content-Type': 'application/json',
            'x-api-key': api_key,
            'anthropic-version': '2023-06-01'
        }

        data = {
            'model': model,
            'max_tokens': max_tokens,
            'temperature': temperature,
            'messages': [
                {
                    'role': 'user',
                    'content': prompt
                }
            ]
        }

        if system_prompt:
            data['system'] = system_prompt

        try:
            response = requests.post(endpoint, headers=headers, json=data, timeout=60)
            response.raise_for_status()
            result = response.json()

            content = result['content'][0]['text']
            tokens_in = result.get('usage', {}).get('input_tokens', 0)
            tokens_out = result.get('usage', {}).get('output_tokens', 0)
            tokens = tokens_in + tokens_out

            return {
                'content': content,
                'tokens_used': tokens
            }

        except Exception as e:
            logger.error(f"Error calling Claude: {e}")
            raise

    def _calculate_cost(self, model: str, tokens: int) -> float:
        """Calculate cost in USD"""
        # Get cost per 1M tokens
        cost_per_million = self.COSTS.get(model, 0.0)

        # Calculate actual cost
        cost = (tokens / 1_000_000) * cost_per_million

        return cost

    def _update_usage(self, model: str, tokens: int, cost: float):
        """Update usage statistics"""
        if model not in self.usage_stats:
            self.usage_stats[model] = UsageStats(
                model=model,
                total_tokens=0,
                total_cost_usd=0.0,
                call_count=0
            )

        stats = self.usage_stats[model]
        stats.total_tokens += tokens
        stats.total_cost_usd += cost
        stats.call_count += 1

        # Save after each call
        self.save_usage_stats()

    def get_usage_summary(self) -> Dict:
        """Get usage summary for all models"""
        summary = {}

        for model, stats in self.usage_stats.items():
            summary[model] = {
                'total_tokens': stats.total_tokens,
                'total_cost_usd': round(stats.total_cost_usd, 2),
                'call_count': stats.call_count,
                'avg_tokens_per_call': round(stats.total_tokens / stats.call_count) if stats.call_count > 0 else 0
            }

        summary['total_cost'] = round(sum(s.total_cost_usd for s in self.usage_stats.values()), 2)

        return summary

    def estimate_cost(self, model_type: str, estimated_tokens: int) -> float:
        """Estimate cost before making a call"""
        llm_config = self.config.get('llm_endpoints', model_type)
        model = llm_config.get('model')

        return self._calculate_cost(model, estimated_tokens)

    def quick_call(self, prompt: str) -> str:
        """Quick call to local model"""
        response = self.call(
            model_type='local_fast',
            prompt=prompt,
            max_tokens=500,
            temperature=0.7
        )
        return response.content

    def analytical_call(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """Call analytical model (GLM 4.6)"""
        response = self.call(
            model_type='analytical',
            prompt=prompt,
            system_prompt=system_prompt,
            max_tokens=1500,
            temperature=0.7
        )
        return response.content

    def deep_call(self, prompt: str, system_prompt: Optional[str] = None,
                  max_tokens: int = 2000) -> LLMResponse:
        """Deep call to Claude Sonnet 4.5 (returns full response for cost tracking)"""
        return self.call(
            model_type='master_narrator',
            prompt=prompt,
            system_prompt=system_prompt,
            max_tokens=max_tokens,
            temperature=0.8  # Slightly higher for creative narration
        )

    def confirm_expensive_call(self, model_type: str, estimated_tokens: int) -> bool:
        """Ask user to confirm expensive API call"""
        cost = self.estimate_cost(model_type, estimated_tokens)

        if cost > 0.05:  # More than 5 cents
            print(f"\n⚠️  This operation will cost approximately ${cost:.2f}")
            print(f"   Estimated tokens: ~{estimated_tokens}")
            response = input("   Proceed? [y/N]: ").strip().lower()
            return response == 'y'

        return True  # Auto-approve cheap calls
