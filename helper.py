import telebot


def call_sender(of: telebot.types.Message):
    return f"@{of.from_user.username}"
