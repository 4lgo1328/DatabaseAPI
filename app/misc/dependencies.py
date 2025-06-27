from sqlalchemy.ext.asyncio import AsyncSession
from app.core.settings import settings
from app.models.user import User
from app.crud.user_crud import get_user
from app.misc.generator import first_alphabet, last_alphabet, magic_number, start_time

async def _verify_user_token(db: AsyncSession, telegram_id: int, token: str) -> bool:
    if token == settings.admin_secret_key: return True
    first_part = token[:5]
    for symb in first_part:
        if symb not in first_alphabet:
            return False
    last_part = token[-5:]
    for symb in last_part:
        if symb not in last_alphabet:
            return False
    main_part = token.replace(first_part, "").replace(last_part, "")
    if not ("S" in main_part):
        return False
    tgid_encoded, ts_encoded = main_part.split("S")
    if not (ts_encoded.isnumeric()) or not (tgid_encoded.isnumeric()):
        return False
    tgid = int((int(tgid_encoded) / magic_number) / magic_number)
    ts = int(int(ts_encoded) / magic_number)
    if tgid < 10_000 or tgid > 1_000_000_000_000:
        return False
    if ts < start_time or ts > start_time * 1.5:
        return False

    user: User | None = await get_user(db, telegram_id)
    if not user: return False
    return token==user.personal_public_token