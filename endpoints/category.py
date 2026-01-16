from fastapi import APIRouter, HTTPException, status
from models import Category, CategoryCreate, User
from beanie import PydanticObjectId
from pydantic import BaseModel

router = APIRouter()

class CategoryUpdate(BaseModel):
    nome: str | None = None

# --- ROTAS ---

@router.post("/", response_model=Category, status_code=status.HTTP_201_CREATED)
async def create_category(cat_in: CategoryCreate):
    user = await User.get(cat_in.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário vinculado não encontrado")
    
    new_cat = Category(nome=cat_in.nome, user=user) # type: ignore
    await new_cat.create()

    return new_cat

@router.get("/", response_model=list[Category])
async def get_categories(user_id: PydanticObjectId | None = None, limit: int = 10, skip: int = 0):
    query = Category.find_all()
    if user_id:
        query = Category.find(Category.user.id == user_id) # type: ignore
    
    return await query.skip(skip).limit(limit).to_list()

@router.get("/{cat_id}", response_model=Category)
async def get_category(cat_id: PydanticObjectId):
    cat = await Category.get(cat_id)
    if not cat:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    return cat

@router.patch("/{cat_id}", response_model=Category)
async def update_category(cat_id: PydanticObjectId, cat_in: CategoryUpdate):
    cat = await Category.get(cat_id)
    if not cat:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    
    await cat.set(cat_in.model_dump(exclude_unset=True))
    return cat

@router.delete("/{cat_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(cat_id: PydanticObjectId):
    cat = await Category.get(cat_id)
    if not cat:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    await cat.delete()
    return None