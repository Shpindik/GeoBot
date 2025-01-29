from aiogram.types import InlineKeyboardButton,  InlineKeyboardMarkup

import dict


keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Нажми меня', callback_data='button1')
        ]
    ]
)
