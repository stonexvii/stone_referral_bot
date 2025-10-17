import os

from aiogram import Router, F
from aiogram.filters import Command, CommandObject
from aiogram.types import Message

from middlewares import AdminMiddleware
from utils import FileManager, MessagePath

admin_router = Router()
admin_router.message.middleware(AdminMiddleware())


@admin_router.message(Command('set'))
async def set_text(message: Message, command: CommandObject):
    file_list = [file.rsplit('.', 1)[0] for file in os.listdir(MessagePath.TEXT.value) if file.endswith('.txt')]
    if command.args:
        file_name, data = command.args.split('\n', 1)
        if file_name in file_list:
            await FileManager.write(MessagePath.TEXT, file_name, data)
            msg_text = f'{file_name} перезаписан!'
        else:
            msg_text = 'Такого файла не существует'
    else:

        msg_text = 'Список файлов для установки:\n' + '\n'.join(file_list)
    await message.answer(
        text=msg_text
    )


@admin_router.message(F.photo)
async def update_pict(message: Message):
    pict_names = [file.rsplit('.', 1)[0] for file in os.listdir(MessagePath.PICT.value) if file.endswith('.txt')]
    file_name = message.caption
    if file_name in pict_names:
        msg_text = f'{file_name} обновлен!'
        await FileManager.write(MessagePath.PICT, file_name, message.photo[0].file_id)
    else:
        msg_text = 'Такого файла нет, выбери из списка:\n' + '\n'.join(pict_names)
    await message.answer(
        text=msg_text,
    )
