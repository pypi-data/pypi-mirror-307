# coding: utf-8

"""
Step 1. Find telegram bot named "@BotFather".
Step 2. To create a new bot type “/newbot” or click on it.
Step 3. Follow instructions.
Step 4. See a new API token generated for it. Like this: 270485614:AAHfiqksKZ8WmR2zSjiQ7_v4TMAKdiHm9T0
"""

from kamera_alerk.settings_handler import SettingsHandler
from kamera_alerk.db_handler import DBHandler
from kamera_alerk.camera_hadler import CameraHandler
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import re
import io
import time
from ksupk import singleton_decorator, get_time_str
from PIL import Image


@singleton_decorator
class ProtectedBot:
    BLOCK_TIME = 10 * 60  # 10 min

    def __init__(self, sh: "SettingsHandler", dbh: "DBHandler", ch: "CameraHandler"):
        self.sh = sh
        self.dbh = dbh
        self.ch = ch
        self.bot = telebot.TeleBot(self.sh.tele_token())
        self.attempts = {}
        self.blocked_users = {}
        self.__password = sh.tele_password()

        self.bot.message_handler(commands=['start'])(self.start)
        self.bot.message_handler(commands=['help'])(self.help)
        self.bot.message_handler(func=lambda message: True)(self.handle_message)
        self.bot.callback_query_handler(func=lambda call: True)(self.callback_handler)

    def start(self, message):
        user_id = message.from_user.id
        user_name = message.from_user.username
        if self.check_is_user_allowed(user_id):
            self.show_root(user_id)
        else:
            self.bot.send_message(user_id, f"Приветствую, {user_name}. \nВведите пароль: ")

    def __help_text(self) -> str:
        return "Тут будет текст с описанием кнопок? "

    def help(self, message):
        user_id = message.from_user.id
        self.bot.send_message(user_id, self.__help_text())

    def handle_message(self, message):
        user_id = message.from_user.id
        if not self.check_is_user_allowed(user_id):
            self.check_password(user_id, message)

    def check_is_user_allowed(self, tele_user_id: int) -> bool:
        allowed_user = self.dbh.get_user_by_telegram_id(tele_user_id)
        if allowed_user is None:
            return False
        else:
            return True

    def __new_user(self, telegram_user_id: int, telegram_user_name: str):
        self.dbh.add_user(telegram_user_name, telegram_user_id)
        users_to_notify = self.dbh.get_users_with_sub(6, id_only=True)
        self.notify_users(users_to_notify, f"New user: {telegram_user_name} ({telegram_user_id})")

    def check_password(self, user_id: int, message):
        message_text = message.text
        if user_id in self.blocked_users and (time.time() - self.blocked_users[user_id]) < ProtectedBot.BLOCK_TIME:
            self.bot.send_message(user_id, "Вы заблокированы на 10 минут за 3 неверные попытки ввода пароля.")
            return False

        if message_text == self.__password:
            self.bot.send_message(user_id, "Пароль принят!")

            self.__new_user(user_id, message.from_user.username)

            self.show_root(user_id)
            if user_id in self.attempts:
                del self.attempts[user_id]
            return True
        else:
            self.bot.send_message(user_id, "Неверный пароль, попробуйте снова.")
            if user_id not in self.attempts:
                self.attempts[user_id] = 0
            self.attempts[user_id] += 1
            if self.attempts[user_id] >= 3:
                self.bot.send_message(user_id, "Вы были заблокированы на 10 минут за 3 неверные попытки.")
                self.blocked_users[user_id] = time.time()
                self.attempts[user_id] = 0
            return False

    def show_root(self, user_id: int):
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("🏷 Подписки", callback_data='root/subs'))
        for i in range(self.ch.camaras_num()):
            markup.add(InlineKeyboardButton(f"📷 Камера {i+1}", callback_data=f"root/camera_{i}"))
        markup.add(InlineKeyboardButton("🛎🎥 Взятие/снятие", callback_data='root/taking'))
        markup.add(InlineKeyboardButton("❔🧩 Помощь", callback_data='root/help!'))
        self.bot.send_message(user_id, "Выберите элемент:", reply_markup=markup)

    def show_subs_menu(self, user_id: int):
        user_subs = self.dbh.get_subs_of_user(self.dbh.get_user_by_telegram_id(user_id))
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("🚏 Назад", callback_data='root'))
        for k_i in user_subs:
            v_, _v = user_subs[k_i]
            sub_stat_text = "активна" if v_ == 1 else "неактивна"
            markup.add(InlineKeyboardButton(f"\"{k_i}\" (текущий статус подписки: {sub_stat_text})",
                                            callback_data=f"root/subs/{_v}!"))
        self.bot.send_message(user_id, "Выберите действие. Подписаться/отписаться на/от: ", reply_markup=markup)

    def show_take_menu(self, user_id: int):
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("🚏 Назад", callback_data='root'))
        markup.add(InlineKeyboardButton("📝 Проверить статус", callback_data='root/taking/status!'))
        markup.add(InlineKeyboardButton("🔐 Взять", callback_data='root/taking/on!'))
        markup.add(InlineKeyboardButton("🔓 Снять", callback_data='root/taking/off!'))
        self.bot.send_message(user_id, "Выберите действие:", reply_markup=markup)

    def show_camera_menu(self, user_id: int, camera_num: int):
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("🚏 Назад", callback_data='root'))
        markup.add(InlineKeyboardButton("📸 Снимок", callback_data=f"root/camera_{camera_num}/snapshot!"))
        self.bot.send_message(user_id, "Выберите действие:", reply_markup=markup)

    def callback_handler(self, call):
        """
        root:
            - Подписки
            - Камера_n
            - Взятие/снятие
            - Помощь
        root/subs:
            - назад (<- root)
            - man (<- root/subs/{n}!)
            - animal (<- root/subs/{n}!)
            - camera_problem (<- root/subs/{n}!)
            - anomaly (<- root/subs/{n}!)
            - electricity (<- root/subs/{n}!)
            - new_user (<- root/subs/{n}!)
            - take_switching (<- root/subs/{n}!)
        root/taking:
            - назад (<- root)
            - статус (<- root/taking/status!)
            - взять (<- root/taking/on!)
            - снять (<- root/taking/off!)
        root/camera_{n}:
            - назад (<- root)
            - Снимок (<- root/camera_{n}/snapshot!)
        """
        user_id = call.from_user.id

        if not self.check_is_user_allowed(user_id):
            self.bot.send_message(user_id, f"Введите пароль: ")
            return

        if call.data == "root":
            self.show_root(user_id)
        elif call.data == "root/subs":
            self.show_subs_menu(user_id)
        elif call.data == "root/taking":
            self.show_take_menu(user_id)
        elif call.data == "root/taking/status!":
            guard_status = CameraHandler().current_taking_guard()
            msg = "🛡Система в состоянии \"взята\". 🛡" if guard_status else "⛓️‍💥Система НЕ взята на наблюдение. ⛓️‍💥"
            self.bot.send_message(user_id, msg)
            self.show_take_menu(user_id)
        elif call.data == "root/taking/on!":
            guard_status = CameraHandler().current_taking_guard()
            msg_appendix = "До этого она уже было взятие. " if guard_status else "До этого система НЕ была взята на наблюдение. "
            CameraHandler().take_guard(True)
            self.bot.send_message(user_id, "🛡Система взята на наблюдение. 🛡. \n" + msg_appendix)
            if not guard_status:
                users_to_notify = self.dbh.get_users_with_sub(7, id_only=True)
                tele_name = self.dbh.get_telegram_username( self.dbh.get_user_by_telegram_id(user_id) )
                self.notify_users(users_to_notify, f"⚠️ Система была взята на наблюдение пользователем \"{tele_name}\". ")
            self.show_root(user_id)
        elif call.data == "root/taking/off!":
            guard_status = CameraHandler().current_taking_guard()
            msg_appendix = "До этого она была взята. " if guard_status else "До этого система уже была НЕ взята на наблюдение. "
            CameraHandler().take_guard(False)
            self.bot.send_message(user_id, "⚠️Система снята с наблюдения. ⚠️. \n" + msg_appendix)
            if guard_status:
                users_to_notify = self.dbh.get_users_with_sub(7, id_only=True)
                tele_name = self.dbh.get_telegram_username( self.dbh.get_user_by_telegram_id(user_id) )
                self.notify_users(users_to_notify, f"⚠️ Система была снята с наблюдения пользователем \"{tele_name}\". ")
            self.show_root(user_id)
        elif bool(re.match(r'^root/subs/\d+!$', call.data)):  # "root/subs/{n}!"
            match = re.match(r'^root/subs/(\d+)!$', call.data)
            sub_num = int(match.group(1))

            sub_new_status = not self.dbh.get_user_sub_state(user_id, sub_num)

            self.dbh.set_user_sub(user_id, sub_num, sub_new_status)

            self.show_subs_menu(user_id)
        elif bool(re.match(r'root/camera_\d+$', call.data)):  # root/camera_{i}
            match = re.match(r'root/camera_(\d+)$', call.data)
            camera_num = int(match.group(1))
            self.show_camera_menu(user_id, camera_num)
        elif bool(re.match(r'root/camera_\d+/snapshot!$', call.data)):  # root/camera_{camera_num}/snapshot!
            match = re.match(r'root/camera_(\d+)/snapshot!$', call.data)
            camera_num = int(match.group(1))

            # image = Image.new('RGB', (100, 100), color=(73, 109, 137))
            image = self.ch.snapshot(camera_num)
            byte_array = io.BytesIO()
            image.save(byte_array, format="PNG")
            byte_array.seek(0)

            self.bot.send_photo(user_id, photo=byte_array, caption=f"{get_time_str()}")

            self.show_camera_menu(user_id, camera_num)
        elif call.data == "root/help!":
            self.bot.send_message(user_id, self.__help_text())
            self.show_root(user_id)
        else:
            self.bot.send_message(user_id,
                                  "ProtectedBot.callback_handler: Failed successfully. \n"
                                  "Пожалуйста, сообщите об этом сообщении. ")

    def run(self):
        self.bot.polling(none_stop=True)

    def notify_users(self, user_ids: list, message_text: str):
        for id_i in user_ids:
            self.notify_user(id_i, message_text)

    def notify_user(self, user_id: int, message_text: str):
        try:
            self.bot.send_message(user_id, message_text)
        except Exception as e:
            kek = f"Ошибка при отправке сообщения: {e}"

    def notify_users_camera_problem(self, message_text: str):
        users = self.dbh.get_users_with_sub(3, id_only=True)
        self.notify_users(users, message_text)

def start_telegram_bot():
    sh = SettingsHandler()
    dbh = DBHandler(sh)
    ch = CameraHandler(sh)

    bot_instance = ProtectedBot(sh, dbh, ch)
    bot_instance.run()
