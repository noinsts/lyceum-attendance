from aiogram import F
from aiogram.types import Message, CallbackQuery, InputRichMessage
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from src.db.connector import DBConnector
from src.utils.keyboards import get_hub_keyboard

from .base import BaseHandler
from .auth import AuthHandler


class StartHandler(BaseHandler):
    def register_handlers(self) -> None:
        self.router.message.register(self.handle, CommandStart())
        self.router.callback_query.register(self.handle, F.data == 'hub')

    async def handle(self, event: Message | CallbackQuery, state: FSMContext, db: DBConnector) -> None:
        exists = await db.users.get_user(event.from_user.id)
        if exists:
            await self.hub(event, state, db)
        else:
            await AuthHandler().handle(event, state)

    async def hub(self, event: Message | CallbackQuery, state: FSMContext, db: DBConnector) -> None:
        await state.clear()
        is_admin = await db.admins.is_admin(event.from_user.id)

        text = (
            "# 👋🏻 Вітаємо!\n"
            "Ви знаходитесь в головному меню. Оберіть, що вас цікавить 👇🏻"
        )

        kwargs = {
            "text": text,
            "rich_message": InputRichMessage(markdown=text),
            "reply_markup": get_hub_keyboard(is_admin),
        }
        if isinstance(event, Message):
            await event.answer_rich(**kwargs)
        elif isinstance(event, CallbackQuery):
            await event.message.edit_text(**kwargs)
