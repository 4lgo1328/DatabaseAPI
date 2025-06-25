from fastapi import Header, HTTPException

from app.core.settings import settings

# Here security only by token is used. However, it can be enhanced later

INTERNAL_KEY = settings.secret_key


async def verify_token(X_Internal_Token: str = Header(alias="X-Internal-Token")):
    if X_Internal_Token != INTERNAL_KEY:
        raise HTTPException(status_code=403, detail="Unauthorized")