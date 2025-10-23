import uuid
from celery import shared_task
from app import models, schemas
from app.ocr.scanner import fetch_text
from app.database import SessionLocal


def create_ocr_title_data(path: str) -> str:
    split_path = path.split("/")[-1].split('.')[0]
    return f"{split_path[:10]}..pdf" if len(split_path) > 10 else f"{split_path}.pdf"


def insert_data_ocr_title(data: schemas.OCRTitleCreated):
    db = SessionLocal()
    try:
        data = models.OCRTitle(**data.model_dump())
        db.add(data)
        db.commit()
        db.refresh(data)
        return data
    finally:
        db.close()


def insert_data_ocr_data(data: schemas.OCRDataCreated):
    db = SessionLocal()
    try:
        data_model = models.OCRData(**data.model_dump())
        db.add(data_model)
        db.commit()
        db.refresh(data_model)
        return data_model
    finally:
        db.close()


def save_data_ocr_title(path: str):
    title = create_ocr_title_data(path)
    user_id = "f47ac10b-58cd-4392-a678-0e02b2c3d479"
    obj = schemas.OCRTitleCreated(title=title, user_id=uuid.UUID(user_id))
    return insert_data_ocr_title(obj)


def get_data_from_data_items(path: str):
    data = fetch_text(path)
    if data is None:
        raise ValueError(f"No OCR data found for path: {path}")
    return data


def save_data_ocr_data(path: str):
    data = get_data_from_data_items(path)
    text_data = save_data_ocr_title(path)
    for key, val in data.items():
        obj = schemas.OCRDataCreated( title_id=text_data.id, page=key, data=val)
        insert_data_ocr_data(obj)


@shared_task(bind=True)
def excecute_ocr_pdf_extraction_task(self, path: str):
    save_data_ocr_data(path)
    

    
