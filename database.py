from pymongo import AsyncMongoClient
from beanie import init_beanie
from dotenv import load_dotenv
from models import User, Account, Category, Transaction 
import logging
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
DATABASE_NAME = os.getenv("DATABASE_NAME")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

logger = logging.getLogger(__name__)

db_client: AsyncMongoClient | None = None

async def init_db():
    global db_client
    if DATABASE_NAME is None:
        logger.error("A variável DATABASE_NAME não foi encontrada no .env")
        return
    
    try:
        db_client = AsyncMongoClient(DATABASE_URL)
        logger.info(f"Using DATABASE_URL: {DATABASE_URL}")
        db = db_client[DATABASE_NAME]

        await init_beanie(
            database=db,
            document_models=[User, Account, Category, Transaction],
        )
        logger.info(f"beanie conectado ao: {DATABASE_NAME}")
        
    except Exception as e:
        logger.error(f"Error ao inicializar o banco: {e}")

async def close_db():
    global db_client
    if db_client is not None:
        await db_client.close()
        logger.info(f"Closed DATABASE_URL: {DATABASE_URL}")
        db_client = None