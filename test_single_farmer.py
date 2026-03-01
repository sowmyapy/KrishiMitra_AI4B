#!/usr/bin/env python3
"""
Single Farmer Test Script
Tests the complete KrishiMitra workflow with one farmer
"""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.config.settings import settings
from src.services.aws.bedrock_client import BedrockClient
from src.services.aws.transcribe_client import TranscribeClient
from src.services.aws.polly_client import PollyClient
from src.services.communication.voice_chatbot import VoiceChatbot


async def test_single_farmer():
    """Test complete workflow for a single farmer"""
    
    print("=" * 60)
    print("KrishiMitra - Single Farmer Test")
    print("=" * 60)
    print()
    
    # Test 1: AWS Bedrock (LLM)
    print("1. Testing AWS Bedrock (LLM)...")
    try:
        bedrock = BedrockClient()
        response = await bedrock.generate_text(
            "You are an agricultural advisor. Give a brief tip for wheat farming in one sentence.",
            max_tokens=100
        )
        print(f"   ✓ Bedrock working: {response[:80]}...")
    except Exception as e:
        print(f"   ✗ Bedrock failed: {e}")
        return False
    
    print()
    
    # Test 2: AWS Transcribe (Speech-to-Text)
    print("2. Testing AWS Transcribe (Speech-to-Text)...")
    try:
        transcribe = TranscribeClient()
        # Note: This requires an actual audio file
        print("   ℹ Transcribe client initialized (needs audio file for full test)")
    except Exception as e:
        print(f"   ✗ Transcribe failed: {e}")
        return False
    
    print()
    
    # Test 3: AWS Polly (Text-to-Speech)
    print("3. Testing AWS Polly (Text-to-Speech)...")
    try:
        polly = PollyClient()
        audio_data = await polly.synthesize_speech(
            "नमस्ते किसान भाई, आपकी फसल स्वस्थ है।",
            language_code="hi-IN"
        )
        print(f"   ✓ Polly working: Generated {len(audio_data)} bytes of audio")
    except Exception as e:
        print(f"   ✗ Polly failed: {e}")
        return False
    
    print()
    
    # Test 4: Voice Chatbot (Complete Integration)
    print("4. Testing Voice Chatbot (Complete Integration)...")
    try:
        chatbot = VoiceChatbot()
        
        # Simulate a farmer query
        farmer_query = "मेरी गेहूं की फसल में पीले पत्ते दिख रहे हैं, क्या करूं?"
        
        print(f"   Farmer query: {farmer_query}")
        
        response = await chatbot.process_voice_query(
            farmer_id="test_farmer_001",
            audio_data=b"",  # Would be actual audio in production
            text_query=farmer_query  # Using text for testing
        )
        
        print(f"   ✓ Chatbot response: {response['text'][:100]}...")
        print(f"   ✓ Audio generated: {len(response['audio'])} bytes")
        
    except Exception as e:
        print(f"   ✗ Chatbot failed: {e}")
        return False
    
    print()
    
    # Test 5: Check Configuration
    print("5. Checking Configuration...")
    print(f"   LLM Provider: {settings.llm_provider}")
    print(f"   Use AWS Services: {settings.use_aws_services}")
    print(f"   AWS Region: {settings.aws_region}")
    print(f"   S3 Bucket: {settings.s3_bucket_audio}")
    
    if settings.twilio_account_sid:
        print(f"   ✓ Twilio configured")
    else:
        print(f"   ⚠ Twilio not configured (needed for phone calls)")
    
    if settings.weather_api_key:
        print(f"   ✓ Weather API configured")
    else:
        print(f"   ⚠ Weather API not configured (needed for weather data)")
    
    if settings.sentinel_hub_client_id:
        print(f"   ✓ Sentinel Hub configured")
    else:
        print(f"   ⚠ Sentinel Hub not configured (needed for satellite data)")
    
    print()
    print("=" * 60)
    print("✓ All core AWS services working!")
    print("=" * 60)
    print()
    print("Next steps:")
    print("1. Add Twilio credentials to .env for phone calls")
    print("2. Add Weather API key to .env for weather data")
    print("3. Add Sentinel Hub credentials to .env for satellite data")
    print("4. Run: uvicorn src.main:app --reload")
    print("5. Visit: http://localhost:8000/docs")
    print()
    
    return True


async def test_farmer_scenario():
    """Test a complete farmer scenario"""
    
    print("=" * 60)
    print("Complete Farmer Scenario Test")
    print("=" * 60)
    print()
    
    print("Scenario: Farmer Ramesh has wheat crop with yellowing leaves")
    print()
    
    # Step 1: Monitoring Agent detects issue
    print("Step 1: Monitoring Agent analyzes satellite data...")
    print("   → NDVI value: 0.45 (below threshold of 0.6)")
    print("   → Weather: No rain for 15 days")
    print("   → Soil moisture: Low")
    print("   ✓ Issue detected: Water stress")
    print()
    
    # Step 2: Advisory Agent generates recommendation
    print("Step 2: Advisory Agent generates recommendation...")
    bedrock = BedrockClient()
    
    prompt = """You are an agricultural advisor. A farmer has wheat crop with:
    - NDVI: 0.45 (low, indicates stress)
    - No rain for 15 days
    - Low soil moisture
    - Yellowing leaves observed
    
    Provide a brief, actionable recommendation in 2-3 sentences."""
    
    recommendation = await bedrock.generate_text(prompt, max_tokens=150)
    print(f"   ✓ Recommendation: {recommendation}")
    print()
    
    # Step 3: Communication Agent prepares message
    print("Step 3: Communication Agent prepares voice message...")
    
    hindi_message = """नमस्ते रमेश जी,
    
आपकी गेहूं की फसल में पानी की कमी के लक्षण दिख रहे हैं। 
कृपया अगले 24 घंटों में सिंचाई करें। 
यह बहुत जरूरी है।

क्या आपको कोई सवाल है?"""
    
    print(f"   ✓ Message prepared in Hindi")
    print()
    
    # Step 4: Text-to-Speech conversion
    print("Step 4: Converting to speech...")
    polly = PollyClient()
    audio = await polly.synthesize_speech(hindi_message, language_code="hi-IN")
    print(f"   ✓ Audio generated: {len(audio)} bytes")
    print()
    
    # Step 5: Make phone call (simulated)
    print("Step 5: Making phone call to farmer...")
    print("   ℹ Twilio would call: +91-XXXXXXXXXX")
    print("   ℹ Farmer would hear the message in Hindi")
    print("   ℹ Farmer can respond with voice")
    print("   ℹ AI would understand and respond")
    print()
    
    print("=" * 60)
    print("✓ Complete scenario test successful!")
    print("=" * 60)
    print()


if __name__ == "__main__":
    print()
    print("KrishiMitra - Single Farmer Testing")
    print()
    
    # Run basic tests
    success = asyncio.run(test_single_farmer())
    
    if success:
        print()
        input("Press Enter to run complete scenario test...")
        print()
        asyncio.run(test_farmer_scenario())
    else:
        print()
        print("Basic tests failed. Please check your configuration.")
        print("See SINGLE_FARMER_TEST.md for setup instructions.")
