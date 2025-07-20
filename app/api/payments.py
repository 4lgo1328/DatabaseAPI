import logging

from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.models.payment import Payment
from app.schemas.payment import PaymentCreate, PaymentRead, PaymentUpdateStatusByTxn, PaymentUpdatePlanByTxn
from app.crud.payment_crud import (create_payment,
                                   get_payment_by_txn_id,
                                   get_payments_by_user,
                                   get_all_payments,
                                   update_payment_status,
                                   delete_payment_by_txn_id,
                                   update_payment_plan)
from app.core.security import verify_token, verify_admin_token
from typing import List


router = APIRouter(prefix="/payments", tags=["Payments"])

@router.post("/create", response_model=PaymentRead)
async def create_payment_route(payment_data: PaymentCreate,
                               db: AsyncSession = Depends(get_db),
                               token: str = Header(alias="X-Auth-Token")):
    res = await verify_token(db, payment_data.user_telegram_id, token)
    if res.get("status") != "OK":
        raise HTTPException(status_code=403, detail="Token is invalid")

    result = await create_payment(db, payment_data)

    return result

@router.get("/by_txn_id", response_model=PaymentRead)
async def get_payment_by_txn_id_route(payment_txn_id: str = Header(alias="Txn-ID"),
                                      db: AsyncSession = Depends(get_db),
                                      token: str = Header(alias="X-Auth-Token")):

    if not payment_txn_id:
        raise HTTPException(status_code=401, detail="Payment transaction id must be passed")

    payment: Payment | None = await get_payment_by_txn_id(db, payment_txn_id)

    if payment is None:
        raise HTTPException(status_code=404, detail="Not found")

    logging.log(logging.WARN, f"HERE-->{payment.user_telegram_id}<--")

    res = await verify_token(db, payment.user_telegram_id, token)
    if res.get("status") != "OK":
        raise HTTPException(status_code=403, detail="Token is invalid")

    return payment

@router.get("/by_user_id", response_model=List[PaymentRead])
async def get_payments_by_user_route(telegram_id: int = Header(alias="X-Telegram-ID"),
                                     db: AsyncSession = Depends(get_db),
                                     token: str = Header(alias="X-Auth-Token")):
    if not telegram_id:
        raise HTTPException(status_code=401, detail="Telegram id must be passed")

    res = await verify_token(db, telegram_id, token)
    if res.get("status") != "OK":
        raise HTTPException(status_code=403, detail="Token is invalid")

    result = await get_payments_by_user(db, telegram_id)
    return result

@router.put("/update_status", response_model=PaymentRead)
async def update_payment_status_route(data: PaymentUpdateStatusByTxn,
                                      db: AsyncSession = Depends(get_db),
                                      token: str = Header(alias="X-Auth-Token")):
    if not data.payment_txn_id:
        raise HTTPException(status_code=401, detail="Payment transaction id must be passed")

    if not data.new_status:
        raise HTTPException(status_code=401, detail="Status must be passed")
    payment: Payment | None = await get_payment_by_txn_id(db, data.payment_txn_id)

    if not payment:
        raise HTTPException(status_code=404, detail="Not found")

    res = await verify_admin_token(token)
    if res.get("status") != "OK":
        raise HTTPException(status_code=403, detail="Token is invalid")

    result = await update_payment_status(db, data.payment_txn_id, data.new_status)
    return result

@router.put("/update_plan", response_model=PaymentRead)
async def update_payment_plan_route(data: PaymentUpdatePlanByTxn,
                                    db: AsyncSession = Depends(get_db),
                                    token: str = Header(alias="X-Auth-Token")):
    if not data.payment_txn_id:
        raise HTTPException(status_code=401, detail="Payment transaction id must be passed")

    if not data.new_plan:
        raise HTTPException(status_code=401, detail="Plan must be passed")

    payment: Payment | None = await get_payment_by_txn_id(db, data.payment_txn_id)

    if not payment:
        raise HTTPException(status_code=404, detail="Not found")

    res = await verify_admin_token(token)
    if res.get("status") != "OK":
        raise HTTPException(status_code=403, detail="Token is invalid")

    result = await update_payment_plan(db, data.payment_txn_id, data.new_plan)
    return result

@router.get("/all", response_model=List[PaymentRead])
async def get_all_payments_route(db: AsyncSession = Depends(get_db),
                                 token: str = Header(alias="X-Auth-Token")):
    res = await verify_admin_token(token)
    if res.get("status") != "OK":
        raise HTTPException(status_code=403, detail="Token is invalid")

    return await get_all_payments(db)

@router.delete("/delete", response_model=PaymentRead)
async def delete_payment_route(payment_txn_id: str = Header(alias="Txn-ID"),
                               db: AsyncSession = Depends(get_db),
                               token: str = Header(alias="X-Auth-Token")):
    if not payment_txn_id:
        raise HTTPException(status_code=401, detail="Payment transaction id must be passed")
    payment: Payment | None = await get_payment_by_txn_id(db, payment_txn_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Not found")
    res = await verify_admin_token(token)
    if res.get("status") != "OK":
        raise HTTPException(status_code=403, detail="Token is invalid")
    result = await delete_payment_by_txn_id(db, payment_txn_id)
    return result
