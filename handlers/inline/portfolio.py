import asyncio
from asyncio import sleep
from random import randint

from aiogram import Router, Bot, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InputMediaPhoto

from database import requests
from database.tables import Menu
from fsm import Slideshow
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
async def projects_menu(callback: CallbackQuery, bot: Bot, state: FSMContext):
    await callback.answer(
        text='Это слайд-шоу с паузой в 5 секунд\nДля остановки нажми "Назад"',
        show_alert=True,
    )
    await sleep(2)
    portfolio = await requests.get_menu('portfolio', full=True)
    task_name = f'task_{callback.from_user.id}'
    task = asyncio.create_task(start_slideshow(portfolio, callback, bot), name=task_name)
    await state.set_state(Slideshow.running)
    await state.set_data(
        {
            'task_name': task_name,
        }
    )
