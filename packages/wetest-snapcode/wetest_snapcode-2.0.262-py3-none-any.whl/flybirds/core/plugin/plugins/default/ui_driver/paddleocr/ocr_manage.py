# -*- coding: utf-8 -*-
"""
Poco manage api
"""
import os

from paddleocr.tools.infer import utility
from paddleocr.tools.infer.predict_system import TextSystem

import flybirds.core.global_resource as gr


def ocr_init(lang=None):
    """
    Initialize the paddleocr object
     :return:
    """
    if lang is None:
        ocr_lang = gr.get_app_config_value("ocr_lang")
    else:
        ocr_lang = lang

    if ocr_lang != "":
        from paddleocr import PaddleOCR
        # Paddleocr support languages
        # example`ch`, `en`, `fr`, `german`, `korean`, `japan`
        det_limit_type = gr.get_frame_config_value("ocr_det_limit_type")
        det_limit_side_len = gr.get_frame_config_value("ocr_det_limit_side_len")

        try:
            if gr.get_frame_config_value("ocr_use_onnx"):
                ocr_onnx_model_dir = gr.get_frame_config_value("ocr_onnx_model_dir")
                if os.path.exists(ocr_onnx_model_dir):
                    parser = utility.init_args()
                    # Notice: PP-OCRv3 running failed with onnx, just use PP-OCRv2
                    #         see https://github.com/PaddlePaddle/PaddleOCR/issues/8699
                    args = parser.parse_args(args=["--use_gpu=False",
                                                   "--use_onnx=True",
                                                   "--rec_image_shape=3,32,320",
                                                   f"--rec_char_dict_path={ocr_onnx_model_dir}/ppocr_keys_v1.txt",
                                                   f"--det_model_dir={ocr_onnx_model_dir}/det/{ocr_lang}/model.onnx",
                                                   f"--rec_model_dir={ocr_onnx_model_dir}/rec/{ocr_lang}/model.onnx",
                                                   f"--cls_model_dir={ocr_onnx_model_dir}/cls/model.onnx"])
                    ocr = TextSystem(args)
                    ocr.ocr = PaddleOCR.ocr.__get__(ocr)
                    return ocr
        except:
            pass
            # ignore

        ocr = PaddleOCR(use_angle_cls=True,
                        lang=ocr_lang,
                        det_limit_type=det_limit_type,
                        det_limit_side_len=det_limit_side_len)
        # need to run only once to download and load model into memory
        return ocr
