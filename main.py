from fastapi import FastAPI
from endpoints import user, account, category, transaction
from contextlib import asynccontextmanager
from database import init_db

app = FastAPI()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    print("Banco de Dados Conectado")
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {"message": "API rodando e banco conectado"}