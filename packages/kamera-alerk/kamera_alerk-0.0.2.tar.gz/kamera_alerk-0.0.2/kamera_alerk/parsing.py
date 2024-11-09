# coding: utf-8

import argparse
import os


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="kamera_alerk. Telegram bot for interact with cameras.")

    subparsers = parser.add_subparsers(dest='command', required=True)

    # gen_config
    gen_file_parser = subparsers.add_parser('gen_config', help='Generate config file')
    gen_file_parser.add_argument('file_path', type=str, help='Path to the file to generate')

    # start
    do_logic_parser = subparsers.add_parser('start', help='Perform logic')
    do_logic_parser.add_argument('file_path', type=str, help='Path to the config file. It is json format.')

    return parser.parse_args()


def process_start_json_settings(args: argparse.Namespace):
    env_start_settings_text = "kamera_alerk_json_start_config"
    if args.command == "start":
        if args.file_path is not None and args.file_path != "":
            return
        else:
            env_file_path = os.getenv(env_start_settings_text)
            if env_file_path is not None:
                args.file_path = env_file_path
                return
            else:
                print(f"No argument file_path and no env var \"{env_start_settings_text}\". Exiting.")
                exit(1)
    else:
        return
