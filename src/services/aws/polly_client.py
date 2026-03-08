"""
AWS Polly client for Text-to-Speech (alternative to ElevenLabs)
"""
import logging

import boto3
from botocore.exceptions import ClientError

from src.config.settings import settings

logger = logging.getLogger(__name__)


class PollyClient:
    """Client for AWS Polly TTS service"""

    # Voice profiles for different languages
    VOICE_PROFILES = {
        "hi": {
            "male": {"voice_id": "Aditi", "name": "Aditi (Hindi Female)", "engine": "standard"},
            "female": {"voice_id": "Aditi", "name": "Aditi (Hindi Female)", "engine": "standard"}
        },
        "en": {
            "male": {"voice_id": "Raveena", "name": "Raveena (English Indian Female)", "engine": "standard"},
            "female": {"voice_id": "Raveena", "name": "Raveena (English Indian Female)", "engine": "standard"}
        },
        # Note: AWS Polly has limited Indian language support
        # For other languages, we'll use standard voices with closest match
        "bn": {
            "male": {"voice_id": "Aditi", "name": "Aditi (Hindi - closest to Bengali)", "engine": "standard"},
            "female": {"voice_id": "Aditi", "name": "Aditi (Hindi - closest to Bengali)", "engine": "standard"}
        },
        "te": {
            "male": {"voice_id": "Aditi", "name": "Aditi (Hindi - closest to Telugu)", "engine": "standard"},
            "female": {"voice_id": "Aditi", "name": "Aditi (Hindi - closest to Telugu)", "engine": "standard"}
        },
        "mr": {
            "male": {"voice_id": "Aditi", "name": "Aditi (Hindi - closest to Marathi)", "engine": "standard"},
            "female": {"voice_id": "Aditi", "name": "Aditi (Hindi - closest to Marathi)", "engine": "standard"}
        },
        "ta": {
            "male": {"voice_id": "Aditi", "name": "Aditi (Hindi - closest to Tamil)", "engine": "standard"},
            "female": {"voice_id": "Aditi", "name": "Aditi (Hindi - closest to Tamil)", "engine": "standard"}
        },
        "gu": {
            "male": {"voice_id": "Aditi", "name": "Aditi (Hindi - closest to Gujarati)", "engine": "standard"},
            "female": {"voice_id": "Aditi", "name": "Aditi (Hindi - closest to Gujarati)", "engine": "standard"}
        },
        "kn": {
            "male": {"voice_id": "Aditi", "name": "Aditi (Hindi - closest to Kannada)", "engine": "standard"},
            "female": {"voice_id": "Aditi", "name": "Aditi (Hindi - closest to Kannada)", "engine": "standard"}
        },
        "ml": {
            "male": {"voice_id": "Aditi", "name": "Aditi (Hindi - closest to Malayalam)", "engine": "standard"},
            "female": {"voice_id": "Aditi", "name": "Aditi (Hindi - closest to Malayalam)", "engine": "standard"}
        },
        "pa": {
            "male": {"voice_id": "Aditi", "name": "Aditi (Hindi - closest to Punjabi)", "engine": "standard"},
            "female": {"voice_id": "Aditi", "name": "Aditi (Hindi - closest to Punjabi)", "engine": "standard"}
        },
        "or": {
            "male": {"voice_id": "Aditi", "name": "Aditi (Hindi - closest to Odia)", "engine": "standard"},
            "female": {"voice_id": "Aditi", "name": "Aditi (Hindi - closest to Odia)", "engine": "standard"}
        }
    }

    def __init__(self):
        """Initialize Polly client"""
        self.client = boto3.client(
            'polly',
            region_name=settings.aws_region
        )
        self.cache = {}  # Simple in-memory cache
        logger.info("AWS Polly client initialized")

    async def synthesize(
        self,
        text: str,
        language: str = "en",
        voice_gender: str = "male",
        optimize_streaming: bool = False
    ) -> bytes:
        """
        Convert text to speech using AWS Polly

        Args:
            text: Text to synthesize
            language: Language code
            voice_gender: Voice gender (male/female)
            optimize_streaming: Optimize for streaming

        Returns:
            Audio data as bytes
        """
        # Check cache
        cache_key = f"{text}_{language}_{voice_gender}"
        if cache_key in self.cache:
            logger.info("Using cached audio")
            return self.cache[cache_key]

        try:
            # Get voice profile
            voice_profile = self._get_voice_profile(language, voice_gender)

            # Synthesize speech
            response = self.client.synthesize_speech(
                Text=text,
                OutputFormat='mp3',
                VoiceId=voice_profile["voice_id"],
                Engine=voice_profile.get("engine", "standard"),  # Use engine from profile
                LanguageCode=self._get_language_code(language)
            )

            # Read audio stream
            audio_bytes = response['AudioStream'].read()

            # Cache if text is short
            if len(text) < 100:
                self.cache[cache_key] = audio_bytes

            logger.info(
                f"Synthesized {len(text)} chars to {len(audio_bytes)} bytes audio, "
                f"language={language}, voice={voice_profile['voice_id']}"
            )

            return audio_bytes

        except ClientError as e:
            logger.error(f"Speech synthesis failed: {e}")
            raise

    async def synthesize_streaming(
        self,
        text: str,
        language: str = "en",
        voice_gender: str = "male"
    ):
        """
        Stream audio generation for low latency

        Args:
            text: Text to synthesize
            language: Language code
            voice_gender: Voice gender

        Yields:
            Audio chunks
        """
        try:
            voice_profile = self._get_voice_profile(language, voice_gender)

            # Polly doesn't support true streaming, but we can chunk the text
            # Split text into sentences
            sentences = self._split_into_sentences(text)

            for sentence in sentences:
                response = self.client.synthesize_speech(
                    Text=sentence,
                    OutputFormat='mp3',
                    VoiceId=voice_profile["voice_id"],
                    Engine=voice_profile.get("engine", "standard"),
                    LanguageCode=self._get_language_code(language)
                )

                # Yield audio chunk
                yield response['AudioStream'].read()

            logger.info(f"Streamed synthesis for {len(text)} chars")

        except ClientError as e:
            logger.error(f"Streaming synthesis failed: {e}")
            raise

    def _get_voice_profile(self, language: str, gender: str = "male") -> dict:
        """Get voice profile for language and gender"""
        profiles = self.VOICE_PROFILES.get(language, self.VOICE_PROFILES["en"])
        return profiles.get(gender, profiles["male"])

    def _get_language_code(self, language: str) -> str:
        """Get AWS Polly language code"""
        language_codes = {
            "hi": "hi-IN",
            "en": "en-IN",
            "bn": "hi-IN",  # Fallback to Hindi
            "te": "hi-IN",
            "mr": "hi-IN",
            "ta": "hi-IN",
            "gu": "hi-IN",
            "kn": "hi-IN",
            "ml": "hi-IN",
            "pa": "hi-IN",
            "or": "hi-IN"
        }
        return language_codes.get(language, "en-IN")

    def _split_into_sentences(self, text: str) -> list:
        """Split text into sentences for streaming"""
        import re
        sentences = re.split(r'[.!?]+', text)
        return [s.strip() for s in sentences if s.strip()]

    async def optimize_for_agriculture(self, text: str) -> str:
        """
        Optimize text for agricultural context using SSML

        Args:
            text: Original text

        Returns:
            SSML-formatted text
        """
        # Use SSML for better control
        ssml = f'<speak>{text}</speak>'

        # Add pauses after sentences
        ssml = ssml.replace('. ', '.<break time="500ms"/> ')

        # Emphasize important agricultural terms
        agricultural_terms = [
            "NDVI", "irrigation", "fertilizer", "pesticide",
            "hectare", "quintal", "crop", "soil"
        ]

        for term in agricultural_terms:
            ssml = ssml.replace(
                term,
                f'<emphasis level="strong">{term}</emphasis><break time="300ms"/>'
            )

        return ssml

    async def synthesize_with_ssml(
        self,
        ssml_text: str,
        language: str = "en"
    ) -> bytes:
        """
        Synthesize with SSML markup for advanced control

        Args:
            ssml_text: Text with SSML markup
            language: Language code

        Returns:
            Audio bytes
        """
        try:
            voice_profile = self._get_voice_profile(language)

            response = self.client.synthesize_speech(
                Text=ssml_text,
                TextType='ssml',  # Enable SSML
                OutputFormat='mp3',
                VoiceId=voice_profile["voice_id"],
                Engine='neural',
                LanguageCode=self._get_language_code(language)
            )

            audio_bytes = response['AudioStream'].read()

            logger.info(f"Synthesized SSML: {len(audio_bytes)} bytes")
            return audio_bytes

        except ClientError as e:
            logger.error(f"SSML synthesis failed: {e}")
            raise

    def clear_cache(self):
        """Clear audio cache"""
        self.cache.clear()
        logger.info("Audio cache cleared")

    def get_cache_size(self) -> int:
        """Get number of cached items"""
        return len(self.cache)

    async def preload_common_phrases(self, language: str):
        """Preload common phrases for faster response"""
        common_phrases = [
            "Hello, this is KrishiMitra calling.",
            "Your crop health alert.",
            "Please take action immediately.",
            "Thank you for your time.",
            "Goodbye."
        ]

        for phrase in common_phrases:
            await self.synthesize(phrase, language)

        logger.info(f"Preloaded {len(common_phrases)} phrases for {language}")
