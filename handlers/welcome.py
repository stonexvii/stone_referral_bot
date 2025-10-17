from aiogram import Router, Bot, F
from aiogram.filters import CommandObject
from aiogram.types import CallbackQuery, Message, InputMediaPhoto
from aiogram.fsm.context import FSMContext
import config
import messages
from database import requests
from database.tables import Users
from keyboards import ikb_welcome, ikb_back, ikb_main_menu, ikb_dispersal_menu, ikb_referrals_menu, ikb_about_menu
from keyboards.callback_data import CallbackMainMenu, CallbackReferral, CallbackBackButton, CallbackWelcome
from middlewares.middleware import UserMiddleware
from utils import FileManager
from fsm.states import NewUser
from datetime import date

welcome_router = Router()
welcome_router.message.middleware(UserMiddleware())
welcome_router.callback_query.middleware(UserMiddleware())


async def welcome_start(message: Message, command: CommandObject, state: FSMContext, bot: Bot):
    referral_id = None
    if command.args and command.args.isdigit():
        referral_id = int(command.args)
        referral = await requests.get_user(referral_id)
        referral_name = referral.name
        msg_text = await FileManager.read('welcome_first', referral_name=referral_name)
    else:
        msg_text = await FileManager.read('welcome_first_wor')
        referral_name = None
    await state.update_data(
        {
            'referral': referral_name,
        }
    )
    await bot.send_photo(
        chat_id=message.from_user.id,
        photo=messages.WELCOME_START,
        caption=msg_text,
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
    msg_text = await FileManager.read('welcome_second')
    await bot.edit_message_media(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        media=InputMediaPhoto(
            media=messages.WELCOME_STONE,
            caption=msg_text,
        ),
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
    msg_text = await FileManager.read('welcome_name', referral_name=referral, name=callback.from_user.full_name)
    await bot.edit_message_media(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        media=InputMediaPhoto(
            media=messages.WELCOME_HUB,
            caption=msg_text,
        ),
        reply_markup=ikb_welcome('Пропустить', 'skip'),
    )


@welcome_router.callback_query(CallbackWelcome.filter(F.button == 'skip'))
async def welcome_last(callback: CallbackQuery, user: Users, state: FSMContext, bot: Bot):
    msg_text = await FileManager.read('main_menu', name=user.name)
    await bot.edit_message_media(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        media=InputMediaPhoto(
            media=messages.MAIN_PICT,
            caption=msg_text,
        ),
        reply_markup=ikb_main_menu(),
    )
    await state.clear()


@welcome_router.message(NewUser.input_name)
async def user_new_name(message: Message, user: Users, state: FSMContext, bot: Bot):
    message_id = await state.get_value('message_id')
    await requests.update_name(
        user_tg_id=message.from_user.id,
        name=message.text,
    )
    await bot.delete_message(
        chat_id=message.from_user.id,
        message_id=message.message_id,
    )
    msg_text = await FileManager.read('main_menu', name=message.text)
    await bot.edit_message_media(
        chat_id=message.from_user.id,
        message_id=message_id,
        media=InputMediaPhoto(
            media=messages.MAIN_PICT,
            caption=msg_text,
        ),
        reply_markup=ikb_main_menu(),
    )
    await state.clear()
