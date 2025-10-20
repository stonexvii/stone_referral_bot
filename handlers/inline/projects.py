from aiogram import Router, Bot, F
from aiogram.types import CallbackQuery, InputMediaPhoto

from keyboards import ikb_dispersal_menu, ikb_projects_menu, ikb_event_fix, ikb_thx_for_event
from keyboards.callback_data import CallbackMainMenu, CallbackProject
from utils import FileManager

projects_router = Router()

projects = {
    'dispersal': ikb_dispersal_menu(),
    'event_fix': ikb_event_fix(),
    'thx_for_event': ikb_thx_for_event(),
}


@projects_router.callback_query(CallbackMainMenu.filter(F.button == 'projects'))
async def projects_menu(callback: CallbackQuery, bot: Bot):
    media = await FileManager.media_kwargs(
        text='projects_menu',
    )
    await bot.edit_message_media(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        media=InputMediaPhoto(**media),
        reply_markup=ikb_projects_menu(),
    )


@projects_router.callback_query(CallbackProject.filter())
async def dispersal_handler(callback: CallbackQuery, callback_data: CallbackProject, bot: Bot):
    if callback_data.button in projects:
        media = await FileManager.media_kwargs(
            text=callback_data.button,
        )
        await bot.edit_message_media(
            chat_id=callback.from_user.id,
            message_id=callback.message.message_id,
            media=InputMediaPhoto(**media),
            reply_markup=projects[callback_data.button],
        )
    else:
        await callback.answer(
            text='Проект в разработке\nСкоро релиз!\nСледите за новостями в канале',
            show_alert=True,
        )
