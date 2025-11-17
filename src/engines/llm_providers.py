"""
Modular LLM Provider System
Supports: Z.AI (GLM), LM Studio, OpenRouter, Anthropic
Designed to be reusable across multiple applications
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


@dataclass
class LLMResponse:
    """Standardized response from any LLM provider"""
    content: str
    model: str
    provider: str
    tokens_used: int
    cost_usd: float
    latency_ms: float
    finish_reason: str = "stop"

    def to_dict(self) -> Dict:
        return {
            'content': self.content,
            'model': self.model,
            'provider': self.provider,
            'tokens_used': self.tokens_used,
            'cost_usd': self.cost_usd,
            'latency_ms': self.latency_ms,
            'finish_reason': self.finish_reason
        }


class BaseLLMProvider(ABC):
    """Abstract base class for LLM providers"""

    def __init__(self, api_key: str = "", endpoint: str = "", **kwargs):
        self.api_key = api_key
        self.endpoint = endpoint
        self.extra_config = kwargs

    @abstractmethod
    def call(self,
             prompt: str,
             system_prompt: Optional[str] = None,
             max_tokens: int = 1000,
             temperature: float = 0.7,
             stream: bool = False,
             **kwargs) -> LLMResponse:
        """Make a call to the LLM"""
        pass

    @abstractmethod
    def get_cost_per_token(self, model: str) -> float:
        """Get cost per token for a model"""
        pass

    @abstractmethod
    def supports_streaming(self) -> bool:
        """Check if provider supports streaming"""
        pass


class ZAIProvider(BaseLLMProvider):
    """Z.AI (GLM) provider using official SDK"""

    MODELS = {
        'glm-4-air': 0.0,  # Free tier
        'glm-4.6': 0.000001,  # $1 per 1M tokens
        'glm-4-plus': 0.00005,  # $50 per 1M tokens
    }

    def __init__(self, api_key: str = "", **kwargs):
        super().__init__(api_key, "https://api.z.ai/api/paas/v4/", **kwargs)
        self.client = None

    def _get_client(self):
        """Lazy load Z.AI client"""
        if self.client is None:
            try:
                from zai import ZaiClient
                self.client = ZaiClient(api_key=self.api_key)
            except ImportError:
                raise ImportError(
                    "Z.AI SDK not installed. Install with: pip install zai-sdk"
                )
        return self.client

    def call(self,
             prompt: str,
             system_prompt: Optional[str] = None,
             max_tokens: int = 1000,
             temperature: float = 0.7,
             stream: bool = False,
             model: str = "glm-4.6",
             **kwargs) -> LLMResponse:
        """Call Z.AI API"""
        import time
        start_time = time.time()

        client = self._get_client()

        # Build messages
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        try:
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
                stream=stream,
                **kwargs
            )

            if stream:
                # Handle streaming separately
                return self._handle_stream(response, model, start_time)

            # Extract response
            content = response.choices[0].message.content
            tokens = getattr(response.usage, 'total_tokens', 0)
            finish_reason = response.choices[0].finish_reason

            latency_ms = (time.time() - start_time) * 1000
            cost = self._calculate_cost(model, tokens)

            return LLMResponse(
                content=content,
                model=model,
                provider="z.ai",
                tokens_used=tokens,
                cost_usd=cost,
                latency_ms=latency_ms,
                finish_reason=finish_reason
            )

        except Exception as e:
            logger.error(f"Z.AI API error: {e}")
            raise

    def _handle_stream(self, stream, model, start_time):
        """Handle streaming response"""
        full_content = ""
        total_tokens = 0

        for chunk in stream:
            if chunk.choices[0].delta.content:
                full_content += chunk.choices[0].delta.content
                total_tokens += 1  # Approximate

        latency_ms = (time.time() - start_time) * 1000
        cost = self._calculate_cost(model, total_tokens)

        return LLMResponse(
            content=full_content,
            model=model,
            provider="z.ai",
            tokens_used=total_tokens,
            cost_usd=cost,
            latency_ms=latency_ms
        )

    def _calculate_cost(self, model: str, tokens: int) -> float:
        """Calculate cost for tokens"""
        cost_per_token = self.MODELS.get(model, 0.0)
        return tokens * cost_per_token

    def get_cost_per_token(self, model: str) -> float:
        """Get cost per token"""
        return self.MODELS.get(model, 0.0)

    def supports_streaming(self) -> bool:
        return True


class LMStudioProvider(BaseLLMProvider):
    """LM Studio local provider (OpenAI-compatible)"""

    def __init__(self, endpoint: str = "http://localhost:1234/v1/chat/completions", **kwargs):
        super().__init__("", endpoint, **kwargs)

    def call(self,
             prompt: str,
             system_prompt: Optional[str] = None,
             max_tokens: int = 1000,
             temperature: float = 0.7,
             stream: bool = False,
             model: str = "local-model",
             **kwargs) -> LLMResponse:
        """Call LM Studio local API"""
        import requests
        import time

        start_time = time.time()

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        data = {
            "model": model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "stream": stream
        }

        try:
            response = requests.post(
                self.endpoint,
                json=data,
                timeout=120,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            result = response.json()

            content = result['choices'][0]['message']['content']
            tokens = result.get('usage', {}).get('total_tokens', 0)

            latency_ms = (time.time() - start_time) * 1000

            return LLMResponse(
                content=content,
                model=model,
                provider="lm_studio",
                tokens_used=tokens,
                cost_usd=0.0,  # Local is free
                latency_ms=latency_ms
            )

        except Exception as e:
            logger.error(f"LM Studio error: {e}")
            raise

    def get_cost_per_token(self, model: str) -> float:
        return 0.0  # Local is free

    def supports_streaming(self) -> bool:
        return True


class OpenRouterProvider(BaseLLMProvider):
    """OpenRouter provider for various models"""

    MODELS = {
        'google/glm-4-plus': 0.002,  # $2 per 1M
        'anthropic/claude-sonnet-4-5': 0.003,  # $3 per 1M
    }

    def __init__(self, api_key: str = "", **kwargs):
        super().__init__(api_key, "https://openrouter.ai/api/v1/chat/completions", **kwargs)

    def call(self,
             prompt: str,
             system_prompt: Optional[str] = None,
             max_tokens: int = 1000,
             temperature: float = 0.7,
             stream: bool = False,
             model: str = "google/glm-4-plus",
             **kwargs) -> LLMResponse:
        """Call OpenRouter API"""
        import requests
        import time

        start_time = time.time()

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        data = {
            "model": model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature
        }

        try:
            response = requests.post(
                self.endpoint,
                json=data,
                headers=headers,
                timeout=120
            )
            response.raise_for_status()
            result = response.json()

            content = result['choices'][0]['message']['content']
            tokens = result.get('usage', {}).get('total_tokens', 0)

            latency_ms = (time.time() - start_time) * 1000
            cost = self._calculate_cost(model, tokens)

            return LLMResponse(
                content=content,
                model=model,
                provider="openrouter",
                tokens_used=tokens,
                cost_usd=cost,
                latency_ms=latency_ms
            )

        except Exception as e:
            logger.error(f"OpenRouter error: {e}")
            raise

    def _calculate_cost(self, model: str, tokens: int) -> float:
        cost_per_token = self.MODELS.get(model, 0.0)
        return tokens * cost_per_token

    def get_cost_per_token(self, model: str) -> float:
        return self.MODELS.get(model, 0.0)

    def supports_streaming(self) -> bool:
        return True


class AnthropicProvider(BaseLLMProvider):
    """Anthropic (Claude) provider"""

    MODELS = {
        'claude-sonnet-4-5': 0.003,  # $3 per 1M input
        'claude-sonnet-4.5': 0.003,
    }

    def __init__(self, api_key: str = "", **kwargs):
        super().__init__(api_key, "https://api.anthropic.com/v1/messages", **kwargs)

    def call(self,
             prompt: str,
             system_prompt: Optional[str] = None,
             max_tokens: int = 1000,
             temperature: float = 0.7,
             stream: bool = False,
             model: str = "claude-sonnet-4-5",
             **kwargs) -> LLMResponse:
        """Call Anthropic API"""
        import requests
        import time

        start_time = time.time()

        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json"
        }

        data = {
            "model": model,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }

        if system_prompt:
            data["system"] = system_prompt

        try:
            response = requests.post(
                self.endpoint,
                json=data,
                headers=headers,
                timeout=120
            )
            response.raise_for_status()
            result = response.json()

            content = result['content'][0]['text']
            tokens_in = result.get('usage', {}).get('input_tokens', 0)
            tokens_out = result.get('usage', {}).get('output_tokens', 0)
            tokens = tokens_in + tokens_out

            latency_ms = (time.time() - start_time) * 1000
            cost = self._calculate_cost(model, tokens)

            return LLMResponse(
                content=content,
                model=model,
                provider="anthropic",
                tokens_used=tokens,
                cost_usd=cost,
                latency_ms=latency_ms
            )

        except Exception as e:
            logger.error(f"Anthropic error: {e}")
            raise

    def _calculate_cost(self, model: str, tokens: int) -> float:
        cost_per_token = self.MODELS.get(model, 0.0)
        return tokens * cost_per_token

    def get_cost_per_token(self, model: str) -> float:
        return self.MODELS.get(model, 0.0)

    def supports_streaming(self) -> bool:
        return True


class UniversalLLMClient:
    """
    Universal LLM client with automatic fallback

    Usage across applications:
    ```python
    from llm_providers import UniversalLLMClient

    client = UniversalLLMClient()
    client.add_provider('z.ai', ZAIProvider(api_key="..."))
    client.add_provider('local', LMStudioProvider())
    client.set_fallback_order(['z.ai', 'local'])

    response = client.call("Write a haiku")
    ```
    """

    def __init__(self):
        self.providers: Dict[str, BaseLLMProvider] = {}
        self.fallback_order: List[str] = []
        self.usage_stats = {}

    def add_provider(self, name: str, provider: BaseLLMProvider):
        """Add a provider"""
        self.providers[name] = provider
        self.usage_stats[name] = {
            'calls': 0,
            'tokens': 0,
            'cost': 0.0,
            'errors': 0
        }

    def set_fallback_order(self, order: List[str]):
        """Set provider fallback order"""
        self.fallback_order = order

    def call(self,
             prompt: str,
             provider: Optional[str] = None,
             **kwargs) -> LLMResponse:
        """
        Call LLM with automatic fallback

        Args:
            prompt: The prompt to send
            provider: Specific provider to use (None for fallback order)
            **kwargs: Additional arguments for the provider
        """
        # If specific provider requested
        if provider:
            if provider not in self.providers:
                raise ValueError(f"Provider {provider} not found")
            return self._call_provider(provider, prompt, **kwargs)

        # Try fallback order
        last_error = None
        for provider_name in self.fallback_order:
            try:
                response = self._call_provider(provider_name, prompt, **kwargs)
                return response
            except Exception as e:
                logger.warning(f"Provider {provider_name} failed: {e}")
                last_error = e
                continue

        # All providers failed
        raise Exception(f"All providers failed. Last error: {last_error}")

    def _call_provider(self, name: str, prompt: str, **kwargs) -> LLMResponse:
        """Call a specific provider and track stats"""
        provider = self.providers[name]

        try:
            response = provider.call(prompt, **kwargs)

            # Update stats
            self.usage_stats[name]['calls'] += 1
            self.usage_stats[name]['tokens'] += response.tokens_used
            self.usage_stats[name]['cost'] += response.cost_usd

            return response

        except Exception as e:
            self.usage_stats[name]['errors'] += 1
            raise

    def get_usage_summary(self) -> Dict:
        """Get usage summary for all providers"""
        return {
            name: {
                'calls': stats['calls'],
                'tokens': stats['tokens'],
                'cost_usd': round(stats['cost'], 4),
                'errors': stats['errors'],
                'avg_tokens_per_call': round(stats['tokens'] / stats['calls']) if stats['calls'] > 0 else 0
            }
            for name, stats in self.usage_stats.items()
        }

    def estimate_cost(self, provider: str, model: str, estimated_tokens: int) -> float:
        """Estimate cost for a call"""
        if provider not in self.providers:
            return 0.0

        cost_per_token = self.providers[provider].get_cost_per_token(model)
        return cost_per_token * estimated_tokens
