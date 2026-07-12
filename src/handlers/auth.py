from aiogram import F
from aiogram.types import CallbackQuery, Message, InputRichMessage
from aiogram.filters import Command
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from .base import BaseHandler
from src.db.connector import DBConnector
from src.db.schemas.user import UserSchema
from src.db.schemas.form import FormSchema
from src.utils.keyboards import get_start_work_keyboard
from src.utils.validators import validate_form, validate_name, is_positive_int


class AuthStates(StatesGroup):
    waiting_for_name = State()
    waiting_for_form = State()
    waiting_for_student_count = State()


class AuthHandler(BaseHandler):
    def register_handlers(self):
        self.router.message.register(self.handle, Command('auth'))
        self.router.callback_query.register(self.handle, F.data == 'auth')
        self.router.message.register(self.get_name, AuthStates.waiting_for_name, F.text)
        self.router.message.register(self.get_form, AuthStates.waiting_for_form, F.text)
        self.router.message.register(self.get_student_count, AuthStates.waiting_for_student_count, F.text)

    async def handle(self, event: Message | CallbackQuery, state: FSMContext) -> None:
        await state.set_state(AuthStates.waiting_for_name)
        text = (
            "# 📝 Реєстрація (1/3)\n"
            "Будь ласка, введіть ваше <b>ПІБ</b> 🙌🏻"
        )
        kwargs = {
            'text': text,
            'rich_message': InputRichMessage(markdown=text),
            'parse_mode': ParseMode.HTML
        }
        if isinstance(event, CallbackQuery):
            await event.message.edit_text(**kwargs)
        elif isinstance(event, Message):
            await event.answer_rich(**kwargs)

    async def get_name(self, message: Message, state: FSMContext) -> None:
        is_valid = validate_name(message.text)
        if not is_valid:
            await message.answer("❌ Невірний формат ПІБ.\nСпробуйте ще раз.")
            return
        await state.set_state(AuthStates.waiting_for_form)
        await state.update_data(name=message.text)
        await message.answer_rich(
            rich_message=InputRichMessage(markdown=(
                "# 📝 Реєстрація (2/3)\n"
                "Тепер вкажіть ваш **клас**.\n"
                "Наприклад: `10-А`"
            )),
            parse_mode=ParseMode.HTML
        )

    async def get_form(self, message: Message, state: FSMContext) -> None:
        if not validate_form(message.text):
            await message.answer("❌ Невірний формат класу.\nСпробуйте ще раз.")
            return
        await state.update_data(form=message.text)
        await state.set_state(AuthStates.waiting_for_student_count)
        await message.answer_rich(
            rich_message=InputRichMessage(markdown=(
                "# 📝 Реєстрація (3/3)\n"
                "Чудово! Вкажіть **кількість учнів** у вашому класі. 👥"
            )),
            parse_mode=ParseMode.HTML
        )

    async def get_student_count(self, message: Message, state: FSMContext, db: DBConnector) -> None:
        if not is_positive_int(message.text):
            await message.answer("❌ Невірний формат кількості учнів.\nСпробуйте ще раз.")
            return
        await state.update_data(student_count=message.text)
        await self.submit(message, state, db)

    async def submit(self, message: Message, state: FSMContext, db: DBConnector) -> None:
        data = await state.get_data()
        await state.clear()
        await db.users.add_user(
            UserSchema(
                user_id=int(message.from_user.id),
                name=data.get("name"),
                form=data.get("form"),
            )
        )
        await db.forms.add_form(
            FormSchema(
                name=data.get("form"),
                students_count=int(data.get("student_count")),
            )
        )
        await message.answer_rich(
            rich_message=InputRichMessage(markdown=(
                "# 📝 Реєстрація завершена\n"
                "Ласкаво просимо 🎉"
            )),
            parse_mode=ParseMode.HTML,
            reply_markup=get_start_work_keyboard(),
        )
