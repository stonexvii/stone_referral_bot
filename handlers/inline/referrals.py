from aiogram import Router, Bot, F
from aiogram.types import CallbackQuery, InputMediaPhoto

import config
from database import requests
from database.tables import User
from handlers.main_menu import callback_main_menu
from keyboards import ikb_back, ikb_referrals_menu
from keyboards.callback_data import CallbackMainMenu, CallbackReferral
from middlewares.middleware import UserMiddleware

referrals_router = Router()
referrals_router.callback_query.middleware(UserMiddleware())


@referrals_router.callback_query(CallbackMainMenu.filter(F.button == 'referrals_menu'))
async def referrals_menu_handler(callback: CallbackQuery, user: User, bot: Bot):
    if user.is_referral:
        msg_data = await requests.get_menu(
            'referral_menu',
            name=user.name,
            user_id=user.id,
        )
    else:
        msg_data = await requests.get_menu(
            'referral_menu_new',
        )
    await bot.edit_message_media(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        media=InputMediaPhoto(**msg_data),
        reply_markup=ikb_referrals_menu(user),
    )


@referrals_router.callback_query(CallbackReferral.filter(F.button == 'new_referral'))
async def new_referral_handler(callback: CallbackQuery, user: User, bot: Bot):
    if user.tg_username:
        msg_text = 'Спасибо!\nТеперь ты реферал\nТвоя персональная ссылка ждет тебя в твоем лично кабинете'
        await bot.send_message(
            chat_id=config.ADMIN_TG_ID,
            text=f'⭐️ У нас новый реферал:\n{user.name}\n@{user.tg_username}'
        )
        await requests.new_referral(
            user_tg_id=user.id,
        )
    else:
        msg_text = 'Телеграм не дает доступа к твоему username :(\nБез него я не смогу сделать тебя рефералом\nПредоставь доступ и попробуй еще раз, пожалуйста'
    await callback.answer(
        text=msg_text,
        show_alert=True,
    )
    await callback_main_menu(callback, user, bot)


@referrals_router.callback_query(CallbackReferral.filter(F.button == 'my_referrals'))
async def my_referrals(callback: CallbackQuery, user: User, bot: Bot):
    referrals_list = await requests.get_referrals(user.id)
    if referrals_list:
        msg_data = await requests.get_menu(
            'my_referrals',
            name=user.name,
        )
        msg_data['caption'] += '\n' + '\n'.join([referral.name for referral in referrals_list])
    else:
        msg_data = await requests.get_menu(
            'no_referrals',
        )
    await bot.edit_message_media(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        media=InputMediaPhoto(**msg_data),
        reply_markup=ikb_back('to_referrals'),
    )
