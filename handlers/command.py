from aiogram import Router, Bot
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from database import requests
from database.tables import Users
from keyboards import ikb_main_menu
from middlewares.middleware import UserMiddleware
from utils import FileManager
from .welcome import welcome_start

command_router = Router()
command_router.message.middleware(UserMiddleware())


@command_router.message(Command('start'))
async def command_start(message: Message, user: Users, command: CommandObject, state: FSMContext, bot: Bot):
    if user:
        media = await FileManager.media_kwargs(
            text='main_menu',
            name=user.name,
        )
        await bot.send_photo(
            chat_id=message.from_user.id,
            photo=media['media'],
            caption=media['caption'],
            reply_markup=ikb_main_menu(user),
        )
    else:
        await welcome_start(message, command, state, bot)


@command_router.message(Command('rename'))
async def rename_user(message: Message, user: Users, command: CommandObject):
    if user and command.args:
        await message.answer(
            text=f'''Я обновил твое имя в нашей базе данных
Теперь буду называть тебя - {command.args}
Кстати, все твои рефералы, будут видеть это же имя!
Для перехода в главное меню используй команду /start''',
        )
        await requests.update_name(
            user_tg_id=message.from_user.id,
            name=command.args,
        )
    else:
        await message.answer(
            text=f'''Если хочешь изменить свое имя используй команду /rename и желаемое имя
Например:
/rename Олег Трубкин''',
        )
