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

    def camera_net(self, id: int) -> (str, int):
        return self.__d["cameras-config"][id]["ip"], self.__d["cameras-config"][id]["port"]

    def camera_auth(self, id: int) -> (str, str):
        return self.__d["cameras-config"][id]["login"], self.__d["cameras-config"][id]["password"]


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
            "login": "admin",
            "password": "admin_password"
        },
        {
            "ip": "192.168.1.130",
            "port": "80",
            "login": "admin",
            "password": "admin_password"
        }
    ],
    "system":
    {
    	"log_file": "/path/to/log/file.txt",
    	"db_file": "/path/to/database/file.db",
    	"electricity_check_file": "/tmp/electricity_check_file.touch"
    }
}    
"""
    write_to_file_str(config_path, template_json_config)
