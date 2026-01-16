from fastapi import APIRouter, HTTPException, status
from models import Transaction, TransactionCreate, Account, Category
from beanie import PydanticObjectId
from pydantic import BaseModel
from typing import List
from datetime import datetime
from beanie.odm.operators.find.comparison import GTE, LTE
from beanie.odm.operators.find.evaluation import RegEx

router = APIRouter()

class TransactionUpdate(BaseModel):
    descricao: str | None = None
    valor: float | None = None
    data: datetime | None = None
    tipo: str | None = None

# --- ROTAS ---

@router.post("/", response_model=Transaction, status_code=status.HTTP_201_CREATED)
async def create_transaction(trans_in: TransactionCreate):
    account = await Account.get(trans_in.conta_id)
    category = await Category.get(trans_in.categoria_id)
    
    if not account or not category:
        raise HTTPException(status_code=404, detail="Conta ou Categoria não encontradas")

    dt = trans_in.data if trans_in.data else datetime.now()

    new_trans = Transaction(
        descricao=trans_in.descricao,
        valor=trans_in.valor,
        data=dt,
        tipo=trans_in.tipo,
        conta=account, # type: ignore
        categoria=category # type: ignore
    )
    await new_trans.create()
    return new_trans

@router.get("/", response_model=List[Transaction])
async def list_transactions(
    term: str | None = None,
    year: int | None = None,
    min_value: float | None = None,
    skip: int = 0,
    limit: int = 20
):
    query = Transaction.find_all()

    if term:
        query = query.find(RegEx(Transaction.descricao, term, "i"))
    
    if year:
        start_date = datetime(year, 1, 1)
        end_date = datetime(year, 12, 31, 23, 59, 59)
        query = query.find(GTE(Transaction.data, start_date), LTE(Transaction.data, end_date))

    if min_value is not None:
        query = query.find(Transaction.valor >= min_value)

    return await query.sort("-data").skip(skip).limit(limit).to_list()

@router.get("/analytics/summary")
async def get_transaction_summary():
    pipeline = [
        {
            "$group": {
                "_id": "$tipo",
                "total_valor": {"$sum": "$valor"},
                "count": {"$sum": 1}
            }
        }
    ]
    result = await Transaction.aggregate(pipeline).to_list()
    return result

@router.get("/{trans_id}", response_model=Transaction)
async def get_transaction(trans_id: PydanticObjectId):
    trans = await Transaction.get(trans_id, fetch_links=True)
    if not trans:
        raise HTTPException(status_code=404, detail="Transação não encontrada")
    return trans

@router.patch("/{trans_id}", response_model=Transaction)
async def update_transaction(trans_id: PydanticObjectId, trans_in: TransactionUpdate):
    trans = await Transaction.get(trans_id)
    if not trans:
        raise HTTPException(status_code=404, detail="Transação não encontrada")
    
    await trans.set(trans_in.model_dump(exclude_unset=True))
    return trans

@router.delete("/{trans_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_transaction(trans_id: PydanticObjectId):
    trans = await Transaction.get(trans_id)
    if not trans:
        raise HTTPException(status_code=404, detail="Transação não encontrada")
    await trans.delete()
    return None