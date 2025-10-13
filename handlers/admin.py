import os

from aiogram import Router, Bot, F
from aiogram.filters import Command, CommandObject
from aiogram.types import Message, FSInputFile

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


@admin_router.message(Command('load'))
async def command_set(message: Message, bot: Bot):
    await bot.send_document(
        chat_id=message.from_user.id,
        document=FSInputFile('messages/promo.pdf'),
    )


@admin_router.message(F.document)
async def all_messages(message: Message, bot: Bot):
    for key, value in dict(message).items():
        if value:
            print(key, value)
    file = await bot.get_file(message.document.file_id)
    await bot.download_file(file.file_path, 'messages/promo.pdf')
