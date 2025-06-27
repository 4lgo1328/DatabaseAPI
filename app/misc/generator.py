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