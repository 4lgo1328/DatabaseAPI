from fastapi import Header, HTTPException

from app.core.settings import settings
from app.db import get_db

from app.misc.dependencies import _verify_user_token


INTERNAL_ADMIN_KEY = settings.admin_secret_key


async def verify_admin_token(public_user_token: str) -> dict[str, str]:
    if public_user_token != INTERNAL_ADMIN_KEY:
        return dict(status="FAILED",
                    user_id="NOT_SPECIFIED",
                    token=public_user_token)
    return dict(status="OK",
                user_id="NOT_SPECIFIED",
                token=public_user_token)

async def verify_token(telegram_id: int, public_user_token: str) -> dict[str, str]:

    res = _verify_user_token(get_db(), telegram_id, public_user_token)
    answer = dict()

    if not(res or public_user_token != INTERNAL_ADMIN_KEY):
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