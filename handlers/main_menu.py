from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext

import asyncio
import os

import db
import keyboards as kb
from init import dp
from config import Config
from utils.youtube_utils import download_audio, convert


# первый экран
@dp.message(CommandStart())
async def command_start_handler(msg: Message, state: FSMContext) -> None:
    await state.clear()
    await db.create_or_update_user(
        user_id=msg.from_user.id,
        full_name=msg.from_user.full_name,
        username=msg.from_user.username,
    )
    text = ('Привет, друг!Это бот для хранения и скачивания с Ютуба твоей любимой музыки,подкастов и аудиокниг\n\n'
            'Скоро тут будет какой-то полезный текст или твоя статистика, но пока нужно создать сам бот)')

    await msg.answer(text=text, reply_markup=kb.get_main_user_kb())
