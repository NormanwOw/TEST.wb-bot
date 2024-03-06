from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_sub_kb():
    buttons = [
        [
            InlineKeyboardButton(text='Подписаться', callback_data='sub'),
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
