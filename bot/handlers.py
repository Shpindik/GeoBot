import re
from functools import wraps
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

import kb
from database import save_user_data, update_completed_tasks
from dict import TEXT_DICT as dict
from dict import CORRECT_ANSWERS as correct_answers


NAME_REGEX = re.compile(r'^[А-Яа-яЁёA-Za-z]+ [А-Яа-яЁёA-Za-z]+$')


router = Router()


class UserState(StatesGroup):
    waiting_for_name = State()


class TaskState(StatesGroup):
    waiting_for_task_2_1_answer = State()
    waiting_for_task_2_2_answer = State()
    waiting_for_task_2_3_answer = State()
    waiting_for_task_2_4_answer = State()
    waiting_for_task_2_5_answer = State()


def check_old_answer(text):
    def decorator(func):
        @wraps(func)
        async def wrapper(callback: CallbackQuery):
            if callback.message.text != text:
                await func(callback)
            await callback.answer()
        return wrapper
    return decorator


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
            print(f"Ошибка при удалении сообщения: {e}")

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

    for msg_id in data.get("messages_to_delete", []):
        try:
            await callback.message.bot.delete_message(
                chat_id=callback.message.chat.id,
                message_id=msg_id
            )
        except Exception as e:
            print(f"Ошибка при удалении сообщения: {e}")

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


@router.callback_query(F.data == 'handle_task_2_cd')
@check_old_answer('handle_task_2')
async def handle_task_2(callback: CallbackQuery):
    video_link = 'https://rutube.ru/video/f8cdfddf0fa59963d92fde841bfde0fb/'
    await callback.message.edit_text(
        text=f'{dict['video_task_2']}\n{video_link}',
        reply_markup=kb.back_to_task
    )


@router.callback_query(F.data == 'into_task_2_cd')
async def into_task_2(callback: CallbackQuery, state: FSMContext):
    await state.set_state(TaskState.waiting_for_task_2_1_answer)

    await state.update_data(last_message_id=callback.message.message_id)

    await callback.message.edit_text(
        text=dict['task_2_1'],
        reply_markup=kb.back_task_2
    )


@router.message(TaskState.waiting_for_task_2_1_answer)
async def handle_task_2_1_answer(message: Message, state: FSMContext):
    data = await state.get_data()
    last_message_id = data.get('last_message_id')
    error_messages = data.get('error_messages', [])

    user_answer = message.text.strip().lower()
    correct_words_2_1 = [
        answer.lower() for answer in correct_answers['correct_answer_2_1']
        ]

    if user_answer in correct_words_2_1:
        for msg_id in error_messages:
            try:
                await message.bot.delete_message(
                    chat_id=message.chat.id,
                    message_id=msg_id
                )
            except Exception as e:
                print(f"Ошибка удаления сообщения {msg_id}: {e}")

        await message.delete()

        await message.bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=last_message_id,
            text=f'{dict['correct_msg']}\n{dict['task_2_2']}',
            reply_markup=kb.back_task_2
        )
        await state.set_state(TaskState.waiting_for_task_2_2_answer)
        await state.update_data(last_message_id=last_message_id,
                                error_messages=[])
    else:
        await message.delete()
        error_msg = await message.answer(
            dict['error_msg']
        )
        error_messages.append(error_msg.message_id)
        await state.update_data(error_messages=error_messages)


@router.message(TaskState.waiting_for_task_2_2_answer)
async def handle_task_2_2_answer(message: Message, state: FSMContext):
    data = await state.get_data()
    last_message_id = data.get('last_message_id')
    error_messages = data.get('error_messages', [])

    user_answer = message.text.strip().lower()
    correct_words_2_2 = [
        answer.lower() for answer in correct_answers['correct_answer_2_2']
        ]

    if user_answer in correct_words_2_2:
        for msg_id in error_messages:
            try:
                await message.bot.delete_message(
                    chat_id=message.chat.id,
                    message_id=msg_id
                )
            except Exception as e:
                print(f"Ошибка удаления сообщения {msg_id}: {e}")

        await message.delete()

        await message.bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=last_message_id,
            text=f'{dict['correct_msg']}\n{dict['task_2_3']}',
            reply_markup=kb.back_task_2
        )
        await state.set_state(TaskState.waiting_for_task_2_3_answer)
        await state.update_data(last_message_id=last_message_id,
                                error_messages=[])
    else:
        await message.delete()
        error_msg = await message.answer(
            dict['error_msg']
        )
        error_messages.append(error_msg.message_id)
        await state.update_data(error_messages=error_messages)


@router.message(TaskState.waiting_for_task_2_3_answer)
async def handle_task_2_3_answer(message: Message, state: FSMContext):
    data = await state.get_data()
    last_message_id = data.get('last_message_id')
    error_messages = data.get('error_messages', [])

    user_answer = message.text.strip().lower()
    correct_words_2_3 = [
        answer.lower() for answer in correct_answers['correct_answer_2_3']
        ]

    if user_answer in correct_words_2_3:
        for msg_id in error_messages:
            try:
                await message.bot.delete_message(
                    chat_id=message.chat.id,
                    message_id=msg_id
                )
            except Exception as e:
                print(f"Ошибка удаления сообщения {msg_id}: {e}")

        await message.delete()

        await message.bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=last_message_id,
            text=f'{dict['correct_msg']}\n{dict['task_2_4']}',
            reply_markup=kb.back_task_2
        )
        await state.set_state(TaskState.waiting_for_task_2_4_answer)
        await state.update_data(last_message_id=last_message_id,
                                error_messages=[])
    else:
        await message.delete()
        error_msg = await message.answer(
            dict['error_msg']
        )
        error_messages.append(error_msg.message_id)
        await state.update_data(error_messages=error_messages)


@router.message(TaskState.waiting_for_task_2_4_answer)
async def handle_task_2_4_answer(message: Message, state: FSMContext):
    data = await state.get_data()
    last_message_id = data.get('last_message_id')
    error_messages = data.get('error_messages', [])

    user_answer = message.text.strip().lower()
    correct_words_2_4 = [
        answer.lower() for answer in correct_answers['correct_answer_2_4']
        ]

    if user_answer in correct_words_2_4:
        for msg_id in error_messages:
            try:
                await message.bot.delete_message(
                    chat_id=message.chat.id,
                    message_id=msg_id
                )
            except Exception as e:
                print(f"Ошибка удаления сообщения {msg_id}: {e}")

        await message.delete()

        await message.bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=last_message_id,
            text=f'{dict['correct_msg']}\n{dict['task_2_5']}',
            reply_markup=kb.back_task_2
        )
        await state.set_state(TaskState.waiting_for_task_2_5_answer)
        await state.update_data(last_message_id=last_message_id,
                                error_messages=[])
    else:
        await message.delete()
        error_msg = await message.answer(
            dict['error_msg']
        )
        error_messages.append(error_msg.message_id)
        await state.update_data(error_messages=error_messages)


@router.message(TaskState.waiting_for_task_2_5_answer)
async def handle_task_2_5_answer(message: Message, state: FSMContext):
    data = await state.get_data()
    last_message_id = data.get('last_message_id')
    error_messages = data.get('error_messages', [])

    user_answer = message.text.strip().lower()
    correct_words_2_5 = [
        answer.lower() for answer in correct_answers['correct_answer_2_5']
        ]

    if user_answer in correct_words_2_5:
        for msg_id in error_messages:
            try:
                await message.bot.delete_message(
                    chat_id=message.chat.id,
                    message_id=msg_id
                )
            except Exception as e:
                print(f"Ошибка удаления сообщения {msg_id}: {e}")

        await message.delete()

        await message.bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=last_message_id,
            text=dict['correct_msg'],
            reply_markup=kb.task_2_done
        )
        user_id = message.from_user.id
        await update_completed_tasks(user_id, 2)

        await state.clear()
    else:
        await message.delete()
        error_msg = await message.answer(
            dict['error_msg']
        )
        error_messages.append(error_msg.message_id)
        await state.update_data(error_messages=error_messages)
