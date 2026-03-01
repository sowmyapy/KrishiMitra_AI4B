#!/usr/bin/env python3
"""
Test script for AWS integration
Tests LLM, STT, and TTS providers
"""
import asyncio
import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.services.llm_factory import get_llm
from src.services.speech_factory import get_stt, get_tts
from src.config.settings import settings


async def test_llm():
    """Test LLM provider"""
    print("\n" + "="*60)
    print("Testing LLM Provider")
    print("="*60)
    
    try:
        llm = get_llm()
        print(f"✓ Provider: {type(llm).__name__}")
        
        # Test completion
        print("\nTesting text generation...")
        response = await llm.generate_completion(
            messages=[
                {"role": "user", "content": "Say hi"}
            ],
            temperature=0.7,
            max_tokens=20  # Minimal tokens to test
        )
        print(f"✓ Response: {response[:100]}...")
        
        # Test embeddings
        print("\nTesting embeddings...")
        embedding = await llm.generate_embedding("crop health monitoring")
        print(f"✓ Embedding dimension: {len(embedding)}")
        
        return True
        
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


async def test_stt():
    """Test STT provider"""
    print("\n" + "="*60)
    print("Testing STT Provider")
    print("="*60)
    
    try:
        stt = get_stt()
        print(f"✓ Provider: {type(stt).__name__}")
        
        # Check supported languages
        languages = stt.get_supported_languages()
        print(f"✓ Supported languages: {len(languages)}")
        print(f"  Sample: {list(languages.keys())[:5]}")
        
        # Note: Actual audio transcription requires audio file
        print("\n⚠ Skipping audio transcription (requires audio file)")
        print("  To test: provide audio file and uncomment test code")
        
        return True
        
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


async def test_tts():
    """Test TTS provider"""
    print("\n" + "="*60)
    print("Testing TTS Provider")
    print("="*60)
    
    try:
        tts = get_tts()
        print(f"✓ Provider: {type(tts).__name__}")
        
        # Test synthesis
        print("\nTesting speech synthesis...")
        text = "Hello, this is KrishiMitra."
        audio = await tts.synthesize(text, language="en")
        print(f"✓ Generated audio: {len(audio)} bytes")
        
        # Test cache
        cache_size = tts.get_cache_size()
        print(f"✓ Cache size: {cache_size} items")
        
        return True
        
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


async def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("AWS Integration Test Suite")
    print("="*60)
    
    # Show configuration
    print("\nConfiguration:")
    print(f"  LLM_PROVIDER: {settings.llm_provider}")
    print(f"  USE_AWS_SERVICES: {settings.use_aws_services}")
    print(f"  AWS_REGION: {settings.aws_region}")
    
    # Run tests
    results = {
        "LLM": await test_llm(),
        "STT": await test_stt(),
        "TTS": await test_tts()
    }
    
    # Summary
    print("\n" + "="*60)
    print("Test Summary")
    print("="*60)
    
    for test_name, passed in results.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{test_name}: {status}")
    
    all_passed = all(results.values())
    
    if all_passed:
        print("\n✓ All tests passed!")
        return 0
    else:
        print("\n✗ Some tests failed")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
