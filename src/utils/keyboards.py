from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_hub_keyboard(is_admin: bool = False) -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton(text="✍️ Відвідуваність", callback_data='send_report', style='primary')],
        [InlineKeyboardButton(text="🍞 Харчування", callback_data='food_report', style='success')],
        [InlineKeyboardButton(text='👤 Профіль', callback_data='profile')],
    ]
    if is_admin:
        keyboard.append(
            [InlineKeyboardButton(text='👑 Адмінка', callback_data='admin', style='danger')],
        )
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_profile_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='✏️ Редагувати', callback_data='auth')],
        [InlineKeyboardButton(text='⬅️ До головного меню', callback_data='hub')]
    ])

def get_back_keyboard(back_trigger: str, style: str = 'danger') -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='⬅️ До головного меню', callback_data=back_trigger, style=style)]
    ])

def get_admin_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='🍞 Сьогоднішній звіт харчування', callback_data='admin_food_report', style='success')],
        [InlineKeyboardButton(text='📊 Сьогоднішня відвідуваність', callback_data='admin_report', style='primary')],
        [InlineKeyboardButton(text='📥 Завантажити сьогоднішню відвідуваність', callback_data='admin_download_report', style='primary')],
        [InlineKeyboardButton(text='⚠️ Не надіслали звіт відвідуваності', callback_data='admin_did_not_send_report', style='primary')],
        [InlineKeyboardButton(text='📩 Надіслати оголошення', callback_data='admin_broadcast', style='danger')],
        [InlineKeyboardButton(text='🧪 Тест оновленої подачі звіту відвідуваності', callback_data='testlib', style='danger')],
        [InlineKeyboardButton(text='⬅️ До головного меню', callback_data='hub')]
    ])

def get_create_report_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✍️ Створити звіт", callback_data='send_report', style='primary')],
    ])

def get_confirmation_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="✅ Так", callback_data='submit', style='success'),
        InlineKeyboardButton(text="❌ Ні", callback_data='cancel', style='danger'),
    ]])

def get_start_work_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='🚀 Почати роботу', callback_data='hub', style='primary')]
    ])
