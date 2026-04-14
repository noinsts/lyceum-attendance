from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_hub_keyboard(is_admin: bool = False) -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton(text="✍️ Створити звіт", callback_data='send_report', style='primary')],
        [InlineKeyboardButton(text='👤 Профіль', callback_data='profile')],
    ]
    if is_admin:
        keyboard.append(
            [InlineKeyboardButton(text='👑 Адмінка', callback_data='admin', style='danger')],
        )
    keyboard.append(
        [InlineKeyboardButton(text='🆘 Допомога', url='https://t.me/omyzsh', style='danger')]
    )
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_profile_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='✏️ Змінити', callback_data='auth')],
        [InlineKeyboardButton(text='⬅️ Назад', callback_data='hub')]
    ])

def get_back_keyboard(back_trigger: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='⬅️ Назад', callback_data=back_trigger, style='danger')]
    ])

def get_admin_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='📊 Отримати звіт', callback_data='admin_report', style='primary')],
        [InlineKeyboardButton(text='📥 Завантажити звіт', callback_data='admin_download_report', style='primary')],
        [InlineKeyboardButton(text='⬅️ Назад', callback_data='hub')]
    ])
