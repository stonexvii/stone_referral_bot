import os
import json
import aiofiles


class FileManager:
    _DIR_MESSAGES = 'messages'
    _DIR_PICTURES = os.path.join('messages', 'pictures')

    @classmethod
    async def read(cls, path: str, **kwargs):
        if path := os.path.join(cls._DIR_MESSAGES, path + '.txt'):
            async with aiofiles.open(path, 'r', encoding='UTF-8') as file:
                response = await file.read()
            return response.format(**kwargs)
        return 'None'

    @classmethod
    async def read_file(cls, path: str):
        if path := os.path.join(cls._DIR_MESSAGES, path):
            async with aiofiles.open(path, 'rb') as file:
                response = await file.read()
            return response

    @classmethod
    async def write(cls, path: str, data: str):
        path = os.path.join(cls._DIR_MESSAGES, path + '.txt')
        async with aiofiles.open(path, 'w', encoding='UTF-8') as file:
            await file.write(data)

    @classmethod
    def write_json(cls, path: str, data: dict[str, str]):
        path = os.path.join(cls._DIR_PICTURES, path + '.json')
        with open(path, 'w', encoding='UTF-8') as file:
            json.dump(data, file, indent=4, sort_keys=True)

    @classmethod
    def load_json(cls, path: str):
        path = os.path.join(cls._DIR_PICTURES, path + '.json')
        with open(path, 'r', encoding='UTF-8') as file:
            return json.load(file)
