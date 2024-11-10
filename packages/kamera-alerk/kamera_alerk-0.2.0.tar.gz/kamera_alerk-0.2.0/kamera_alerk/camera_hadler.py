# coding: utf-8

from onvif import ONVIFCamera
from requests import get
from requests.auth import HTTPDigestAuth
import os
import time
from PIL import Image
import io
import threading
from ksupk import singleton_decorator
from kamera_alerk.settings_handler import SettingsHandler


@singleton_decorator
class CameraHandler:
    def __init__(self, sh: "SettingsHandler"):
        self._cameras = []
        self.__taking = True  # Взятие
        self.sh = sh
        for i in range(sh.camera_num()):
            self._cameras.append({"net": sh.camera_net(i), "auth": sh.camera_auth(i),
                                  "name": sh.camera_name(i), "lock": threading.Lock()})

    def camaras_num(self) -> int:
        return len(self._cameras)

    def snapshot(self, camera_num: int) -> "Image" or None:
        with self._cameras[camera_num]["lock"]:
            img = self.__snapshot_low(camera_num)
        if img is not None:
            rotation_angle, scale_factor = self.sh.camera_postprocessing(camera_num)
            if scale_factor != 1.0:
                new_width = int(img.width * scale_factor)
                new_height = int(img.height * scale_factor)
                resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                img = resized_img

            if rotation_angle != 0 and rotation_angle != 360:
                rotated_img = img.rotate(rotation_angle, expand=True)
                img = rotated_img

            return img
        else:
            return None

    def __snapshot_low(self, camera_num: int) -> "Image" or None:
        try:
            CAMERA_IP, PORT = self._cameras[camera_num]["net"]
            USERNAME, PASSWORD = self._cameras[camera_num]["auth"]
            camera = ONVIFCamera(CAMERA_IP, PORT, USERNAME, PASSWORD)

            media_service = camera.create_media_service()

            profiles = media_service.GetProfiles()
            profile = profiles[0]

            request = media_service.create_type('GetSnapshotUri')
            request.ProfileToken = profile.token
            snapshot_uri = media_service.GetSnapshotUri(request).Uri

            try:
                response = get(snapshot_uri, auth=HTTPDigestAuth(USERNAME, PASSWORD), stream=True, timeout=10)
                if response.status_code == 200:
                    image_data = response.content
                    image = Image.open(io.BytesIO(image_data))
                    return image
                else:
                    kek = f"(Камера {camera_num}) Не удалось получить снимок, код ошибки: {response.status_code}"
                    self.report_camera_problem(kek)
                    return None
            except Exception as e:
                kek = f"(Камера {camera_num}) Ошибка при получении снимка: {e}"
                self.report_camera_problem(kek)
                return None
        except Exception as e:
            kek = f"(Камера {camera_num}) Ошибка подключения или выполнения: {e}"
            self.report_camera_problem(kek)
            return None

    def take_guard(self, do: bool):
        self.__taking = do

    def current_taking_guard(self) -> bool:
        return self.__taking

    def report_camera_problem(self, msg: str):
        from kamera_alerk.telegram_bot import ProtectedBot
        ProtectedBot().notify_users_camera_problem(f"⚠️ Проблема с камерой: {msg}")


def transform_image(input_image_path, output_image_path, scale_factor, rotation_angle):
    # Открываем изображение
    with Image.open(input_image_path) as img:
        # Изменяем размер изображения
        new_width = int(img.width * scale_factor)
        new_height = int(img.height * scale_factor)
        resized_img = img.resize((new_width, new_height), Image.ANTIALIAS)

        # Поворачиваем изображение
        rotated_img = resized_img.rotate(rotation_angle, expand=True)

        # Сохраняем изменённое изображение
        rotated_img.save(output_image_path)