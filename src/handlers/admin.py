from datetime import date

from aiogram import F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.enums import ParseMode

from .base import BaseHandler
from src.db.connector import DBConnector
from src.utils.keyboards import get_admin_keyboard, get_back_keyboard


class AdminHandler(BaseHandler):
    def register_handlers(self) -> None:
        self.router.message.register(self.handle, Command('admin'))
        self.router.callback_query.register(self.handle, F.data == 'admin')
        self.router.callback_query.register(self.report, F.data == 'admin_report')

    async def handle(self, event: Message | CallbackQuery, db: DBConnector) -> None:
        name = await db.admins.get_name(event.from_user.id)
        prompt = (
            f"<b>Привіт, {name}</b>\n\n"
            f"Оберіть, що вас цікавить"
        )
        kwargs = {
            "text": prompt,
            "reply_markup": get_admin_keyboard(),
            "parse_mode": ParseMode.HTML
        }
        if isinstance(event, Message):
            await event.answer(**kwargs)
        elif isinstance(event, CallbackQuery):
            await event.message.edit_text(**kwargs)

    async def report(self, callback: CallbackQuery, db: DBConnector) -> None:
        reports = await db.reports.get_reports_by_day(date.today())
        prompt = f"<b>Звіт на {date.today()}</b>\n\n"
        for report in reports:
            prompt += f"<b>{report.form}</b>: відсутніх: {report.absentees}, хворих: {report.patients}\n"
        await callback.message.edit_text(
            prompt,
            reply_markup=get_back_keyboard('admin'),
            parse_mode=ParseMode.HTML
        )
        