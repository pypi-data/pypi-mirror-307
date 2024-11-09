# coding: utf-8

import numpy as np
import time
from ultralytics import YOLO

from PIL import Image, ImageDraw

from ksupk import get_time_str

from ultralytics.utils.checks import check_imshow
from ultralytics.utils.plotting import Annotator, colors

from kamera_alerk.settings_handler import SettingsHandler
from kamera_alerk.camera_hadler import CameraHandler
from kamera_alerk.telegram_bot import ProtectedBot
from pathlib import Path


def get_model() -> "model":
    sh = SettingsHandler()
    model = YOLO(Path(sh.get_model_path()))
        # names = model.model.names
        # Classification 	Detection 	Segmentation 	Kind
        # yolov8n-cls.pt 	yolov8n.pt 	yolov8n-seg.pt 	Nano
        # yolov8s-cls.pt 	yolov8s.pt 	yolov8s-seg.pt 	Small
        # yolov8m-cls.pt 	yolov8m.pt 	yolov8m-seg.pt 	Medium
        # yolov8l-cls.pt 	yolov8l.pt 	yolov8l-seg.pt 	Large
        # yolov8x-cls.pt 	yolov8x.pt 	yolov8x-seg.pt 	Huge
    return model


# def find_persons(model, frame: Image) -> tuple or None:
#     results = model(frame, verbose=False)
#     persons_count = 0
#     persons_boxes = []
#     if len(results) == 0:
#         return None
#     else:
#         for res_i in results[0]:
#             class_num = int(res_i.boxes.cls.cpu())
#             if class_num == 0:
#                 boxes = res_i.boxes.xyxy.cpu()
#                 # boxes_coord = [int(round(el_i, 0)) for el_i in boxes.tolist()[0]]
#                 boxes_coord = boxes.tolist()[0]
#                 draw = ImageDraw.Draw(frame)
#                 draw.rectangle(boxes_coord, width=1, outline="#0000ff")
#                 persons_boxes.append([int(round(el_i, 0)) for el_i in boxes_coord])
#                 persons_count += 1
#
#     return (frame, persons_count)


def find_persons(model, frame, proba_threshold: float):
    results = model(frame, verbose=False)
    persons_count = 0
    persons_boxes = []
    persons_probabilities = []

    if len(results) == 0:
        return None
    else:
        for res_i in results:
            for box in res_i.boxes:
                class_num = int(box.cls)
                if class_num == 0:
                    boxes = box.xyxy[0].numpy()
                    probability = box.conf.item()
                    if probability > proba_threshold:
                        draw = ImageDraw.Draw(frame)
                        draw.rectangle(boxes, width=1, outline="#0000ff")

                        text_position = (boxes[0], boxes[1])
                        draw.text(text_position, f'{probability:.2f}', fill="#00ff00")

                        persons_boxes.append([int(round(el_i, 0)) for el_i in boxes])
                        persons_probabilities.append(probability)
                        persons_count += 1

    return (frame, persons_count)


def start_nn_circles():
    time.sleep(5)

    model = get_model()
    proba_threshold = SettingsHandler().get_proba_threshold()

    sleep_time, between_time = SettingsHandler().get_sleep_and_between_timings()

    ch = CameraHandler()

    while True:
        try:
            for i in range(ch.camaras_num()):
                frame = ch.snapshot(i)
                if frame is not None:
                    findings = find_persons(model, frame, proba_threshold)
                    if findings is not None and findings[1] > 0:
                        boxed_frame, count = findings
                        msg = f"⚠️ ({get_time_str()}) Найдены люди на изображении ({count} шт.)"
                        ProtectedBot().notify_users_man_findings(msg, boxed_frame)
                time.sleep(between_time)

            time.sleep(sleep_time)
        except Exception as e:
            kek = f"{e}"

