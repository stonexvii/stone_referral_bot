import asyncio
from asyncio import sleep
from random import randint

from aiogram import Router, Bot, F
from aiogram.types import CallbackQuery, InputMediaPhoto

import config
from database import requests
from database.tables import Menu
from keyboards import ikb_back
from keyboards.callback_data import CallbackMainMenu

portfolio_router = Router()


async def start_slideshow(data: Menu, callback: CallbackQuery, bot: Bot):
    while data.media:
        media = data.media.pop(randint(0, len(data.media) - 1))
        await bot.edit_message_media(
            chat_id=callback.from_user.id,
            message_id=callback.message.message_id,
            media=InputMediaPhoto(
                media=media.media_id,
                caption=media.description,
            ),
            reply_markup=ikb_back('to_about'),
        )
        await sleep(5)


@portfolio_router.callback_query(CallbackMainMenu.filter(F.button == 'portfolio'))
async def projects_menu(callback: CallbackQuery, bot: Bot):
    await callback.answer(
        text='Это слайд-шоу с паузой в 5 секунд\nДля остановки нажми "Назад"',
        show_alert=True,
    )
    await sleep(5)
    portfolio = await requests.get_menu('portfolio', full=True)
    config.SLIDESHOW_TASK = asyncio.create_task(start_slideshow(portfolio, callback, bot))
