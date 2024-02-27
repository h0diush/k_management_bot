from enum import Enum
from typing import Union

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from models import Base
from models.base import int_pk


class User(Base):
    __tablename__ = "users"

    user_id: Mapped[int_pk]
    username: Mapped[Union[str]] = mapped_column(nullable=True)


class StatusTask(Enum):
    done = "Выполнено"
    not_done = "Не выполнено"


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int_pk]
    title: Mapped[str]
    description: Mapped[Union[str]] = mapped_column(nullable=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    status: Mapped[StatusTask] = mapped_column(default=StatusTask.not_done)
