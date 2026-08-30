"""
Food report
"""

from datetime import date

from aiogram import F
from aiogram.types import CallbackQuery, Message, InputRichMessage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from .base import BaseHandler
from src.db.schemas.food import FoodSchema
from src.db.connector import DBConnector
from src.utils.keyboards import get_back_keyboard
from src.utils.validators import is_positive_int


class FoodStates(StatesGroup):
    waiting_for_count = State()


class FoodHandler(BaseHandler):
    def register_handlers(self) -> None:
        self.router.callback_query.register(self.handle, F.data == 'food_report')
        self.router.message.register(self.get_count, F.text, FoodStates.waiting_for_count)

    async def handle(self, callback: CallbackQuery, state: FSMContext, db: DBConnector) -> None:
        user = await db.users.get_user(callback.from_user.id)
        if not user:
            await callback.answer(
                "❌ Ви не авторизовані.\nВикористайте /auth",
                show_alert=True
            )
            return

        await state.set_state(FoodStates.waiting_for_count)
        await state.update_data(user=user)

        form = await db.forms.get_form_by_name(user.form)
        await state.update_data(form=form.name)
        await state.update_data(total=form.students_count)

        text = (
            "# Звіт харчування\n\n"
            "Введіть кількість учнів, які сьогодні **будуть** харчуватись"
        )

        await callback.message.edit_text(
            text=text,
            rich_message=InputRichMessage(markdown=text),
            reply_markup=get_back_keyboard("hub"),
        )

    async def get_count(self, message: Message, state: FSMContext, db: DBConnector) -> None:
        if not message.text or not is_positive_int(message.text):
            await message.answer("❌ Введіть ціле додатнє число")
            return

        await state.update_data(count=message.text)
        await self.submit(message, state, db)

    async def submit(self, message: Message, state: FSMContext, db: DBConnector) -> None:
        data = await state.get_data()
        await state.clear()

        await db.foods.add_report(
            FoodSchema(
                form=data.get("form", "unknown"),
                date=date.today(),
                count=data.get("count", 0),
                total=data.get("total", 0),
            )
        )

        text = (
            f"# Звіт харчування успішно створено!\n\n"
            f"* **Клас:** {data.get('form')}\n"
            f"* **Дата:** {date.today()}\n"
            f"* **Дітей харчується:** {data.get('count', -1)}\n"
            f"* **Всього дітей у класі:** {data.get('total', -1)}\n"
        )

        await message.answer_rich(
            rich_message=InputRichMessage(markdown=text),
            reply_markup=get_back_keyboard('hub', 'primary')
        )
