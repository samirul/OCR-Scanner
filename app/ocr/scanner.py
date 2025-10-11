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
    del data
    gc.collect()

def calculate_new_image_size(max_size: tuple[int, int], original_size: tuple[int, int]):
    calculate_new_ratio = min(
        max_size[0] / original_size[0],
        max_size[1] / original_size[1]
    )

    new_width = int(original_size[0] * calculate_new_ratio)
    new_height = int(original_size[1] * calculate_new_ratio)

    return new_width, new_height
  

def resize_images(image: Any, max_size: tuple[int, int] = (MAX_WIDTH, MAX_HEIGHT)):
    original_width, original_height = image.size

    if original_width <= max_size[0] and original_height <= max_size[1]:
        return image
    
    new_width, new_height = calculate_new_image_size(
        max_size=(max_size[0], max_size[1]), 
        original_size=(original_width, original_height)
    )

    return image.resize((new_width, new_height), Image.Resampling.LANCZOS)


def get_model_prediction(index, page_image, pipeline):
    resized_image = resize_images(page_image)
    temp_image_path = os.path.join("images/", f"page_{index}.png")
    resized_image.save(temp_image_path, "PNG")
    return pipeline.predict(str(temp_image_path))

def out_result(index, result):
    result.save_to_markdown(save_path="output")
    file_path = os.path.join("output/", f"page_{index}.md")
    with open(file_path, 'r', encoding='utf-8') as f:
        markdown_text = f.read()
    return markdown.markdown(markdown_text)


def process_text(images, pipeline):
    results_data = {}
    for index, page_image in enumerate(images, start=1):
        results = get_model_prediction(index, page_image, pipeline)
        for result in results:
            result_html_content = out_result(index, result)
            results_data[f"{index}"] = str(result_html_content)
        os.remove(f"images/page_{index}.png")
        clear_data(page_image)
    return results_data


def fetch_text(file_path):
    pipeline = run_ocr_model()
    os.makedirs('images/', exist_ok=True)
    images = convert_from_path(file_path)
    return process_text(images, pipeline)