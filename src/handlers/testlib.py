"""
Експериментальний flow вибору ПІБ відсутніх/хворих учнів
"""

from aiogram import F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, InputRichMessage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters.callback_data import CallbackData

from .base import BaseHandler
from src.utils.keyboards import get_back_keyboard


class StudentCallbackData(CallbackData, prefix="student"):
    id: int


class TestLibStates(StatesGroup):
    waiting_for_selection = State()


STUDENTS = [
    "Шевченко Тарас Григорович",
    "Франко Іван Якович",
    "Остапенко Михайло Олексійович",
    "Михайленко Остап Олексійович",
]


STATUS_STYLES = {
    'present': 'success',   # green
    'absent': 'danger',     # red
    'sick': 'primary',      # blue
}


def build_keyboard(curr_statuses: dict) -> InlineKeyboardMarkup:
    """
    curr_statuses: dict {0: "present", 1: "absent", ...}
    """
    kb = []
    for idx, name in enumerate(STUDENTS):
        status = curr_statuses.get(idx, "present")
        btn_style = STATUS_STYLES[status]
        kb.append([
            InlineKeyboardButton(
                text=name,
                callback_data=StudentCallbackData(id=idx).pack(),
                style=btn_style,
            )
        ])
    kb.append([InlineKeyboardButton(text="✅ Підтвердити вибір", callback_data="confirm_selection")])
    kb.append([InlineKeyboardButton(text='⬅️ Скасувати', callback_data='admin')])
    return InlineKeyboardMarkup(inline_keyboard=kb)


class TestLibHandler(BaseHandler):
    def register_handlers(self) -> None:
        self.router.callback_query.register(self.handler, F.data == 'testlib')
        self.router.callback_query.register(
            self.select_student_handler,
            StudentCallbackData.filter(),
            TestLibStates.waiting_for_selection,
        )
        self.router.callback_query.register(self.confirm_handler, F.data == "confirm_selection")

    async def handler(self, callback: CallbackQuery, state: FSMContext) -> None:
        await state.set_state(TestLibStates.waiting_for_selection)

        init_statuses = {idx: "present" for idx in range(len(STUDENTS))}
        await state.update_data(statuses=init_statuses)

        text = (
            "# 📋 Створення звіту (1/2)\n\n"
            f"> Зверніть увагу: це демка, яка не вміє надсилати звіт\n\n"
            "Для кожного учня оберіть відповідний колір\n\n"
            "Зміна кольору відбувається натисканням на потрібного учня\n"
            "### Умовні позначення:\n"
            "* 🟢 - у школі;\n"
            "* 🔴 - відсутній;\n"
            "* 🔵 - хворий.\n"
        )

        await callback.message.edit_text(
            text=text,
            rich_message=InputRichMessage(markdown=text),
            reply_markup=build_keyboard(init_statuses),
        )

    async def select_student_handler(self, callback: CallbackQuery, state: FSMContext, callback_data: StudentCallbackData) -> None:
        """
        Хендлер спрацьовує на натискання інлайн кнопки з учнем
        """
        statuses = (await state.get_data()).get("statuses", {})

        student_id = callback_data.id
        curr_status = statuses.get(student_id, "present")

        # Cycle: present -> absent -> sick -> present
        if curr_status == "present":
            new_status = "absent"
        elif curr_status == "absent":
            new_status = "sick"
        else:
            new_status = "present"

        statuses[student_id] = new_status
        await state.update_data(statuses=statuses)

        await callback.message.edit_reply_markup(
            reply_markup=build_keyboard(statuses),
        )
        await callback.answer()

    async def confirm_handler(self, callback: CallbackQuery, state: FSMContext) -> None:
        statuses = (await state.get_data()).get("statuses", {})
        await state.clear()

        absentees = []
        patients = []

        for idx, status in statuses.items():
            if status == "absent":
                absentees.append(STUDENTS[idx])
            elif status == "sick":
                patients.append(STUDENTS[idx])

        absentees_text = "\n".join(f"* {a}" for a in absentees) if absentees else "Всі присутні 🤩"
        patients_text = "\n".join(f"* {p}" for p in patients) if patients else "Всі здорові 🤩"

        response = (
            f"# 📋 Створення звіту (2/2)\n"
            f"> Зверніть увагу: це демка, яка не вміє надсилати звіт\n\n"
            f"Надіслані наступні дані:\n\n"
            f"### Список відсутніх учнів:\n{absentees_text}\n\n"
            f"### Список хворих учнів:\n{patients_text}"
        )
        await callback.message.edit_text(
            text=response,
            rich_message=InputRichMessage(markdown=response),
            reply_markup=get_back_keyboard('admin')
        )
