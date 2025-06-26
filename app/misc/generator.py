from datetime import datetime
import random

first_alphabet = "BCDFGHJKLMNPQ"
last_alphabet = "RSTVWXZ"
magic_number = 8
start_time = 1750950009

class InvalidTokenException(BaseException):
    pass

def generate_token(telegram_id: int):
    l = list()
    for i in range(5):
        l.append(random.choice(first_alphabet))
    l.append(str(telegram_id*magic_number*magic_number))
    l.append("S")
    l.append(str(int(datetime.now().timestamp()) * magic_number))
    for i in range(5):
        l.append(random.choice(last_alphabet))
    return "".join(l)

def validate_token(token: str) -> bool | tuple[int, int]:
    first_part = token[:5]
    for symb in first_part:
        if symb not in first_alphabet:
            return False
    last_part = token[-5:]
    for symb in last_part:
        if symb not in last_alphabet:
            return False
    main_part = token.replace(first_part, "").replace(last_part, "")
    if not("S" in main_part):
        return False
    tgid_encoded, ts_encoded = main_part.split("S")
    if not(ts_encoded.isnumeric()) or not(tgid_encoded.isnumeric()):
        return False
    tgid = int((int(tgid_encoded)/magic_number)/magic_number)
    ts = int(int(ts_encoded)/magic_number)
    if tgid < 10_000 or tgid > 1_000_000_000_000:
        return False
    if ts < start_time or ts > start_time*1.5:
        return False
    return tgid, ts

def decypher_token(token: str) -> tuple[int, int]:
    """returns a decyphered token: tgid: ts"""
    result: bool | tuple[int, int] = validate_token(token)
    if isinstance(result, tuple):
        return result
    raise InvalidTokenException("Token is invalid!")