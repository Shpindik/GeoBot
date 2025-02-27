from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from dict import ADMIN_DICT as admin_dict
from dict import TEXT_DICT as dict

""" Admin panel keyboard """


admin_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text=admin_dict['admin_add_user'],
                callback_data='admin_add_user_cd'
            ),
            InlineKeyboardButton(
                text=admin_dict['admin_delete_user'],
                callback_data='admin_delete_user_cd'
            )
        ],
        [
            InlineKeyboardButton(
                text=admin_dict['admin_start_spam'],
                callback_data='admin_start_spam_cd'
            )
        ],
        [
            InlineKeyboardButton(
                text=admin_dict['admin_view_user'],
                callback_data='admin_view_user_cd'
            )
        ],
        [
            InlineKeyboardButton(
                text=admin_dict['admin_close_admin'],
                callback_data='back_to_main_cd'
            )
        ]
    ]
)


def get_delete_admin_keyboard(admins_to_show):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=admin_dict['admin_delete'].format(
                        admin_id=admin_id
                    ),
                    callback_data=f'delete_admin_{admin_id}'
                )
            ]for admin_id in admins_to_show
        ] + [
            [
                InlineKeyboardButton(
                    text=admin_dict['admin_close'],
                    callback_data='cancel_delete_cd'
                )
            ]
        ]
    )


def get_confirm_delete_keyboard(admin_id_to_delete):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=admin_dict['admin_ok'],
                    callback_data=f'confirm_delete_{admin_id_to_delete}'
                ),
                InlineKeyboardButton(
                    text=admin_dict['admin_close'],
                    callback_data='cancel_delete_cd'
                )
            ]
        ]
    )


admin_show_user_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text=admin_dict['admin_export_users'],
                                 callback_data='admin_export_users_cd')
        ],
        [
            InlineKeyboardButton(text=admin_dict['admin_back_to_admin'],
                                 callback_data='back_to_admin_cd')
        ]
    ]
)

admin_reply_to_admin = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text=admin_dict['admin_close'],
                callback_data='cancel_feedback_cd'
            )
        ]
    ]
)


def get_reply_keyboard(user_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=admin_dict['admin_answer'],
                    callback_data=f'reply_to_{user_id}'
                )
            ]
        ]
    )


reply_admin_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=admin_dict['admin_close'],
                    callback_data='cancel_reply_cd'
                )
            ]
        ]
    )

admin_spam_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=admin_dict['admin_close'],
                    callback_data='back_to_admin_cd'
                )
            ]
        ]
)


""" Main menu panel keyboard"""


main_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text=dict['chose_class'], callback_data='chose_class_cd')
        ],
        [
            InlineKeyboardButton(
                text=dict['about_button'], callback_data='about_cd')
        ],
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

accept_and_back = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text=dict['back_task_list'],
                callback_data='chose_task_cd'
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


""" Task panel keyboard """


def create_task_done_keyboard(task_callback_data: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=dict['back_task'],
                    callback_data=task_callback_data
                )
            ],
            [
                InlineKeyboardButton(
                    text=dict['back_task_list'],
                    callback_data='back_to_task_cd'
                )
            ],
            [
                InlineKeyboardButton(
                    text=dict['ask_to_admin'],
                    callback_data='ask_admin_cd'
                )
            ]
        ]
    )


task_2_done = create_task_done_keyboard(task_callback_data='handle_task_2_cd')
task_3_done = create_task_done_keyboard(task_callback_data='handle_task_3_cd')
task_5_done = create_task_done_keyboard(task_callback_data='handle_task_5_cd')
task_6_done = create_task_done_keyboard(task_callback_data='handle_task_6_cd')


def create_back_task_keyboard(task_number: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=dict['back_task'],
                    callback_data=f'handle_task_{task_number}_cd'
                )
            ]
        ]
    )


back_task_2 = create_back_task_keyboard(task_number=2)
back_task_3 = create_back_task_keyboard(task_number=3)
back_task_5 = create_back_task_keyboard(task_number=5)
back_task_6 = create_back_task_keyboard(task_number=6)


def create_back_to_task_keyboard(task_number: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=dict['into_task'],
                    callback_data=f'into_task_{task_number}_cd'
                )
            ],
            [
                InlineKeyboardButton(
                    text=dict['back_task_list'],
                    callback_data='back_to_task_cd'
                )
            ]
        ]
    )


back_to_task_2 = create_back_to_task_keyboard(task_number=2)
back_to_task_3 = create_back_to_task_keyboard(task_number=3)
back_to_task_5 = create_back_to_task_keyboard(task_number=5)
back_to_task_6 = create_back_to_task_keyboard(task_number=6)
