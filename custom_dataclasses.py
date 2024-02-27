from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import registry
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import Column
from sqlalchemy import Table

from typing import Optional
from typing import List

import telebot

reg = registry()

association_table = Table(
    "association_table",
    reg.metadata,
    Column("group_id", ForeignKey("groups.id"), primary_key=True),
    Column("member_id", ForeignKey("members.id"), primary_key=True),
)

@reg.mapped_as_dataclass(order=True)
class Member:
    __tablename__ = "members"

    username: Mapped[str]
    personal_chat_id: Mapped[Optional[int]] = mapped_column(default=None, nullable=True)
    id: Mapped[int] = mapped_column(primary_key=True)# = field(compare=False, repr=False)

    # group_id: Mapped[int] = mapped_column(ForeignKey("group.id"))
    # group: Mapped["Group"] = relationship(default=None)

    @staticmethod
    def from_(message: telebot.types.Message):
        # For some reason sometimes thinks the messages are coming from the bot itself
        if message.from_user.is_bot and message.reply_to_message and not message.reply_to_message.from_user.username:
            return Member(message.reply_to_message.from_user.username, message.reply_to_message.from_user.id)
        return Member(message.from_user.username, message.from_user.id)


@reg.mapped_as_dataclass(order=True)
class Group:
    __tablename__ = "groups"

    # TODO: make id the only field used when compared as a dataclass
    id: Mapped[int] = mapped_column(primary_key=True)  # = field(default=None, compare=False, repr=False)

    members: Mapped[List["Member"]] = relationship(secondary=association_table)
    # members: set[Member] = mapped_column(default_factory=set, compare=False, hash=False)# = field(default_factory=set, compare=False, hash=False)

    registering: Optional[telebot.types.Message] = None# = field(compare=False, hash=False, repr=False)

    title: Mapped[str] = mapped_column(default="")# = field(default="", hash=False)
