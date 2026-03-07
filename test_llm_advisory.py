"""
Test LLM advisory generation
"""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src.services.llm_factory import get_llm

async def test_llm():
    """Test LLM generation"""
    try:
        llm = get_llm()
        print(f"LLM provider: {type(llm).__name__}")
        
        prompt = """You are an agricultural advisor speaking to a farmer over the phone. Generate a natural, conversational advisory message in Hindi.

Farmer's crop: rice, sugarcane
Crop health: moderate stress
Temperature: 28 degrees Celsius
Humidity: 65 percent
Stress type: general_stress

CRITICAL INSTRUCTIONS FOR VOICE DELIVERY:
1. Write ONLY in Hindi script - NO English words, NO technical terms like NDVI
2. Use simple, everyday language that farmers understand
3. Spell out ALL numbers in words (not digits)
4. NO symbols like %, °C, ₹ - spell everything out in words
5. Keep it conversational and natural for phone calls
6. Maximum 150 words
7. Structure: greeting, crop status, 2-3 simple actions with costs in words, closing

Generate the advisory message in Hindi:"""
        
        messages = [{"role": "user", "content": prompt}]
        
        print("\nCalling LLM...")
        result = await llm.generate_completion(messages, temperature=0.7, max_tokens=500)
        
        print(f"\nResult length: {len(result)} chars")
        print(f"\nResult:\n{result}")
        
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_llm())
