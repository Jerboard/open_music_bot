from enum import Enum


class BaseCB(str, Enum):
    PERFORMER = 'my_music_performer'
    TRACK = 'my_music_track'
    SAND = 'my_music_send'
