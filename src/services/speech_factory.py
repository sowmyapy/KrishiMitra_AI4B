"""
Speech Service Factory - Provides unified interface for STT and TTS providers
"""
import logging
from typing import Protocol, Dict, Optional

from src.config.settings import settings

logger = logging.getLogger(__name__)


class STTProvider(Protocol):
    """Protocol for Speech-to-Text providers"""
    
    async def transcribe(
        self,
        audio_data: bytes,
        language: Optional[str] = None,
        format: str = "mp3"
    ) -> Dict:
        """Transcribe audio to text"""
        ...
    
    async def detect_language(self, audio_data: bytes) -> str:
        """Detect language from audio"""
        ...
    
    async def transcribe_with_timestamps(
        self,
        audio_data: bytes,
        language: Optional[str] = None
    ) -> Dict:
        """Transcribe with word-level timestamps"""
        ...
    
    def validate_language(self, language_code: str) -> bool:
        """Check if language is supported"""
        ...
    
    def get_supported_languages(self) -> Dict[str, str]:
        """Get list of supported languages"""
        ...


class TTSProvider(Protocol):
    """Protocol for Text-to-Speech providers"""
    
    async def synthesize(
        self,
        text: str,
        language: str = "en",
        voice_gender: str = "male",
        optimize_streaming: bool = False
    ) -> bytes:
        """Convert text to speech"""
        ...
    
    async def synthesize_streaming(
        self,
        text: str,
        language: str = "en",
        voice_gender: str = "male"
    ):
        """Stream audio generation"""
        ...
    
    async def optimize_for_agriculture(self, text: str) -> str:
        """Optimize text for agricultural context"""
        ...
    
    async def synthesize_with_ssml(
        self,
        ssml_text: str,
        language: str = "en"
    ) -> bytes:
        """Synthesize with SSML markup"""
        ...
    
    def clear_cache(self):
        """Clear audio cache"""
        ...
    
    def get_cache_size(self) -> int:
        """Get number of cached items"""
        ...
    
    async def preload_common_phrases(self, language: str):
        """Preload common phrases"""
        ...


class WhisperSTTProvider:
    """OpenAI Whisper STT provider"""
    
    def __init__(self):
        from src.services.communication.speech_to_text import SpeechToTextService
        self.service = SpeechToTextService()
        logger.info("Using OpenAI Whisper for STT")
    
    async def transcribe(
        self,
        audio_data: bytes,
        language: Optional[str] = None,
        format: str = "mp3"
    ) -> Dict:
        return await self.service.transcribe(audio_data, language, format)
    
    async def detect_language(self, audio_data: bytes) -> str:
        return await self.service.detect_language(audio_data)
    
    async def transcribe_with_timestamps(
        self,
        audio_data: bytes,
        language: Optional[str] = None
    ) -> Dict:
        return await self.service.transcribe_with_timestamps(audio_data, language)
    
    def validate_language(self, language_code: str) -> bool:
        return self.service.validate_language(language_code)
    
    def get_supported_languages(self) -> Dict[str, str]:
        return self.service.get_supported_languages()


class TranscribeSTTProvider:
    """AWS Transcribe STT provider"""
    
    def __init__(self):
        from src.services.aws.transcribe_client import TranscribeClient
        self.service = TranscribeClient()
        logger.info("Using AWS Transcribe for STT")
    
    async def transcribe(
        self,
        audio_data: bytes,
        language: Optional[str] = None,
        format: str = "mp3"
    ) -> Dict:
        return await self.service.transcribe(audio_data, language, format)
    
    async def detect_language(self, audio_data: bytes) -> str:
        return await self.service.detect_language(audio_data)
    
    async def transcribe_with_timestamps(
        self,
        audio_data: bytes,
        language: Optional[str] = None
    ) -> Dict:
        return await self.service.transcribe_with_timestamps(audio_data, language)
    
    def validate_language(self, language_code: str) -> bool:
        return self.service.validate_language(language_code)
    
    def get_supported_languages(self) -> Dict[str, str]:
        return self.service.get_supported_languages()


class ElevenLabsTTSProvider:
    """ElevenLabs TTS provider"""
    
    def __init__(self):
        from src.services.communication.text_to_speech import TextToSpeechService
        self.service = TextToSpeechService()
        logger.info("Using ElevenLabs for TTS")
    
    async def synthesize(
        self,
        text: str,
        language: str = "en",
        voice_gender: str = "male",
        optimize_streaming: bool = False
    ) -> bytes:
        return await self.service.synthesize(text, language, voice_gender, optimize_streaming)
    
    async def synthesize_streaming(
        self,
        text: str,
        language: str = "en",
        voice_gender: str = "male"
    ):
        async for chunk in self.service.synthesize_streaming(text, language, voice_gender):
            yield chunk
    
    async def optimize_for_agriculture(self, text: str) -> str:
        return await self.service.optimize_for_agriculture(text)
    
    async def synthesize_with_ssml(
        self,
        ssml_text: str,
        language: str = "en"
    ) -> bytes:
        return await self.service.synthesize_with_ssml(ssml_text, language)
    
    def clear_cache(self):
        self.service.clear_cache()
    
    def get_cache_size(self) -> int:
        return self.service.get_cache_size()
    
    async def preload_common_phrases(self, language: str):
        await self.service.preload_common_phrases(language)


class PollyTTSProvider:
    """AWS Polly TTS provider"""
    
    def __init__(self):
        from src.services.aws.polly_client import PollyClient
        self.service = PollyClient()
        logger.info("Using AWS Polly for TTS")
    
    async def synthesize(
        self,
        text: str,
        language: str = "en",
        voice_gender: str = "male",
        optimize_streaming: bool = False
    ) -> bytes:
        return await self.service.synthesize(text, language, voice_gender, optimize_streaming)
    
    async def synthesize_streaming(
        self,
        text: str,
        language: str = "en",
        voice_gender: str = "male"
    ):
        async for chunk in self.service.synthesize_streaming(text, language, voice_gender):
            yield chunk
    
    async def optimize_for_agriculture(self, text: str) -> str:
        return await self.service.optimize_for_agriculture(text)
    
    async def synthesize_with_ssml(
        self,
        ssml_text: str,
        language: str = "en"
    ) -> bytes:
        return await self.service.synthesize_with_ssml(ssml_text, language)
    
    def clear_cache(self):
        self.service.clear_cache()
    
    def get_cache_size(self) -> int:
        return self.service.get_cache_size()
    
    async def preload_common_phrases(self, language: str):
        await self.service.preload_common_phrases(language)


def get_stt_provider() -> STTProvider:
    """
    Get STT provider based on configuration
    
    Returns:
        STT provider instance
    """
    if settings.use_aws_services:
        return TranscribeSTTProvider()
    else:
        return WhisperSTTProvider()


def get_tts_provider() -> TTSProvider:
    """
    Get TTS provider based on configuration
    
    Returns:
        TTS provider instance
    """
    if settings.use_aws_services:
        return PollyTTSProvider()
    else:
        return ElevenLabsTTSProvider()


# Global provider instances
_stt_provider = None
_tts_provider = None


def get_stt() -> STTProvider:
    """Get singleton STT provider instance"""
    global _stt_provider
    if _stt_provider is None:
        _stt_provider = get_stt_provider()
    return _stt_provider


def get_tts() -> TTSProvider:
    """Get singleton TTS provider instance"""
    global _tts_provider
    if _tts_provider is None:
        _tts_provider = get_tts_provider()
    return _tts_provider
