"""
Text-to-Speech service using ElevenLabs or AWS Polly
"""
import logging
from typing import Dict, Optional

from src.config.settings import settings

logger = logging.getLogger(__name__)

# Try to import ElevenLabs, but make it optional
try:
    from elevenlabs import generate, Voice, VoiceSettings
    from elevenlabs.client import ElevenLabs
    ELEVENLABS_AVAILABLE = True
except ImportError:
    ELEVENLABS_AVAILABLE = False
    logger.warning("ElevenLabs not available, will use AWS Polly only")


class TextToSpeechService:
    """Service for converting text to speech"""
    
    # Voice profiles for different languages
    VOICE_PROFILES = {
        "hi": {"voice_id": "hindi_male_1", "name": "Hindi Male"},
        "bn": {"voice_id": "bengali_male_1", "name": "Bengali Male"},
        "te": {"voice_id": "telugu_male_1", "name": "Telugu Male"},
        "mr": {"voice_id": "marathi_male_1", "name": "Marathi Male"},
        "ta": {"voice_id": "tamil_male_1", "name": "Tamil Male"},
        "gu": {"voice_id": "gujarati_male_1", "name": "Gujarati Male"},
        "kn": {"voice_id": "kannada_male_1", "name": "Kannada Male"},
        "ml": {"voice_id": "malayalam_male_1", "name": "Malayalam Male"},
        "pa": {"voice_id": "punjabi_male_1", "name": "Punjabi Male"},
        "or": {"voice_id": "odia_male_1", "name": "Odia Male"},
        "en": {"voice_id": "english_male_1", "name": "English Male"}
    }
    
    def __init__(self):
        """Initialize TTS service"""
        if ELEVENLABS_AVAILABLE and settings.elevenlabs_api_key:
            self.client = ElevenLabs(api_key=settings.elevenlabs_api_key)
            self.use_elevenlabs = True
            logger.info("Text-to-Speech service initialized with ElevenLabs")
        else:
            self.client = None
            self.use_elevenlabs = False
            logger.info("Text-to-Speech service initialized (AWS Polly only)")
        self.cache = {}  # Simple in-memory cache for common phrases
    
    async def synthesize(
        self,
        text: str,
        language: str = "en",
        voice_gender: str = "male",
        optimize_streaming: bool = False
    ) -> bytes:
        """
        Convert text to speech
        
        Args:
            text: Text to synthesize
            language: Language code
            voice_gender: Voice gender (male/female)
            optimize_streaming: Optimize for streaming
        
        Returns:
            Audio data as bytes
        """
        if not self.use_elevenlabs:
            raise NotImplementedError(
                "ElevenLabs not available. "
                "Use AWS Polly via speech_factory instead."
            )
        
        # Check cache first
        cache_key = f"{text}_{language}_{voice_gender}"
        if cache_key in self.cache:
            logger.info("Using cached audio")
            return self.cache[cache_key]
        
        try:
            # Get voice profile
            voice_profile = self._get_voice_profile(language, voice_gender)
            
            # Generate speech
            audio = generate(
                text=text,
                voice=Voice(
                    voice_id=voice_profile["voice_id"],
                    settings=VoiceSettings(
                        stability=0.75,
                        similarity_boost=0.75,
                        style=0.5,
                        use_speaker_boost=True
                    )
                ),
                model="eleven_multilingual_v2"
            )
            
            # Convert generator to bytes
            audio_bytes = b"".join(audio)
            
            # Cache if text is short (common phrases)
            if len(text) < 100:
                self.cache[cache_key] = audio_bytes
            
            logger.info(
                f"Synthesized {len(text)} chars to {len(audio_bytes)} bytes audio, "
                f"language={language}"
            )
            
            return audio_bytes
            
        except Exception as e:
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
            
            # Generate with streaming
            audio_stream = generate(
                text=text,
                voice=Voice(
                    voice_id=voice_profile["voice_id"],
                    settings=VoiceSettings(
                        stability=0.75,
                        similarity_boost=0.75
                    )
                ),
                model="eleven_multilingual_v2",
                stream=True
            )
            
            for chunk in audio_stream:
                yield chunk
            
            logger.info(f"Streamed synthesis for {len(text)} chars")
            
        except Exception as e:
            logger.error(f"Streaming synthesis failed: {e}")
            raise
    
    def _get_voice_profile(self, language: str, gender: str = "male") -> Dict:
        """Get voice profile for language and gender"""
        
        # Get base profile
        profile = self.VOICE_PROFILES.get(language, self.VOICE_PROFILES["en"])
        
        # Adjust for gender if needed
        if gender == "female":
            profile = {
                "voice_id": profile["voice_id"].replace("male", "female"),
                "name": profile["name"].replace("Male", "Female")
            }
        
        return profile
    
    async def optimize_for_agriculture(self, text: str) -> str:
        """
        Optimize text for agricultural context
        
        Args:
            text: Original text
        
        Returns:
            Optimized text with better pronunciation
        """
        # Add pauses for better comprehension
        optimized = text
        
        # Add pause after sentences
        optimized = optimized.replace(". ", "... ")
        
        # Add pause after important terms
        agricultural_terms = [
            "NDVI", "irrigation", "fertilizer", "pesticide",
            "hectare", "quintal", "crop", "soil"
        ]
        
        for term in agricultural_terms:
            optimized = optimized.replace(term, f"{term}...")
        
        return optimized
    
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
        # ElevenLabs doesn't support SSML directly
        # Strip SSML tags and synthesize
        import re
        plain_text = re.sub(r'<[^>]+>', '', ssml_text)
        
        return await self.synthesize(plain_text, language)
    
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
