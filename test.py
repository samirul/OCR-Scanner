# # Initialize PaddleOCR instance using PPStructureV3

# import os
# import json
# import markdown
# import paddle
# import gc
# from pdf2image import convert_from_path
# from paddleocr import PPStructureV3
# from functools import lru_cache
# from PIL import Image

# paddle.set_flags({
#     "FLAGS_fraction_of_cpu_memory_to_use": 0.2, # Adjust this value as needed
#     "FLAGS_allocator_strategy": "naive_best_fit",
#     "FLAGS_eager_delete_scope": True,
#     "FLAGS_eager_delete_tensor_gb": 0.0,
#     "FLAGS_fast_eager_deletion_mode": True,
#     "FLAGS_use_pinned_memory": False
# })

# def resize_image(image, max_size=(1024, 1024)):
#     """
#     Resizes a PIL image to a smaller size, maintaining aspect ratio.
#     :param image: The PIL Image object to resize.
#     :param max_size: A tuple (width, height) specifying the maximum dimensions.
#     :return: The resized PIL Image object.
#     """
#     # Get original width and height
#     original_width, original_height = image.size

#     # Check if image is already smaller than max_size
#     if original_width <= max_size[0] and original_height <= max_size[1]:
#         return image

#     # Calculate new dimensions while maintaining aspect ratio
#     ratio = min(max_size[0] / original_width, max_size[1] / original_height)
#     new_width = int(original_width * ratio)
#     new_height = int(original_height * ratio)

#     # Resize the image using the LANCZOS filter for high quality downsampling
#     resized_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
#     print(resized_image)
#     return resized_image

# @lru_cache(maxsize=1)
# def get_ocr_model():
#     return PPStructureV3(
#     use_doc_orientation_classify=False,
#     use_doc_unwarping=False,
#     use_textline_orientation=False,
#     use_seal_recognition=False,
#     use_chart_recognition=False,
#     use_formula_recognition=False,
#     use_table_recognition=True,
#     text_recognition_model_name="PP-OCRv5_mobile_rec"
#     )


# # ocr_model = None

# # def get_ocr_model():
# #     global ocr_model
# #     if ocr_model is None:
# #         ocr_model = PPStructureV3(
# #         use_doc_orientation_classify=False,
# #         use_doc_unwarping=False,
# #         use_textline_orientation=False,
# #         use_seal_recognition=False,
# #         use_chart_recognition=False,
# #         use_formula_recognition=False,
# #         use_table_recognition=True,
# #         text_recognition_model_name="PP-OCRv5_mobile_rec"
# #     )
# #     return ocr_model

# # pipeline = PPStructureV3(
# #     use_doc_orientation_classify=False,
# #     use_doc_unwarping=False,
# #     use_textline_orientation=False
# #   )

# def process_text(pages):
#     pipeline = get_ocr_model()
#     os.makedirs('images/', exist_ok=True)
#     results_data = {}
#     for i, page_image in enumerate(pages, start=1):
#         print(f"Processing page {i+1}...")
#         resized_img = resize_image(page_image)
#         temp_image_path = os.path.join("images/", f"page_{i}.png")
#         resized_img.save(temp_image_path, "PNG")
#         result = pipeline.predict(str(temp_image_path))
#         for res in result:
#             res.save_to_markdown(save_path="output")
#             file_path = os.path.join("output/", f"page_{i}.md")
#             with open(file_path, 'r', encoding='utf-8') as f:
#                 markdown_text = f.read()
#             html_content = markdown.markdown(markdown_text)
#             results_data[f"page_{i}_data"] = str(html_content)
#         os.remove(f"images/page_{i}.png")
#         del page_image
#         gc.collect()
#     # os.removedirs('images/')
#     json_data = json.dumps({"result": f"{results_data}\n"})
#     print(json_data)

# pages = convert_from_path("/home/sag/Downloads/sample-tables.pdf")
# process_text(pages)

from ocr.scanner import fetch_text

data = fetch_text("/home/sag/Downloads/test1.pdf")
print(data)
