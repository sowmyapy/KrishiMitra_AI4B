"""
AWS Transcribe client for Speech-to-Text (alternative to Whisper)
"""
import logging
import time
import uuid
from typing import Dict, Optional
import boto3
from botocore.exceptions import ClientError

from src.config.settings import settings

logger = logging.getLogger(__name__)


class TranscribeClient:
    """Client for AWS Transcribe STT service"""
    
    # Language code mapping (AWS format)
    LANGUAGE_CODES = {
        "hi": "hi-IN",  # Hindi
        "bn": "bn-IN",  # Bengali
        "te": "te-IN",  # Telugu
        "mr": "mr-IN",  # Marathi
        "ta": "ta-IN",  # Tamil
        "gu": "gu-IN",  # Gujarati
        "kn": "kn-IN",  # Kannada
        "ml": "ml-IN",  # Malayalam
        "pa": "pa-IN",  # Punjabi
        "en": "en-IN",  # English (India)
    }
    
    def __init__(self):
        """Initialize Transcribe client"""
        self.client = boto3.client(
            'transcribe',
            region_name=settings.aws_region
        )
        self.s3_client = boto3.client(
            's3',
            region_name=settings.aws_region
        )
        self.bucket = settings.s3_bucket_audio
        logger.info("AWS Transcribe client initialized")
    
    async def transcribe(
        self,
        audio_data: bytes,
        language: Optional[str] = None,
        format: str = "mp3"
    ) -> Dict:
        """
        Transcribe audio to text using AWS Transcribe
        
        Args:
            audio_data: Audio file bytes
            language: Language code (auto-detect if None)
            format: Audio format (mp3, wav, etc.)
        
        Returns:
            Transcription result with text and metadata
        """
        job_name = f"transcribe-{uuid.uuid4()}"
        s3_key = f"transcribe-input/{job_name}.{format}"
        
        try:
            # Upload audio to S3
            self.s3_client.put_object(
                Bucket=self.bucket,
                Key=s3_key,
                Body=audio_data
            )
            
            s3_uri = f"s3://{self.bucket}/{s3_key}"
            
            # Start transcription job
            job_params = {
                'TranscriptionJobName': job_name,
                'Media': {'MediaFileUri': s3_uri},
                'MediaFormat': format,
                'OutputBucketName': self.bucket,
            }
            
            # Add language or enable auto-detection
            if language:
                aws_lang = self.LANGUAGE_CODES.get(language, "en-IN")
                job_params['LanguageCode'] = aws_lang
            else:
                job_params['IdentifyLanguage'] = True
                job_params['LanguageOptions'] = list(self.LANGUAGE_CODES.values())
            
            self.client.start_transcription_job(**job_params)
            
            # Wait for completion
            result = await self._wait_for_job(job_name)
            
            # Cleanup S3
            self._cleanup_s3(s3_key, job_name)
            
            return result
            
        except ClientError as e:
            logger.error(f"Transcription failed: {e}")
            raise
    
    async def _wait_for_job(self, job_name: str, max_wait: int = 300) -> Dict:
        """Wait for transcription job to complete"""
        start_time = time.time()
        
        while time.time() - start_time < max_wait:
            response = self.client.get_transcription_job(
                TranscriptionJobName=job_name
            )
            
            status = response['TranscriptionJob']['TranscriptionJobStatus']
            
            if status == 'COMPLETED':
                return self._parse_result(response)
            elif status == 'FAILED':
                reason = response['TranscriptionJob'].get('FailureReason', 'Unknown')
                raise Exception(f"Transcription failed: {reason}")
            
            time.sleep(2)
        
        raise TimeoutError(f"Transcription job {job_name} timed out")
    
    def _parse_result(self, response: Dict) -> Dict:
        """Parse transcription result"""
        job = response['TranscriptionJob']
        
        # Get transcript URI
        transcript_uri = job['Transcript']['TranscriptFileUri']
        
        # Download transcript
        import requests
        transcript_data = requests.get(transcript_uri).json()
        
        # Extract results
        results = transcript_data['results']
        transcript = results['transcripts'][0]['transcript']
        
        # Extract language
        language_code = job.get('LanguageCode', 'en-IN')
        language = self._aws_to_standard_lang(language_code)
        
        # Extract segments
        segments = []
        if 'items' in results:
            current_segment = {"start": 0, "end": 0, "text": ""}
            
            for item in results['items']:
                if item['type'] == 'pronunciation':
                    start = float(item.get('start_time', 0))
                    end = float(item.get('end_time', 0))
                    word = item['alternatives'][0]['content']
                    
                    if not current_segment["text"]:
                        current_segment["start"] = start
                    
                    current_segment["text"] += word + " "
                    current_segment["end"] = end
                    
                    # Create segment every 10 words
                    if len(current_segment["text"].split()) >= 10:
                        segments.append(current_segment)
                        current_segment = {"start": end, "end": end, "text": ""}
            
            if current_segment["text"]:
                segments.append(current_segment)
        
        # Estimate confidence
        confidence = self._calculate_confidence(results)
        
        result = {
            "text": transcript,
            "language": language,
            "duration": float(job.get('MediaSampleRateHertz', 0)) / 1000,
            "confidence": confidence,
            "segments": segments
        }
        
        logger.info(
            f"Transcribed audio: {len(transcript)} chars, "
            f"language={language}, confidence={confidence:.2f}"
        )
        
        return result
    
    def _calculate_confidence(self, results: Dict) -> float:
        """Calculate average confidence from items"""
        if 'items' not in results:
            return 0.8
        
        confidences = []
        for item in results['items']:
            if item['type'] == 'pronunciation':
                conf = float(item['alternatives'][0].get('confidence', 0.8))
                confidences.append(conf)
        
        return sum(confidences) / len(confidences) if confidences else 0.8
    
    def _aws_to_standard_lang(self, aws_lang: str) -> str:
        """Convert AWS language code to standard format"""
        for std_lang, aws_code in self.LANGUAGE_CODES.items():
            if aws_code == aws_lang:
                return std_lang
        return "en"
    
    def _cleanup_s3(self, input_key: str, job_name: str):
        """Cleanup S3 files"""
        try:
            # Delete input file
            self.s3_client.delete_object(Bucket=self.bucket, Key=input_key)
            
            # Delete output file
            output_key = f"{job_name}.json"
            self.s3_client.delete_object(Bucket=self.bucket, Key=output_key)
            
        except Exception as e:
            logger.warning(f"S3 cleanup failed: {e}")
    
    async def detect_language(self, audio_data: bytes) -> str:
        """
        Detect language from audio
        
        Args:
            audio_data: Audio file bytes
        
        Returns:
            Detected language code
        """
        result = await self.transcribe(audio_data, language=None)
        return result.get("language", "en")
    
    async def transcribe_with_timestamps(
        self,
        audio_data: bytes,
        language: Optional[str] = None
    ) -> Dict:
        """
        Transcribe with word-level timestamps
        
        Args:
            audio_data: Audio file bytes
            language: Language code
        
        Returns:
            Transcription with timestamps
        """
        # AWS Transcribe provides word-level timestamps by default
        result = await self.transcribe(audio_data, language)
        
        # Extract words from segments
        words = []
        for segment in result.get("segments", []):
            segment_words = segment["text"].split()
            duration = segment["end"] - segment["start"]
            word_duration = duration / len(segment_words) if segment_words else 0
            
            for i, word in enumerate(segment_words):
                words.append({
                    "word": word,
                    "start": segment["start"] + (i * word_duration),
                    "end": segment["start"] + ((i + 1) * word_duration)
                })
        
        result["words"] = words
        return result
    
    def validate_language(self, language_code: str) -> bool:
        """Check if language is supported"""
        return language_code in self.LANGUAGE_CODES
    
    def get_supported_languages(self) -> Dict[str, str]:
        """Get list of supported languages"""
        return {
            code: f"{code.upper()} (AWS Transcribe)"
            for code in self.LANGUAGE_CODES.keys()
        }
