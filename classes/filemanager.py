import aiofiles
import os


class FileManager:
    _DIR_MESSAGES = 'text'

    @classmethod
    async def read(cls, path: str):
        if path := os.path.join(cls._DIR_MESSAGES, path + '.txt'):
            async with aiofiles.open(path, 'r', encoding='UTF-8') as file:
                response = await file.read()
            return response
        return 'None'

    @classmethod
    async def write(cls, path: str, data: str):
        path = os.path.join(cls._DIR_MESSAGES, path + '.txt')
        async with aiofiles.open(path, 'w', encoding='UTF-8') as file:
            await file.write(data)
