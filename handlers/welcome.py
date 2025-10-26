from datetime import date

from aiogram import Router, Bot, F
from aiogram.filters import CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, InputMediaPhoto

import config
from database import requests
from database.tables import User
from fsm.states import NewUser
from keyboards import ikb_welcome, ikb_main_menu
from keyboards.callback_data import CallbackWelcome
from middlewares.middleware import UserMiddleware
from utils import FileManager, MessagePath

welcome_router = Router()
welcome_router.message.middleware(UserMiddleware())
welcome_router.callback_query.middleware(UserMiddleware())


async def welcome_start(message: Message, command: CommandObject, state: FSMContext, bot: Bot):
    referral_id = None
    if command.args and command.args.isdigit():
        referral_id = int(command.args)
        referral = await requests.get_user(referral_id)
        referral_name = referral.name
        # msg_text = await FileManager.read(MessagePath.TEXT, 'welcome_start', referral_name=referral_name)
        msg_data = await requests.get_menu('welcome_start', as_kwargs=False, referral_name=referral_name)
    else:
        referral_name = None
        msg_data = await requests.get_menu('welcome_start_wor', as_kwargs=False)
    await state.update_data(
        {
            'referral': referral_name,
        }
    )
    # msg_pict = await FileManager.read(MessagePath.PICT, 'welcome_start')
    await bot.send_photo(
        chat_id=message.from_user.id,
        photo=msg_data.media_id,
        caption=msg_data.text,
        reply_markup=ikb_welcome('Кто такой Стоун?', 'first_step'),
    )
    await requests.new_user(
        user_tg_id=message.from_user.id,
        name=message.from_user.full_name,
        tg_username=message.from_user.username,
        register_date=date.today(),
        referral_id=referral_id,
    )


@welcome_router.callback_query(CallbackWelcome.filter(F.button == 'first_step'))
async def welcome_next(callback: CallbackQuery, bot: Bot):
    # media = await FileManager.media_kwargs(
    #     text='welcome_stone',
    # )
    msg_data = await requests.get_menu('welcome_stone')
    await bot.edit_message_media(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        media=InputMediaPhoto(**msg_data),
        reply_markup=ikb_welcome('Да, в чём твоя польза?', 'second_step'),
    )


@welcome_router.callback_query(CallbackWelcome.filter(F.button == 'second_step'))
async def welcome_last(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await state.set_state(NewUser.input_name)
    await state.update_data(
        {
            'message_id': callback.message.message_id,
        }
    )
    referral_name = await state.get_value('referral')
    referral = ''
    if referral_name:
        referral = f' (та самая, которая тебе досталась от {referral_name}'
    # media = await FileManager.media_kwargs(
    #     text='welcome_hub',
    #     referral_name=referral,
    #     name=callback.from_user.full_name,
    # )
    msg_data = await requests.get_menu(
        'welcome_hub',
        referral_name=referral,
        name=callback.from_user.full_name,
    )
    await bot.edit_message_media(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        media=InputMediaPhoto(**msg_data),
        reply_markup=ikb_welcome('Пропустить', 'skip'),
    )


@welcome_router.callback_query(CallbackWelcome.filter(F.button == 'skip'))
async def welcome_last(callback: CallbackQuery, user: User, state: FSMContext, bot: Bot):
    # media = await FileManager.media_kwargs(
    #     text='main_menu',
    #     name=user.name,
    # )
    msg_data = await requests.get_menu(
        'main_menu',
        name=user.name,
    )
    await bot.edit_message_media(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        media=InputMediaPhoto(**msg_data),
        reply_markup=ikb_main_menu(user),
    )
    await bot.send_message(
        chat_id=config.ADMIN_TG_ID,
        text=f'🥳 У нас новый пользователь:\n{user.name}\n@{user.tg_username}'
    )
    await state.clear()


@welcome_router.message(NewUser.input_name)
async def user_new_name(message: Message, user: User, state: FSMContext, bot: Bot):
    message_id = await state.get_value('message_id')
    await requests.update_name(
        user_tg_id=message.from_user.id,
        name=message.text,
    )
    await bot.delete_message(
        chat_id=message.from_user.id,
        message_id=message.message_id,
    )
    # media = await FileManager.media_kwargs(
    #     text='main_menu',
    #     name=message.text,
    # )
    msg_data = await requests.get_menu(
        'main_menu',
        name=message.text,
    )
    await bot.edit_message_media(
        chat_id=message.from_user.id,
        message_id=message_id,
        media=InputMediaPhoto(**msg_data),
        reply_markup=ikb_main_menu(user),
    )
    await bot.send_message(
        chat_id=config.ADMIN_TG_ID,
        text=f'🥳 У нас новый пользователь:\n{message.text}\n@{user.tg_username}'
    )
    await state.clear()
