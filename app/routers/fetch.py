import json
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



