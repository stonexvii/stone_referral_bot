import os

import aiofiles


class FileManager:
    _DIR_MESSAGES = 'messages'

    @classmethod
    async def read(cls, path: str, **kwargs):
        if path := os.path.join(cls._DIR_MESSAGES, path + '.txt'):
            async with aiofiles.open(path, 'r', encoding='UTF-8') as file:
                response = await file.read()
            return response.format(**kwargs)
        return 'None'

    @classmethod
    async def write(cls, path: str, data: str):
        path = os.path.join(cls._DIR_MESSAGES, path + '.txt')
        async with aiofiles.open(path, 'w', encoding='UTF-8') as file:
            await file.write(data)
