import os

import aiofiles

from .enum import MessagePath


class FileManager:

    @staticmethod
    async def read(directory: MessagePath, path: str, **kwargs):
        path = os.path.join(directory.value, path + '.txt')
        async with aiofiles.open(path, 'r', encoding='UTF-8') as file:
            response = await file.read()
        return response.strip().format(**kwargs)

    @staticmethod
    async def write(directory: MessagePath, path: str, data: str):
        path = os.path.join(directory.value, path + '.txt')
        async with aiofiles.open(path, 'w', encoding='UTF-8') as file:
            await file.write(data)

    @classmethod
    async def media_kwargs(cls, text: str, pict: str | None = None, **kwargs):
        pict = pict if pict else text
        txt = await cls.read(MessagePath.TEXT, text, **kwargs)
        pct = await cls.read(MessagePath.PICT, pict)
        return {
            'media': pct,
            'caption': txt,
        }
