from datetime import date

from aiogram import Bot
from aiogram.enums import ParseMode

from src.db.connector import DBConnector
from src.db.db import session_maker

async def send_reminder(bot: Bot) -> None:
    async with session_maker() as session:
        db = DBConnector(session)
        text = (
            "⏰ <b>Нагадування</b>!\n\n" \
            "Не забудьте надіслати сьогоднішній звіт."
        )
        reports = await db.reports.get_reports_by_day(date.today())
        users = await db.users.get_users_without_reports(reports)
        for user in users:
            try:
                await bot.send_message(user.user_id, text, parse_mode=ParseMode.HTML)
            except Exception:
                pass
