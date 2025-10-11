from celery import shared_task
from app.ocr.scanner import fetch_text

import sys
sys.path.append("OCR-Scanner/ocr/")

@shared_task(bind=True)
def excecute_ocr_pdf_extraction_task(self, path: str):
    print(path)
    fetch_text(path)
