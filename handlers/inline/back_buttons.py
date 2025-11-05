import asyncio

from aiogram import Router, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from database.tables import User
from handlers.main_menu import callback_main_menu
from keyboards.callback_data import CallbackBackButton
from .about import about_handler
from .projects import projects_menu
from .referrals import referrals_menu_handler

back_button_router = Router()


async def get_task(task_name: str):
    loop = asyncio.get_running_loop()
    for task in asyncio.all_tasks(loop):
        if task.get_name() == task_name:
            return task


@back_button_router.callback_query(CallbackBackButton.filter())
async def back_button(callback: CallbackQuery, callback_data: CallbackBackButton, user: User, state: FSMContext,
                      bot: Bot):
    if callback_data.button != 'to_about':
        await state.clear()
    if callback_data.button == 'to_main':
        await callback_main_menu(callback, user, bot)
    elif callback_data.button == 'to_referrals':
        await referrals_menu_handler(callback, user, bot)
    elif callback_data.button == 'to_projects':
        await projects_menu(callback, bot)
    elif callback_data.button == 'to_about':
        task_name = await state.get_value('task_name')
        if task_name:
            task = await get_task(task_name)
            if task and not task.done():
                task.cancel()
        await state.clear()
        await about_handler(callback, bot)
