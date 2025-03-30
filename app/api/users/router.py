from pathlib import Path
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Response,
    status,
)
from app.crud.users import get_user_audiofiles, update_user_info
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


@router.get("/audiofiles", response_model=list[FileOut])
async def get_user_files(
    session: AsyncSession = Depends(db.session_getter),
    current_user: UserOut = Depends(get_current_user),
):
    audiofiles = await get_user_audiofiles(
        user_id=current_user.id, session=session
    )

    return audiofiles
