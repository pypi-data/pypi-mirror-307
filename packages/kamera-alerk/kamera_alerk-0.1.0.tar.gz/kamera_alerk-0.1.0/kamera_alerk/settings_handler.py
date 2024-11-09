# coding: utf-8

from ksupk import singleton_decorator, restore_json, write_to_file_str


@singleton_decorator
class SettingsHandler:

    def __init__(self, json_path: str):
        self.__json_setting_path = json_path
        self.__d = restore_json(json_path)

    def d(self) -> dict:
        return self.__d.copy()

    def db_path(self) -> str:
        return self.__d["system"]["db_file"]

    def tele_token(self) -> str:
        return self.__d["telegram-config"]["token"]

    def tele_password(self) -> str:
        return self.__d["telegram-config"]["password"]

    def camera_num(self) -> int:
        return len(self.__d["cameras-config"])

    def camera_net(self, camera_num: int) -> (str, int):
        return self.__d["cameras-config"][camera_num]["ip"], self.__d["cameras-config"][camera_num]["port"]

    def camera_auth(self, camera_num: int) -> (str, str):
        return self.__d["cameras-config"][camera_num]["login"], self.__d["cameras-config"][camera_num]["password"]

    def camera_name(self, camera_num: int) -> str:
        return self.__d["cameras-config"][camera_num]["name"]

    def electricity_file(self) -> str:
        return self.__d["system"]["electricity_check_file"]

    def get_model_path(self) -> str:
        return self.__d["auto_find"]["model_path"]

    def get_sleep_and_between_timings(self) -> (float, float):
        return (self.__d["auto_find"]["sleep_timing"], self.__d["auto_find"]["between_timing"])


def gen_config(config_path: str):
    template_json_config = """{
    "telegram-config":
    {
        "token": "your_token_here",
        "password": "you_password_here"
    },
    "cameras-config":
    [
        {
            "ip": "192.168.1.129",
            "port": "80",
            "name": "Camera 1",
            "login": "admin",
            "password": "admin_password"
        },
        {
            "ip": "192.168.1.130",
            "port": "80",
            "name": "Camera 2",
            "login": "admin",
            "password": "admin_password"
        }
    ],
    "auto_find":
    {
        "model_path": "/path/to/model.pt",
        "between_timing": 1.0,
        "sleep_timing": 2.0
    },
    "system":
    {
    	"log_file": "/path/to/log/file.txt",
    	"db_file": "/path/to/database/file.db",
    	"electricity_check_file": "/tmp/electricity_check_file.touch"
    }
}    
"""
    write_to_file_str(config_path, template_json_config)
