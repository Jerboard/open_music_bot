from enum import Enum


class SoundType(str, Enum):
    MUSIC = 'music'
    PODCAST = 'podcast'
    BOOK = 'book'
