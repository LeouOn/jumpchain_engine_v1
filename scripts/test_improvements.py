#!/usr/bin/env python3
"""
Test script for Phase 2.5 improvements
Tests: .env loading, API key validation, retry logic, SDK usage
"""

import sys
import os
from pathlib import Path

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))


def print_section(title):
    """Print formatted section header"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def test_dotenv_loading():
    """Test that .env file can be loaded"""
    print_section("TEST 1: .env Loading")

    from dotenv import load_dotenv

    # Try to load .env
    env_path = Path('.env')
    example_path = Path('.env.example')

    if env_path.exists():
        print(f"  ✅ .env file found at: {env_path.absolute()}")
        load_dotenv()
        print(f"  ✅ .env file loaded successfully")
    else:
        print(f"  ⚠️  No .env file found (this is normal for testing)")
        print(f"  ℹ️  Use .env.example as template: {example_path.absolute()}")

    # Check that .env.example exists
    if example_path.exists():
        print(f"  ✅ .env.example template exists")

        # Count how many keys are documented
        with open(example_path, 'r') as f:
            content = f.read()
            key_count = content.count('API_KEY=')
            print(f"  ℹ️  Template includes {key_count} API key configurations")
    else:
        print(f"  ❌ .env.example not found!")
        return False

    print("\n✅ Test 1 Passed: .env support working")
    return True


def test_api_key_validation():
    """Test API key validation function"""
    print_section("TEST 2: API Key Validation")

    from src.engines.llm_providers import validate_api_keys

    # Test with keys that probably don't exist
    test_keys = ['ANTHROPIC_API_KEY', 'ZAI_API_KEY', 'OPENROUTER_API_KEY']

    print("\n  Testing key validation...")
    results = validate_api_keys(test_keys, warn_only=True)

    for key, is_present in results.items():
        status = "✅ Present" if is_present else "⚠️  Missing"
        print(f"    {key}: {status}")

    # Test that the function returns correct structure
    assert isinstance(results, dict), "Results should be a dict"
    assert len(results) == len(test_keys), "Should return result for each key"

    print("\n✅ Test 2 Passed: API key validation working")
    return True


def test_retry_decorator():
    """Test that retry decorator is available and configured"""
    print_section("TEST 3: Retry Logic")

    from src.engines.llm_providers import retry_api_call

    print("\n  ✅ Retry decorator imported successfully")

    # Check that it's callable
    assert callable(retry_api_call), "retry_api_call should be callable"
    print("  ✅ Retry decorator is callable")

    # Test creating a decorated function
    @retry_api_call(max_attempts=2)
    def test_function():
        return "success"

    result = test_function()
    assert result == "success", "Decorated function should work"
    print("  ✅ Retry decorator can decorate functions")

    print("\n✅ Test 3 Passed: Retry logic available")
    return True


def test_anthropic_provider():
    """Test Anthropic provider SDK integration"""
    print_section("TEST 4: Anthropic Provider SDK")

    from src.engines.llm_providers import AnthropicProvider

    print("\n  Testing Anthropic provider initialization...")

    # Test with dummy key (won't make actual calls)
    provider = AnthropicProvider(api_key="test_key")

    print(f"  ✅ Provider created")
    print(f"  ℹ️  Using SDK: {provider.use_sdk}")
    print(f"  ℹ️  Supported models: {list(provider.MODELS.keys())}")

    # Check that it has both SDK and HTTP methods
    assert hasattr(provider, '_call_with_sdk'), "Should have SDK method"
    assert hasattr(provider, '_call_with_http'), "Should have HTTP fallback"
    print("  ✅ Provider has both SDK and HTTP methods")

    print("\n✅ Test 4 Passed: Anthropic provider SDK integration ready")
    return True


def test_universal_client_validation():
    """Test UniversalLLMClient validation"""
    print_section("TEST 5: Universal Client Validation")

    from src.engines.llm_providers import UniversalLLMClient

    print("\n  Creating client with validation disabled...")
    client1 = UniversalLLMClient(validate_keys=False)
    print("  ✅ Client created without validation")

    print("\n  Creating client with validation enabled...")
    client2 = UniversalLLMClient(validate_keys=True)
    print("  ✅ Client created with validation (check warnings above)")

    # Test validate_environment method
    print("\n  Testing validate_environment method...")
    results = client2.validate_environment(warn_only=True)
    print(f"  ✅ Validation returned {len(results)} results")

    print("\n✅ Test 5 Passed: Universal client validation working")
    return True


def test_provider_retry_integration():
    """Test that providers have retry logic integrated"""
    print_section("TEST 6: Provider Retry Integration")

    from src.engines.llm_providers import (
        LMStudioProvider,
        OpenRouterProvider,
        AnthropicProvider
    )

    print("\n  Checking LMStudioProvider...")
    lm = LMStudioProvider()
    assert hasattr(lm, '_call_with_retry'), "LMStudioProvider should have retry method"
    print("  ✅ LMStudioProvider has retry logic")

    print("\n  Checking OpenRouterProvider...")
    opr = OpenRouterProvider(api_key="test")
    assert hasattr(opr, '_call_with_retry'), "OpenRouterProvider should have retry method"
    print("  ✅ OpenRouterProvider has retry logic")

    print("\n  Checking AnthropicProvider...")
    anth = AnthropicProvider(api_key="test")
    assert hasattr(anth, '_http_with_retry'), "AnthropicProvider should have HTTP retry"
    print("  ✅ AnthropicProvider has retry logic")

    print("\n✅ Test 6 Passed: All providers have retry integration")
    return True


def main():
    """Run all tests"""
    print("\n" + "=" * 70)
    print("  IMPROVEMENTS TEST SUITE")
    print("  Phase 2.5: Enhanced Production Readiness")
    print("=" * 70)

    tests = [
        (".env Loading", test_dotenv_loading),
        ("API Key Validation", test_api_key_validation),
        ("Retry Logic", test_retry_decorator),
        ("Anthropic Provider SDK", test_anthropic_provider),
        ("Universal Client Validation", test_universal_client_validation),
        ("Provider Retry Integration", test_provider_retry_integration),
    ]

    passed = 0
    failed = 0

    for name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                failed += 1
                print(f"\n❌ Test Failed: {name}")
        except Exception as e:
            failed += 1
            print(f"\n❌ Test Failed: {name}")
            print(f"   Error: {e}")
            import traceback
            traceback.print_exc()

    # Final summary
    print("\n" + "=" * 70)
    print("  TEST SUMMARY")
    print("=" * 70)
    print(f"\n  Total tests: {len(tests)}")
    print(f"  Passed: {passed} ✅")
    print(f"  Failed: {failed} ❌")

    if failed == 0:
        print("\n  🎉 All tests passed! Improvements are working correctly.")
    else:
        print("\n  ⚠️  Some tests failed. Check output above.")

    print("\n" + "=" * 70)

    return failed == 0


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
