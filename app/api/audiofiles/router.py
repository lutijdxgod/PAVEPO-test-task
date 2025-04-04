from pathlib import Path
import shutil
from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile
from app.api.users.utils import validate_audio_file
from app.functions.crud_helpers import get_single_entity_by_field
from app.models import models
from app.models.database import db_helper as db

from sqlalchemy.ext.asyncio import AsyncSession

from app.oauth2 import get_current_user
from app.schemas.audiofiles import FileOut
from app.schemas.auth import UserOut

router = APIRouter(prefix="/audiofiles", tags=["Audiofiles"])


@router.post("/upload")
async def upload_audiofile(
    file: UploadFile = Depends(validate_audio_file),
    filename: str | None = Query(default=None),
    session: AsyncSession = Depends(db.session_getter),
    current_user: UserOut = Depends(get_current_user),
):
    upload_dir = Path("uploaded_audiofiles")
    upload_dir.mkdir(exist_ok=True)

    new_filename = file.filename
    if filename:
        new_filename = filename + Path(file.filename).suffix

    file_path = upload_dir / new_filename

    if file_path.exists():
        raise HTTPException(
            status_code=400, detail="Файл с таким именем уже существует."
        )

    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    new_file = models.AudioFile(
        **{
            "filename": new_filename,
            "filepath": str(file_path),
            "owner_id": current_user.id,
        }
    )
    session.add(new_file)
    await session.commit()

    return {"filename": new_filename, "message": "Файл успешно загружен."}


@router.get("/{id}", response_model=FileOut)
async def get_audiofile_by_id(
    id: int,
    session: AsyncSession = Depends(db.session_getter),
    current_user: UserOut = Depends(get_current_user),
):
    file = await get_single_entity_by_field(
        models.AudioFile, models.AudioFile.id, id, session
    )

    return file
