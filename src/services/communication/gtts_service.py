"""
Google Text-to-Speech service for Indian languages
"""
import logging
import os
import hashlib
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

# Try to import gTTS
try:
    from gtts import gTTS
    GTTS_AVAILABLE = True
except ImportError:
    GTTS_AVAILABLE = False
    logger.warning("gTTS not available. Install with: pip install gtts")


class GTTSService:
    """Service for Google Text-to-Speech"""
    
    # Language mapping
    LANGUAGE_MAP = {
        "hi": "hi",  # Hindi
        "te": "te",  # Telugu
        "ta": "ta",  # Tamil
        "mr": "mr",  # Marathi
        "bn": "bn",  # Bengali
        "gu": "gu",  # Gujarati
        "kn": "kn",  # Kannada
        "ml": "ml",  # Malayalam
        "pa": "pa",  # Punjabi (Gurmukhi)
        "en": "en"   # English
    }
    
    def __init__(self, audio_dir: str = "audio_cache"):
        """Initialize gTTS service"""
        if not GTTS_AVAILABLE:
            raise ImportError("gTTS not installed. Install with: pip install gtts")
        
        self.audio_dir = Path(audio_dir)
        self.audio_dir.mkdir(exist_ok=True)
        logger.info(f"gTTS service initialized, audio dir: {self.audio_dir}")
    
    def generate_audio(
        self,
        text: str,
        language: str = "en",
        slow: bool = False
    ) -> str:
        """
        Generate audio file from text
        
        Args:
            text: Text to convert to speech
            language: Language code (hi, te, ta, etc.)
            slow: Speak slowly for better comprehension
        
        Returns:
            Path to generated audio file
        """
        try:
            # Get gTTS language code
            lang_code = self.LANGUAGE_MAP.get(language, "en")
            
            # Generate cache key from text
            cache_key = hashlib.md5(f"{text}_{lang_code}_{slow}".encode()).hexdigest()
            audio_file = self.audio_dir / f"{cache_key}.mp3"
            
            # Check if already cached
            if audio_file.exists():
                logger.info(f"Using cached audio: {audio_file}")
                return str(audio_file)
            
            # Generate audio
            tts = gTTS(text=text, lang=lang_code, slow=slow)
            tts.save(str(audio_file))
            
            logger.info(f"Generated audio: {audio_file} ({len(text)} chars, {lang_code})")
            return str(audio_file)
            
        except Exception as e:
            logger.error(f"Failed to generate audio: {e}")
            raise
    
    def clear_cache(self):
        """Clear all cached audio files"""
        try:
            for file in self.audio_dir.glob("*.mp3"):
                file.unlink()
            logger.info("Audio cache cleared")
        except Exception as e:
            logger.error(f"Failed to clear cache: {e}")
    
    def get_cache_size(self) -> int:
        """Get number of cached audio files"""
        return len(list(self.audio_dir.glob("*.mp3")))
