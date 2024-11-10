# coding: utf-8

import sqlite3
import threading
import os
from ksupk import singleton_decorator
from kamera_alerk.settings_handler import SettingsHandler
import re


@singleton_decorator
class DBHandler:
    def __init__(self, sh: "SettingsHandler"):
        self.__db_lock = threading.Lock()
        self.__db_path = sh.db_path()

        """
                        Типы подписок:
                        человек в кадре (man_sub)
                        животное в кадре (animal_sub)
                        пропала связь с камерой (camera_problem_sub)
                        аномалия (anomaly_sub)
                        пропадало электричество (electricity_sub)
                        новый пользователь (new_user_sub)
                        взятие/снятие (take_switching)
        """
        self._subs_nums = {1: "man_sub", 2: "animal_sub", 3: "camera_problem_sub", 4: "anomaly_sub",
                           5: "electricity_sub", 6: "new_user_sub", 7: "take_switching"}

        self.__initialize_db()

    def add_user(self, tele_username: str, user_id: int):
        username = self.clean_string(tele_username)
        with self.__db_lock:
            password_state = 1
            status = 0
            role = 0
            note = ""
            conn = sqlite3.connect(self.__db_path)
            cursor = conn.cursor()

            text_to_insert = ", ".join([self._subs_nums[k_i] for k_i in self._subs_nums]) + ","
            qqq = "?, "*len(self._subs_nums)
            cursor.execute(f'''
                INSERT INTO USERS (username, user_id, password_state, status,
                                   {text_to_insert}
                                   role, note)
                VALUES (?, ?, ?, ?, {qqq}?, ?)
            ''', (username, user_id, password_state, status,
                  *(0,)*len(self._subs_nums),
                  role, note))

            conn.commit()
            conn.close()

    def get_users_with_sub(self, sub_num: int, id_only: bool = False) -> list:
        """
        {1: "man_sub", 2: "animal_sub", 3: "camera_problem_sub",
        4: "anomaly_sub", 5: "electricity_sub", 6: "new_user_sub", 7: "take_switching"}
        """
        needed_sub = self._subs_nums[sub_num]

        with self.__db_lock:
            conn = sqlite3.connect(self.__db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            cursor.execute(f"SELECT * FROM USERS WHERE {needed_sub} = 1")

            users = [dict(row) for row in cursor.fetchall()]
            conn.close()
        if id_only:
            users = [user_i["user_id"] for user_i in users]
        return users

    def set_user_sub(self, user_tele_id: int, sub_num: int, sub_new_state: bool):
        """
        {1: "man_sub", 2: "animal_sub", 3: "camera_problem_sub",
        4: "anomaly_sub", 5: "electricity_sub", 6: "new_user_sub", 7: "take_switching"}
        """
        needed_sub = self._subs_nums[sub_num]
        sub_new_state_text = "1" if sub_new_state else "0"

        with self.__db_lock:
            conn = sqlite3.connect(self.__db_path)
            cursor = conn.cursor()

            cursor.execute(f"UPDATE USERS SET {needed_sub} = {sub_new_state_text} WHERE user_id = ?",
                           (user_tele_id,))

            conn.commit()
            conn.close()

    def get_user_sub_state(self, user_tele_id: int, sub_num: int) -> bool:
        """
        {1: "man_sub", 2: "animal_sub", 3: "camera_problem_sub",
        4: "anomaly_sub", 5: "electricity_sub", 6: "new_user_sub", 7: "take_switching"}
        """
        user = self.get_user_by_telegram_id(user_tele_id)
        user_sub_state_int = user[self._subs_nums[sub_num]]
        return False if user_sub_state_int == 0 else True

    def get_user_by_telegram_id(self, user_id: int) -> dict or None:
        with self.__db_lock:
            conn = sqlite3.connect(self.__db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            cursor.execute('''
                SELECT * FROM USERS
                WHERE user_id = ?
            ''', (user_id,))

            user = cursor.fetchone()
            conn.close()
            if user is None:
                return None
            else:
                return dict(user)

    def delete_user_by_telegram_id(self, user_id: int):
        with self.__db_lock:
            conn = sqlite3.connect(self.__db_path)
            cursor = conn.cursor()

            cursor.execute('''
                DELETE FROM USERS
                WHERE user_id = ?
            ''', (user_id,))

            conn.commit()
            conn.close()

    def __initialize_db(self):
        with self.__db_lock:
            conn = sqlite3.connect(self.__db_path)
            cursor = conn.cursor()

            """
            username -- telegram username
            user_id -- telegram user id
            password_state -- password challenge
            status -- status inside menu ways
                    {self._subs_nums}
            role -- роль (админ или кто-то ещё)
            note -- примечание
            """
            execute_text = """
                    CREATE TABLE IF NOT EXISTS USERS (
                        id INTEGER PRIMARY KEY,
                        username TEXT,
                        user_id INTEGER,
                        password_state INTEGER,
                        status INTEGER,
"""

            for k_i in self._subs_nums:
                v_i = self._subs_nums[k_i]
                execute_text += f"                        {v_i} INTEGER,\n"

            execute_text += """                        role INTEGER,
                        note TEXT
                    )
                """

            # print(execute_text)

            cursor.execute(execute_text)
            conn.commit()
            conn.close()

    def get_telegram_username(self, user: dict) -> str:
        return user["username"]

    def get_subs_of_user(self, user: dict) -> dict:
        """
        {1: "man_sub", 2: "animal_sub", 3: "camera_problem_sub",
        4: "anomaly_sub", 5: "electricity_sub", 6: "new_user_sub", 7: "take_switching"}
        """
        res = {
            "человек в кадре": (user[self._subs_nums[1]], 1),
            "животное в кадре": (user[self._subs_nums[2]], 2),
            "проблема с камерой": (user[self._subs_nums[3]], 3),
            "аномалия": (user[self._subs_nums[4]], 4),
            "перезапуск": (user[self._subs_nums[5]], 5),
            "новый пользователь": (user[self._subs_nums[6]], 6),
            "взятие/снятие": (user[self._subs_nums[7]], 7),
        }
        return res

    def clean_string(self, input_string: str) -> str:
        pattern = r'[^\w\s]'
        cleaned_string = re.sub(pattern, '', input_string, flags=re.UNICODE)
        return cleaned_string
