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


def find_persons(model, frame: "Image", proba_threshold: float):
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
                    if probability*100 > proba_threshold:
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
            if CameraHandler().current_taking_guard():
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


"""
import cv2
import numpy as np

image1 = cv2.imread('image1.jpg')
image2 = cv2.imread('image2.jpg')

gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

diff = cv2.absdiff(gray1, gray2)

_, thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)

contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

for contour in contours:
    if cv2.contourArea(contour) > 500:  # Отфильтровать мелкие изменения
        cv2.drawContours(image1, [contour], -1, (0, 255, 0), 2)

cv2.imshow('Detected Changes', image1)
cv2.waitKey(0)
cv2.destroyAllWindows()

import cv2
import numpy as np

image1 = cv2.imread('image1.jpg')
image2 = cv2.imread('image2.jpg')

gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

diff = cv2.absdiff(gray1, gray2)

_, thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)

contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

for contour in contours:
    if cv2.contourArea(contour) > 500:
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(image1, (x, y), (x + w, y + h), (0, 255, 0), 2)

cv2.imshow('Detected Changes', image1)
cv2.waitKey(0)
cv2.destroyAllWindows()

import numpy as np
import cv2
 
# initialize the HOG descriptor/person detector
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

cv2.startWindowThread()

cap = cv2.VideoCapture(0)

out = cv2.VideoWriter(
    'output.avi',
    cv2.VideoWriter_fourcc(*'MJPG'),
    15.,
    (640,480))

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # resizing for faster detection
    frame = cv2.resize(frame, (640, 480))
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

    boxes, weights = hog.detectMultiScale(frame, winStride=(8,8) )

    boxes = np.array([[x, y, x + w, y + h] for (x, y, w, h) in boxes])

    for (xA, yA, xB, yB) in boxes:
        cv2.rectangle(frame, (xA, yA), (xB, yB),
                          (0, 255, 0), 2)
    
    out.write(frame.astype('uint8'))
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
out.release()
cv2.destroyAllWindows()
cv2.waitKey(1)

from onvif import ONVIFCamera
import cv2
import time

ip = 'CAMERA_IP'
port = 80  # Обычно 80
user = 'USER'
password = 'PASSWORD'

camera = ONVIFCamera(ip, port, user, password)

media_service = camera.create_media_service()

profiles = media_service.GetProfiles()
profile = profiles[0] 

stream_setup = {
    'StreamSetup': {'Stream': 'RTP-Unicast', 'Transport': {'Protocol': 'RTSP'}},
    'ProfileToken': profile.token
}
stream_uri = media_service.GetStreamUri(**stream_setup)

rtsp_url = stream_uri.Uri
print(f"RTSP URL: {rtsp_url}")

cap = cv2.VideoCapture(rtsp_url)

fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))

start_time = time.time()
record_time = 5  

while int(time.time() - start_time) < record_time:
    ret, frame = cap.read()
    if ret:
        out.write(frame)
        # cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

cap.release()
out.release()
cv2.destroyAllWindows()


3 animaly algos:
1. spider_hash
2. anomaly_row
3. moving_spot
"""