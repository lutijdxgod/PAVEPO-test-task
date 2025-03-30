from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import models
from app.schemas.user import UserUpdate


async def update_user_info(
    user_id: int, session: AsyncSession, data: UserUpdate
) -> None:
    new_info = data.model_dump(exclude_unset=True)

    user_query = (
        update(models.User).where(models.User.id == user_id).values(new_info)
    )
    await session.execute(user_query)
    await session.commit()


async def get_user_audiofiles(user_id: int, session: AsyncSession):
    files_query = select(models.AudioFile).where(
        models.AudioFile.owner_id == user_id
    )
    query_result = await session.scalars(files_query)
    files = query_result.all()

    return files
