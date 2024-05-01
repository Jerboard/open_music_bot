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
from enums import BaseCB


@dp.callback_query(lambda cb: cb.data.startswith(BaseCB.PERFORMER))
async def my_music_performer(cb: CallbackQuery):
    my_music = await db.get_tracks(cb.from_user.id)
    await cb.message.edit_text('Исполнители', reply_markup=kb.get_performer_kb(my_music))


@dp.callback_query(lambda cb: cb.data.startswith(BaseCB.TRACK))
async def my_music_performer(cb: CallbackQuery):
    _, performer_id = cb.data.split(':')

    track = await db.get_track(int(performer_id))

    my_music = await db.get_tracks(cb.from_user.id, performer=track.performer)
    await cb.message.edit_text('Исполнители', reply_markup=kb.get_tracks_kb(my_music))


@dp.callback_query (lambda cb: cb.data.startswith (BaseCB.TRACK))
async def my_music_performer(cb: CallbackQuery):
    _, track_id = cb.data.split (':')

    track = await db.get_track (int (track_id))

    await cb.message.answer_audio(
        audio=track.file_id,
        performer=track.performer,
        title=track.title
    )