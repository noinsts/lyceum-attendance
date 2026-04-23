from datetime import date, datetime, time
import pytz

from aiogram import F
from aiogram.types import CallbackQuery, Message
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from .base import BaseHandler
from src.db.connector import DBConnector
from src.db.schemas.report import ReportSchema
from src.utils.keyboards import get_back_keyboard
from src.utils.validators import is_positive_int


class ReportStates(StatesGroup):
    waiting_for_absentees = State()
    waiting_for_patients = State()


class ReportHandler(BaseHandler):
    def register_handlers(self):
        self.router.callback_query.register(self.handle, F.data == 'send_report')
        self.router.message.register(self.get_absentees, ReportStates.waiting_for_absentees, F.text)
        self.router.message.register(self.get_patients, ReportStates.waiting_for_patients, F.text)

    async def handle(self, callback: CallbackQuery, state: FSMContext, db: DBConnector) -> None:
        user = await db.users.get_user(callback.from_user.id)
        if not user:
            await callback.answer(
                "❌ Ви не авторизовані.\nВикористайте /auth",
                show_alert=True
            )
            return
        tz = pytz.timezone("Europe/Kyiv")
        now = datetime.now(tz).time()
        limit = time(9, 25)
        if now >= limit:
            await callback.message.edit_text(
                "⏰ Час для створення звіту минув. Спробуйте завтра зранку.",
                reply_markup=get_back_keyboard('hub'),
                show_alert=True
            )
            return
        await state.set_state(ReportStates.waiting_for_absentees)
        await state.update_data(form=user.form)
        form = await db.forms.get_form_by_name(user.form)
        await state.update_data(student_count=form.students_count)
        await callback.message.edit_text(
            "📋 <b>Створення звіту</b>\n\n"
            "Введіть кількість <b>відсутніх учнів</b>:",
            parse_mode=ParseMode.HTML,
            reply_markup=get_back_keyboard("hub")
        )

    async def get_absentees(self, message: Message, state: FSMContext) -> None:
        if not is_positive_int(message.text):
            await message.answer("❌ Введіть ціле додатнє число")
            return
        await state.update_data(absentees=message.text)
        await state.set_state(ReportStates.waiting_for_patients)
        await message.answer(
            "🤒 Тепер введіть кількість <b>хворих</b>",
            parse_mode=ParseMode.HTML,
            reply_markup=get_back_keyboard('hub')
        )

    async def get_patients(self, message: Message, state: FSMContext, db: DBConnector) -> None:
        if not is_positive_int(message.text):
            await message.answer("❌ Введіть ціле додатнє число")
            return
        if int(message.text) > int((await state.get_data()).get("absentees")):
            await message.answer("🧐 Кількість хворих не може перевищувати кількість відсутніх.")
            return
        await state.update_data(patients=message.text)
        await self.submit(message, state, db)


    async def submit(self, message: Message, state: FSMContext, db: DBConnector) -> None:
        data = await state.get_data()
        await state.clear()
        await db.reports.add_report(
            ReportSchema(
                form=data.get("form"),
                date=date.today(),
                absentees=data.get("absentees"),
                patients=data.get("patients"),
                total=data.get("student_count")
            )
        )
        await message.answer(
            "✅ <b>Звіт успішно створено!</b>",
            parse_mode=ParseMode.HTML,
            reply_markup=get_back_keyboard('hub')
        )
