import paddle
from paddleocr import PPStructureV3


paddle.set_flags({
    "FLAGS_fraction_of_cpu_memory_to_use": 0.2, # Adjust this value as needed
    "FLAGS_allocator_strategy": "naive_best_fit",
    "FLAGS_eager_delete_scope": True,
    "FLAGS_eager_delete_tensor_gb": 0.0,
    "FLAGS_fast_eager_deletion_mode": True,
    "FLAGS_use_pinned_memory": False
})


ocr_model = None

def run_ocr_model():
    global ocr_model
    if ocr_model is None:
        ocr_model = PPStructureV3(
        paddlex_config="PP-StructureV3.yaml",
        use_doc_orientation_classify=False,
        use_doc_unwarping=False,
        use_textline_orientation=False,
        use_seal_recognition=False,
        use_chart_recognition=False,
        use_formula_recognition=True,
        use_table_recognition=True,
        text_recognition_model_name="PP-OCRv5_mobile_rec"
    )
    return ocr_model


