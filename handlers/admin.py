from aiogram import Router, F
from aiogram.types import Message

from database import requests
from middlewares import AdminMiddleware

admin_router = Router()
admin_router.message.middleware(AdminMiddleware())


@admin_router.message(F.photo)
async def update_pict(message: Message):
    msg_text = message.photo[0].file_id
    if message.caption:
        await requests.add_portfolio(
            file_id=message.photo[0].file_id,
            desc=message.caption,
        )
        msg_text = 'Фото в портфолио добавлено'
    await message.answer(
        text=msg_text,
    )
