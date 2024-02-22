import logging
import telebot

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

if __name__ == '__main__':

    bot = telebot.TeleBot("", parse_mode=None)  # You can set parse_mode by default. HTML or MARKDOWN


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

