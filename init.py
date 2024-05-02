from aiogram import Dispatcher
from aiogram.types.bot_command import BotCommand
from aiogram import Bot
from aiogram.enums import ParseMode

from dotenv import load_dotenv
from os import getenv
from pytz import timezone
# from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime

import logging
import traceback
import redis
import os

from sqlalchemy.ext.asyncio import create_async_engine

import asyncio
try:
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except:
    pass

load_dotenv ()
loop = asyncio.get_event_loop()
dp = Dispatcher()
bot = Bot(getenv("TOKEN"), parse_mode=ParseMode.HTML)

TZ = timezone('Europe/Moscow')

# scheduler = AsyncIOScheduler(timezone=TZ)

DEBUG = bool(getenv('DEBUG'))

ENGINE = create_async_engine(url=getenv('DB_URL'))

REDIS_CLIENT = redis.Redis(host=getenv('REDIS_HOST'), port=getenv('REDIS_PORT'), db=0)

DATE_FORMAT = getenv('DATE_FORMAT')
TIME_FORMAT = getenv('TIME_FORMAT')


async def set_main_menu():
    main_menu_commands = [
        BotCommand(command='/start',
                   description='Перезапустить')
    ]

    await bot.set_my_commands(main_menu_commands)


def log_error(message, with_traceback: bool = True):
    now = datetime.now(TZ)
    log_folder = now.strftime ('%m-%Y')
    log_path = os.path.join('logs', log_folder)

    if not os.path.exists(log_path):
        os.makedirs(log_path)

    log_file_path = os.path.join(log_path, f'{now.day}.log')
    logging.basicConfig (level=logging.WARNING, filename=log_file_path, encoding='utf-8')
    if with_traceback:
        ex_traceback = traceback.format_exc()
        logging.warning(f'{now}\n{ex_traceback}\n{message}\n=======================\n')
    else:
        logging.warning(f'{now}\n{message}\n=====================\n')
