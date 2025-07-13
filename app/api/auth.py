from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from uuid import uuid4

from app.db.database import AsyncSessionLocal
from app.crud.user_crud import get_or_create_user
from app.util.utils import create_jwt_token

router = APIRouter()

login_codes: dict[str, dict] = {}

@router.post("/prepare-login")
async def prepare_login():
    code = str(uuid4())
    login_codes[code] = {"status": "waiting", "user": None}
    return {"code": code}


class LoginConfirmRequest(BaseModel):
    code: str
    telegram_id: int
    first_name: str
    username: str

@router.post("/confirm")
async def confirm_login(data: LoginConfirmRequest):
    if data.code not in login_codes:
        return {"status": "invalid code"}
    login_codes[data.code] = {
        "status": "ok",
        "user": {
            "id": data.telegram_id,
            "first_name": data.first_name,
            "username": data.username
        }
    }
    return {"status": "confirmed"}


@router.get("/status/{code}")
async def check_status(code: str):
    entry = login_codes.get(code)
    if not entry:
        return JSONResponse(status_code=404, content={"detail": "code not found"})

    if entry["status"] != "ok":
        return {"status": "waiting"}

    user_data = entry["user"]

    async with AsyncSessionLocal() as db:
        user = await get_or_create_user(
            db,
            telegram_id=user_data["id"],
            username=user_data["username"],
            first_name=user_data["first_name"]
        )

    token = create_jwt_token(user.telegram_id)

    return {
        "token": token,
        "id": str(user.telegram_id),
        "firstName": user.first_name,
        "username": user.username
    }

class TelegramCallbackRequest(BaseModel):
    code: str
    id: int
    first_name: str
    username: str

@router.post("/telegram_callback")
async def telegram_callback(req: TelegramCallbackRequest):
    if req.code not in login_codes:
        return JSONResponse(status_code=404, content={"detail": "Code not found"})

    login_codes[req.code]["user"] = {
        "id": req.id,
        "first_name": req.first_name,
        "username": req.username
    }
    login_codes[req.code]["status"] = "ok"

    return {"status": "success"}
