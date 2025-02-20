from aiogram.types import InlineKeyboardButton,  InlineKeyboardMarkup

from dict import TEXT_DICT as dict


main_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text=dict['chose_class'], callback_data='chose_class_cd')
        ],
        [
            InlineKeyboardButton(
                text=dict['about_button'], callback_data='about_cd')
        ]
    ]
)

back_to_main_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text=dict['back_to_main_button'],
                callback_data='back_to_main_cd'
            )
        ]
    ]
)

chose_class_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text=class_name, callback_data=f'handle_class_{class_name}'
            )
        ] for class_name in dict['class']
    ]
)

accept_user_data = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text=dict['accept'], callback_data='accept_user_data_cd')
        ],
        [
            InlineKeyboardButton(
                text=dict['cancel'], callback_data='cancel_user_data_cd')
        ]
    ]
)

chose_task = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text=dict['chose_task'], callback_data='chose_task_cd'
            )
        ]
    ]
)

choosing_task = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text=task, callback_data=f'handle_task_{task}_cd'
            ) for task in dict['tasks'][i:i+4]
        ] for i in range(0, len(dict['tasks']), 4)
    ]
)

back_to_task = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text=dict['into_task_2'], callback_data='into_task_2_cd'
            )
        ],
        [
            InlineKeyboardButton(
                text=dict['back_task_list'], callback_data='back_to_task_cd'
            )
        ]
    ]
)

back_task_2 = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text=dict['back_task_2'], callback_data='handle_task_2_cd'
            )
        ]
    ]
)

task_2_done = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text=dict['back_task_2'], callback_data='handle_task_2_cd'
            )
        ],
        [
            InlineKeyboardButton(
                text=dict['back_task_list'], callback_data='back_to_task_cd'
            )
        ]
    ]
)
