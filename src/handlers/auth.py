from aiogram import F
from aiogram.types import CallbackQuery, Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from .base import BaseHandler
from src.db.connector import DBConnector
from src.db.schemas.user import UserSchema
from src.utils.keyboards import get_hub_keyboard
from src.utils.validators import validate_form, validate_name


class AuthStates(StatesGroup):
    waiting_for_name = State()
    waiting_for_form = State()


class AuthHandler(BaseHandler):
    def register_handlers(self):
        self.router.message.register(self.handle, Command('auth'))
        self.router.callback_query.register(self.handle, F.data == 'auth')
        self.router.message.register(self.get_name, AuthStates.waiting_for_name)
        self.router.message.register(self.get_form, AuthStates.waiting_for_form)

    async def handle(self, event: Message | CallbackQuery, state: FSMContext) -> None:
        await state.set_state(AuthStates.waiting_for_name)
        text = "Введіть ваше ПІБ"
        if isinstance(event, CallbackQuery):
            await event.message.edit_text(text)
        elif isinstance(event, Message):
            await event.answer(text)

    async def get_name(self, message: Message, state: FSMContext) -> None:
        is_valid = validate_name(message.text)
        if not is_valid:
            await message.answer("Введіть валідне ім'я.")
            return
        await state.set_state(AuthStates.waiting_for_form)
        await state.update_data(name=message.text)
        await message.answer("Вкажіть клас:")

    async def get_form(self, message: Message, state: FSMContext, db: DBConnector) -> None:
        if not validate_form(message.text):
            await message.answer("Введіть валідний клас")
            return
        await state.update_data(form=message.text)
        await self.submit(message, state, db)

    async def submit(self, message: Message, state: FSMContext, db: DBConnector) -> None:
        data = await state.get_data()
        await state.clear()
        await db.users.add_user(
            UserSchema(
                user_id=message.from_user.id,
                name=data.get("name"),
                form=data.get("form")
            )
        )
        await message.answer(
            "Успішно зареєстровано!",
            reply_markup=get_hub_keyboard()
        )
