from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext

import asyncio
import os

import db
# import keyboards as kb
from init import dp
from config import Config
from utils.youtube_utils import download_audio, convert


# первый экран
@dp.message(CommandStart())
async def command_start_handler(msg: Message, state: FSMContext) -> None:
    await state.clear()
    audio_file = os.path.join (Config.convert_path, 'Afterglow.mp3')
    user_db_file = FSInputFile (audio_file)
    await msg.answer_audio (audio=user_db_file)


# скачивает трек по ссылке с ютуба
# @dp.message()
# async def download_music(msg: Message) -> None:
#     print('strt')
#     video_file = download_audio(msg.text)
#     print(video_file)
    # await asyncio.sleep(1)
    # audio_file = convert(video_file)
    # audio_file = os.path.join (Config.download_path, video_file)
    # user_db_file = FSInputFile (audio_file)
    # sent = await msg.answer_audio (audio=user_db_file)

    # await db.add_track (
    #     user_id=msg.from_user.id,
    #     performer=sent.audio.performer,
    #     title=sent.audio.title,
    #     file_name=sent.audio.file_name,
    #     mime_type=sent.audio.mime_type,
    #     file_size=sent.audio.file_size,
    #     duration=sent.audio.duration,
    #     file_id=sent.audio.file_id
    # )

