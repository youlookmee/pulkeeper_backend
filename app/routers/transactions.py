# app/routers/transactions.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.schemas import TransactionCreate, TransactionResponse
from app import crud

router = APIRouter()


# ------------------------------------------------------------
# 📌 Создать транзакцию
# ------------------------------------------------------------
@router.post("/", response_model=TransactionResponse)
async def create_transaction_api(data: TransactionCreate, db: AsyncSession = Depends(get_session)):
    tx = await crud.create_transaction(db, data)
    return tx


# ------------------------------------------------------------
# 📌 Получить историю транзакций
# ------------------------------------------------------------
@router.get("/{user_id}/history", response_model=list[TransactionResponse])
async def get_history_api(user_id: int, limit: int = 20, db: AsyncSession = Depends(get_session)):
    items = await crud.get_history(db, user_id, limit)
    return items


# ------------------------------------------------------------
# 📌 Обновить транзакцию
# ------------------------------------------------------------
@router.put("/{tx_id}", response_model=TransactionResponse)
async def update_transaction_api(tx_id: int, fields: dict, db: AsyncSession = Depends(get_session)):
    tx = await crud.update_transaction(db, tx_id, **fields)
    if not tx:
        raise HTTPException(404, "Транзакция не найдена")
    return tx


# ------------------------------------------------------------
# 📌 Удалить транзакцию
# ------------------------------------------------------------
@router.delete("/{tx_id}")
async def delete_transaction_api(tx_id: int, db: AsyncSession = Depends(get_session)):
    ok = await crud.delete_transaction(db, tx_id)
    if not ok:
        raise HTTPException(404, "Транзакция не найдена")
    return {"status": "deleted"}
