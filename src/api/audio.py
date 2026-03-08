"""
Audio file serving for voice calls
"""
import logging
from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/audio", tags=["audio"])


@router.get("/{filename}")
async def serve_audio(filename: str):
    """Serve audio file for Twilio playback"""
    try:
        audio_path = Path("audio_cache") / filename

        if not audio_path.exists():
            raise HTTPException(status_code=404, detail="Audio file not found")

        return FileResponse(
            path=str(audio_path),
            media_type="audio/mpeg",
            filename=filename
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error serving audio: {e}")
        raise HTTPException(status_code=500, detail=str(e))
