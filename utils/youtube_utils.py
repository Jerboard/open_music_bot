from pytube import YouTube
from moviepy.editor import AudioFileClip

import os

from config import Config as cfg
from enums import SoundType


# проверка длинны видео ссылки на ютуб
def download_audio(link: str):
    if not os.path.exists (cfg.download_path):
        os.makedirs (cfg.download_path)

    yt = YouTube(link)
    audio = yt.streams.filter (only_audio=True).get_audio_only()
    audio.download (cfg.download_path)
    return os.path.join (cfg.download_path, audio.default_filename), audio.default_filename[:-4]


# конвертирует видео в аудио
def convert(mp4_file_name: str) -> str:
    mp4_file_path = os.path.join (cfg.download_path, mp4_file_name)
    audio_hn = AudioFileClip (mp4_file_path)
    filename = mp4_file_name.split ('.')[0]
    mp3_file_path = os.path.join (cfg.convert_path, f'{filename}.mp3')
    audio_hn.write_audiofile (mp3_file_path)
    return mp3_file_path
