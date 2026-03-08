"""
Speech-to-Text service using OpenAI Whisper or AWS Transcribe
"""
import io
import logging

from src.config.settings import settings

logger = logging.getLogger(__name__)

# Try to import OpenAI, but make it optional
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    logger.warning("OpenAI not available, will use AWS Transcribe only")


class SpeechToTextService:
    """Service for converting speech to text"""

    # Supported languages (Indian languages)
    SUPPORTED_LANGUAGES = {
        "hi": "Hindi",
        "bn": "Bengali",
        "te": "Telugu",
        "mr": "Marathi",
        "ta": "Tamil",
        "gu": "Gujarati",
        "kn": "Kannada",
        "ml": "Malayalam",
        "pa": "Punjabi",
        "or": "Odia",
        "en": "English"
    }

    def __init__(self):
        """Initialize STT service"""
        if OPENAI_AVAILABLE and settings.openai_api_key:
            self.client = OpenAI(api_key=settings.openai_api_key)
            self.use_openai = True
            logger.info("Speech-to-Text service initialized with OpenAI")
        else:
            self.client = None
            self.use_openai = False
            logger.info("Speech-to-Text service initialized (AWS Transcribe only)")

    async def transcribe(
        self,
        audio_data: bytes,
        language: str | None = None,
        format: str = "mp3"
    ) -> dict:
        """
        Transcribe audio to text

        Args:
            audio_data: Audio file bytes
            language: Language code (auto-detect if None)
            format: Audio format (mp3, wav, etc.)

        Returns:
            Transcription result with text and metadata
        """
        if not self.use_openai:
            raise NotImplementedError(
                "OpenAI Whisper not available. "
                "Use AWS Transcribe via speech_factory instead."
            )

        try:
            # Create file-like object
            audio_file = io.BytesIO(audio_data)
            audio_file.name = f"audio.{format}"

            # Transcribe using Whisper
            transcript = self.client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                language=language,
                response_format="verbose_json"
            )

            result = {
                "text": transcript.text,
                "language": transcript.language if hasattr(transcript, 'language') else language,
                "duration": transcript.duration if hasattr(transcript, 'duration') else None,
                "confidence": self._estimate_confidence(transcript),
                "segments": self._extract_segments(transcript) if hasattr(transcript, 'segments') else []
            }

            logger.info(
                f"Transcribed audio: {len(transcript.text)} chars, "
                f"language={result['language']}"
            )

            return result

        except Exception as e:
            logger.error(f"Transcription failed: {e}")
            raise

    async def detect_language(self, audio_data: bytes) -> str:
        """
        Detect language from audio

        Args:
            audio_data: Audio file bytes

        Returns:
            Detected language code
        """
        try:
            # Transcribe without language hint
            result = await self.transcribe(audio_data, language=None)
            detected_lang = result.get("language", "en")

            logger.info(f"Detected language: {detected_lang}")
            return detected_lang

        except Exception as e:
            logger.error(f"Language detection failed: {e}")
            return "en"  # Default to English

    def _estimate_confidence(self, transcript) -> float:
        """
        Estimate transcription confidence

        Args:
            transcript: Whisper transcript object

        Returns:
            Confidence score (0-1)
        """
        # Whisper doesn't provide confidence directly
        # Estimate based on text characteristics

        if not hasattr(transcript, 'text') or not transcript.text:
            return 0.0

        text = transcript.text

        # Simple heuristics
        confidence = 0.8  # Base confidence

        # Reduce confidence for very short transcripts
        if len(text) < 10:
            confidence -= 0.2

        # Reduce confidence if lots of [inaudible] markers
        if "[inaudible]" in text.lower():
            confidence -= 0.3

        return max(0.0, min(1.0, confidence))

    def _extract_segments(self, transcript) -> list:
        """Extract time-stamped segments"""
        if not hasattr(transcript, 'segments'):
            return []

        segments = []
        for seg in transcript.segments:
            segments.append({
                "start": seg.get("start", 0),
                "end": seg.get("end", 0),
                "text": seg.get("text", "")
            })

        return segments

    async def transcribe_with_timestamps(
        self,
        audio_data: bytes,
        language: str | None = None
    ) -> dict:
        """
        Transcribe with word-level timestamps

        Args:
            audio_data: Audio file bytes
            language: Language code

        Returns:
            Transcription with timestamps
        """
        try:
            audio_file = io.BytesIO(audio_data)
            audio_file.name = "audio.mp3"

            transcript = self.client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                language=language,
                response_format="verbose_json",
                timestamp_granularities=["word"]
            )

            result = {
                "text": transcript.text,
                "language": transcript.language if hasattr(transcript, 'language') else language,
                "words": []
            }

            # Extract word-level timestamps if available
            if hasattr(transcript, 'words'):
                for word in transcript.words:
                    result["words"].append({
                        "word": word.get("word", ""),
                        "start": word.get("start", 0),
                        "end": word.get("end", 0)
                    })

            logger.info(f"Transcribed with {len(result['words'])} words")
            return result

        except Exception as e:
            logger.error(f"Timestamp transcription failed: {e}")
            # Fallback to regular transcription
            return await self.transcribe(audio_data, language)

    def validate_language(self, language_code: str) -> bool:
        """Check if language is supported"""
        return language_code in self.SUPPORTED_LANGUAGES

    def get_supported_languages(self) -> dict[str, str]:
        """Get list of supported languages"""
        return self.SUPPORTED_LANGUAGES.copy()
