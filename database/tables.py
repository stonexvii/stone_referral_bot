from datetime import date

from sqlalchemy import String, BigInteger, Date, Boolean, ForeignKey
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String(900))
    tg_username: Mapped[str] = mapped_column(String(900), nullable=True)
    referral_id: Mapped[int] = mapped_column(BigInteger, nullable=True)
    register_date: Mapped[date] = mapped_column(Date)
    is_referral: Mapped[bool] = mapped_column(Boolean, default=False)
    balance: Mapped[int] = mapped_column(BigInteger)


class Menu(Base):
    __tablename__ = 'menu'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(900), default='Какой-то меню')
    button: Mapped[str] = mapped_column(String(900), nullable=True)
    description: Mapped[str] = mapped_column(String(4000), default='Описание')

    media = relationship('Media', back_populates='menu')


class Project(Base):
    __tablename__ = 'projects'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(900), default='Какой-то меню')
    button: Mapped[str] = mapped_column(String(900), nullable=True)
    description: Mapped[str] = mapped_column(String(4000), default='Описание')
    mini_desc: Mapped[str] = mapped_column(String(900), default='Описание')
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    media = relationship('Media', back_populates='project')
    buttons = relationship('Button', back_populates='project')


class Media(Base):
    __tablename__ = 'media'
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    menu_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('menu.id'), nullable=True)
    project_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('projects.id'), nullable=True)
    media_id: Mapped[str] = mapped_column(String(900), default='Какой-то меню')

    menu = relationship('Menu', back_populates='media')
    project = relationship('Project', back_populates='media')


class Button(Base):
    __tablename__ = 'buttons'
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    project_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('projects.id'))
    text: Mapped[str] = mapped_column(String(900), nullable=True)
    callback: Mapped[str] = mapped_column(String(900), nullable=True)
    url: Mapped[str] = mapped_column(String(900), nullable=True)

    project = relationship('Project', back_populates='buttons')
