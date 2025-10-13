from aiogram import Router

from .admin import admin_router
from .command import command_router
from .inline import inline_router
from .fsm import fsm_router

main_router = Router()

main_router.include_routers(
    admin_router,
    fsm_router,
    command_router,
    inline_router,
)
