from aiogram.filters import StateFilter
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.state import default_state
from aiogram.enums.content_type import ContentType
from aiogram.enums.message_entity_type import MessageEntityType

import re
import os
import asyncio

import db
# import keyboards as kb
from init import dp, bot
from utils.youtube_utils import download_audio


# сохраняет присланные треки
@dp.message(lambda msg: msg.content_type == ContentType.AUDIO)
async def save_music(msg: Message) -> None:
    await db.add_track(
        user_id=msg.from_user.id,
        performer=msg.audio.performer,
        title=msg.audio.title,
        file_name=msg.audio.file_name,
        mime_type=msg.audio.mime_type,
        file_size=msg.audio.file_size,
        duration=msg.audio.duration,
        file_id=msg.audio.file_id
    )
    

# скачивает трек по ссылке с ютуба
@dp.message(StateFilter(default_state))
async def download_music(msg: Message) -> None:
    entities = msg.entities if msg.entities else msg.caption_entities
    text = msg.text if msg.text else msg.caption

    if not entities:
        text = ('Прости, дружище, не нашёл ссылку в твоём сообщении 🤷\n\n'
                'Ты можешь отправить ссылку на видео с YouTube, и получишь звуковую дорожку оттуда\n'
                '❕ Обрати внимание - видео должно быть не длиннее 10 минут')
        await msg.answer(text)
        return

    youtube_link = None
    for entity in entities:
        temp_url = None
        if entity.type == MessageEntityType.URL:
            temp_url = text[entity.offset:entity.offset + entity.length]
        elif entity.type == MessageEntityType.TEXT_LINK:
            temp_url = entity.url

        if temp_url:
            result = re.search('youtu', temp_url, re.IGNORECASE)
            if result:
                youtube_link = temp_url
                break

    if not youtube_link:
        text = ('Похоже тут нет ссылки на YouTube🤷\n\n'
                'Ты можешь отправить ссылку на видео с YouTube, и получишь звуковую дорожку оттуда\n'
                '❕ Обрати внимание - видео должно быть не длиннее 10 минут')
        await msg.answer (text)
        return

    file_path = download_audio (youtube_link)

    audio = FSInputFile (file_path)
    sent = await msg.answer_audio (audio=audio)
    text = 'Лови! Теперь трек доступен в лк бота'
    await msg.answer (text)

    await db.add_track (
        user_id=msg.from_user.id,
        performer=sent.audio.performer,
        title=sent.audio.title,
        file_name=sent.audio.file_name,
        mime_type=sent.audio.mime_type,
        file_size=sent.audio.file_size,
        duration=sent.audio.duration,
        file_id=sent.audio.file_id
    )
    await asyncio.sleep(1)
    os.remove(file_path)

