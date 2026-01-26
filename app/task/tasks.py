import contextlib
import shutil
import uuid
from celery import shared_task
from app import models, schemas
from app.ocr.scanner import fetch_text
from app.database import SessionLocal

def remove_file(path: str):
    """Remove a file or directory path without raising errors.

    This function attempts to delete the given path and suppresses any
    exceptions that occur during the removal process.

    Args:
        path: The filesystem path to remove.
    """
    with contextlib.suppress(Exception):
        shutil.rmtree(path)


def create_ocr_title_data(path: str) -> str:
    """Generate a user-friendly OCR title from a file path.

    This function derives a concise PDF title from the file name segment of
    the given path, truncating overly long names.

    Args:
        path: The full filesystem path to the source file.

    Returns:
        A string representing the generated PDF title.
    """
    split_path = path.split("/")[-1].split('.')[0]
    return f"{split_path[:10]}..pdf" if len(split_path) > 10 else f"{split_path}.pdf"


def insert_data_ocr_title(data: schemas.OCRTitleCreated):
    """Create and persist an OCR title record in the database.

    This function converts the provided OCR title data into a database model,
    saves it, and returns the newly created record.

    Args:
        data: The OCR title data to be stored.

    Returns:
        The persisted OCRTitle database model instance.
    """
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
    """Create and persist OCR data associated with an OCR title.

    This function stores the provided OCR page data in the database and
    returns the newly created record.

    Args:
        data: The OCR data payload to be stored.

    Returns:
        The persisted OCRData database model instance.
    """
    db = SessionLocal()
    try:
        data_model = models.OCRData(**data.model_dump())
        db.add(data_model)
        db.commit()
        db.refresh(data_model)
        return data_model
    finally:
        db.close()


def save_data_ocr_title(path: str, user_id:str):
    """Create and store an OCR title for a given file and user.

    This function generates a title from the file path, associates it with
    the specified user, and saves it to the database.

    Args:
        path: The filesystem path of the source file.
        user_id: The identifier of the user who owns the OCR title.

    Returns:
        The persisted OCRTitle database model instance.
    """
    title = create_ocr_title_data(path)
    obj = schemas.OCRTitleCreated(title=title, user_id=uuid.UUID(user_id))
    return insert_data_ocr_title(obj)


def get_data_from_data_items(path: str, user_id: str, random_uuid: str):
    """Retrieve OCR data items for a specific file and user.

    This function delegates to the OCR scanner to fetch text data and ensures
    that a meaningful error is raised when no data is available.

    Args:
        path: The filesystem path of the source file to be processed.
        user_id: The identifier of the user requesting the OCR data.
        random_uuid: The unique identifier associated with the OCR operation.

    Returns:
        The OCR data items returned by the scanner.

    Raises:
        ValueError: If no OCR data is found for the given path.
    """
    data = fetch_text(path, user_id, random_uuid)
    if data is None:
        raise ValueError(f"No OCR data found for path: {path}")
    return data


def save_data_ocr_data(path: str, user_id: str, random_uuid: str):
    """Persist OCR extraction results for a given file and user.

    This function coordinates fetching OCR text, creating the associated title,
    and storing each page of OCR data, returning identifiers for the saved data.

    Args:
        path: The filesystem path of the source file to extract OCR from.
        user_id: The identifier of the user owning the OCR data.
        random_uuid: The unique identifier associated with the OCR extraction run.

    Returns:
        A dictionary containing metadata about the saved OCR data, including title IDs.
    """
    results = {}
    data = get_data_from_data_items(path, user_id, random_uuid)
    text_data = save_data_ocr_title(path, user_id)
    for key, val in data.items():
        obj = schemas.OCRDataCreated( title_id=text_data.id, page=key, data=val)
        result = insert_data_ocr_data(obj)
        results['title_id'] = result.title_id
    return results


@shared_task(bind=True)
def excecute_ocr_pdf_extraction_task(self, path: str, user_id: str):
    """Run the asynchronous OCR extraction workflow for a PDF file.

    This task orchestrates OCR processing, persists the extracted data, and
    cleans up any temporary resources created during the operation.

    Args:
        path: The filesystem path to the PDF file to be processed.
        user_id: The identifier of the user who initiated the OCR task.

    Returns:
        A dictionary containing metadata about the saved OCR data, including title IDs.
    """
    random_uuid = uuid.uuid4()
    result = save_data_ocr_data(path, user_id, str(random_uuid))
    remove_file(f"images/{user_id}/{random_uuid}/")
    return result