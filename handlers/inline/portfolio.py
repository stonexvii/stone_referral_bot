import asyncio
from asyncio import sleep
from random import choice

from aiogram import Router, Bot, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InputMediaPhoto

from database import requests
from fsm import Portfolio
from keyboards import ikb_portfolio
from keyboards.callback_data import CallbackPortfolio
from middlewares import UserMiddleware
from .back_buttons import get_task

portfolio_router = Router()
portfolio_router.callback_query.middleware(UserMiddleware())


async def next_photo(photo_list, state: FSMContext):
    data = await state.get_data()
    if not data:
        await state.set_state(Portfolio.manual)
        used_idx = set()
        await state.update_data(
            {
                'used_idx': used_idx,
                'slideshow': False,
            }
        )
    else:
        used_idx = await state.get_value('used_idx')
    all_idx = set(range(len(photo_list.media) - 1))
    available_idx = all_idx.difference(used_idx)
    if not available_idx:
        available_idx = set(range(len(photo_list.media) - 1))
        last_idx = await state.get_value('last_idx')
        used_idx = {last_idx}
    idx = choice(list(available_idx))
    await state.update_data({'last_idx': idx})
    used_idx.add(idx)
    await state.update_data({'used_idx': used_idx})
    return photo_list.media[idx]


async def create_slideshow(callback: CallbackQuery, state: FSMContext, admin: bool, bot: Bot):
    portfolio = await requests.get_menu('portfolio', full=True)
    slideshow_status = await state.get_value('slideshow')
    while True:
        media = await next_photo(portfolio, state)
        msg_data = {
            'media': media.media_id,
            'caption': media.description,
        }
        await bot.edit_message_media(
            chat_id=callback.from_user.id,
            message_id=callback.message.message_id,
            media=InputMediaPhoto(**msg_data),
            reply_markup=ikb_portfolio(slideshow_status, media.id, admin),
        )
        await sleep(5)


@portfolio_router.callback_query(CallbackPortfolio.filter(F.button == 'portfolio'))
async def portfolio_menu(callback: CallbackQuery, callback_data: CallbackPortfolio, bot: Bot, admin: bool,
                         state: FSMContext):
    await state.set_state(Portfolio.manual)
    portfolio = await requests.get_menu('portfolio', full=True)
    media = await next_photo(portfolio, state)
    msg_data = {
        'media': media.media_id,
        'caption': media.description,
    }
    slideshow = await state.get_value('slideshow')
    await bot.edit_message_media(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        media=InputMediaPhoto(**msg_data),
        reply_markup=ikb_portfolio(slideshow, media.id, admin),
    )


@portfolio_router.callback_query(CallbackPortfolio.filter(F.button == 'start_slideshow'))
async def start_slideshow(callback: CallbackQuery, state: FSMContext, admin: bool, bot: Bot):
    task_name = f'task_{callback.from_user.id}'
    await state.update_data(
        {
            'slideshow': True,
            'task_name': task_name,
        }
    )
    loop = asyncio.get_event_loop()
    task = await loop.create_task(create_slideshow(callback, state, admin, bot), name=task_name)


@portfolio_router.callback_query(CallbackPortfolio.filter(F.button == 'stop_slideshow'))
async def stop_slideshow(callback: CallbackQuery, state: FSMContext, admin: bool, bot: Bot):
    await state.update_data(
        {
            'slideshow': False,
        }
    )
    task_name = await state.get_value('task_name')
    if task_name:
        task = await get_task(task_name)
        if not task.done():
            task.cancel()
    await portfolio_menu(callback, bot, admin, state)


@portfolio_router.callback_query(CallbackPortfolio.filter(F.button == 'delete_media'))
async def delete_media_handler(callback: CallbackQuery, callback_data: CallbackPortfolio):
    await requests.delete_media(callback_data.idx)
    await callback.answer(
        text='Фото удалено!',
        show_alert=True,
    )
