from dataclasses import *
import telebot

from dataclasses import field


@dataclass(order=True, frozen=True)
class Member:
    username: str
    id: int = field(compare=False, repr=False)

    @staticmethod
    def from_(message: telebot.types.Message):
        # For some reason sometimes thinks the messages are coming from the bot itself
        if message.from_user.is_bot and message.reply_to_message and not message.reply_to_message.from_user.username:
            return Member(message.reply_to_message.from_user.username, message.reply_to_message.from_user.id)
        return Member(message.from_user.username, message.from_user.id)


@dataclass(order=True)
class Group:
    registering: telebot.types.Message = field(compare=False, hash=False, repr=False)
    members: set[Member] = field(default_factory=set, compare=False, hash=False)
    title: str = field(default="", hash=False)
    # TODO: make id the only field used when compared as a dataclass
    id: int | None = field(default=None, compare=False, repr=False)
