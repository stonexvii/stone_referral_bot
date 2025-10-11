from aiogram import Router, Bot, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

import config
from classes import FileManager
from database import requests
from keyboards.callback_data import UserMainMenu, BackButton
from keyboards import ikb_back, ikb_user_main_menu

inline_router = Router()


@inline_router.callback_query(UserMainMenu.filter(F.button == 'my_referrals'))
async def questions_results(callback: CallbackQuery, bot: Bot):
    user = await requests.get_user(callback.from_user.id)
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
        reply_markup=ikb_back(user.user_name),
    )


@inline_router.callback_query(UserMainMenu.filter(F.button == 'contact_stone'))
async def contact_stone(callback: CallbackQuery, bot: Bot):
    user = await requests.get_user(callback.from_user.id)
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


@inline_router.callback_query(UserMainMenu.filter(F.button == 'about_referral'))
async def about_referral(callback: CallbackQuery, bot: Bot):
    user = await requests.get_user(callback.from_user.id)
    msg_text = await FileManager.read('about_referral')
    await bot.edit_message_text(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        text=msg_text.format(name=user.user_name),
        reply_markup=ikb_back(user.user_name),
    )


@inline_router.callback_query(BackButton.filter())
async def back_button(callback: CallbackQuery, callback_data: BackButton, state: FSMContext, bot: Bot):
    message_text = f'Привет, {callback_data.user_name}!\nВот твоя реферальная ссылка:\n{config.REFERRAL_LINK_BASE}{callback.from_user.id}\n\nДелись ей со своими друзьями! Они получат скидку от меня, а ты получишь кэшбек от сделки'
    await bot.edit_message_text(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        text=message_text,
        reply_markup=ikb_user_main_menu(),
    )
