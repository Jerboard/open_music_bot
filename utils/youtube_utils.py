from pytube import YouTube
from moviepy.editor import AudioFileClip

import os

from config import Config as cfg
from utils.objects import Track
from enums import SoundType


# проверка длинны видео ссылки на ютуб
def download_audio(link: str) -> Track:
    if not os.path.exists (cfg.download_path):
        os.makedirs (cfg.download_path)

    yt = YouTube(link)
    audio = yt.streams.filter (only_audio=True).get_audio_only()
    title_audio = audio.title
    author_audio = yt.author
    audio.download (cfg.download_path)
    # return os.path.join (cfg.download_path, audio.default_filename), audio.default_filename[:-4]
    return Track(
        title=title_audio,
        performer=author_audio,
        filepath=os.path.join (cfg.download_path, audio.default_filename),
    )


# конвертирует видео в аудио
# def convert(mp4_file_name: str) -> str:
#     mp4_file_path = os.path.join (cfg.download_path, mp4_file_name)
#     audio_hn = AudioFileClip (mp4_file_path)
#     filename = mp4_file_name.split ('.')[0]
#     mp3_file_path = os.path.join (cfg.convert_path, f'{filename}.mp3')
#     audio_hn.write_audiofile (mp3_file_path)
#     return mp3_file_path
