from aiogram import Router

from .admin import admin_router
from .command import command_router
from .fsm import fsm_router
from .inline import inline_router
from .welcome import welcome_router

main_router = Router()

main_router.include_routers(
    welcome_router,
    admin_router,
    fsm_router,
    command_router,
    inline_router,
)
