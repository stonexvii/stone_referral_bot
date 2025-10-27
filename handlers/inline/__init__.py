from aiogram import Router

from middlewares.middleware import UserMiddleware
from .about import about_router
from .back_buttons import back_button_router
from .projects import projects_router
from .referrals import referrals_router
from .portfolio import portfolio_router

inline_router = Router()
inline_router.callback_query.middleware(UserMiddleware())

inline_router.include_routers(
    portfolio_router,
    about_router,
    back_button_router,
    projects_router,
    referrals_router,
)
