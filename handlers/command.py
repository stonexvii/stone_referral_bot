from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from database import requests
from database.tables import Users
from fsm import NewUser
from keyboards import ikb_user_main_menu
from middlewares.middleware import UserMiddleware
from utils import FileManager

command_router = Router()
command_router.message.middleware(UserMiddleware())


@command_router.message(Command('start'))
async def command_start(message: Message, command: CommandObject, user: Users, state: FSMContext):
    # user = await requests.get_user(message.from_user.id)
    if user:
        referral_block = '\n'
        if user.referral_id:
            referral = await requests.get_user(user.referral_id)
            referral_block = await FileManager.read('referral_block', referral_name=referral.user_name)
        msg_text = await FileManager.read('main_menu', username=user.user_name, referral_block=referral_block)
        keyboard = ikb_user_main_menu()
    else:

        await state.set_state(NewUser.input_name)
        await state.update_data(
            {
                'referral_id': int(command.args) if command.args else None,
            }
        )
        msg_text = await FileManager.read('new_user')
        keyboard = None
    await message.answer(
        text=msg_text,
        reply_markup=keyboard,
    )
