"""
Voice call API endpoints for Twilio integration
"""
import logging
from uuid import UUID

from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import Response
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.models.advisory import Advisory
from src.models.farmer import Farmer
from src.services.communication.voice_call_service import VoiceCallService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/voice", tags=["voice"])

# Initialize voice service
voice_service = VoiceCallService()


@router.post("/call/{farmer_id}")
async def initiate_call(
    farmer_id: UUID,
    db: Session = Depends(get_db)
):
    """
    Initiate a voice call to a farmer with their latest advisory
    """
    try:
        # Get farmer
        farmer = db.query(Farmer).filter(Farmer.farmer_id == farmer_id).first()
        if not farmer:
            raise HTTPException(status_code=404, detail="Farmer not found")

        # Get latest advisory for farmer
        advisory = db.query(Advisory).filter(
            Advisory.farmer_id == farmer_id
        ).order_by(Advisory.created_at.desc()).first()

        if not advisory:
            raise HTTPException(
                status_code=404,
                detail="No advisory found for this farmer. Please generate an advisory first."
            )

        # Get callback URL based on environment
        import os
        environment = os.getenv("ENVIRONMENT", "development")
        
        if environment == "production":
            # Use Elastic Beanstalk URL in production
            base_url = "http://krishimitra-prod.eba-gz6myy8n.ap-south-1.elasticbeanstalk.com"
        else:
            # Use ngrok URL for local development
            base_url = os.getenv("NGROK_URL", "https://emma-autecologic-gregg.ngrok-free.dev")
        
        callback_url = f"{base_url}/api/v1/voice/advisory"

        # Initiate call
        call_result = await voice_service.initiate_call(
            to_number=farmer.phone_number,
            callback_url=callback_url,
            farmer_id=str(farmer_id),
            call_type="advisory"
        )

        logger.info(f"Initiated call to farmer {farmer_id}: {call_result['call_sid']}")

        return {
            "status": "success",
            "call_sid": call_result["call_sid"],
            "message": f"Call initiated to {farmer.phone_number}"
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error initiating call: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to initiate call: {str(e)}")


@router.post("/advisory")
async def advisory_call_webhook(request: Request, db: Session = Depends(get_db)):
    """
    Twilio webhook for advisory calls
    This endpoint is called when Twilio connects the call
    """
    try:
        # Get form data from Twilio
        form_data = await request.form()

        call_sid = form_data.get("CallSid")
        from_number = form_data.get("From")  # Twilio number
        to_number = form_data.get("To")      # Farmer's number
        call_status = form_data.get("CallStatus")

        logger.info("=" * 80)
        logger.info("WEBHOOK CALLED: Advisory call webhook")
        logger.info(f"Call SID: {call_sid}, Status: {call_status}")
        logger.info(f"From: {from_number}, To: {to_number}")
        logger.info(f"All form data: {dict(form_data)}")
        logger.info("=" * 80)

        # Default values
        language = "hi"
        advisory_text = "No advisory available at this time."

        try:
            # Find farmer by phone number (the 'To' field contains farmer's number)
            if to_number:
                # Clean the phone number (remove any formatting)
                clean_number = to_number.strip()

                logger.info(f"Looking for farmer with phone: {clean_number}")

                farmer = db.query(Farmer).filter(Farmer.phone_number == clean_number).first()

                if farmer:
                    language = farmer.preferred_language
                    logger.info(f"Found farmer {farmer.farmer_id}, language: {language}")

                    # Get latest advisory for farmer
                    advisory = db.query(Advisory).filter(
                        Advisory.farmer_id == farmer.farmer_id
                    ).order_by(Advisory.created_at.desc()).first()

                    if advisory:
                        advisory_text = advisory.advisory_text
                        logger.info(f"Found advisory {advisory.advisory_id} with text length: {len(advisory_text)}")
                    else:
                        logger.warning(f"No advisory found for farmer {farmer.farmer_id}")
                        # Generate a default message in farmer's language
                        if language == "hi":
                            advisory_text = "नमस्ते किसान भाई, इस समय कोई सलाह उपलब्ध नहीं है। कृपया बाद में पुनः प्रयास करें।"
                        elif language == "te":
                            advisory_text = "నమస్కారం రైతు గారు, ఈ సమయంలో ఎటువంటి సలహా అందుబాటులో లేదు। దయచేసి తర్వాత మళ్లీ ప్రయత్నించండి।"
                        else:
                            advisory_text = "Hello farmer, no advisory is available at this time. Please try again later."
                else:
                    logger.warning(f"Farmer not found for phone: {clean_number}")
                    # Try to find any farmer and use their advisory
                    any_farmer = db.query(Farmer).first()
                    if any_farmer:
                        logger.info(f"Using fallback farmer: {any_farmer.farmer_id}")
                        language = any_farmer.preferred_language
                        advisory = db.query(Advisory).filter(
                            Advisory.farmer_id == any_farmer.farmer_id
                        ).order_by(Advisory.created_at.desc()).first()
                        if advisory:
                            advisory_text = advisory.advisory_text
            else:
                logger.error("No 'To' number in Twilio request")

        except Exception as db_error:
            logger.error(f"Database error in webhook: {db_error}", exc_info=True)
            # Continue with defaults

        # Generate TwiML response
        try:
            twiml = voice_service.generate_advisory_twiml(
                advisory_text=advisory_text,
                language=language,
                allow_replay=True
            )

            logger.info(f"Generated TwiML for language: {language}, text length: {len(advisory_text)}")
            return Response(content=twiml, media_type="application/xml")

        except Exception as twiml_error:
            logger.error(f"Error generating TwiML: {twiml_error}", exc_info=True)
            # Return a simple error message
            from twilio.twiml.voice_response import VoiceResponse
            response = VoiceResponse()
            response.say("An error occurred. Please try again later.", language="en-IN")
            response.hangup()
            return Response(content=str(response), media_type="application/xml")

    except Exception as e:
        logger.error(f"Error in advisory webhook: {e}", exc_info=True)
        # Return a simple error TwiML instead of raising exception
        from twilio.twiml.voice_response import VoiceResponse
        response = VoiceResponse()
        response.say("An error occurred. Please try again later.", language="en-IN")
        response.hangup()
        return Response(content=str(response), media_type="application/xml")


@router.post("/advisory/replay")
async def advisory_replay_webhook(
    request: Request,
    Digits: str | None = Form(None),
    db: Session = Depends(get_db)
):
    """
    Handle replay request from farmer
    """
    try:
        form_data = await request.form()
        call_sid = form_data.get("CallSid")
        digits = form_data.get("Digits", "")
        to_number = form_data.get("To")

        logger.info(f"Replay request: {call_sid}, digits: {digits}")

        # Find farmer by phone number
        farmer = db.query(Farmer).filter(Farmer.phone_number == to_number).first()

        if not farmer:
            language = "hi"
        else:
            language = farmer.preferred_language

        if digits == "1":
            # Get latest advisory for farmer
            if farmer:
                advisory = db.query(Advisory).filter(
                    Advisory.farmer_id == farmer.farmer_id
                ).order_by(Advisory.created_at.desc()).first()

                if advisory:
                    advisory_text = advisory.advisory_text
                else:
                    advisory_text = "No advisory available."
            else:
                advisory_text = "No advisory available."

            twiml = voice_service.generate_advisory_twiml(
                advisory_text=advisory_text,
                language=language,
                allow_replay=False  # Don't allow infinite replays
            )
        else:
            # End call
            from twilio.twiml.voice_response import VoiceResponse
            response = VoiceResponse()

            # Goodbye message in farmer's language
            goodbye_messages = {
                "hi": "धन्यवाद। नमस्ते।",
                "en": "Thank you. Goodbye.",
                "te": "ధన్యవాదాలు. వీడ్కోలు.",
                "ta": "நன்றி. பிரியாவிடை.",
                "mr": "धन्यवाद. निरोप."
            }

            language_codes = {
                "hi": "hi-IN",
                "en": "en-IN",
                "te": "te-IN",
                "ta": "ta-IN",
                "mr": "mr-IN"
            }

            goodbye_text = goodbye_messages.get(language, goodbye_messages["hi"])
            language_code = language_codes.get(language, "hi-IN")

            response.say(goodbye_text, language=language_code)
            response.hangup()
            twiml = str(response)

        return Response(content=twiml, media_type="application/xml")

    except Exception as e:
        logger.error(f"Error in replay webhook: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/advisory/status")
async def advisory_status_webhook(request: Request):
    """
    Twilio status callback for call events
    """
    try:
        form_data = await request.form()

        call_sid = form_data.get("CallSid")
        call_status = form_data.get("CallStatus")
        call_duration = form_data.get("CallDuration")

        logger.info(
            f"Call status update: {call_sid}, "
            f"status: {call_status}, duration: {call_duration}s"
        )

        # In production, update database with call status
        # await update_call_record(call_sid, call_status, call_duration)

        return {"status": "received"}

    except Exception as e:
        logger.error(f"Error in status webhook: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/advisory/recording")
async def advisory_recording_webhook(request: Request):
    """
    Twilio recording callback
    """
    try:
        form_data = await request.form()

        recording_sid = form_data.get("RecordingSid")
        recording_url = form_data.get("RecordingUrl")
        call_sid = form_data.get("CallSid")

        logger.info(
            f"Recording available: {recording_sid}, "
            f"call: {call_sid}, url: {recording_url}"
        )

        # In production, download and store recording
        # recording_data = await voice_service.get_recording(recording_sid)
        # await store_recording(call_sid, recording_data)

        return {"status": "received"}

    except Exception as e:
        logger.error(f"Error in recording webhook: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/chatbot/input")
async def chatbot_input_webhook(request: Request):
    """
    Handle voice input from chatbot interaction
    """
    try:
        form_data = await request.form()

        call_sid = form_data.get("CallSid")
        speech_result = form_data.get("SpeechResult")

        logger.info(f"Chatbot input: {call_sid}, speech: {speech_result}")

        # In production, process speech with AI agent
        # response_text = await process_farmer_query(speech_result)

        response_text = "मैं आपकी बात समझ गया। धन्यवाद।"

        twiml = voice_service.generate_chatbot_twiml(
            initial_message=response_text,
            language="hi"
        )

        return Response(content=twiml, media_type="application/xml")

    except Exception as e:
        logger.error(f"Error in chatbot webhook: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/ivr/handle")
async def ivr_handle_webhook(
    request: Request,
    Digits: str | None = Form(None)
):
    """
    Handle IVR menu selection
    """
    try:
        form_data = await request.form()
        call_sid = form_data.get("CallSid")
        digits = form_data.get("Digits", "")

        logger.info(f"IVR selection: {call_sid}, digits: {digits}")

        from twilio.twiml.voice_response import VoiceResponse
        response = VoiceResponse()

        if digits == "1":
            response.say("आप सलाह सुनने के लिए चुना है।", language="hi-IN")
            # Redirect to advisory
            response.redirect("/voice/advisory")
        elif digits == "2":
            response.say("आप एजेंट से बात करने के लिए चुना है।", language="hi-IN")
            # Connect to agent (in production)
            response.say("क्षमा करें, यह सुविधा जल्द ही उपलब्ध होगी।", language="hi-IN")
        else:
            response.say("गलत विकल्प। धन्यवाद।", language="hi-IN")

        response.hangup()

        return Response(content=str(response), media_type="application/xml")

    except Exception as e:
        logger.error(f"Error in IVR webhook: {e}")
        raise HTTPException(status_code=500, detail=str(e))
