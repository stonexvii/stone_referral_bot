from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

import config
from database import requests


class AdminMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        if event.from_user.id == config.ADMIN_TG_ID:
            result = await handler(event, data)
            return result


class UserMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        user = await requests.get_user(event.from_user.id)
        data['user'] = user
        data['admin'] = False
        if event.from_user.id == config.ADMIN_TG_ID:
            data['admin'] = True
        return await handler(event, data)
