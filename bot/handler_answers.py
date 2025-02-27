import os
from typing import Optional

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, FSInputFile, Message
from database import update_completed_tasks
from dict import CORRECT_ANSWERS as correct_answers
from dict import TEXT_DICT as dict
from states import TaskState

router = Router()


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEDIA_DIR = os.path.join(BASE_DIR, 'media')


async def handle_task(
    callback: CallbackQuery,
    state: FSMContext | None,
    task_text: str,
    reply_markup: Optional[str] = None,
    next_state: Optional[TaskState] = None,
    parse_mode: Optional[str] = None,
    image_filename: Optional[str] = None,
    video_link: Optional[str] = None
):
    """
    Universal function for handling tasks.

    :param callback: CallbackQuery from user.
    :param state: FSMContext for control state.
    :param task_text: Text for task.
    :param reply_markup: Keyboard for task.
    :param next_state: Next state(if exist).
    :param parse_mode: Parse mode(if exist).
    :param video_link: Video link(if exist).
    :param image_filename: Image(if exist)
    """

    data = await state.get_data() if state else {}
    last_message_id = data.get('last_message_id')

    if last_message_id:
        try:
            await callback.bot.delete_message(
                chat_id=callback.message.chat.id,
                message_id=last_message_id
            )
        except Exception as e:
            print(f'Ошибка удаления сообщения: {e}')

    final_text = task_text
    if video_link:
        final_text += f'\n\n📹 Видео: {video_link}'

    try:
        if image_filename:
            media_path = os.path.join(MEDIA_DIR, image_filename)
            if os.path.exists(media_path):
                photo = FSInputFile(media_path)
                new_message = await callback.message.answer_photo(
                    photo=photo,
                    caption=final_text,
                    reply_markup=reply_markup,
                    parse_mode=parse_mode
                )
            else:
                new_message = await callback.message.answer(
                    text=f'❌ Ошибка: Файл {image_filename} не найден.\
                        \n{task_text}',
                    reply_markup=reply_markup,
                    parse_mode=parse_mode
                )
        else:
            new_message = await callback.message.answer(
                text=final_text,
                reply_markup=reply_markup,
                parse_mode=parse_mode
            )

        if next_state:
            await state.set_state(next_state)

        await state.update_data(last_message_id=new_message.message_id)

    except Exception as e:
        print(f'Ошибка отправки сообщения: {e}')


async def handle_task_answer(
    message: Message,
    state: FSMContext,
    correct_answers_key: str,
    next_task_text: str,
    next_state: TaskState,
    reply_markup: str = None,
    parse_mode: Optional[str] = None,
    image_filename: Optional[str] = None,
    final_step: bool = False,
    task_number: Optional[int] = None
):
    data = await state.get_data()
    last_message_id = data.get('last_message_id')
    error_messages = data.get('error_messages', [])

    user_answer = message.text.strip().lower()
    correct_words = [
        answer.lower() for answer in correct_answers[correct_answers_key]
    ]

    if user_answer in correct_words:
        for msg_id in error_messages:
            try:
                await message.bot.delete_message(
                    chat_id=message.chat.id,
                    message_id=msg_id
                )
            except Exception as e:
                print(f'Ошибка удаления сообщения {msg_id}: {e}')

        await message.delete()

        if last_message_id:
            try:
                await message.bot.delete_message(
                    chat_id=message.chat.id,
                    message_id=last_message_id
                )
            except Exception as e:
                print(f'Ошибка удаления сообщения задания: {e}')

        try:
            if image_filename:
                media_path = os.path.join(MEDIA_DIR, image_filename)
                if os.path.exists(media_path):
                    photo = FSInputFile(media_path)
                    new_message = await message.answer_photo(
                        photo=photo,
                        caption=f"{dict['correct_msg']}\n{next_task_text}",
                        reply_markup=reply_markup,
                        parse_mode=parse_mode
                    )
                else:
                    new_message = await message.answer(
                        text=f'❌ Ошибка: Файл {image_filename} не найден.\
                            \n{dict['correct_msg']}\n{next_task_text}',
                        reply_markup=reply_markup,
                        parse_mode=parse_mode
                    )
            else:
                new_message = await message.answer(
                    text=f'{dict['correct_msg']}\n{next_task_text}',
                    reply_markup=reply_markup,
                    parse_mode=parse_mode
                )

            if final_step:
                user_id = message.from_user.id
                await update_completed_tasks(user_id, task_number)
                await state.clear()
            else:
                await state.set_state(next_state)
                await state.update_data(
                    last_message_id=new_message.message_id,
                    error_messages=[]
                )

        except Exception as e:
            print(f'Ошибка отправки нового сообщения: {e}')

    else:
        await message.delete()
        error_msg = await message.answer(dict['error_msg'])
        error_messages.append(error_msg.message_id)
        await state.update_data(error_messages=error_messages)
