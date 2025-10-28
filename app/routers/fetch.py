from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session, joinedload, selectinload
from sqlalchemy import select
from app import models, schemas, auth
from app.database import get_db
from app.task.tasks import excecute_ocr_pdf_extraction_task
from app.custom_exceptions.exceptions import check_valid_uuid

router = APIRouter(
    prefix="/ocr",
    tags=["ocr"]
)

async def query_ocr_data(db: Session, title_id: str, user_id: str):
    return db.scalars(select(models.OCRTitle)
        .where(models.OCRTitle.id == title_id)
        .where(models.OCRTitle.user_id == UUID(user_id))
        .options(selectinload(models.OCRTitle.ocr_data),
                 joinedload(models.OCRTitle.user)))



@router.post("/scan", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.CeleryOutResponse)
async def ocr_celery_task(path: schemas.GetPath, current_user: models.User = Depends(auth.get_current_user)):
    return excecute_ocr_pdf_extraction_task.delay(str(path.path), str(current_user.id)) # pyright: ignore[reportCallIssue]


@router.get("/titles/", status_code=status.HTTP_200_OK, response_model=List[schemas.OCRTitlesOut])
async def get_ocr_titles(db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    data = db.scalars(select(models.OCRTitle).where(models.OCRTitle.user_id == str(current_user.id))).all()
    if data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No OCR titles found")
    return data


@router.get("/data/{title_id}", status_code=status.HTTP_200_OK, response_model=List[schemas.OCRDataDetailedOut])
async def get_ocr_data(title_id: str, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    check_valid_uuid(title_id)
    data = await query_ocr_data(db, title_id, str(current_user.id))
    query = data.unique().first()
    if query is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No OCR data found")
    return [query]


