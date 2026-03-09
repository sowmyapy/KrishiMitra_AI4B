"""
LLM Factory - Provides unified interface for different LLM providers
"""
import logging
from typing import Protocol

from src.config.settings import settings

logger = logging.getLogger(__name__)

# Optional imports - only import if needed
try:
    from groq import Groq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False
    logger.warning("Groq package not installed. Install with: pip install groq")


class LLMProvider(Protocol):
    """Protocol for LLM providers"""

    async def generate_completion(
        self,
        messages: list[dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 1000
    ) -> str:
        """Generate text completion"""
        ...

    async def generate_embedding(self, text: str) -> list[float]:
        """Generate text embedding"""
        ...


class GroqProvider:
    """Groq LLM provider (fast and free!)"""

    def __init__(self):
        if not GROQ_AVAILABLE:
            raise ImportError(
                "Groq package not installed. Install with: pip install groq"
            )
        self.client = Groq(api_key=settings.groq_api_key)
        logger.info("Using Groq as LLM provider")

    async def generate_completion(
        self,
        messages: list[dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 1000
    ) -> str:
        """Generate completion using Groq"""
        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",  # Fast and capable model
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content

    async def generate_embedding(self, text: str) -> list[float]:
        """Generate embedding - Groq doesn't support embeddings, use Bedrock"""
        logger.warning("Groq doesn't support embeddings, this will fail")
        raise NotImplementedError("Groq doesn't support embeddings")


class BedrockProvider:
    """AWS Bedrock LLM provider with Groq fallback"""

    def __init__(self):
        from src.services.aws.bedrock_client import BedrockClient
        self.client = BedrockClient()
        self.fallback_provider = None
        logger.info("Using AWS Bedrock as LLM provider")

    def _get_fallback_provider(self):
        """Get Groq fallback provider if available"""
        if self.fallback_provider is None:
            if GROQ_AVAILABLE:
                try:
                    if settings.groq_api_key and settings.groq_api_key != "":
                        self.fallback_provider = GroqProvider()
                        logger.info("Groq fallback provider initialized")
                        return self.fallback_provider
                except Exception as e:
                    logger.warning(f"Failed to initialize Groq fallback: {e}")
        
        return self.fallback_provider

    async def generate_completion(
        self,
        messages: list[dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 1000
    ) -> str:
        """Generate completion using Bedrock with Groq fallback"""
        logger.info("BedrockProvider.generate_completion called - ENTRY POINT")
        try:
            logger.info("About to call bedrock_client.generate_completion")
            result = await self.client.generate_completion(messages, temperature, max_tokens)
            logger.info("Bedrock call succeeded")
            return result
        except Exception as e:
            logger.error(f"Bedrock failed with exception type: {type(e).__name__}, message: {e}")
            fallback = self._get_fallback_provider()
            if fallback:
                logger.info(f"Attempting Groq fallback after Bedrock failure")
                try:
                    result = await fallback.generate_completion(messages, temperature, max_tokens)
                    logger.info("Groq fallback succeeded!")
                    return result
                except Exception as fallback_error:
                    logger.error(f"Groq fallback also failed: {fallback_error}")
                    raise e  # Re-raise original Bedrock error
            else:
                logger.warning("No fallback provider available")
                raise

    async def generate_embedding(self, text: str) -> list[float]:
        """Generate embedding using Bedrock (no fallback for embeddings)"""
        try:
            return await self.client.generate_embedding(text)
        except Exception as e:
            logger.error(f"Bedrock embedding failed: {e}")
            raise


def get_llm_provider() -> LLMProvider:
    """
    Get LLM provider based on configuration

    Returns:
        LLM provider instance
    """
    provider = settings.llm_provider.lower()

    if provider == "bedrock" or settings.use_aws_services:
        return BedrockProvider()
    elif provider == "groq":
        if not GROQ_AVAILABLE:
            logger.error("Groq selected but package not installed. Falling back to Bedrock.")
            return BedrockProvider()
        return GroqProvider()
    else:
        logger.warning(f"Unknown LLM provider '{provider}', defaulting to Bedrock")
        return BedrockProvider()


# Global LLM provider instance
_llm_provider = None


def get_llm() -> LLMProvider:
    """Get singleton LLM provider instance"""
    global _llm_provider
    if _llm_provider is None:
        _llm_provider = get_llm_provider()
    return _llm_provider
