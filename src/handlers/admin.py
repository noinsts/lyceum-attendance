from datetime import date
from operator import attrgetter

from aiogram import F
from aiogram.types import Message, CallbackQuery, BufferedInputFile
from aiogram.filters import Command
from aiogram.enums import ParseMode

from .base import BaseHandler
from src.db.connector import DBConnector
from src.utils.keyboards import get_admin_keyboard, get_back_keyboard
from src.utils.spreedsheet import build_report_excel


class AdminHandler(BaseHandler):
    def register_handlers(self) -> None:
        self.router.message.register(self.handle, Command('admin'))
        self.router.callback_query.register(self.handle, F.data == 'admin')
        self.router.callback_query.register(self.send_report, F.data == 'admin_report')
        self.router.callback_query.register(self.download_report, F.data == 'admin_download_report')
        self.router.callback_query.register(self.did_not_send_report, F.data == 'admin_did_not_send_report')

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

    async def send_report(self, callback: CallbackQuery, db: DBConnector) -> None:
        reports = await db.reports.get_reports_by_day(date.today())
        reports.sort(key=attrgetter('form'))
        prompt = f"<b>Звіт на {date.today()}</b>\n\n"
        for report in reports:
            prompt += f"<b>{report.form}</b>: відсутніх: {report.absentees}, хворих: {report.patients}\n"

        total_absentees = sum(report.absentees for report in reports)
        total_patients = sum(report.patients for report in reports)
        prompt += f"\n<b>Всього відсутніх:</b> {total_absentees}\n<b>Всього хворих:</b> {total_patients}"
        
        await callback.message.edit_text(
            prompt,
            reply_markup=get_back_keyboard('admin'),
            parse_mode=ParseMode.HTML
        )

    async def download_report(self, callback: CallbackQuery, db: DBConnector) -> None:
        reports = await db.reports.get_reports_by_day(date.today())
        data = [
            {
                "class": report.form,
                "absent": report.absentees,
                "sick": report.patients,
                "total": report.total
            }
            for report in reports
        ]
        data.sort(key=lambda x: x['class'])
        bytes = build_report_excel(data)
        file = BufferedInputFile(bytes, filename=f"report_{date.today()}.xlsx")
        await callback.message.delete()
        await callback.message.answer_document(
            document=file,
            caption=f"📊 Звіт на {date.today()}",
        )

    async def did_not_send_report(self, callback: CallbackQuery, db: DBConnector) -> None:
        all_forms = await db.forms.get_all_form_names()
        sent_reports = await db.reports.get_reports_by_day(date.today())
        did_not_send = [form for form in all_forms if form not in [report.form for report in sent_reports]]
        did_not_send.sort()
        prompt = "<b>Список класів, які не надіслали звіт сьогодні:</b>\n\n"
        for form in did_not_send:
            prompt += f"<b>{form}</b>\n"
        await callback.message.edit_text(
            prompt,
            reply_markup=get_back_keyboard('admin'),
            parse_mode=ParseMode.HTML
        )
