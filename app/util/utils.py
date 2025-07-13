import jwt
from app.core.settings import settings

def create_jwt_token(telegram_id: int) -> str:
    payload = {"telegram_id": telegram_id}
    return jwt.encode(payload, settings.admin_secret_key, algorithm=settings.algorithm)
