from aiogram import F
from aiogram.types import CallbackQuery
from aiogram.enums import ParseMode

from .base import BaseHandler
from src.db.connector import DBConnector
from src.utils.keyboards import get_profile_keyboard


class ProfileHandler(BaseHandler):
    def register_handlers(self) -> None:
        self.router.callback_query.register(self.handle, F.data == 'profile')

    async def handle(self, callback: CallbackQuery, db: DBConnector) -> None:
        user = await db.users.get_user(callback.from_user.id)
        if user:
            text = (
                f"<b>Ваші дані</b>:\n\n"
                f"Ім'я: {user.name}\n"
                f"Клас: {user.form}\n\n"
                f"<i>Щоб змінити дані, натисніть нижче.</i>"
            )
        else:
            text = "Помилка.."
        await callback.message.edit_text(
            text, 
            parse_mode=ParseMode.HTML, 
            reply_markup=get_profile_keyboard()
        )
