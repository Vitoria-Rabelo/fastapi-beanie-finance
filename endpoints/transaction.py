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
    """
    Criar uma nova transação.
    
    **Parâmetros:**
    - descricao: Descrição da transação (ex: Salário, Compra)
    - valor: Valor da transação em reais
    - data: Data da transação (opcional, usa data/hora atual se não informada)
    - tipo: Tipo da transação (Entrada, Saída, Transferência)
    - conta_id: ID da conta envolvida
    - categoria_id: ID da categoria para classificação
    
    **Retorna:** Transação criada com ID gerado
    
    **Erros:**
    - 404: Conta ou Categoria não encontradas
    """
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
        conta=account, 
        categoria=category 
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
    """
    Listar transações com múltiplos filtros.
    
    **Parâmetros:**
    - term: Buscar por descrição (case-insensitive, opcional)
    - year: Filtrar por ano (opcional)
    - min_value: Filtrar por valor mínimo (opcional)
    - skip: Número de registros a pular (padrão: 0)
    - limit: Quantidade de transações a retornar (padrão: 20)
    
    **Retorna:** Lista de transações filtradas e ordenadas por data (decrescente)
    
    **Exemplo:**
    - GET /transactions/?year=2026&min_value=100
    - GET /transactions/?term=salário&limit=10
    """
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
    """
    Obter resumo agregado de transações por tipo.
    
    **Retorna:**
    - _id: Tipo de transação (Entrada, Saída, Transferência)
    - total_valor: Soma total do valor das transações desse tipo
    - count: Quantidade de transações desse tipo
    
    **Exemplo de resposta:**
    ```json
    [
        {
            "_id": "Entrada",
            "total_valor": 5000.50,
            "count": 2
        },
        {
            "_id": "Saída",
            "total_valor": 1500.00,
            "count": 15
        }
    ]
    ```
    """
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
    """
    Obter uma transação específica pelo ID.
    
    **Parâmetros:**
    - trans_id: ID da transação (ObjectId)
    
    **Retorna:** Dados completos da transação com links resolvidos
    
    **Erros:**
    - 404: Transação não encontrada
    """
    trans = await Transaction.get(trans_id, fetch_links=True)
    if not trans:
        raise HTTPException(status_code=404, detail="Transação não encontrada")
    return trans

@router.patch("/{trans_id}", response_model=Transaction)
async def update_transaction(trans_id: PydanticObjectId, trans_in: TransactionUpdate):
    """
    Atualizar dados de uma transação.
    
    **Parâmetros:**
    - trans_id: ID da transação a atualizar
    - descricao: Nova descrição (opcional)
    - valor: Novo valor (opcional)
    - data: Nova data (opcional)
    - tipo: Novo tipo (opcional)
    
    **Retorna:** Transação atualizada
    
    **Erros:**
    - 404: Transação não encontrada
    """
    trans = await Transaction.get(trans_id)
    if not trans:
        raise HTTPException(status_code=404, detail="Transação não encontrada")
    
    await trans.set(trans_in.model_dump(exclude_unset=True))
    return trans

@router.delete("/{trans_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_transaction(trans_id: PydanticObjectId):
    """
    Deletar uma transação.
    
    **Parâmetros:**
    - trans_id: ID da transação a deletar
    
    **Retorna:** 204 No Content
    
    **Erros:**
    - 404: Transação não encontrada
    """
    trans = await Transaction.get(trans_id)
    if not trans:
        raise HTTPException(status_code=404, detail="Transação não encontrada")
    await trans.delete()
    return None