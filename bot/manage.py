from functools import wraps
from aiogram import Dispatcher, F
from aiogram.types import Message, CallbackQuery

import kb
from dict import TEXT_DICT as dict

dp = Dispatcher()


def check_old_answer(text):
    def decorator(func):
        @wraps(func)
        async def wrapper(callback: CallbackQuery):
            if callback.message.text != text:
                await func(callback)
            await callback.answer()
        return wrapper
    return decorator


@dp.message(F.text == '/start')
async def cmd_start(message: Message):
    await message.answer(
        dict['greet'].format(name=message.from_user.first_name),
        reply_markup=kb.main_menu
        )


@dp.callback_query(F.text == 'button1')
@check_old_answer('button1')
async def cmd_button1(callback: CallbackQuery):
    await callback.message.edit_text('Вы нажали кнопку 1')
    await callback.answer()


def register_handlers(dp: Dispatcher):
    dp.message.register(
        cmd_start
    )
    dp.callback_query.register(
        cmd_button1
    )
