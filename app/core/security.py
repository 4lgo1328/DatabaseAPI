from fastapi import Header, HTTPException

from app.core.settings import settings

#from app.db. todo

INTERNAL_ADMIN_KEY = settings.admin_secret_key


async def verify_token(X_Internal_Token: str = Header(alias="X-Internal-Token")):
    if X_Internal_Token != INTERNAL_ADMIN_KEY:
        raise HTTPException(status_code=403, detail="Unauthorized")

async def verify_key(public_user_token: int = Header(alias="X-User-Token")):
    pass
    #todo