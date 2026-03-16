from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_hub_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Відправити звіт", callback_data='send_report', style='primary')],
        [InlineKeyboardButton(text='Профіль', callback_data='profile')],
        [InlineKeyboardButton(text='Адмінка', callback_data='admin', style='danger')],
        [InlineKeyboardButton(text='Допомога', url='https://t.me/omyzsh', style='danger')]

    ])

def get_profile_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Edit', callback_data='auth')],
        [InlineKeyboardButton(text='Back', callback_data='hub')]
    ])

def get_back_keyboard(back_trigger: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Back', callback_data=back_trigger, style='danger')]
    ])

def get_admin_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Звіт', callback_data='admin_report', style='primary')],
        [InlineKeyboardButton(text='Back', callback_data='hub')]
    ])
