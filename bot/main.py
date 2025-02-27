import asyncio
import logging
import os
import signal
import sys

from aiogram import Bot, Dispatcher
from database import setup_database
from dotenv import load_dotenv
from handlers import router

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TOKEN')


def check_tokens():
    """ Check if all required environment variables are set """
    missing_tokens = [
        name for name, value in {
            'TOKEN': TELEGRAM_TOKEN,
        }.items() if not value
    ]
    if missing_tokens:
        logging.critical(f'Отсутствуют обязательные переменные окружения: \
                         {", ".join(missing_tokens)}')
    return not missing_tokens


bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()
dp.include_router(router)


async def main():
    print('Бот запущен. Для остановки нажмите Ctrl+C.')

    setup_database()
    await bot.delete_webhook(drop_pending_updates=True)
    polling_task = asyncio.create_task(
        dp.start_polling(
            bot,
            allowed_updates=dp.resolve_used_update_types()
        )
    )

    def shutdown():
        polling_task.cancel()

    for sig in (signal.SIGINT, signal.SIGTERM):
        asyncio.get_event_loop().add_signal_handler(sig, shutdown)

    try:
        await polling_task
    except asyncio.CancelledError:
        pass

if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[logging.StreamHandler(sys.stdout)]
    )
    asyncio.run(main())
