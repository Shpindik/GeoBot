from aiogram import Router
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from typing import Optional

from database import update_completed_tasks
from dict import TEXT_DICT as dict
from dict import CORRECT_ANSWERS as correct_answers
from states import TaskState


router = Router()


async def handle_task(
    callback: CallbackQuery,
    state: FSMContext,
    task_text: str,
    reply_markup: str = None,
    next_state: Optional[TaskState] = None,
    parse_mode: Optional[str] = None,
    video_link: Optional[str] = None
):
    """
    Универсальная функция для обработки заданий.

    :param callback: CallbackQuery от пользователя.
    :param state: FSMContext для управления состоянием.
    :param task_text: Текст задания.
    :param reply_markup: Клавиатура для задания.
    :param next_state: Следующее состояние (если есть).
    :param parse_mode: Режим разметки (например, 'HTML').
    :param video_link: Ссылка на видео (если есть).
    """
    if next_state:
        await state.set_state(next_state)
        await state.update_data(last_message_id=callback.message.message_id)

    text = task_text
    if video_link:
        text = f"{task_text}\n{video_link}"

    await callback.message.edit_text(
        text=text,
        reply_markup=reply_markup,
        parse_mode=parse_mode
    )


async def handle_task_answer(
    message: Message,
    state: FSMContext,
    correct_answers_key: str,
    next_task_text: str,
    next_state: TaskState,
    reply_markup: str,
    parse_mode: str = None,
    final_step: bool = False,
    task_number: int = None
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
                print(f"Ошибка удаления сообщения {msg_id}: {e}")

        await message.delete()
        if last_message_id:
            try:
                await message.bot.edit_message_text(
                    chat_id=message.chat.id,
                    message_id=last_message_id,
                    text=f"{dict['correct_msg']}\n{next_task_text}",
                    parse_mode=parse_mode,
                    reply_markup=reply_markup
                )
            except Exception as e:
                print(f"Ошибка редактирования сообщения \
                      {last_message_id}: {e}")

        if final_step:
            user_id = message.from_user.id
            await update_completed_tasks(user_id, task_number)
            await state.clear()
        else:
            await state.set_state(next_state)
            await state.update_data(
                last_message_id=last_message_id,
                error_messages=[]
            )

    else:
        await message.delete()
        error_msg = await message.answer(dict['error_msg'])
        error_messages.append(error_msg.message_id)
        await state.update_data(error_messages=error_messages)
