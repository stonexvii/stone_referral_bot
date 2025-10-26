import os.path

from aiogram import Router, Bot, F
from aiogram.types import CallbackQuery, InputMediaPhoto, FSInputFile

import config
from database import requests
from database.tables import User
from keyboards import ikb_about_menu
from keyboards.callback_data import CallbackMainMenu
from middlewares.middleware import UserMiddleware
from utils import FileManager

about_router = Router()
about_router.callback_query.middleware(UserMiddleware())


@about_router.callback_query(CallbackMainMenu.filter(F.button == 'about_stone'))
async def about_handler(callback: CallbackQuery, bot: Bot):
    media = await FileManager.media_kwargs(
        text='about',
    )
    msg_data = await requests.get_menu(
        'about',
    )
    await bot.edit_message_media(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        media=InputMediaPhoto(**msg_data),
        reply_markup=ikb_about_menu(),
    )


@about_router.callback_query(CallbackMainMenu.filter(F.button == 'download_pdf'))
async def download_handler(callback: CallbackQuery, bot: Bot):
    if os.path.exists(r'messages/promo.pdf'):
        await bot.send_document(
            chat_id=callback.from_user.id,
            document=FSInputFile(r'messages/promo.pdf')
        )
    else:
        await callback.answer(
            text='PDF в разработке!\nБудет доступно позже',
            show_alert=True,
        )


@about_router.callback_query(CallbackMainMenu.filter(F.button == 'contact_stone'))
async def contact_stone(callback: CallbackQuery, user: User, bot: Bot):
    referral_user = await requests.get_user(user.referral_id)
    await bot.send_message(
        chat_id=config.ADMIN_TG_ID,
        text=f'{user.name} кинул заявку\n' + (
            f'Его привел: {referral_user.tg_username}\n' if referral_user else '') + f'@{user.tg_username}'
    )
    await callback.answer(
        text='Спасибо!\nМы передали Стоуну твою заявку, скоро он с тобой свяжется',
        show_alert=True,
    )
