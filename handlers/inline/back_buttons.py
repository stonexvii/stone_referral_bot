from aiogram import Router, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from database.tables import Users
from handlers.main_menu import callback_main_menu
from keyboards.callback_data import CallbackBackButton
from .projects import projects_menu
from .referrals import referrals_menu_handler

back_button_router = Router()


@back_button_router.callback_query(CallbackBackButton.filter())
async def back_button(callback: CallbackQuery, callback_data: CallbackBackButton, user: Users, state: FSMContext,
                      bot: Bot):
    await state.clear()
    if callback_data.button == 'to_main':
        await callback_main_menu(callback, user, bot)
    elif callback_data.button == 'to_referrals':
        await referrals_menu_handler(callback, user, bot)
    elif callback_data.button == 'to_projects':
        await projects_menu(callback, bot)
