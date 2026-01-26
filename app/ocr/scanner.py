import os
import gc
import markdown
import toml
from typing import Any
from PIL import Image
from pdf2image import convert_from_path
from app.ocr.model_ocr import run_ocr_model

with open('config.toml', 'r', encoding='utf-8') as f:
    config = toml.load(f)

MAX_WIDTH = int(config['resolution']['width'])
MAX_HEIGHT = int(config['resolution']['height'])

def clear_data(data):
    """Release references to in-memory data to aid garbage collection.

    This function removes the given data reference and explicitly triggers
    Python's garbage collector to free associated resources sooner.

    Args:
        data: The in-memory object to dereference and clear.
    """
    del data
    gc.collect()

def calculate_new_image_size(max_size: tuple[int, int], original_size: tuple[int, int]):
    """Compute scaled image dimensions that fit within a maximum size.

    This function preserves the original aspect ratio while determining
    new width and height values that do not exceed the given bounds.

    Args:
        max_size: The maximum allowed (width, height) for the resized image.
        original_size: The original (width, height) of the image.

    Returns:
        A tuple of (new_width, new_height) representing the resized dimensions.
    """
    calculate_new_ratio = min(
        max_size[0] / original_size[0],
        max_size[1] / original_size[1]
    )

    new_width = int(original_size[0] * calculate_new_ratio)
    new_height = int(original_size[1] * calculate_new_ratio)

    return new_width, new_height
  

def resize_images(image: Any, max_size: tuple[int, int] = (MAX_WIDTH, MAX_HEIGHT)):
    """Resize an image so it fits within a maximum resolution.

    This function scales the image down while preserving its aspect ratio,
    leaving images unchanged if they are already within the target size.

    Args:
        image: The image object to be resized.
        max_size: The maximum allowed (width, height) for the image.

    Returns:
        The resized image object, or the original image if no resizing was needed.
    """
    original_width, original_height = image.size

    if original_width <= max_size[0] and original_height <= max_size[1]:
        return image
    
    new_width, new_height = calculate_new_image_size(
        max_size=(max_size[0], max_size[1]), 
        original_size=(original_width, original_height)
    )

    return image.resize((new_width, new_height), Image.Resampling.LANCZOS)


def get_model_prediction(index, page_image, pipeline, user_id: str, random_uuid:str):
    """Generate OCR model predictions for a single page image.

    This function prepares the page image for inference, routes it through
    the OCR pipeline, and returns the model's prediction output.

    Args:
        index: The page index used for naming intermediate artifacts.
        page_image: The image object representing the page to analyze.
        pipeline: The OCR model pipeline used to perform prediction.
        user_id: The identifier of the user associated with this request.
        random_uuid: The unique identifier for this OCR processing session.

    Returns:
        The prediction result produced by the OCR pipeline for the page.
    """
    resized_image = resize_images(page_image)
    temp_image_path = os.path.join(f"images/{user_id}/{random_uuid}/", f"page_{index}.png")
    resized_image.save(temp_image_path, "PNG")
    return pipeline.predict(str(temp_image_path))

def out_result(index, result):
    """Convert a single OCR result page into HTML content.

    This function reads the page's markdown output from disk and transforms
    it into HTML suitable for downstream display or storage.

    Args:
        index: The page index used to locate the markdown file.
        result: The OCR result object capable of saving itself as markdown.

    Returns:
        A string containing the HTML representation of the page content.
    """
    result.save_to_markdown(save_path="output")
    file_path = os.path.join("output/", f"page_{index}.md")
    with open(file_path, 'r', encoding='utf-8') as file:
        markdown_text = file.read()
    return markdown.markdown(markdown_text)


def process_text(images, pipeline, user_id: str, random_uuid: str):
    """Orchestrate OCR processing for a sequence of page images.

    This function iterates through all pages, runs OCR, converts outputs to
    HTML, and aggregates the results keyed by page index.

    Args:
        images: An iterable of page image objects to process.
        pipeline: The OCR model pipeline used to perform predictions.
        user_id: The identifier of the user associated with this request.
        random_uuid: The unique identifier for this OCR processing session.

    Returns:
        A dictionary mapping page indices (as strings) to HTML content.
    """
    results_data = {}
    for index, page_image in enumerate(images, start=1):
        results = get_model_prediction(index, page_image, pipeline, user_id, random_uuid)
        for result in results:
            result_html_content = out_result(index, result)
            results_data[f"{index}"] = str(result_html_content)
        os.remove(f"images/{user_id}/{random_uuid}/page_{index}.png")
        clear_data(page_image)
    return results_data


def fetch_text(file_path, user_id: str, random_uuid: str):
    """Run the full OCR extraction pipeline for a PDF file.

    This function sets up the OCR model, prepares intermediate storage, and
    processes all pages of the document into structured HTML content.

    Args:
        file_path: The path to the PDF file to be processed.
        user_id: The identifier of the user requesting OCR processing.
        random_uuid: The unique identifier for this OCR processing session.

    Returns:
        A dictionary mapping page indices (as strings) to HTML content.
    """
    pipeline = run_ocr_model()
    os.makedirs(f'images/{user_id}/{random_uuid}/', exist_ok=True)
    images = convert_from_path(file_path)
    return process_text(images, pipeline, user_id, random_uuid)