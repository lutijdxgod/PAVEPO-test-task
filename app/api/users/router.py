from pathlib import Path
import shutil
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    Response,
    UploadFile,
    status,
)
from app.api.users.utils import validate_audio_file
from app.config import settings
from app.crud.users import get_user_audiofiles, update_user_info
from app.models import models
from app.models.database import db_helper as db

from sqlalchemy.ext.asyncio import AsyncSession

from app.oauth2 import get_current_user
from app.schemas.audiofiles import FileOut
from app.schemas.auth import UserOut
from app.schemas.user import UserUpdate

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/my_info", response_model=UserOut)
async def get_my_info(
    current_user: UserOut = Depends(get_current_user),
):
    return current_user


@router.post("/update_info")
async def update_info(
    data: UserUpdate,
    session: AsyncSession = Depends(db.session_getter),
    current_user: UserOut = Depends(get_current_user),
):
    if not data.name and not data.surname:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You must update at least one field",
        )
    await update_user_info(user_id=current_user.id, session=session, data=data)

    return Response(
        status_code=status.HTTP_200_OK,
        content="Successfully updated user's info",
    )


@router.post("/upload_audiofile")
async def upload_audiofile(
    file: UploadFile = Depends(validate_audio_file),
    filename: str | None = Query(),
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


@router.get("/audiofiles", response_model=list[FileOut])
async def get_user_files(
    session: AsyncSession = Depends(db.session_getter),
    current_user: UserOut = Depends(get_current_user),
):
    audiofiles = await get_user_audiofiles(
        user_id=current_user.id, session=session
    )

    return audiofiles
