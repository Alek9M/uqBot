import logging
import telebot
from dotenv import load_dotenv
import os
import signal

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

load_dotenv('.env')


class SignalHandler:
    shutdown_requested = False
    bot = None

    def __init__(self, bot):
        self.bot = bot
        signal.signal(signal.SIGINT, self.request_shutdown)
        signal.signal(signal.SIGTERM, self.request_shutdown)

    def request_shutdown(self, *args):
        print('Request to shutdown received, stopping')
        self.shutdown_requested = True
        bot.stop_polling()
        bot.stop_bot()
        bot.close()

    def can_run(self):
        return not self.shutdown_requested


class Member:
    username: str
    id: int


class Group:
    title: str
    id: int
    registering: telebot.types.Message
    members: list[Member] = []


# 'same origin' (Message) function to determine if messages come from the same group and person and returns Bool
def same_origin(message1: telebot.types.Message, message2: telebot.types.Message):
    if message1.chat.id != message2.chat.id:
        return False

    if message1.chat.type == "private":
        return True
    elif message1.chat.type == "supergroup":
        return message1.from_user.id == message2.from_user.id

    return False


groups: list[Group] = list()

def register_group(group: Group, from_: telebot.types.Message):
    group.title = from_.chat.title
    group.id = from_.chat.id
    group.registering = None


def init_regestering_group(from_: telebot.types.Message):
    group = Group()
    group.registering = from_

    groups.append(group)


def call_sender(of: telebot.types.Message):
    return f"@{of.from_user.username}"

if __name__ == '__main__':

    bot = telebot.TeleBot(os.getenv('TBOT_KEY'), parse_mode=None)  # You can set parse_mode by default. HTML or MARKDOWN


    @bot.message_handler(commands=['start'])
    def start_command(message: telebot.types.Message):
        if message.chat.type == "private":
            logging.log(logging.INFO, message.chat.username)
        elif message.chat.type == "supergroup":
            if any(group.id == message.chat.id for group in groups):
                bot.send_message(message.chat.id, "Already registered")
                return
            elif any(same_origin(group.registering, message) for group in groups):
                bot.send_message(message.chat.id, "Already registering")
                return

            init_regestering_group(message)

            bot.send_message(message.chat.id, f"{call_sender(message)}\nEnter password:")
            bot.register_next_step_handler(message, password_check)


    def password_check(message):
        if message.text == os.getenv('PASSWORD'):
            matched_groups = [group for group in groups if group.registering is not None and same_origin(group.registering, message)]
            if len(matched_groups) > 1 or len(matched_groups) == 0:
                bot.send_message(message.chat.id, "Groups error")
                return
            group = matched_groups[0]
            register_group(group, message)
            bot.send_message(message.chat.id, "Password accepted")
            if group.registering is not None and same_origin(group.registering, message):
                register_group(group, message)
                bot.send_message(message.chat.id, "Password accepted")
            else:
                bot.send_message(message.chat.id, "Unknown user")

        else:
            bot.send_message(message.chat.id, "Wrong password")
            return

        logging.log(logging.INFO, groups)

    @bot.message_handler(commands=['start', 'help'])
    def send_welcome(message):
        bot.reply_to(message, "Howdy, how are you doing?")
        if message.chat.type == "private":
            logging.log(logging.INFO, message.chat.username)

        if message.chat.type == "group":
            logging.log(logging.INFO, "Upgrade to superchat")

        if message.chat.type == "supergroup":
            chat = bot.get_chat(message.chat.id)
            count = bot.get_chat_member_count(message.chat.id)
            # bot.register_my_chat_member_handler()
            logging.log(logging.INFO, chat.username)
            logging.log(logging.INFO, count)
            logging.log(logging.INFO, message.chat.active_usernames)


    bot.infinity_polling()
