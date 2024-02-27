from datetime import datetime
from typing import Annotated

from sqlalchemy import text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

int_pk = Annotated[int, mapped_column(primary_key=True, unique=True)]
created_at = Annotated[datetime, mapped_column(
    server_default=text("TIMEZONE('utc', now())"))]


class Base(DeclarativeBase):
    created_at: Mapped[created_at]
