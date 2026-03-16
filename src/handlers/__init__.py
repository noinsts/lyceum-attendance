from aiogram import Router

from .auth import AuthHandler
from .start import StartHandler
from .profile import ProfileHandler
from .report import ReportHandler
from .admin import AdminHandler
from .test import TestHandler

from src.middlewares.admin import AdminMiddleware

def get_admin_router() -> Router:
    router = Router(name="admin")

    router.include_router(AdminHandler().get_router())

    admin_middleware = AdminMiddleware()
    router.message.middleware(admin_middleware)
    router.callback_query.middleware(admin_middleware)

    return router



def get_router() -> Router:
    router = Router()

    routers = [
        StartHandler().get_router(),
        AuthHandler().get_router(),
        ProfileHandler().get_router(),
        ReportHandler().get_router(),
        TestHandler().get_router(),
        get_admin_router()
    ]

    for r in routers:
        router.include_router(r)

    return router
