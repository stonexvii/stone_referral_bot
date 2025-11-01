from aiogram import Router, Bot, F
from aiogram.types import CallbackQuery, InputMediaPhoto

from database import requests
from keyboards import ikb_projects_menu, ikb_project_menu
from keyboards.callback_data import CallbackMainMenu, CallbackProject

projects_router = Router()


@projects_router.callback_query(CallbackMainMenu.filter(F.button == 'projects'))
async def projects_menu(callback: CallbackQuery, bot: Bot):
    projects = await requests.get_all_projects()
    projects_list = '\n'.join(item.mini_desc for item in projects)
    msg_data = await requests.get_menu(
        'projects_menu',
        projects=projects_list,
    )
    await bot.edit_message_media(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        media=InputMediaPhoto(**msg_data),
        reply_markup=ikb_projects_menu(projects),
    )


@projects_router.callback_query(CallbackProject.filter())
async def project_handler(callback: CallbackQuery, callback_data: CallbackProject, bot: Bot):
    project = await requests.get_project(
        callback_data.callback,
        as_kwargs=False,
    )
    if project.is_active:
        await bot.edit_message_media(
            chat_id=callback.from_user.id,
            message_id=callback.message.message_id,
            media=InputMediaPhoto(
                media=project.media[0].media_id,
                caption=project.description,
            ),
            reply_markup=ikb_project_menu(project),
        )
    else:
        await callback.answer(
            text='Проект в разработке\nСкоро релиз!\nСледите за новостями в канале',
            show_alert=True,
        )
