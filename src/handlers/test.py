from datetime import date

from aiogram.types import Message
from aiogram.filters import Command
from aiogram.enums import ParseMode

from .base import BaseHandler
from src.db.connector import DBConnector


class TestHandler(BaseHandler):
    def register_handlers(self):
        self.router.message.register(self.handle, Command('help'))

    async def handle(self, message: Message, db: DBConnector) -> None:
        reports = await db.reports.get_reports_by_day(date.today())
        users = await db.users.get_users_without_reports(reports);

        response = "<b>Список вчителів, які не відправили запит</b>\n\n"
        if users:
            for user in users:
                response += f"{user.name}, {user.form}\n"
        await message.answer(
            response,
            parse_mode=ParseMode.HTML
        )
