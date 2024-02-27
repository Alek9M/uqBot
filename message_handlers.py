import logging
import os

import telebot

from custom_dataclasses import *
from database_connection import add_group, db_register, add_member, db_find_group
from helper import *

groups: list[Group] = list()


# 'same origin' (Message) function to determine if messages come from the same group and person and returns Bool
def same_origin(message1: telebot.types.Message, message2: telebot.types.Message):
    if message1.chat.id != message2.chat.id:
        return False

    if message1.chat.type == "private":
        return True
    elif message1.chat.type == "supergroup":
        return message1.from_user.id == message2.from_user.id

    return False


def originates(message: telebot.types.Message, from_: Group):
    return message.chat.id == from_.id


def register_group(group: Group, from_: telebot.types.Message):
    group.registering = None
    member = Member(id=from_.from_user.id, username=from_.from_user.username)
    db_register(group, member)
    groups.remove(group)


def init_registering_group(from_: telebot.types.Message):
    group = Group(id=from_.chat.id, registering=from_, title=from_.chat.title)
    groups.append(group)


def init_bot_handlers(bot):
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

            init_registering_group(message)

            bot.send_message(message.chat.id, f"{call_sender(message)}\nEnter password:")
            bot.register_next_step_handler(message, password_check)

    def password_check(message):
        if message.text == os.getenv('PASSWORD'):
            matched_groups = [group for group in groups if
                              group.registering is not None and same_origin(group.registering, message)]
            if len(matched_groups) > 1 or len(matched_groups) == 0:
                bot.send_message(message.chat.id, "Groups error")
                return
            group = matched_groups[0]
            # register_group(group, message)
            # bot.send_message(message.chat.id, "Password accepted")
            if group.registering is not None and same_origin(group.registering, message):
                register_group(group, message)
                bot.register_next_step_handler(message, processing)
                bot.send_message(message.chat.id, "Password accepted")
                bot.send_message(group.id, f"Registered {group.id}")
            else:
                bot.send_message(message.chat.id, "Unknown user")

        else:
            bot.send_message(message.chat.id, "Wrong password")
            return

        logging.log(logging.INFO, groups)

    @bot.message_handler(commands=['help'])
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

    @bot.message_handler(content_types=['text'])
    def processing(message: telebot.types.Message):
        if message.chat.type == "supergroup":
            group = db_find_group(message)
            member = Member.from_(message)
            if not group.members.contains(member):
                group.members.append(member)
                add_member(member)
                logging.info(group)
