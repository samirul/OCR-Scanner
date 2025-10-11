from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from app import models, schemas
from app.database import get_db

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

async def commit_to_db(db: Session, model_instance: models.User):
    db.add(model_instance)
    db.commit()
    db.refresh(model_instance)

async def check_user(db: Session, new_user: models.User):
    user = db.scalars(select(models.User).where(models.User.email == new_user.email)).first()
    if user is not None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"{new_user.email} already exists.")
    

async def check_user_id(db: Session, new_user: models.User):
    user_id = db.scalars(select(models.User).where(models.User.id == new_user.id)).first()
    if user_id is not None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"{new_user.id} already exists.")


@router.post("/create", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOutResponse)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    new_user = models.User(**user.model_dump())
    await check_user(db, new_user)
    await check_user_id(db, new_user)
    await commit_to_db(db, new_user)
    return new_user
