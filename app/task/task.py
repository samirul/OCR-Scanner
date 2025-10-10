from celery import shared_task

@shared_task(bind=True)
def excecute_ocr_pdf_extraction_task():
    pass