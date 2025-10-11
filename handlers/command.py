from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

# from classes import FileManager
from database import requests
from fsm import NewUser
from keyboards import ikb_user_main_menu
import config

command_router = Router()


@command_router.message(Command('start'))
async def command_start(message: Message, command: CommandObject, state: FSMContext):
    user = await requests.get_user(message.from_user.id)
    if not user:
        message_text = 'Введите ваши имя и фамилию\nВводите реальные данные они будут использоваться в реферальной программе'
        keyboard = None
        await state.set_state(NewUser.input_name)
        await state.update_data(
            {
                'referral_id': int(command.args) if command.args else None,
            }
        )
    else:
        keyboard = ikb_user_main_menu()
        message_text = f'Привет, {user.user_name}!\nВот твоя реферальная ссылка:\n{config.REFERRAL_LINK_BASE}{message.from_user.id}\n\nДелись ей со своими друзьями! Они получат скидку от меня, а ты получишь кэшбек от сделки'
    await message.answer(
        text=message_text,
        reply_markup=keyboard,
    )
