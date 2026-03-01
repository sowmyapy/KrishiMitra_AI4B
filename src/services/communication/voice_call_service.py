"""
Voice call service using Twilio
"""
import logging
from typing import Dict, Optional, Callable
from datetime import datetime
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse, Gather

from src.config.settings import settings
from src.services.communication.speech_to_text import SpeechToTextService
from src.services.communication.text_to_speech import TextToSpeechService

logger = logging.getLogger(__name__)


class VoiceCallService:
    """Service for managing voice calls"""
    
    # Call statuses
    STATUS_INITIATED = "initiated"
    STATUS_RINGING = "ringing"
    STATUS_IN_PROGRESS = "in-progress"
    STATUS_COMPLETED = "completed"
    STATUS_FAILED = "failed"
    STATUS_NO_ANSWER = "no-answer"
    STATUS_BUSY = "busy"
    
    def __init__(self):
        """Initialize voice call service"""
        self.client = Client(
            settings.twilio_account_sid,
            settings.twilio_auth_token
        )
        self.from_number = settings.twilio_phone_number
        self.stt_service = SpeechToTextService()
        self.tts_service = TextToSpeechService()
        
        logger.info("Voice call service initialized")
    
    async def initiate_call(
        self,
        to_number: str,
        callback_url: str,
        farmer_id: str,
        call_type: str = "advisory"
    ) -> Dict:
        """
        Initiate outbound call
        
        Args:
            to_number: Farmer's phone number
            callback_url: Webhook URL for call events
            farmer_id: Farmer ID
            call_type: Type of call (advisory, chatbot, etc.)
        
        Returns:
            Call information
        """
        try:
            call = self.client.calls.create(
                to=to_number,
                from_=self.from_number,
                url=callback_url,
                status_callback=f"{callback_url}/status",
                status_callback_event=['initiated', 'ringing', 'answered', 'completed'],
                record=True,
                recording_status_callback=f"{callback_url}/recording"
            )
            
            result = {
                "call_sid": call.sid,
                "to_number": to_number,
                "from_number": self.from_number,
                "status": call.status,
                "farmer_id": farmer_id,
                "call_type": call_type,
                "initiated_at": datetime.utcnow().isoformat()
            }
            
            logger.info(f"Initiated call {call.sid} to {to_number}")
            return result
            
        except Exception as e:
            logger.error(f"Failed to initiate call: {e}")
            raise
    
    def generate_advisory_twiml(
        self,
        advisory_text: str,
        language: str = "en",
        allow_replay: bool = True
    ) -> str:
        """
        Generate TwiML for advisory delivery
        
        Args:
            advisory_text: Advisory message
            language: Language code
            allow_replay: Allow farmer to replay message
        
        Returns:
            TwiML XML string
        """
        response = VoiceResponse()
        
        # Greeting
        greeting = self._get_greeting(language)
        response.say(greeting, language=self._get_twilio_language(language))
        
        # Pause
        response.pause(length=1)
        
        # Advisory message
        response.say(advisory_text, language=self._get_twilio_language(language))
        
        if allow_replay:
            # Gather input for replay
            gather = Gather(
                num_digits=1,
                action="/voice/advisory/replay",
                method="POST",
                timeout=5
            )
            gather.say(
                self._get_replay_prompt(language),
                language=self._get_twilio_language(language)
            )
            response.append(gather)
        
        # Goodbye
        response.say(
            self._get_goodbye(language),
            language=self._get_twilio_language(language)
        )
        
        response.hangup()
        
        return str(response)
    
    def generate_chatbot_twiml(
        self,
        initial_message: str,
        language: str = "en",
        gather_url: str = "/voice/chatbot/input"
    ) -> str:
        """
        Generate TwiML for chatbot interaction
        
        Args:
            initial_message: Initial chatbot message
            language: Language code
            gather_url: URL to handle user input
        
        Returns:
            TwiML XML string
        """
        response = VoiceResponse()
        
        # Initial message
        response.say(initial_message, language=self._get_twilio_language(language))
        
        # Gather speech input
        gather = Gather(
            input='speech',
            action=gather_url,
            method="POST",
            language=self._get_twilio_language(language),
            speech_timeout="auto",
            speech_model="phone_call"
        )
        
        response.append(gather)
        
        # If no input, prompt again
        response.say(
            "I didn't hear anything. Please speak after the beep.",
            language=self._get_twilio_language(language)
        )
        response.redirect(gather_url)
        
        return str(response)
    
    def generate_ivr_twiml(
        self,
        menu_options: Dict[str, str],
        language: str = "en"
    ) -> str:
        """
        Generate TwiML for IVR menu
        
        Args:
            menu_options: Dict of digit -> option description
            language: Language code
        
        Returns:
            TwiML XML string
        """
        response = VoiceResponse()
        
        # Build menu prompt
        menu_text = "Please select an option. "
        for digit, option in menu_options.items():
            menu_text += f"Press {digit} for {option}. "
        
        gather = Gather(
            num_digits=1,
            action="/voice/ivr/handle",
            method="POST",
            timeout=5
        )
        gather.say(menu_text, language=self._get_twilio_language(language))
        response.append(gather)
        
        # If no input
        response.say("No input received. Goodbye.")
        response.hangup()
        
        return str(response)
    
    async def get_call_status(self, call_sid: str) -> Dict:
        """
        Get call status
        
        Args:
            call_sid: Twilio call SID
        
        Returns:
            Call status information
        """
        try:
            call = self.client.calls(call_sid).fetch()
            
            return {
                "call_sid": call.sid,
                "status": call.status,
                "duration": call.duration,
                "start_time": call.start_time.isoformat() if call.start_time else None,
                "end_time": call.end_time.isoformat() if call.end_time else None,
                "direction": call.direction,
                "answered_by": call.answered_by
            }
            
        except Exception as e:
            logger.error(f"Failed to get call status: {e}")
            raise
    
    async def get_recording(self, recording_sid: str) -> bytes:
        """
        Get call recording
        
        Args:
            recording_sid: Twilio recording SID
        
        Returns:
            Recording audio bytes
        """
        try:
            recording = self.client.recordings(recording_sid).fetch()
            
            # Download recording
            recording_url = f"https://api.twilio.com{recording.uri.replace('.json', '.mp3')}"
            
            import httpx
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    recording_url,
                    auth=(settings.twilio_account_sid, settings.twilio_auth_token)
                )
                response.raise_for_status()
                return response.content
            
        except Exception as e:
            logger.error(f"Failed to get recording: {e}")
            raise
    
    async def hangup_call(self, call_sid: str):
        """
        Hangup active call
        
        Args:
            call_sid: Twilio call SID
        """
        try:
            self.client.calls(call_sid).update(status='completed')
            logger.info(f"Hung up call {call_sid}")
            
        except Exception as e:
            logger.error(f"Failed to hangup call: {e}")
            raise
    
    def _get_twilio_language(self, language_code: str) -> str:
        """Map language code to Twilio language"""
        mapping = {
            "hi": "hi-IN",
            "bn": "bn-IN",
            "te": "te-IN",
            "mr": "mr-IN",
            "ta": "ta-IN",
            "gu": "gu-IN",
            "kn": "kn-IN",
            "ml": "ml-IN",
            "pa": "pa-IN",
            "en": "en-IN"
        }
        return mapping.get(language_code, "en-IN")
    
    def _get_greeting(self, language: str) -> str:
        """Get greeting in language"""
        greetings = {
            "hi": "नमस्ते, यह कृषि मित्र है।",
            "en": "Hello, this is KrishiMitra.",
            "ta": "வணக்கம், இது கிருஷி மித்ரா.",
            "te": "నమస్కారం, ఇది కృషి మిత్ర.",
        }
        return greetings.get(language, greetings["en"])
    
    def _get_goodbye(self, language: str) -> str:
        """Get goodbye in language"""
        goodbyes = {
            "hi": "धन्यवाद। नमस्ते।",
            "en": "Thank you. Goodbye.",
            "ta": "நன்றி. வணக்கம்.",
            "te": "ధన్యవాదాలు. నమస్కారం.",
        }
        return goodbyes.get(language, goodbyes["en"])
    
    def _get_replay_prompt(self, language: str) -> str:
        """Get replay prompt in language"""
        prompts = {
            "hi": "संदेश दोबारा सुनने के लिए 1 दबाएं।",
            "en": "Press 1 to replay the message.",
            "ta": "செய்தியை மீண்டும் கேட்க 1 ஐ அழுத்தவும்.",
            "te": "సందేశాన్ని మళ్లీ వినడానికి 1 నొక్కండి.",
        }
        return prompts.get(language, prompts["en"])
    
    async def check_calling_hours(self, timezone: str) -> bool:
        """
        Check if current time is appropriate for calling
        
        Args:
            timezone: Farmer's timezone
        
        Returns:
            True if appropriate time to call
        """
        from datetime import datetime
        import pytz
        
        try:
            tz = pytz.timezone(timezone)
            local_time = datetime.now(tz)
            hour = local_time.hour
            
            # Appropriate calling hours: 9 AM to 7 PM
            return 9 <= hour < 19
            
        except Exception as e:
            logger.error(f"Failed to check calling hours: {e}")
            return True  # Default to allowing call
