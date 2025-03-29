from urllib.parse import urlencode
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
import httpx
from sqlalchemy import select
from app.config import settings
from app.models import models
from app.models.database import db_helper as db

from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.auth import UserOut

router = APIRouter(prefix="/auth", tags=["Authentication"])

YANDEX_AUTH_URL = "https://oauth.yandex.ru/authorize"
YANDEX_TOKEN_URL = "https://oauth.yandex.ru/token"
YANDEX_USER_INFO_URL = "https://login.yandex.ru/info"


@router.get("/login")
async def login():
    params = {
        "response_type": "code",
        "client_id": settings.yandex.client_id,
        "scope": "login:email",
    }
    auth_url = f"{YANDEX_AUTH_URL}?{urlencode(params)}"
    return RedirectResponse(auth_url)


@router.get("/callback", response_model=UserOut)
async def auth_callback(
    request: Request, session: AsyncSession = Depends(db.session_getter)
):
    code = request.query_params.get("code")
    if not code:
        raise HTTPException(
            status_code=400, detail="Authorization code not provided"
        )
    token_data = {
        "grant_type": "authorization_code",
        "code": code,
        "client_id": settings.yandex.client_id,
        "client_secret": settings.yandex.client_secret,
    }

    async with httpx.AsyncClient() as client:
        token_response = await client.post(
            YANDEX_TOKEN_URL,
            data=token_data,
        )
        token_response_data = token_response.json()

        if token_response.status_code != 200:
            raise HTTPException(
                status_code=400, detail="Failed to obtain access token."
            )

        access_token = token_response_data.get("access_token")

        user_info_response = await client.get(
            YANDEX_USER_INFO_URL,
            headers={"Authorization": f"OAuth {access_token}"},
        )
        user_info = user_info_response.json()

        if user_info_response.status_code != 200:
            raise HTTPException(
                status_code=400, detail="Failed to obtain user info"
            )

        user_email = user_info.get("default_email")
        user_query = select(models.User).where(models.User.email == user_email)
        query_result = await session.scalars(user_query)
        user = query_result.first()

        if not user:
            new_user = models.User(**{"email": user_email})
            session.add(new_user)
            await session.commit()
            await session.refresh(new_user)
            user = new_user

        return user
