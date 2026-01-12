from pymongo import AsyncMongoClient
from beanie import init_beanie
from dotenv import load_dotenv
from models import User, Account, Category, Transaction 
import os

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)



async def init_db():
    load_dotenv()
    db = os.getenv("DATABASE_URL")
    client = AsyncMongoClient(db)
    
    # Inicializa o Beanie com os modelos
    await init_beanie(
        database=client.db_financeiro,
        document_models=[User, Category, Transaction, Account]
    )
    #  await init_beanie(database=client.dbTeste, document_models=[Produto,Fornecedor,ProdutoFornecedor])