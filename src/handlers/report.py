from datetime import date

from aiogram import F
from aiogram.types import CallbackQuery, Message
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
        self.router.message.register(self.get_absentees, ReportStates.waiting_for_absentees)
        self.router.message.register(self.get_patients, ReportStates.waiting_for_patients)

    async def handle(self, callback: CallbackQuery, state: FSMContext, db: DBConnector) -> None:
        user = await db.users.get_user(callback.from_user.id)
        if not user:
            await callback.answer("Помилка авторизації, використайте /auth", show_alert=True)
            return
        await state.update_data(form=user.form)
        await state.set_state(ReportStates.waiting_for_absentees)
        await callback.message.edit_text(
            "Введіть кількість відсутніх",
            reply_markup=get_back_keyboard('hub')
        )
        

    async def get_absentees(self, message: Message, state: FSMContext) -> None:
        if not is_positive_int(message.text):
            await message.answer("Введіть ціле позитивне число")
            return
        await state.update_data(absentees=message.text)
        await state.set_state(ReportStates.waiting_for_patients)
        await message.answer(
            "Введіть кількість хворих",
            reply_markup=get_back_keyboard('hub')
        )

    async def get_patients(self, message: Message, state: FSMContext, db: DBConnector) -> None:
        if not is_positive_int(message.text):
            await message.answer("Введіть ціле позитивне число")
            return
        if int(message.text) > int((await state.get_data()).get("absentees")):
            await message.answer("Кількість хворих не може бути більшою за кількість відсутніх. Це не логічно 🧐")
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
                patients=data.get("patients")
            )
        )
        await message.answer(
            "Успішно.",
            reply_markup=get_back_keyboard('hub')
        )
