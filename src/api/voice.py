"""
Voice call API endpoints for Twilio integration
"""
from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import Response
from typing import Optional
import logging

from src.services.communication.voice_call_service import VoiceCallService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/voice", tags=["voice"])

# Initialize voice service
voice_service = VoiceCallService()


@router.post("/advisory")
async def advisory_call_webhook(request: Request):
    """
    Twilio webhook for advisory calls
    This endpoint is called when Twilio connects the call
    """
    try:
        # Get form data from Twilio
        form_data = await request.form()
        
        call_sid = form_data.get("CallSid")
        from_number = form_data.get("From")
        to_number = form_data.get("To")
        call_status = form_data.get("CallStatus")
        
        logger.info(f"Advisory call webhook: {call_sid}, status: {call_status}")
        
        # Generate advisory TwiML
        # In production, fetch actual advisory from database based on farmer
        advisory_text = """
        नमस्ते। यह कृषि मित्र है।
        
        आपकी फसल में पानी की कमी के संकेत दिख रहे हैं।
        जोखिम स्कोर 75 प्रतिशत है।
        
        तुरंत करने योग्य कार्य:
        
        पहला: अगले 24 घंटे में सिंचाई करें। लागत लगभग 500 रुपये।
        
        दूसरा: 3 दिन में मल्चिंग करें। लागत लगभग 1250 रुपये।
        
        कुल अनुमानित लागत 1750 रुपये है।
        
        कृपया जल्द से जल्द कार्रवाई करें।
        धन्यवाद।
        """
        
        twiml = voice_service.generate_advisory_twiml(
            advisory_text=advisory_text,
            language="hi",
            allow_replay=True
        )
        
        return Response(content=twiml, media_type="application/xml")
        
    except Exception as e:
        logger.error(f"Error in advisory webhook: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/advisory/replay")
async def advisory_replay_webhook(
    request: Request,
    Digits: Optional[str] = Form(None)
):
    """
    Handle replay request from farmer
    """
    try:
        form_data = await request.form()
        call_sid = form_data.get("CallSid")
        digits = form_data.get("Digits", "")
        
        logger.info(f"Replay request: {call_sid}, digits: {digits}")
        
        if digits == "1":
            # Replay the advisory
            advisory_text = """
            आपकी फसल में पानी की कमी के संकेत दिख रहे हैं।
            जोखिम स्कोर 75 प्रतिशत है।
            
            तुरंत करने योग्य कार्य:
            
            पहला: अगले 24 घंटे में सिंचाई करें। लागत लगभग 500 रुपये।
            
            दूसरा: 3 दिन में मल्चिंग करें। लागत लगभग 1250 रुपये।
            
            कुल अनुमानित लागत 1750 रुपये है।
            """
            
            twiml = voice_service.generate_advisory_twiml(
                advisory_text=advisory_text,
                language="hi",
                allow_replay=False  # Don't allow infinite replays
            )
        else:
            # End call
            from twilio.twiml.voice_response import VoiceResponse
            response = VoiceResponse()
            response.say("धन्यवाद। नमस्ते।", language="hi-IN")
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
    Digits: Optional[str] = Form(None)
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
