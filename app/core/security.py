from sqlalchemy.ext.asyncio import AsyncSession

from app.core.settings import settings

from app.misc.misc import _verify_user_token


INTERNAL_ADMIN_KEY = settings.admin_secret_key


async def verify_admin_token(public_user_token: str) -> dict[str, str]:
    if public_user_token != INTERNAL_ADMIN_KEY:
        return {"status": "FAILED", "user_id": "NOT_SPECIFIED", "token": public_user_token}
    return {"status": "OK", "user_id": "NOT_SPECIFIED", "token": public_user_token}


async def verify_token(db: AsyncSession, telegram_id: int, public_user_token: str) -> dict[str, str]:

    res = await _verify_user_token(db, telegram_id, public_user_token)
    answer = dict()

    if res == False and public_user_token != INTERNAL_ADMIN_KEY:
        answer.update({
            "status": "FAILED",
            "user_id": str(res),
            "token": public_user_token
        })
        return answer

    answer.update({
        "status": "OK",
        "user_id": str(res),
        "token": public_user_token
    })
    return answer
