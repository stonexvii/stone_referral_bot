import os

from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message

from middlewares import AdminMiddleware
from utils import FileManager

admin_router = Router()
admin_router.message.middleware(AdminMiddleware())


@admin_router.message(Command('set'))
async def command_set(message: Message, command: CommandObject):
    file_list = [file.rsplit('.', 1)[0] for file in os.listdir('messages') if not file.startswith('__')]
    if command.args:
        file_name, data = command.args.split('\n', 1)
        if file_name in file_list:
            await FileManager.write(file_name, data)
            msg_text = f'{file_name} перезаписан!'
        else:
            msg_text = 'Такого файла не существует'
    else:

        msg_text = 'Список файлов для установки:\n' + '\n'.join(file_list)
    await message.answer(
        text=msg_text
    )
