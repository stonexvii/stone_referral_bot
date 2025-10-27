import asyncio
from asyncio import sleep
from random import choice

from aiogram import Router, Bot, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InputMediaPhoto

from .about import about_handler
from database import requests
from database.tables import Menu
from fsm import Portfolio
from keyboards import ikb_back, ikb_portfolio
from keyboards.callback_data import CallbackMainMenu, CallbackPortfolio
from middlewares import UserMiddleware

portfolio_router = Router()
portfolio_router.callback_query.middleware(UserMiddleware())


async def start_slideshow(data: Menu, callback: CallbackQuery, state: FSMContext, bot: Bot):
    while data.media:
        # media = data.media.pop(randint(0, len(data.media) - 1))
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
    await state.clear()
    await about_handler(callback, bot)


@portfolio_router.callback_query(CallbackPortfolio.filter(F.button == 'portfolio'))
async def portfolio_menu(callback: CallbackQuery, bot: Bot, admin: bool, state: FSMContext):
    portfolio = await requests.get_menu('portfolio', full=True)
    data = await state.get_data()
    if not data:
        await state.set_state(Portfolio.manual)
        used_idx = set()
        slideshow = False
        await state.update_data(
            {
                'used_idx': used_idx,
                'slideshow': slideshow,
            }
        )
    else:
        used_idx = await state.get_value('used_idx')
        slideshow = await state.get_value('slideshow')
    all_idx = set(range(len(portfolio.media) - 1))
    available_idx = all_idx.difference(used_idx)
    if not available_idx:
        available_idx = set(range(len(portfolio.media) - 1))
        last_idx = await state.get_value('last_idx')
        used_idx = {last_idx}
    idx = choice(list(available_idx))
    await state.update_data({'last_idx': idx})
    used_idx.add(idx)
    await state.update_data({'used_idx': used_idx})
    portfolio = await requests.get_menu('portfolio', full=True)
    media = portfolio.media[idx]
    msg_data = {
        'media': media.media_id,
        'caption': media.description,
    }
    # task_name = f'task_{callback.from_user.id}'
    # task = asyncio.create_task(start_slideshow(portfolio, callback, state, bot), name=task_name)
    # await state.set_data(
    #     {
    #         'task_name': task_name,
    #     }
    # )
    await bot.edit_message_media(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        media=InputMediaPhoto(**msg_data),
        reply_markup=ikb_portfolio(slideshow, admin),
    )


@portfolio_router.callback_query(CallbackMainMenu.filter(F.button == 'portfolio'))
async def start_slideshow(callback: CallbackQuery, bot: Bot, state: FSMContext):
    # await callback.answer(
    #     text='Это слайд-шоу с паузой в 5 секунд\nДля остановки нажми "Назад"',
    #     show_alert=True,
    # )
    # await sleep(2)
    await state.set_state(Slideshow.running)
    portfolio = await requests.get_menu('portfolio', full=True)
    task_name = f'task_{callback.from_user.id}'
    task = asyncio.create_task(start_slideshow(portfolio, callback, state, bot), name=task_name)
    await state.set_data(
        {
            'task_name': task_name,
        }
    )
