from aiogram.types import InlineKeyboardButton,  InlineKeyboardMarkup

import dict


main_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Нажать кнопку 1', callback_data='button1')
        ],
        [
            InlineKeyboardButton(
                text='Нажать кнопку 2', callback_data='button2')
        ],
        [
            InlineKeyboardButton(
                text='Нажать кнопку 3', callback_data='button3')
        ],
    ]
)
