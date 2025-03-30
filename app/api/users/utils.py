from pathlib import Path
from fastapi import File, HTTPException, UploadFile

from app.api.users.constants import (
    ALLOWED_AUDIO_EXTENSIONS,
    ALLOWED_AUDIO_MIME_TYPES,
)


def validate_audio_file(file: UploadFile = File(...)):
    if file.content_type not in ALLOWED_AUDIO_MIME_TYPES:
        raise HTTPException(status_code=400, detail="Forbidden file type")

    extension = Path(file.filename).suffix
    if extension not in ALLOWED_AUDIO_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Forbidden file extension")

    return file
