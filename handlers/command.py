from aiogram import Router, Bot
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InputMediaPhoto

from datetime import date
from database import requests
from database.tables import Users
from keyboards import ikb_main_menu
from middlewares.middleware import UserMiddleware
from utils import FileManager
import messages
from .welcome import welcome_start

command_router = Router()
command_router.message.middleware(UserMiddleware())


@command_router.message(Command('start'))
async def command_start(message: Message, user: Users, command: CommandObject, state: FSMContext, bot: Bot):
    if user:
        msg_text = await FileManager.read('main_menu', name=user.name)
        await bot.send_photo(
            chat_id=message.from_user.id,
            photo=messages.MAIN_PICT,
            caption=msg_text,
            reply_markup=ikb_main_menu(),
        )
    else:
        await welcome_start(message, command, state, bot)
