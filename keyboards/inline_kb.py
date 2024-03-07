from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_sub_kb() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(text='Подписаться', callback_data='sub'),
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def get_cancel_kb() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(text='Отмена', callback_data='cancel'),
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def get_pagination_kb(mailing_id: int, count: int, page: int = 1) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(text='◀', callback_data=f'prev_{page-1}'),
            InlineKeyboardButton(text='▶', callback_data=f'next_{page+1}'),
        ],
        [
            InlineKeyboardButton(text='Остановить', callback_data=f'stop_{mailing_id}')
        ]
    ]
    if count == 1:
        del buttons[0]

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard