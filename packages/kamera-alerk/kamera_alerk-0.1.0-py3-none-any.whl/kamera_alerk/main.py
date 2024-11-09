# coding: utf-8

from kamera_alerk.settings_handler import SettingsHandler, gen_config
from kamera_alerk.db_handler import DBHandler
from kamera_alerk.camera_hadler import CameraHandler
from kamera_alerk.parsing import get_args, process_start_json_settings
from kamera_alerk.telegram_bot import start_telegram_bot, ProtectedBot
from kamera_alerk.NN import start_nn_circles
from threading import Thread
from ksupk import get_time_str
import time
import os


def main():
    args = get_args()
    if args.command == 'gen_config':
        gen_config(args.file_path)
    elif args.command == 'start':
        process_start_json_settings(args)
        sh = SettingsHandler(args.file_path)

        DBHandler(sh)
        CameraHandler(sh)

        t = Thread(target=start_telegram_bot)
        t.start()

        t = Thread(target=electricity_check)
        t.start()

        t = Thread(target=start_nn_circles)
        t.start()
    else:
        print("Failed successfully (main). ")


def electricity_check():
    time.sleep(5)
    try:
        sh = SettingsHandler()
        if os.path.isfile(sh.electricity_file()):
            msg = f"⚠️ kamera_alerk restarted ({get_time_str()})."
        else:
            msg = f"⚠️ kamera_alerk restarted after lost electricity ({get_time_str()})."
            fd = open(sh.electricity_file(), 'w')
            fd.flush()
            fd.close()
        ProtectedBot().notify_users_electricity_problem(msg)
        ProtectedBot().notify_users_taking_event("️⚠️ Система была взята на наблюдение после перезапуска. 🔧")
    except Exception as e:
        kek = f"{e}"


if __name__ == "__main__":
    main()
