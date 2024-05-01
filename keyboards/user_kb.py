from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup

import db
from enums import BaseCB


# основная клавиатура пользователя
def get_main_user_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text='🎼 Моя музыка', callback_data=BaseCB.PERFORMER.value)
    kb.button(text='🔍 Поиск по трекам', callback_data='in_dev')
    kb.button(text='🔍 Поиск по исполнителям', callback_data='in_dev')
    return kb.adjust (1, 2).as_markup ()


# клава с исполнителями
def get_performer_kb(music: tuple[db.TrackRow]) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder ()
    kb.button (text='🔙 Назад', callback_data='in_dev')
    ex_list = []
    for performer in music:
        if performer.performer not in ex_list:
            kb.button(text=performer.performer, callback_data=f'{BaseCB.TRACK.value}:{performer.id}')
            ex_list.append(performer.performer)

    return kb.adjust(1).as_markup()


# клава с треками
def get_tracks_kb(music: tuple[db.TrackRow]) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder ()
    kb.button (text='🔙 Назад', callback_data='in_dev')
    for track in music:
        kb.button(text=track.title, callback_data=f'{BaseCB.SAND.value}:{track.id}')

    return kb.adjust (1).as_markup ()