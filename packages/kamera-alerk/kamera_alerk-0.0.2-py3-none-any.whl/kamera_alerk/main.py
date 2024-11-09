# coding: utf-8

from kamera_alerk.settings_handler import SettingsHandler, gen_config
from kamera_alerk.db_handler import DBHandler
from kamera_alerk.camera_hadler import CameraHandler
from kamera_alerk.parsing import get_args, process_start_json_settings
from kamera_alerk.telegram_bot import start_telegram_bot


def main():
    args = get_args()
    if args.command == 'gen_config':
        gen_config(args.file_path)
    elif args.command == 'start':
        process_start_json_settings(args)
        sh = SettingsHandler(args.file_path)

        DBHandler(sh)
        CameraHandler(sh)

        start_telegram_bot()
    else:
        print("Failed successfully (main). ")


if __name__ == "__main__":
    main()
