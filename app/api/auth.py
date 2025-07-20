from fastapi.exceptions import HTTPException
from fastapi import APIRouter, Depends, Header
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from uuid import uuid4
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import verify_admin_token
from app.crud.staff_crud import create_code, issue_code
from app.db.database import get_db
from app.crud.user_crud import get_or_create_user
from app.models.enums import UserRole
from app.schemas.user import UserGetOrCreate
from app.util.utils import create_jwt_token

router = APIRouter(prefix="/auth", tags=["Auth"])

login_codes = {}
last_cleanup = datetime.now()


async def cleanup_codes():
    global last_cleanup
    now = datetime.now()
    if now - last_cleanup > timedelta(minutes=5):
        expired = [code for code, data in login_codes.items()
                   if datetime.now() - data["created"] > timedelta(minutes=10)]
        for code in expired:
            del login_codes[code]
        last_cleanup = now


@router.post("/prepare-login")
async def prepare_login():
    await cleanup_codes()
    code = str(uuid4())
    login_codes[code] = {
        "status": "waiting",
        "user": None,
        "created": datetime.now()
    }
    return {"code": code}


class LoginConfirmRequest(BaseModel):
    code: str
    telegram_id: int
    first_name: str
    username: str


@router.post("/confirm")
async def confirm_login(data: LoginConfirmRequest, db: AsyncSession = Depends(get_db)):
    await cleanup_codes()

    if data.code not in login_codes:
        return JSONResponse(
            status_code=404,
            content={"detail": "Invalid code"}
        )

    user_data = UserGetOrCreate(
        telegram_id=data.telegram_id,
        username=data.username,
        first_name=data.first_name,
        phone_number=None
    )
    user = await get_or_create_user(db, user_data)

    token = create_jwt_token(user.telegram_id)

    login_codes[data.code] = {
        "status": "ok",
        "token": token,
        "user": {
            "id": str(user.telegram_id),
            "first_name": user.first_name,
            "username": user.username
        }
    }

    return {"status": "confirmed"}


@router.get("/status/{code}")
async def check_status(code: str):
    await cleanup_codes()
    entry = login_codes.get(code)

    if not entry:
        return JSONResponse(
            status_code=404,
            content={"detail": "Code not found or expired"}
        )

    if entry["status"] != "ok":
        return {"status": "waiting"}

    return {
        "token": entry["token"],
        "id": entry["user"]["id"],
        "firstName": entry["user"]["first_name"],
        "username": entry["user"]["username"]
    }

class TelegramCallbackRequest(BaseModel):
    code: str
    id: int
    first_name: str
    username: str

@router.post("/create-system-code", response_model=str)
async def create_system_code(token: str = Header(alias="X-Auth-Token"),
                             role: str = Header(alias="User-Role"),
                             db: AsyncSession = Depends(get_db)):
    auth = await verify_admin_token(token)
    if auth.get("status") != "OK":
        raise HTTPException(status_code=403, detail="Invalid auth token")
    formatted_role: UserRole | None = None
    match role.lower():
        case "assistant":
            formatted_role = UserRole.assistant
        case "manager":
            formatted_role = UserRole.manager
    if formatted_role is None:
        raise HTTPException(status_code=422, detail="Wrong formattd role given")
    code: str = await create_code(db, formatted_role)
    return code

@router.post("/issue-system-code", response_model=str)
async def issue_system_code(token: str = Header(alias="X-Auth-Token"),
                            code: str = Header(alias="X-User-Code"),
                            db: AsyncSession = Depends(get_db)):
    auth = await verify_admin_token(token)
    if auth.get("status") != "OK":
        raise HTTPException(status_code=403, detail="Invalid auth token")
    return await issue_code(db, code)
