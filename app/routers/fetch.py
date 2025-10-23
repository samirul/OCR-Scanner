from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from app import models, schemas
from app.database import get_db
from app.task.tasks import excecute_ocr_pdf_extraction_task

router = APIRouter(
    prefix="/ocr",
    tags=["ocr"]
)

@router.post("/scan", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.CeleryOutResponse)
async def ocr_celery_task(path: schemas.GetPath):
    return excecute_ocr_pdf_extraction_task.delay(str(path.path)) # pyright: ignore[reportCallIssue]


@router.get("/titles/{user_id}", status_code=status.HTTP_200_OK, response_model=List[schemas.OCRTitlesOut])
async def get_ocr_titles(user_id: str, db: Session = Depends(get_db)):
    if (titles := db.scalars(select(models.OCRTitle).where(models.OCRTitle.user_id == user_id)).all()):
        return titles
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No OCR titles found for user_id: {user_id}")

 




