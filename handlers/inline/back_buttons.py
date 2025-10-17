from aiogram import Router, Bot, F
from aiogram.types import CallbackQuery, Message, InputMediaPhoto
from aiogram.fsm.context import FSMContext
import config
import messages
from database import requests
from database.tables import Users
from keyboards import ikb_back, ikb_main_menu, ikb_dispersal_menu, ikb_referrals_menu, ikb_about_menu
from keyboards.callback_data import CallbackMainMenu, CallbackReferral, CallbackBackButton
from middlewares.middleware import UserMiddleware
from utils import FileManager
from fsm.states import NewReferral
from handlers.main_menu import callback_main_menu
from .referrals import referrals_menu_handler
from .projects import projects_menu

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
        await projects_menu(callback, user, bot)
