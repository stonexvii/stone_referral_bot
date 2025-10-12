from aiogram import Router, Bot, F
from aiogram.types import CallbackQuery, Message

import config
from database import requests
from database.tables import Users
from keyboards import ikb_back, ikb_user_main_menu, ikb_dispersal_menu, ikb_referrals_menu
from keyboards.callback_data import UserMainMenu, BackButton, ReferralMenu
from middlewares.middleware import UserMiddleware
from utils import FileManager

inline_router = Router()
inline_router.callback_query.middleware(UserMiddleware())


async def main_menu(callback: CallbackQuery | Message, user: Users, bot: Bot):
    referral_block = ''
    if user.referral_id:
        referral = await requests.get_user(user.referral_id)
        referral_block = await FileManager.read('referral_block', referral_name=referral.user_name)
    msg_text = await FileManager.read('main_menu', username=user.user_name, referral_block=referral_block)
    await bot.edit_message_text(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        text=msg_text,
        reply_markup=ikb_user_main_menu(),
    )


@inline_router.callback_query(ReferralMenu.filter(F.button == 'my_referrals'))
async def my_referrals(callback: CallbackQuery, user: Users, bot: Bot):
    response = await requests.get_referrals(callback.from_user.id)
    if response:
        message_text = f'{user.user_name}, список твоих рефералов:\n' + '\n'.join(
            [f'\t- {referral_name}' for referral_name in response])
    else:
        message_text = 'У тебя пока нет рефералов'
    await bot.edit_message_text(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        text=message_text,
        reply_markup=ikb_back('to_referral'),
    )


@inline_router.callback_query(UserMainMenu.filter(F.button == 'contact_stone'))
async def contact_stone(callback: CallbackQuery, user: Users, bot: Bot):
    referral_user = await requests.get_user(user.referral_id)
    await bot.send_message(
        chat_id=config.ADMIN_TG_ID,
        text=f'{user.user_name} кинул заявку\n' + (
            f'Его привел: {referral_user.user_name}\n' if referral_user else '') + f'{user.tg_user_name}'
    )
    await callback.answer(
        text='Спасибо!\nМы передали Стоуну твою заявку, скоро он с тобой свяжется',
        show_alert=True,
    )


@inline_router.callback_query(UserMainMenu.filter(F.button == 'referrals'))
async def referral_menu(callback: CallbackQuery, user: Users, bot: Bot):
    msg_text = await FileManager.read('referral_menu', name=user.user_name)
    await bot.edit_message_text(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        text=msg_text.format(name=user.user_name),
        reply_markup=ikb_referrals_menu(),
    )


@inline_router.callback_query(UserMainMenu.filter(F.button == 'dispersal_of_events'))
async def dispersal_link(callback: CallbackQuery, user: Users, bot: Bot):
    msg_text = await FileManager.read('dispersal')
    await bot.edit_message_text(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        text=msg_text.format(name=user.user_name),
        reply_markup=ikb_dispersal_menu(),
    )


@inline_router.callback_query(BackButton.filter())
async def back_button(callback: CallbackQuery, callback_data: BackButton, user: Users, bot: Bot):
    if callback_data.button == 'to_main':
        await main_menu(callback, user, bot)
    elif callback_data.button == 'to_referral':
        await referral_menu(callback, bot)
