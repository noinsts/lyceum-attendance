import re
from datetime import date

from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery, BufferedInputFile
from aiogram.filters import Command
from aiogram.enums import ParseMode

from .base import BaseHandler
from src.utils.keyboards import get_confirmation_keyboard
from src.db.connector import DBConnector
from src.utils.keyboards import get_admin_keyboard, get_back_keyboard
from src.utils.spreedsheet import build_report_excel


class BroadcastStates(StatesGroup):
    waiting_for_message = State()
    waiting_for_confirmation = State()


class AdminHandler(BaseHandler):
    def register_handlers(self) -> None:
        self.router.message.register(self.handle, Command('admin'))
        self.router.callback_query.register(self.handle, F.data == 'admin')
        self.router.callback_query.register(self.send_report, F.data == 'admin_report')
        self.router.callback_query.register(self.download_report, F.data == 'admin_download_report')
        self.router.callback_query.register(self.did_not_send_report, F.data == 'admin_did_not_send_report')
        self.router.callback_query.register(self.broadcast_handler, F.data == 'admin_broadcast')
        self.router.message.register(self.broadcast_recv_message_handler, F.text, BroadcastStates.waiting_for_message)
        self.router.callback_query.register(self.broadcast_submit_handler, F.data == 'submit', BroadcastStates.waiting_for_confirmation)
        self.router.callback_query.register(self.handle, F.data == 'cancel', BroadcastStates.waiting_for_confirmation)

    async def handle(self, event: Message | CallbackQuery, db: DBConnector, state: FSMContext) -> None:
        await state.clear()
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
        reports.sort(key=lambda r: self._form_sort(r.form))
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
        data.sort(key=lambda x: self._form_sort(x['class']))
        bytes = build_report_excel(data)
        file = BufferedInputFile(bytes, filename=f"report_{date.today()}.xlsx")
        await callback.message.delete()
        await callback.message.answer_document(
            document=file,
            caption=f"📊 Звіт на {date.today()}",
        )

    async def did_not_send_report(self, callback: CallbackQuery, db: DBConnector) -> None:
        debug_forms = [
            '10-Г', # липовий клас Василя Анатолійовича
            '10-Д', # липовий клас Андрій
            '10-З', # ще один липовий клас Андрія
        ]
        # їх ми не включаємо до списку не надіславших звіт
        all_forms = await db.forms.get_all_form_names()
        sent_reports = await db.reports.get_reports_by_day(date.today())
        sent_form_names = [report.form for report in sent_reports]
        did_not_send = [
            form for form in all_forms
            if form not in sent_form_names and form not in debug_forms
        ]
        did_not_send.sort(key=self._form_sort)

        if len(did_not_send) == 0:
            prompt = "Всі класи надіслали звіт 🎉"
        else:
            prompt = "<b>Список класів, які не надіслали звіт сьогодні:</b>\n\n"
            for form in did_not_send:
                prompt += f"<b>{form}</b>\n"

        await callback.message.edit_text(
            prompt,
            reply_markup=get_back_keyboard('admin'),
            parse_mode=ParseMode.HTML
        )

    # ---------------------------------------------------
    # Broadcast
    # ---------------------------------------------------

    async def broadcast_handler(self, callback: CallbackQuery, state: FSMContext) -> None:
        await state.set_state(BroadcastStates.waiting_for_message)
        prompt = (
            "📥 <b>Створення оголошення</b>\n\n"
            "Введіть текст сповіщення, яке надійде всім вчителям"
        )
        await callback.message.edit_text(
            prompt,
            reply_markup=get_back_keyboard('admin'),
            parse_mode=ParseMode.HTML
        )

    async def broadcast_recv_message_handler(self, message: Message, state: FSMContext) -> None:
        msg = message.text
        if not msg:
            return
        await state.set_state(BroadcastStates.waiting_for_confirmation)
        await state.update_data(msg=msg)
        prompt = (
            f"📥 Ви хочете надіслати повідомлення це повідомленням всім вчителям\n\n"
            f"<blockquote>{msg}</blockquote>\n\n"
            f"<i>вірно?</i>"
        )
        await message.answer(
            prompt,
            reply_markup=get_confirmation_keyboard(),
            parse_mode=ParseMode.HTML
        )

    async def broadcast_submit_handler(self, callback: CallbackQuery, state: FSMContext, db: DBConnector) -> None:
        msg = (await state.get_data()).get('msg', '')
        if not msg:
            return
        users = await db.users.get_all_users()
        sender = await db.admins.get_name(callback.from_user.id)
        response = (
            f"📥 <b>Оголошення</b>\n\n"
            f"<blockquote>{msg}</blockquote>\n\n"
            f"<i>Від: {sender}</i>"
        )
        for user in users:
            await callback.bot.send_message(user.user_id, response, parse_mode=ParseMode.HTML)
        await state.clear()
        await callback.message.edit_text(
            "✅ Повідомлення успішно надіслано!",
            reply_markup=get_back_keyboard('admin'),
            parse_mode=ParseMode.HTML
        )

    # ---------------------------------------------------
    # Utilities
    # ---------------------------------------------------

    @staticmethod
    def _form_sort(form: str):
        match = re.match(r'(\d+)', form)
        if match:
            num = int(match.group(1))
            suffix = form[match.end():]
            return (num, suffix)
        return (0, form)
