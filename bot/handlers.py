import os
import re
from functools import wraps

import kb
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, ContentType, FSInputFile, Message
from database import (export_users_to_excel, get_user_full_name, get_user_ids,
                      get_users, save_user_data, update_completed_tasks)
from dict import ADMIN_DICT as admin_dict
from dict import TASK_DICT as dict_task
from dict import TEXT_DICT as dict
from dict import VIDEO_LINKS as video_dict
from dotenv import dotenv_values, load_dotenv
from handler_answers import handle_task, handle_task_answer
from states import AdminState, FeedbackStates, TaskState, UserState

load_dotenv()

NAME_REGEX = re.compile(r'^[А-Яа-яЁёA-Za-z]+ [А-Яа-яЁёA-Za-z]+$')
ADMIN_TOKEN = os.getenv('ADMIN', 'admin1_id,admin2_id').split(',')


router = Router()


def check_old_answer(text):
    def decorator(func):
        @wraps(func)
        async def wrapper(callback: CallbackQuery):
            if callback.message.text != text:
                await func(callback)
            await callback.answer()
        return wrapper
    return decorator


""" Admin handlers """


@router.message(F.text == '/admin')
async def admin_panel(message: Message):
    if str(message.from_user.id) in ADMIN_TOKEN:
        await message.answer(
            admin_dict['admin_accept'],
            reply_markup=kb.admin_keyboard
        )
    else:
        await message.answer(
            admin_dict['admin_denied']
        )


@router.callback_query(F.data == 'admin_add_user_cd')
async def add_admin_callback(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup(
        reply_markup=None
    )
    await callback.message.answer(
        admin_dict['admin_add_new_admin']
    )
    await state.set_state(AdminState.waiting_for_admin_id)


@router.message(AdminState.waiting_for_admin_id)
async def process_admin_id(message: Message, state: FSMContext):
    new_admin_id = message.text.strip()
    if new_admin_id.isdigit():

        if len(new_admin_id) < 9 or len(new_admin_id) > 10:
            await message.answer(
                admin_dict['admin_length_alert'],
                reply_markup=kb.admin_keyboard
            )
            return

        new_admin_id = int(new_admin_id)

        if str(new_admin_id) in ADMIN_TOKEN:
            await message.answer(
                admin_dict['admin_already_exists'].format(
                    new_admin_id=new_admin_id
                ),
                reply_markup=kb.admin_keyboard
            )
        else:
            with open('.env', 'a') as env_file:
                env_file.write(f',{new_admin_id}')
            ADMIN_TOKEN.append(str(new_admin_id))
            await message.answer(
                admin_dict['admin_succes_add_admin'].format(
                    new_admin_id=new_admin_id
                ),
                reply_markup=kb.admin_keyboard
            )
    else:
        await message.answer(
            admin_dict['admin_add_alert'],
            reply_markup=kb.admin_keyboard
        )

    await state.clear()


@router.callback_query(F.data == 'admin_delete_user_cd')
async def delete_admin_handler(callback: CallbackQuery):
    admins_to_show = ADMIN_TOKEN[2:] if len(ADMIN_TOKEN) > 2 else []

    if not admins_to_show:
        await callback.message.edit_text(
            admin_dict['admin_empty'],
            reply_markup=kb.admin_keyboard
        )
        return

    await callback.message.edit_text(
        admin_dict['admin_delete_list'],
        reply_markup=kb.get_delete_admin_keyboard(admins_to_show)
    )


@router.callback_query(F.data.startswith('delete_admin_'))
async def confirm_delete_admin(callback: CallbackQuery):
    admin_id_to_delete = callback.data.split('_')[-1]
    await callback.message.edit_text(
        admin_dict['admin_confirm'].format(
            admin_id_to_delete=admin_id_to_delete
        ),
        reply_markup=kb.get_confirm_delete_keyboard(admin_id_to_delete)
    )


@router.callback_query(F.data.startswith('confirm_delete_'))
async def execute_delete_admin(callback: CallbackQuery):
    admin_id_to_delete = callback.data.split('_')[-1]
    if admin_id_to_delete in ADMIN_TOKEN:
        if len(ADMIN_TOKEN) > 2:
            try:
                config = dotenv_values('.env')
                ADMIN_TOKEN.remove(admin_id_to_delete)
                new_admins = ','.join(ADMIN_TOKEN)
                config['ADMIN'] = new_admins

                with open('.env', 'w') as f:
                    for key, value in config.items():
                        f.write(f'{key}={value}\n')
                await callback.message.edit_text(
                    admin_dict['admin_delete_accept'].format(
                        admin_id_to_delete=admin_id_to_delete
                    ),
                    reply_markup=kb.admin_keyboard
                    )
            except Exception as e:
                await callback.message.edit_text(
                    f'{admin_dict['admin_alert']}{str(e)}',
                    reply_markup=kb.admin_keyboard
                    )
        else:
            await callback.message.edit_text(
                admin_dict['admin_alert_delete_admin'],
                reply_markup=kb.admin_keyboard
                )
    else:
        await callback.message.edit_text(
            admin_dict['admin_not_found'],
            reply_markup=kb.admin_keyboard
            )


@router.callback_query(F.data == 'cancel_delete_cd')
async def cancel_delete(callback: CallbackQuery):
    await callback.message.edit_text(
        admin_dict['admin_accept'],
        reply_markup=kb.admin_keyboard)


@router.callback_query(F.data == 'admin_view_user_cd')
async def handle_view_users(callback: CallbackQuery, state: FSMContext):
    await state.update_data()
    await show_users_page(callback, state)


async def show_users_page(callback: CallbackQuery, state: FSMContext):
    users = await get_users()

    if not users:
        if callback.message.text != admin_dict['admin_empty_users']:
            await callback.message.edit_text(
                admin_dict['admin_empty_users'],
                reply_markup=kb.admin_keyboard
            )
        return

    response = f'{admin_dict['admin_view_users']}\n\n'
    for user in users:
        user_id, class_name, full_name, completed_tasks = user
        tasks = completed_tasks if completed_tasks else ' - '
        response += (
            f'├ ID: {user_id}\n'
            f'├ Класс: {class_name}\n'
            f'├ Имя: {full_name}\n'
            f'└ Выполненные задания: {tasks}\n\n'
        )

    await callback.message.edit_text(
        response,
        reply_markup=kb.admin_show_user_keyboard
    )


@router.callback_query(F.data == 'admin_export_users_cd')
async def handle_export_users(callback: CallbackQuery):
    try:
        file_path = await export_users_to_excel()
        file = FSInputFile(file_path, filename='users_export.xlsx')
        await callback.message.answer_document(file)
        await callback.answer(admin_dict['admin_export_accept'])
    except Exception as e:
        await callback.message.answer(f'{admin_dict['admin_alert']}{str(e)}')


@router.callback_query(F.data == 'back_to_admin_cd')
async def handle_back_to_admin(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(
        admin_dict['admin_accept'],
        reply_markup=kb.admin_keyboard
    )


@router.callback_query(F.data == 'ask_admin_cd')
async def ask_admin_handler(callback: CallbackQuery, state: FSMContext):
    msg = await callback.message.answer(
        admin_dict['admin_user_message'],
        reply_markup=kb.admin_reply_to_admin
        )
    await state.update_data(
        bot_message_id=msg.message_id,
        user_message_id=callback.message.message_id
    )

    await state.set_state(FeedbackStates.waiting_for_user_message)


@router.message(FeedbackStates.waiting_for_user_message)
async def forward_to_admin(message: Message, state: FSMContext):
    full_name = await get_user_full_name(message.from_user.id)
    await state.update_data(message_text=message.text)

    username = f'@{message.from_user.username}' \
        if message.from_user.username else f'(ID: {message.from_user.id})'

    reply_markup = kb.get_reply_keyboard(message.from_user.id)

    for admin_id in ADMIN_TOKEN:
        try:
            await message.bot.send_message(
                admin_id,
                f'{admin_dict['admin_new_msg']}{full_name} '
                f'{username}:\n{message.text}',
                reply_markup=reply_markup
            )
        except Exception as e:
            print(f'{admin_dict['admin_alert']}{e}')

    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    user_message_id = data.get('user_message_id')

    try:
        await message.bot.delete_message(message.chat.id, message.message_id)
        if bot_message_id:
            await message.bot.delete_message(message.chat.id, bot_message_id)
        if user_message_id:
            await message.bot.delete_message(message.chat.id, user_message_id)
    except Exception as e:
        print(f'Ошибка при удалении сообщений: {e}')

    await message.answer(
        admin_dict['admin_answer_success'],
        reply_markup=kb.accept_and_back
    )
    await state.clear()


@router.callback_query(F.data.startswith('reply_to_'))
async def start_admin_reply(callback: CallbackQuery, state: FSMContext):
    user_id = callback.data.split('_')[-1]
    full_name = await get_user_full_name(user_id)
    await state.update_data(target_user_id=user_id)
    await callback.message.answer(
        f'{admin_dict['admin_reply_to_user']} {full_name}:',
        reply_markup=kb.reply_admin_markup
        )
    await state.set_state(FeedbackStates.waiting_for_admin_reply)


@router.message(
    FeedbackStates.waiting_for_admin_reply,
    F.text | F.photo | F.video | F.voice | F.video_note | F.document
)
async def send_admin_reply(message: Message, state: FSMContext):
    data = await state.get_data()
    user_id = data.get('target_user_id')
    full_name = await get_user_full_name(user_id)

    caption_text = (
        f'{admin_dict['admin_bot_reply']}\n\n{message.caption or ''}'
    ).strip()

    try:
        if message.text:
            await message.bot.send_message(
                user_id,
                f'{admin_dict['admin_bot_reply']}\n\n{message.text}'
            )
        elif message.photo:
            await message.bot.send_photo(
                user_id,
                message.photo[-1].file_id,
                caption=caption_text
            )
        elif message.video:
            await message.bot.send_video(
                user_id,
                message.video.file_id,
                caption=caption_text
            )
        elif message.voice:
            await message.bot.send_voice(
                user_id,
                message.voice.file_id
            )
            if message.caption:
                await message.bot.send_message(user_id, caption_text)
        elif message.video_note:
            await message.bot.send_video_note(
                user_id,
                message.video_note.file_id
            )
            if message.caption:
                await message.bot.send_message(user_id, caption_text)
        elif message.document:
            await message.bot.send_document(
                user_id,
                message.document.file_id,
                caption=caption_text
            )

        await message.answer(
            f'{admin_dict['admin_answer_success_to_user']} {full_name}'
        )
    except Exception as e:
        await message.answer(f'{admin_dict['admin_alert']}{str(e)}')

    await state.clear()


@router.callback_query(F.data == 'cancel_reply_cd')
async def cancel_reply(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.delete()


@router.callback_query(F.data == 'cancel_feedback_cd')
async def cancel_feedback(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.delete()


@router.callback_query(F.data == 'admin_start_spam_cd')
async def start_spam(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        text=admin_dict['admin_accept_spam'],
        reply_markup=kb.admin_spam_keyboard
    )
    await state.set_state(FeedbackStates.waiting_for_spam_message)


@router.message(F.content_type.in_({
    ContentType.TEXT,
    ContentType.PHOTO,
    ContentType.VIDEO,
    ContentType.VOICE,
    ContentType.VIDEO_NOTE,
    ContentType.DOCUMENT,
    ContentType.AUDIO}), FeedbackStates.waiting_for_spam_message)
async def handle_spam_message(message: Message, state: FSMContext):
    user_ids = await get_user_ids()
    await send_spam(message, user_ids)
    await message.answer(
        admin_dict['admin_spam_success']
    )
    await state.clear()
    await message.answer(
        admin_dict['admin_accept'],
        reply_markup=kb.admin_keyboard
    )


async def send_spam(message: Message, user_ids: list[int]):
    for user_id in user_ids:
        try:
            if message.content_type == ContentType.TEXT:
                await message.bot.send_message(
                    user_id,
                    message.text
                )
            elif message.content_type == ContentType.PHOTO:
                await message.bot.send_photo(
                    user_id,
                    message.photo[-1].file_id,
                    caption=message.caption
                )
            elif message.content_type == ContentType.VIDEO:
                await message.bot.send_video(
                    user_id,
                    message.video.file_id,
                    caption=message.caption
                )
            elif message.content_type == ContentType.VOICE:
                await message.bot.send_voice(
                    user_id,
                    message.voice.file_id
                )
            elif message.content_type == ContentType.VIDEO_NOTE:
                await message.bot.send_video_note(
                    user_id,
                    message.video_note.file_id
                )
            elif message.content_type == ContentType.DOCUMENT:
                await message.bot.send_document(
                    user_id,
                    message.document.file_id,
                    caption=message.caption
                )
            elif message.content_type == ContentType.AUDIO:
                await message.bot.send_audio(
                    user_id,
                    message.audio.file_id,
                    caption=message.caption
                )
        except Exception as e:
            print(f'{admin_dict['admin_alert']} {e}')

""" Main menu handlers"""


@router.message(F.text == '/start')
async def cmd_start(message: Message):
    await message.answer(
        dict['greet'].format(name=message.from_user.first_name),
        reply_markup=kb.main_menu
        )


@router.callback_query(F.data == 'about_cd')
@check_old_answer('about_cd')
async def handle_about(callback: CallbackQuery):
    await callback.message.edit_text(
        dict['about'],
        reply_markup=kb.back_to_main_menu
    )


@router.callback_query(F.data == 'back_to_main_cd')
@check_old_answer('back_to_main_cd')
async def handle_back_to_main(callback: CallbackQuery):
    await callback.message.edit_text(
        dict['greet'].format(name=callback.from_user.first_name),
        reply_markup=kb.main_menu
    )


@router.callback_query(F.data == 'chose_class_cd')
@check_old_answer('chose_class_cd')
async def handle_chose_class(callback: CallbackQuery):
    await callback.message.edit_text(
        dict['chose_class'],
        reply_markup=kb.chose_class_menu
    )


@router.callback_query(F.data.in_(
        [f'handle_class_{class_name}' for class_name in dict['class']]
        )
    )
async def handle_class_callback(callback: CallbackQuery, state: FSMContext):
    class_name = callback.data.split('_')[-1]

    await state.update_data(
        class_name=class_name,
        last_message_id=callback.message.message_id,
        messages_to_delete=[]
    )

    await state.update_data(class_name=class_name)

    await callback.message.edit_text(
        dict['next_step_class']
    )

    await state.set_state(UserState.waiting_for_name)


@router.message(F.text, UserState.waiting_for_name)
async def handle_name_input(message: Message, state: FSMContext):
    data = await state.get_data()
    messages_to_delete = data.get('messages_to_delete', [])

    if not NAME_REGEX.match(message.text):
        await message.delete()
        error_msg = await message.answer(
            dict['allert_input_name']
        )
        messages_to_delete.append(error_msg.message_id)
        await state.update_data(messages_to_delete=messages_to_delete)
        return

    for msg_id in messages_to_delete:
        try:
            await message.bot.delete_message(
                chat_id=message.chat.id,
                message_id=msg_id
            )
        except Exception as e:
            print(f'Ошибка при удалении сообщения: {e}')

    data = await state.get_data()
    class_name = data.get('class_name')
    last_message_id = data.get('last_message_id')

    await state.update_data(full_name=message.text, messages_to_delete=[])

    await message.bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=last_message_id,
        text=dict['approve_data'].format(
            message=message.text,
            class_name=class_name
        ),
        reply_markup=kb.accept_user_data
    )

    await message.delete()


@router.callback_query(F.data == 'accept_user_data_cd')
async def handle_accept_user_data(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    class_name = data.get('class_name')
    full_name = data.get('full_name')
    user_id = callback.from_user.id

    for msg_id in data.get('messages_to_delete', []):
        try:
            await callback.message.bot.delete_message(
                chat_id=callback.message.chat.id,
                message_id=msg_id
            )
        except Exception as e:
            print(f'Ошибка при удалении сообщения: {e}')

    await save_user_data(user_id, class_name, full_name)

    await callback.message.delete()
    await state.clear()

    await callback.message.answer(
        dict['main_menu'].format(name=full_name),
        reply_markup=kb.chose_task
    )


@router.callback_query(F.data == 'cancel_user_data_cd')
async def handle_cancel_user_data(callback: CallbackQuery, state: FSMContext):
    await state.clear()

    await callback.message.edit_text(
        dict['chose_class'],
        reply_markup=kb.chose_class_menu
    )


@router.callback_query(F.data == 'chose_task_cd')
@check_old_answer('chose_task_cd')
async def handle_chose_task(callback: CallbackQuery):
    await callback.message.edit_reply_markup(
        reply_markup=None
    )
    await callback.message.answer(
        text=dict['chose_task'],
        reply_markup=kb.choosing_task
    )


@router.callback_query(F.data == 'back_to_task_cd')
@check_old_answer('back_to_task_cd')
async def handle_back_to_task(callback: CallbackQuery):
    await callback.message.edit_text(
        dict['chose_task'],
        reply_markup=kb.choosing_task
    )


""" Task Handlers """


@router.callback_query(F.data == 'handle_task_2_cd')
@check_old_answer('handle_task_2_cd')
async def handle_task_2(callback: CallbackQuery):
    await callback.message.delete()
    video_link = video_dict['video_2']
    await handle_task(
        callback=callback,
        state=None,
        task_text=dict_task['video_task'],
        reply_markup=kb.back_to_task_2,
        video_link=video_link
    )


@router.callback_query(F.data == 'into_task_2_cd')
async def into_task_2(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await handle_task(
        callback=callback,
        state=state,
        task_text=dict_task['task_2_1'],
        reply_markup=kb.back_task_2,
        next_state=TaskState.waiting_for_task_2_1_answer
    )


@router.message(TaskState.waiting_for_task_2_1_answer)
async def handle_task_2_1_answer(message: Message, state: FSMContext):
    await handle_task_answer(
        message=message,
        state=state,
        correct_answers_key='correct_answer_2_1',
        next_task_text=dict_task['task_2_2'],
        reply_markup=kb.back_task_2,
        next_state=TaskState.waiting_for_task_2_2_answer
    )


@router.message(TaskState.waiting_for_task_2_2_answer)
async def handle_task_2_2_answer(message: Message, state: FSMContext):
    await handle_task_answer(
        message=message,
        state=state,
        correct_answers_key='correct_answer_2_2',
        next_task_text=dict_task['task_2_3'],
        reply_markup=kb.back_task_2,
        next_state=TaskState.waiting_for_task_2_3_answer
    )


@router.message(TaskState.waiting_for_task_2_3_answer)
async def handle_task_2_3_answer(message: Message, state: FSMContext):
    await handle_task_answer(
        message=message,
        state=state,
        correct_answers_key='correct_answer_2_3',
        next_task_text=dict_task['task_2_4'],
        reply_markup=kb.back_task_2,
        next_state=TaskState.waiting_for_task_2_4_answer
    )


@router.message(TaskState.waiting_for_task_2_4_answer)
async def handle_task_2_4_answer(message: Message, state: FSMContext):
    await handle_task_answer(
        message=message,
        state=state,
        correct_answers_key='correct_answer_2_4',
        next_task_text=dict_task['task_2_5'],
        reply_markup=kb.back_task_2,
        next_state=TaskState.waiting_for_task_2_5_answer
    )


@router.message(TaskState.waiting_for_task_2_5_answer)
async def handle_task_2_5_answer(message: Message, state: FSMContext):
    await handle_task_answer(
        message=message,
        state=state,
        correct_answers_key='correct_answer_2_5',
        next_task_text='',
        next_state=None,
        reply_markup=kb.task_2_done,
        final_step=True,
        task_number=2
    )


@router.callback_query(F.data == 'handle_task_3_cd')
@check_old_answer('handle_task_3_cd')
async def handle_task_3(callback: CallbackQuery):
    await callback.message.delete()
    await handle_task(
        callback=callback,
        state=None,
        task_text=dict_task['task_3'],
        reply_markup=kb.back_to_task_3,
        parse_mode='HTML'
    )


@router.callback_query(F.data == 'into_task_3_cd')
async def into_task_3(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await handle_task(
        callback=callback,
        state=state,
        task_text=dict_task['task_3_1'],
        reply_markup=kb.back_task_3,
        next_state=TaskState.waiting_for_task_3_1_answer,
        parse_mode='HTML'
    )


@router.message(TaskState.waiting_for_task_3_1_answer)
async def handle_task_3_1_answer(message: Message, state: FSMContext):
    await handle_task_answer(
        message=message,
        state=state,
        correct_answers_key='correct_answer_3_1',
        next_task_text=dict_task['task_3_2'],
        parse_mode='HTML',
        reply_markup=kb.back_task_3,
        next_state=TaskState.waiting_for_task_3_2_answer
    )


@router.message(TaskState.waiting_for_task_3_2_answer)
async def handle_task_3_2_answer(message: Message, state: FSMContext):
    await handle_task_answer(
        message=message,
        state=state,
        correct_answers_key='correct_answer_3_2',
        next_task_text=dict_task['task_3_3'],
        parse_mode='HTML',
        reply_markup=kb.back_task_3,
        next_state=TaskState.waiting_for_task_3_3_answer
    )


@router.message(TaskState.waiting_for_task_3_3_answer)
async def handle_task_3_3_answer(message: Message, state: FSMContext):
    await handle_task_answer(
        message=message,
        state=state,
        correct_answers_key='correct_answer_3_3',
        next_task_text=dict_task['task_3_4'],
        parse_mode='HTML',
        reply_markup=kb.back_task_3,
        next_state=TaskState.waiting_for_task_3_4_answer
    )


@router.message(TaskState.waiting_for_task_3_4_answer)
async def handle_task_3_4_answer(message: Message, state: FSMContext):
    await handle_task_answer(
        message=message,
        state=state,
        correct_answers_key='correct_answer_3_4',
        next_task_text=dict_task['task_3_5'],
        parse_mode='HTML',
        reply_markup=kb.back_task_3,
        next_state=TaskState.waiting_for_task_3_5_answer
    )


@router.message(TaskState.waiting_for_task_3_5_answer)
async def handle_task_3_5_answer(message: Message, state: FSMContext):
    await handle_task_answer(
        message=message,
        state=state,
        correct_answers_key='correct_answer_3_5',
        next_task_text='',
        next_state=None,
        reply_markup=kb.task_3_done,
        final_step=True,
        task_number=3
    )


@router.callback_query(F.data == 'handle_task_5_cd')
@check_old_answer('handle_task_5_cd')
async def handle_task_5(callback: CallbackQuery):
    await callback.message.delete()
    video_link = video_dict['video_5']
    await handle_task(
        callback=callback,
        state=None,
        task_text=dict_task['video_task'],
        reply_markup=kb.back_to_task_5,
        parse_mode='HTML',
        video_link=video_link
    )


@router.callback_query(F.data == 'into_task_5_cd')
async def into_task_5(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await handle_task(
        callback=callback,
        state=state,
        task_text=dict_task['task_5_1'],
        reply_markup=kb.back_task_5,
        next_state=TaskState.waiting_for_task_5_1_answer,
        parse_mode='HTML',
        image_filename='image_5_1.jpg'
    )


@router.message(TaskState.waiting_for_task_5_1_answer)
async def handle_task_5_1_answer(message: Message, state: FSMContext):
    await handle_task_answer(
        message=message,
        state=state,
        correct_answers_key='correct_answer_5_1',
        next_task_text=dict_task['task_5_2'],
        parse_mode='HTML',
        reply_markup=kb.back_task_5,
        next_state=TaskState.waiting_for_task_5_2_answer,
        image_filename='image_5_2.jpg'
    )


@router.message(TaskState.waiting_for_task_5_2_answer)
async def handle_task_5_2_answer(message: Message, state: FSMContext):
    await handle_task_answer(
        message=message,
        state=state,
        correct_answers_key='correct_answer_5_2',
        next_task_text=dict_task['task_5_3'],
        parse_mode='HTML',
        reply_markup=kb.back_task_5,
        next_state=TaskState.waiting_for_task_5_3_answer,
        image_filename='image_5_3.jpg'
    )


@router.message(TaskState.waiting_for_task_5_3_answer)
async def handle_task_5_3_answer(message: Message, state: FSMContext):
    await handle_task_answer(
        message=message,
        state=state,
        correct_answers_key='correct_answer_5_3',
        next_task_text=dict_task['task_5_4'],
        parse_mode='HTML',
        reply_markup=kb.back_task_5,
        next_state=TaskState.waiting_for_task_5_4_answer,
        image_filename='image_5_4.jpg'
    )


@router.message(TaskState.waiting_for_task_5_4_answer)
async def handle_task_5_4_answer(message: Message, state: FSMContext):
    await handle_task_answer(
        message=message,
        state=state,
        correct_answers_key='correct_answer_5_4',
        next_task_text=dict_task['task_5_5'],
        parse_mode='HTML',
        reply_markup=kb.back_task_5,
        next_state=TaskState.waiting_for_task_5_5_answer,
        image_filename='image_5_5.jpg'
    )


@router.message(TaskState.waiting_for_task_5_5_answer)
async def handle_task_5_5_answer(message: Message, state: FSMContext):
    await handle_task_answer(
        message=message,
        state=state,
        correct_answers_key='correct_answer_5_5',
        next_task_text='',
        next_state=None,
        reply_markup=kb.task_5_done,
        final_step=True,
        task_number=5
    )


@router.callback_query(F.data == 'handle_task_6_cd')
@check_old_answer('handle_task_6_cd')
async def handle_task_6(callback: CallbackQuery):
    await callback.message.delete()
    video_link = video_dict['video_6']
    await handle_task(
        callback=callback,
        state=None,
        task_text=dict_task['video_task'],
        reply_markup=kb.back_to_task_6,
        parse_mode='HTML',
        video_link=video_link
    )


@router.callback_query(F.data == 'into_task_6_cd')
async def into_task_6(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await handle_task(
        callback=callback,
        state=state,
        task_text=dict_task['task_6_1'],
        reply_markup=kb.back_task_6,
        next_state=TaskState.waiting_for_task_6_1_answer,
        parse_mode='HTML',
        image_filename='image_6_1.jpg'
    )


@router.message(TaskState.waiting_for_task_6_1_answer)
async def handle_task_6_1_answer(message: Message, state: FSMContext):
    await handle_task_answer(
        message=message,
        state=state,
        correct_answers_key='correct_answer_6_1',
        next_task_text=dict_task['task_6_2'],
        parse_mode='HTML',
        reply_markup=kb.back_task_6,
        next_state=TaskState.waiting_for_task_6_2_answer,
        image_filename='image_6_2.jpg'
    )


@router.message(TaskState.waiting_for_task_6_2_answer)
async def handle_task_6_2_answer(message: Message, state: FSMContext):
    await handle_task_answer(
        message=message,
        state=state,
        correct_answers_key='correct_answer_6_2',
        next_task_text=dict_task['task_6_3'],
        parse_mode='HTML',
        reply_markup=kb.back_task_6,
        next_state=TaskState.waiting_for_task_6_3_answer,
        image_filename='image_6_3.jpg'
    )


@router.message(TaskState.waiting_for_task_6_3_answer)
async def handle_task_6_3_answer(message: Message, state: FSMContext):
    await handle_task_answer(
        message=message,
        state=state,
        correct_answers_key='correct_answer_6_3',
        next_task_text=dict_task['task_6_4'],
        parse_mode='HTML',
        reply_markup=kb.back_task_6,
        next_state=TaskState.waiting_for_task_6_4_answer,
        image_filename='image_6_4.jpg'
    )


@router.message(TaskState.waiting_for_task_6_4_answer)
async def handle_task_6_4_answer(message: Message, state: FSMContext):
    await handle_task_answer(
        message=message,
        state=state,
        correct_answers_key='correct_answer_6_4',
        next_task_text=dict_task['task_6_5'],
        parse_mode='HTML',
        reply_markup=kb.back_task_6,
        next_state=TaskState.waiting_for_task_6_5_answer,
        image_filename='image_6_5.jpg'
    )


@router.message(TaskState.waiting_for_task_6_5_answer)
async def handle_task_6_5_answer(message: Message, state: FSMContext):
    await handle_task_answer(
        message=message,
        state=state,
        correct_answers_key='correct_answer_6_5',
        next_task_text='',
        next_state=None,
        reply_markup=kb.task_6_done,
        final_step=True,
        task_number=6
    )


@router.callback_query(F.data == 'handle_task_8_cd')
@check_old_answer('handle_task_8_cd')
async def handle_task_8(callback: CallbackQuery):
    await callback.message.delete()
    await handle_task(
        callback=callback,
        state=None,
        task_text=dict_task['task_8'],
        reply_markup=kb.back_to_task_8,
        parse_mode='HTML'
    )


@router.callback_query(F.data == 'into_task_8_cd')
async def into_task_8(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await handle_task(
        callback=callback,
        state=state,
        task_text=dict_task['task_8_1'],
        reply_markup=kb.back_task_8,
        next_state=TaskState.waiting_for_task_8_1_answer,
        parse_mode='HTML',
        image_filename='image_8_1.jpg'
    )


@router.message(TaskState.waiting_for_task_8_1_answer)
async def handle_task_8_1_answer(message: Message, state: FSMContext):
    await handle_task_answer(
        message=message,
        state=state,
        correct_answers_key='correct_answer_8_1',
        next_task_text=dict_task['task_8_2'],
        parse_mode='HTML',
        reply_markup=kb.back_task_8,
        next_state=TaskState.waiting_for_task_8_2_answer,
        image_filename='image_8_2.jpg'
    )


@router.message(TaskState.waiting_for_task_8_2_answer)
async def handle_task_8_2_answer(message: Message, state: FSMContext):
    await handle_task_answer(
        message=message,
        state=state,
        correct_answers_key='correct_answer_8_2',
        next_task_text=dict_task['task_8_3'],
        parse_mode='HTML',
        reply_markup=kb.back_task_8,
        next_state=TaskState.waiting_for_task_8_3_answer,
        image_filename='image_8_3.jpg'
    )


@router.message(TaskState.waiting_for_task_8_3_answer)
async def handle_task_8_3_answer(message: Message, state: FSMContext):
    await handle_task_answer(
        message=message,
        state=state,
        correct_answers_key='correct_answer_8_3',
        next_task_text=dict_task['task_8_4'],
        parse_mode='HTML',
        reply_markup=kb.back_task_8,
        next_state=TaskState.waiting_for_task_8_4_answer,
        image_filename='image_8_4.jpg'
    )


@router.message(TaskState.waiting_for_task_8_4_answer)
async def handle_task_8_4_answer(message: Message, state: FSMContext):
    await handle_task_answer(
        message=message,
        state=state,
        correct_answers_key='correct_answer_8_4',
        next_task_text=dict_task['task_8_5'],
        parse_mode='HTML',
        reply_markup=kb.back_task_8,
        next_state=TaskState.waiting_for_task_8_5_answer,
        image_filename='image_8_5.jpg'
    )


@router.message(TaskState.waiting_for_task_8_5_answer)
async def handle_task_8_5_answer(message: Message, state: FSMContext):
    await handle_task_answer(
        message=message,
        state=state,
        correct_answers_key='correct_answer_8_5',
        next_task_text='',
        next_state=None,
        reply_markup=kb.task_8_done,
        final_step=True,
        task_number=8
    )


@router.callback_query(F.data == 'handle_task_9_cd')
async def handle_task_9(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    video_link = video_dict['video_9']
    await handle_task(
        callback=callback,
        state=None,
        task_text=dict_task['video_no_task'],
        reply_markup=kb.back_to_task_9,
        parse_mode='HTML',
        video_link=video_link
    )
    user_id = callback.from_user.id
    await update_completed_tasks(user_id, task_number=9)
    await state.clear()


@router.callback_query(F.data == 'handle_task_10_cd')
@check_old_answer('handle_task_10_cd')
async def handle_task_10(callback: CallbackQuery):
    await callback.message.delete()
    video_link = video_dict['video_10']
    await handle_task(
        callback=callback,
        state=None,
        task_text=dict_task['video_task'],
        reply_markup=kb.back_to_task_10,
        parse_mode='HTML',
        video_link=video_link
    )


@router.callback_query(F.data == 'into_task_10_cd')
async def into_task_10(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await handle_task(
        callback=callback,
        state=state,
        task_text=dict_task['task_10_1'],
        reply_markup=kb.back_task_10,
        next_state=TaskState.waiting_for_task_10_1_answer,
        parse_mode='HTML',
        image_filename='image_10_1.jpg'
    )


@router.message(TaskState.waiting_for_task_10_1_answer)
async def handle_task_10_1_answer(message: Message, state: FSMContext):
    await handle_task_answer(
        message=message,
        state=state,
        correct_answers_key='correct_answer_10_1',
        next_task_text=dict_task['task_10_2'],
        parse_mode='HTML',
        reply_markup=kb.back_task_10,
        next_state=TaskState.waiting_for_task_10_2_answer,
        image_filename='image_10_2.jpg'
    )


@router.message(TaskState.waiting_for_task_10_2_answer)
async def handle_task_10_2_answer(message: Message, state: FSMContext):
    await handle_task_answer(
        message=message,
        state=state,
        correct_answers_key='correct_answer_10_2',
        next_task_text=dict_task['task_10_3'],
        parse_mode='HTML',
        reply_markup=kb.back_task_10,
        next_state=TaskState.waiting_for_task_10_3_answer,
        image_filename='image_10_3.jpg'
    )


@router.message(TaskState.waiting_for_task_10_3_answer)
async def handle_task_10_3_answer(message: Message, state: FSMContext):
    await handle_task_answer(
        message=message,
        state=state,
        correct_answers_key='correct_answer_10_3',
        next_task_text=dict_task['task_10_4'],
        parse_mode='HTML',
        reply_markup=kb.back_task_10,
        next_state=TaskState.waiting_for_task_10_4_answer,
        image_filename='image_10_4.jpg'
    )


@router.message(TaskState.waiting_for_task_10_4_answer)
async def handle_task_10_4_answer(message: Message, state: FSMContext):
    await handle_task_answer(
        message=message,
        state=state,
        correct_answers_key='correct_answer_10_4',
        next_task_text=dict_task['task_10_5'],
        parse_mode='HTML',
        reply_markup=kb.back_task_10,
        next_state=TaskState.waiting_for_task_10_5_answer,
        image_filename='image_10_5.jpg'
    )


@router.message(TaskState.waiting_for_task_10_5_answer)
async def handle_task_10_5_answer(message: Message, state: FSMContext):
    await handle_task_answer(
        message=message,
        state=state,
        correct_answers_key='correct_answer_10_5',
        next_task_text='',
        next_state=None,
        reply_markup=kb.task_10_done,
        final_step=True,
        task_number=10
    )


@router.callback_query(F.data == 'handle_task_11_cd')
@check_old_answer('handle_task_11_cd')
async def handle_task_11(callback: CallbackQuery):
    await callback.message.delete()
    video_link = video_dict['video_11']
    await handle_task(
        callback=callback,
        state=None,
        task_text=dict_task['video_task'],
        reply_markup=kb.back_to_task_11,
        parse_mode='HTML',
        video_link=video_link
    )


@router.callback_query(F.data == 'into_task_11_cd')
async def into_task_11(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await handle_task(
        callback=callback,
        state=state,
        task_text=dict_task['task_11_1'],
        reply_markup=kb.back_task_11,
        next_state=TaskState.waiting_for_task_11_1_answer,
        parse_mode='HTML',
        image_filename='image_11_1.jpg'
    )


@router.message(TaskState.waiting_for_task_11_1_answer)
async def handle_task_11_1_answer(message: Message, state: FSMContext):
    await handle_task_answer(
        message=message,
        state=state,
        correct_answers_key='correct_answer_11_1',
        next_task_text=dict_task['task_11_2'],
        parse_mode='HTML',
        reply_markup=kb.back_task_11,
        next_state=TaskState.waiting_for_task_11_2_answer,
        image_filename='image_11_2.jpg'
    )


@router.message(TaskState.waiting_for_task_11_2_answer)
async def handle_task_11_2_answer(message: Message, state: FSMContext):
    await handle_task_answer(
        message=message,
        state=state,
        correct_answers_key='correct_answer_11_2',
        next_task_text=dict_task['task_11_3'],
        parse_mode='HTML',
        reply_markup=kb.back_task_11,
        next_state=TaskState.waiting_for_task_11_3_answer,
        image_filename='image_11_3.jpg'
    )


@router.message(TaskState.waiting_for_task_11_3_answer)
async def handle_task_11_3_answer(message: Message, state: FSMContext):
    await handle_task_answer(
        message=message,
        state=state,
        correct_answers_key='correct_answer_11_3',
        next_task_text=dict_task['task_11_4'],
        parse_mode='HTML',
        reply_markup=kb.back_task_11,
        next_state=TaskState.waiting_for_task_11_4_answer,
        image_filename='image_11_4.jpg'
    )


@router.message(TaskState.waiting_for_task_11_4_answer)
async def handle_task_11_4_answer(message: Message, state: FSMContext):
    await handle_task_answer(
        message=message,
        state=state,
        correct_answers_key='correct_answer_11_4',
        next_task_text=dict_task['task_11_5'],
        parse_mode='HTML',
        reply_markup=kb.back_task_11,
        next_state=TaskState.waiting_for_task_11_5_answer,
        image_filename='image_11_5.jpg'
    )


@router.message(TaskState.waiting_for_task_11_5_answer)
async def handle_task_11_5_answer(message: Message, state: FSMContext):
    await handle_task_answer(
        message=message,
        state=state,
        correct_answers_key='correct_answer_11_5',
        next_task_text='',
        next_state=None,
        reply_markup=kb.task_11_done,
        final_step=True,
        task_number=11
    )


@router.callback_query(F.data == 'handle_task_15_cd')
@check_old_answer('handle_task_15_cd')
async def handle_task_15(callback: CallbackQuery):
    await callback.message.delete()
    await handle_task(
        callback=callback,
        state=None,
        task_text=dict_task['task_15'],
        reply_markup=kb.back_to_task_15,
        parse_mode='HTML'
    )


@router.callback_query(F.data == 'into_task_15_cd')
async def into_task_15(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await handle_task(
        callback=callback,
        state=state,
        task_text=dict_task['task_15_1'],
        reply_markup=kb.back_task_15,
        next_state=TaskState.waiting_for_task_15_1_answer,
        parse_mode='HTML'
    )


@router.message(TaskState.waiting_for_task_15_1_answer)
async def handle_task_15_1_answer(message: Message, state: FSMContext):
    await handle_task_answer(
        message=message,
        state=state,
        correct_answers_key='correct_answer_15_1',
        next_task_text=dict_task['task_15_2'],
        parse_mode='HTML',
        reply_markup=kb.back_task_15,
        next_state=TaskState.waiting_for_task_15_2_answer
    )


@router.message(TaskState.waiting_for_task_15_2_answer)
async def handle_task_15_2_answer(message: Message, state: FSMContext):
    await handle_task_answer(
        message=message,
        state=state,
        correct_answers_key='correct_answer_15_2',
        next_task_text=dict_task['task_15_3'],
        parse_mode='HTML',
        reply_markup=kb.back_task_15,
        next_state=TaskState.waiting_for_task_15_3_answer
    )


@router.message(TaskState.waiting_for_task_15_3_answer)
async def handle_task_15_3_answer(message: Message, state: FSMContext):
    await handle_task_answer(
        message=message,
        state=state,
        correct_answers_key='correct_answer_15_3',
        next_task_text=dict_task['task_15_4'],
        parse_mode='HTML',
        reply_markup=kb.back_task_15,
        next_state=TaskState.waiting_for_task_15_4_answer
    )


@router.message(TaskState.waiting_for_task_15_4_answer)
async def handle_task_15_4_answer(message: Message, state: FSMContext):
    await handle_task_answer(
        message=message,
        state=state,
        correct_answers_key='correct_answer_15_4',
        next_task_text=dict_task['task_15_5'],
        parse_mode='HTML',
        reply_markup=kb.back_task_15,
        next_state=TaskState.waiting_for_task_15_5_answer
    )


@router.message(TaskState.waiting_for_task_15_5_answer)
async def handle_task_15_5_answer(message: Message, state: FSMContext):
    await handle_task_answer(
        message=message,
        state=state,
        correct_answers_key='correct_answer_15_5',
        next_task_text='',
        next_state=None,
        reply_markup=kb.task_15_done,
        final_step=True,
        task_number=15
    )


@router.callback_query(F.data == 'handle_task_19_cd')
@check_old_answer('handle_task_19_cd')
async def handle_task_19(callback: CallbackQuery):
    await callback.message.delete()
    await handle_task(
        callback=callback,
        state=None,
        task_text=dict_task['task_19'],
        reply_markup=kb.back_to_task_19,
        parse_mode='HTML'
    )


@router.callback_query(F.data == 'into_task_19_cd')
async def into_task_19(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await handle_task(
        callback=callback,
        state=state,
        task_text=dict_task['task_19_1'],
        reply_markup=kb.back_task_19,
        next_state=TaskState.waiting_for_task_19_1_answer,
        parse_mode='HTML'
    )


@router.message(TaskState.waiting_for_task_19_1_answer)
async def handle_task_19_1_answer(message: Message, state: FSMContext):
    await handle_task_answer(
        message=message,
        state=state,
        correct_answers_key='correct_answer_19_1',
        next_task_text=dict_task['task_19_2'],
        parse_mode='HTML',
        reply_markup=kb.back_task_19,
        next_state=TaskState.waiting_for_task_19_2_answer
    )


@router.message(TaskState.waiting_for_task_19_2_answer)
async def handle_task_19_2_answer(message: Message, state: FSMContext):
    await handle_task_answer(
        message=message,
        state=state,
        correct_answers_key='correct_answer_19_2',
        next_task_text=dict_task['task_19_3'],
        parse_mode='HTML',
        reply_markup=kb.back_task_19,
        next_state=TaskState.waiting_for_task_19_3_answer
    )


@router.message(TaskState.waiting_for_task_19_3_answer)
async def handle_task_19_3_answer(message: Message, state: FSMContext):
    await handle_task_answer(
        message=message,
        state=state,
        correct_answers_key='correct_answer_19_3',
        next_task_text=dict_task['task_19_4'],
        parse_mode='HTML',
        reply_markup=kb.back_task_19,
        next_state=TaskState.waiting_for_task_19_4_answer
    )


@router.message(TaskState.waiting_for_task_19_4_answer)
async def handle_task_19_4_answer(message: Message, state: FSMContext):
    await handle_task_answer(
        message=message,
        state=state,
        correct_answers_key='correct_answer_19_4',
        next_task_text=dict_task['task_19_5'],
        parse_mode='HTML',
        reply_markup=kb.back_task_19,
        next_state=TaskState.waiting_for_task_19_5_answer
    )


@router.message(TaskState.waiting_for_task_19_5_answer)
async def handle_task_19_5_answer(message: Message, state: FSMContext):
    await handle_task_answer(
        message=message,
        state=state,
        correct_answers_key='correct_answer_19_5',
        next_task_text='',
        next_state=None,
        reply_markup=kb.task_19_done,
        final_step=True,
        task_number=19
    )


@router.callback_query(F.data == 'handle_task_22_cd')
@check_old_answer('handle_task_22_cd')
async def handle_task_22(callback: CallbackQuery):
    await callback.message.delete()
    await handle_task(
        callback=callback,
        state=None,
        task_text=dict_task['task_22'],
        reply_markup=kb.back_to_task_22,
        parse_mode='HTML'
    )


@router.callback_query(F.data == 'into_task_22_cd')
async def into_task_22(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await handle_task(
        callback=callback,
        state=state,
        task_text=dict_task['task_22_1'],
        reply_markup=kb.back_task_22,
        next_state=TaskState.waiting_for_task_22_1_answer,
        parse_mode='HTML',
        image_filename='image_22_1.jpg'
    )


@router.message(TaskState.waiting_for_task_22_1_answer)
async def handle_task_22_1_answer(message: Message, state: FSMContext):
    await handle_task_answer(
        message=message,
        state=state,
        correct_answers_key='correct_answer_22_1',
        next_task_text=dict_task['task_22_2'],
        parse_mode='HTML',
        reply_markup=kb.back_task_22,
        next_state=TaskState.waiting_for_task_22_2_answer,
        image_filename='image_22_2.jpg'
    )


@router.message(TaskState.waiting_for_task_22_2_answer)
async def handle_task_22_2_answer(message: Message, state: FSMContext):
    await handle_task_answer(
        message=message,
        state=state,
        correct_answers_key='correct_answer_22_2',
        next_task_text=dict_task['task_22_3'],
        parse_mode='HTML',
        reply_markup=kb.back_task_22,
        next_state=TaskState.waiting_for_task_22_3_answer,
        image_filename='image_22_3.jpg'
    )


@router.message(TaskState.waiting_for_task_22_3_answer)
async def handle_task_22_3_answer(message: Message, state: FSMContext):
    await handle_task_answer(
        message=message,
        state=state,
        correct_answers_key='correct_answer_22_3',
        next_task_text=dict_task['task_22_4'],
        parse_mode='HTML',
        reply_markup=kb.back_task_22,
        next_state=TaskState.waiting_for_task_22_4_answer,
        image_filename='image_22_4.jpg'
    )


@router.message(TaskState.waiting_for_task_22_4_answer)
async def handle_task_22_4_answer(message: Message, state: FSMContext):
    await handle_task_answer(
        message=message,
        state=state,
        correct_answers_key='correct_answer_22_4',
        next_task_text=dict_task['task_22_5'],
        parse_mode='HTML',
        reply_markup=kb.back_task_22,
        next_state=TaskState.waiting_for_task_22_5_answer,
        image_filename='image_22_5.jpg'
    )


@router.message(TaskState.waiting_for_task_22_5_answer)
async def handle_task_22_5_answer(message: Message, state: FSMContext):
    await handle_task_answer(
        message=message,
        state=state,
        correct_answers_key='correct_answer_22_5',
        next_task_text='',
        next_state=None,
        reply_markup=kb.task_22_done,
        final_step=True,
        task_number=22
    )


@router.callback_query(F.data == 'handle_task_24_cd')
@check_old_answer('handle_task_24_cd')
async def handle_task_24(callback: CallbackQuery):
    await callback.message.delete()
    await handle_task(
        callback=callback,
        state=None,
        task_text=dict_task['task_24'],
        reply_markup=kb.back_to_task_24,
        parse_mode='HTML'
    )


@router.callback_query(F.data == 'into_task_24_cd')
async def into_task_24(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await handle_task(
        callback=callback,
        state=state,
        task_text=dict_task['task_24_1'],
        reply_markup=kb.back_task_24,
        next_state=TaskState.waiting_for_task_24_1_answer,
        parse_mode='HTML'
    )


@router.message(TaskState.waiting_for_task_24_1_answer)
async def handle_task_24_1_answer(message: Message, state: FSMContext):
    await handle_task_answer(
        message=message,
        state=state,
        correct_answers_key='correct_answer_24_1',
        next_task_text=dict_task['task_24_2'],
        parse_mode='HTML',
        reply_markup=kb.back_task_24,
        next_state=TaskState.waiting_for_task_24_2_answer
    )


@router.message(TaskState.waiting_for_task_24_2_answer)
async def handle_task_24_2_answer(message: Message, state: FSMContext):
    await handle_task_answer(
        message=message,
        state=state,
        correct_answers_key='correct_answer_24_2',
        next_task_text=dict_task['task_24_3'],
        parse_mode='HTML',
        reply_markup=kb.back_task_24,
        next_state=TaskState.waiting_for_task_24_3_answer
    )


@router.message(TaskState.waiting_for_task_24_3_answer)
async def handle_task_24_3_answer(message: Message, state: FSMContext):
    await handle_task_answer(
        message=message,
        state=state,
        correct_answers_key='correct_answer_24_3',
        next_task_text=dict_task['task_24_4'],
        parse_mode='HTML',
        reply_markup=kb.back_task_24,
        next_state=TaskState.waiting_for_task_24_4_answer
    )


@router.message(TaskState.waiting_for_task_24_4_answer)
async def handle_task_24_4_answer(message: Message, state: FSMContext):
    await handle_task_answer(
        message=message,
        state=state,
        correct_answers_key='correct_answer_24_4',
        next_task_text=dict_task['task_24_5'],
        parse_mode='HTML',
        reply_markup=kb.back_task_24,
        next_state=TaskState.waiting_for_task_24_5_answer
    )


@router.message(TaskState.waiting_for_task_24_5_answer)
async def handle_task_24_5_answer(message: Message, state: FSMContext):
    await handle_task_answer(
        message=message,
        state=state,
        correct_answers_key='correct_answer_24_5',
        next_task_text='',
        next_state=None,
        reply_markup=kb.task_24_done,
        final_step=True,
        task_number=24
    )


@router.callback_query(F.data == 'handle_task_25_cd')
@check_old_answer('handle_task_25_cd')
async def handle_task_25(callback: CallbackQuery):
    await callback.message.delete()
    video_link = video_dict['video_25']
    await handle_task(
        callback=callback,
        state=None,
        task_text=dict_task['video_task'],
        reply_markup=kb.back_to_task_25,
        parse_mode='HTML',
        video_link=video_link
    )


@router.callback_query(F.data == 'into_task_25_cd')
async def into_task_25(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await handle_task(
        callback=callback,
        state=state,
        task_text=dict_task['task_25_1'],
        reply_markup=kb.back_task_25,
        next_state=TaskState.waiting_for_task_25_1_answer,
        parse_mode='HTML'
    )


@router.message(TaskState.waiting_for_task_25_1_answer)
async def handle_task_25_1_answer(message: Message, state: FSMContext):
    await handle_task_answer(
        message=message,
        state=state,
        correct_answers_key='correct_answer_25_1',
        next_task_text=dict_task['task_25_2'],
        parse_mode='HTML',
        reply_markup=kb.back_task_25,
        next_state=TaskState.waiting_for_task_25_2_answer
    )


@router.message(TaskState.waiting_for_task_25_2_answer)
async def handle_task_25_2_answer(message: Message, state: FSMContext):
    await handle_task_answer(
        message=message,
        state=state,
        correct_answers_key='correct_answer_25_2',
        next_task_text=dict_task['task_25_3'],
        parse_mode='HTML',
        reply_markup=kb.back_task_25,
        next_state=TaskState.waiting_for_task_25_3_answer
    )


@router.message(TaskState.waiting_for_task_25_3_answer)
async def handle_task_25_3_answer(message: Message, state: FSMContext):
    await handle_task_answer(
        message=message,
        state=state,
        correct_answers_key='correct_answer_25_3',
        next_task_text=dict_task['task_25_4'],
        parse_mode='HTML',
        reply_markup=kb.back_task_25,
        next_state=TaskState.waiting_for_task_25_4_answer
    )


@router.message(TaskState.waiting_for_task_25_4_answer)
async def handle_task_25_4_answer(message: Message, state: FSMContext):
    await handle_task_answer(
        message=message,
        state=state,
        correct_answers_key='correct_answer_25_4',
        next_task_text=dict_task['task_25_5'],
        parse_mode='HTML',
        reply_markup=kb.back_task_25,
        next_state=TaskState.waiting_for_task_25_5_answer
    )


@router.message(TaskState.waiting_for_task_25_5_answer)
async def handle_task_25_5_answer(message: Message, state: FSMContext):
    await handle_task_answer(
        message=message,
        state=state,
        correct_answers_key='correct_answer_25_5',
        next_task_text='',
        next_state=None,
        reply_markup=kb.task_25_done,
        final_step=True,
        task_number=25
    )


@router.callback_query(F.data == 'handle_task_26_cd')
@check_old_answer('handle_task_26_cd')
async def handle_task_26(callback: CallbackQuery):
    await callback.message.delete()
    video_link = video_dict['video_26']
    await handle_task(
        callback=callback,
        state=None,
        task_text=dict_task['video_task'],
        reply_markup=kb.back_to_task_26,
        parse_mode='HTML',
        video_link=video_link
    )


@router.callback_query(F.data == 'into_task_26_cd')
async def into_task_26(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await handle_task(
        callback=callback,
        state=state,
        task_text=dict_task['task_26_1'],
        reply_markup=kb.back_task_26,
        next_state=TaskState.waiting_for_task_26_1_answer,
        parse_mode='HTML'
    )


@router.message(TaskState.waiting_for_task_26_1_answer)
async def handle_task_26_1_answer(message: Message, state: FSMContext):
    await handle_task_answer(
        message=message,
        state=state,
        correct_answers_key='correct_answer_26_1',
        next_task_text=dict_task['task_26_2'],
        parse_mode='HTML',
        reply_markup=kb.back_task_26,
        next_state=TaskState.waiting_for_task_26_2_answer
    )


@router.message(TaskState.waiting_for_task_26_2_answer)
async def handle_task_26_2_answer(message: Message, state: FSMContext):
    await handle_task_answer(
        message=message,
        state=state,
        correct_answers_key='correct_answer_26_2',
        next_task_text=dict_task['task_26_3'],
        parse_mode='HTML',
        reply_markup=kb.back_task_26,
        next_state=TaskState.waiting_for_task_26_3_answer
    )


@router.message(TaskState.waiting_for_task_26_3_answer)
async def handle_task_26_3_answer(message: Message, state: FSMContext):
    await handle_task_answer(
        message=message,
        state=state,
        correct_answers_key='correct_answer_26_3',
        next_task_text=dict_task['task_26_4'],
        parse_mode='HTML',
        reply_markup=kb.back_task_26,
        next_state=TaskState.waiting_for_task_26_4_answer
    )


@router.message(TaskState.waiting_for_task_26_4_answer)
async def handle_task_26_4_answer(message: Message, state: FSMContext):
    await handle_task_answer(
        message=message,
        state=state,
        correct_answers_key='correct_answer_26_4',
        next_task_text=dict_task['task_26_5'],
        parse_mode='HTML',
        reply_markup=kb.back_task_26,
        next_state=TaskState.waiting_for_task_26_5_answer
    )


@router.message(TaskState.waiting_for_task_26_5_answer)
async def handle_task_26_5_answer(message: Message, state: FSMContext):
    await handle_task_answer(
        message=message,
        state=state,
        correct_answers_key='correct_answer_26_5',
        next_task_text='',
        next_state=None,
        reply_markup=kb.task_26_done,
        final_step=True,
        task_number=26
    )
