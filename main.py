from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import init_db

# Importando os módulos de rota
from endpoints import user, account, category, transaction

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Inicializa o banco ao subir a aplicação
    await init_db()
    print("Banco de Dados Conectado")
    yield

app = FastAPI(lifespan=lifespan)

# --- AQUI ESTAVA FALTANDO: Conectando as rotas ao app principal ---
app.include_router(user.router, prefix="/users", tags=["Users"])
app.include_router(account.router, prefix="/accounts", tags=["Accounts"])
app.include_router(category.router, prefix="/categories", tags=["Categories"])
app.include_router(transaction.router, prefix="/transactions", tags=["Transactions"])

@app.get("/")
async def root():
    return {"message": "API rodando e banco conectado"}