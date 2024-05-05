from aiogram.types import Message, InputTextMessageContent, InlineQuery, InlineQueryResultArticle
from aiogram.fsm.context import FSMContext

import hashlib

import db
import keyboards as kb
from init import dp, bot
from enums import UserStatus


# инлайн поиск
@dp.inline_query()
async def inline(call: InlineQuery, state: FSMContext):
    results = await db.search_tracks (request=call.query)

    search_results = []
    for result in results:
        search_results.append(
            InlineQueryResultArticle (
                id=hashlib.md5 (f'{result.id}'.encode ()).hexdigest (),
                title=result.title,
                input_message_content=InputTextMessageContent (message_text=f'{result.id}'),
            )
        )

    await call.answer(search_results, cache_time=60, is_personal=True)


# результат
@dp.message(lambda msg: msg.via_bot is not None)
async def get_video(msg: Message, state: FSMContext):
    await msg.delete()
    track_id = int(msg.text)
    track = await db.get_track(track_id=track_id)
    await msg.answer_audio(audio=track.file_id, performer=track.performer, title=track.title)
