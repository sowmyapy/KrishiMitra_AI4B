"""
LLM Factory - Provides unified interface for different LLM providers
"""
import logging
from typing import Protocol

from src.config.settings import settings

logger = logging.getLogger(__name__)

# Optional imports - only import if needed
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    logger.warning("OpenAI package not installed. Only AWS Bedrock will be available.")


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


class OpenAIProvider:
    """OpenAI LLM provider"""

    def __init__(self):
        if not OPENAI_AVAILABLE:
            raise ImportError(
                "OpenAI package not installed. Install with: pip install openai\n"
                "Or use AWS Bedrock by setting LLM_PROVIDER=bedrock in .env"
            )
        self.client = OpenAI(api_key=settings.openai_api_key)
        logger.info("Using OpenAI as LLM provider")

    async def generate_completion(
        self,
        messages: list[dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 1000
    ) -> str:
        """Generate completion using OpenAI"""
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content

    async def generate_embedding(self, text: str) -> list[float]:
        """Generate embedding using OpenAI"""
        response = self.client.embeddings.create(
            model="text-embedding-3-small",
            input=text
        )
        return response.data[0].embedding


class BedrockProvider:
    """AWS Bedrock LLM provider"""

    def __init__(self):
        from src.services.aws.bedrock_client import BedrockClient
        self.client = BedrockClient()
        logger.info("Using AWS Bedrock as LLM provider")

    async def generate_completion(
        self,
        messages: list[dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 1000
    ) -> str:
        """Generate completion using Bedrock"""
        return await self.client.generate_completion(messages, temperature, max_tokens)

    async def generate_embedding(self, text: str) -> list[float]:
        """Generate embedding using Bedrock"""
        return await self.client.generate_embedding(text)


def get_llm_provider() -> LLMProvider:
    """
    Get LLM provider based on configuration

    Returns:
        LLM provider instance
    """
    provider = settings.llm_provider.lower()

    if provider == "bedrock" or settings.use_aws_services:
        return BedrockProvider()
    elif provider == "openai":
        if not OPENAI_AVAILABLE:
            logger.error("OpenAI selected but package not installed. Falling back to Bedrock.")
            return BedrockProvider()
        return OpenAIProvider()
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
