import asyncio
import logging
import sys

from handlers import dp
from init import set_main_menu, bot, DEBUG, log_error
from db.base import init_models


async def main() -> None:
    await init_models()
    await set_main_menu()
    await dp.start_polling(bot)


if __name__ == "__main__":
    if DEBUG:
        logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    else:
        log_error('start bot', with_traceback=False)
    asyncio.run(main())
