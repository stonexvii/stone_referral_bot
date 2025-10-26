from aiogram import Router, F
from aiogram.types import Message

from middlewares import AdminMiddleware

admin_router = Router()
admin_router.message.middleware(AdminMiddleware())


@admin_router.message(F.photo)
async def update_pict(message: Message):
    await message.answer(
        text=message.photo[0].file_id,
    )
