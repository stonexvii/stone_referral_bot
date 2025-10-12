from datetime import date

from sqlalchemy import String, BigInteger, Date
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase


class Base(AsyncAttrs, DeclarativeBase):
    pass


class Users(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    user_name: Mapped[str] = mapped_column(String(900))
    tg_user_name: Mapped[str] = mapped_column(String(900))
    referral_id: Mapped[int] = mapped_column(BigInteger, nullable=True)
    register_date: Mapped[date] = mapped_column(Date)
