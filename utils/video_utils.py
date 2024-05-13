from pytube import YouTube
from moviepy.editor import AudioFileClip
import typing as t

import os

from config import Config as cfg
from utils.objects import Track
from enums import SoundType


# определеят название и исполнителя
def hand_yt_video_name(video_name: str) -> t.Union[list[str], str]:
    name_split = video_name.split(' - ')
    if len(name_split) == 2:
        return name_split


# проверка длинны видео ссылки на ютуб
def download_audio(link: str) -> Track:
    if not os.path.exists (cfg.download_path):
        os.makedirs (cfg.download_path)

    yt = YouTube(link)
    audio = yt.streams.filter (only_audio=True).get_audio_only()

    name_split = audio.title.split (' - ')
    if len (name_split) == 2:
        title_audio = name_split[0]
        performer = name_split[1]
    else:
        title_audio = audio.title
        performer = None

    audio.download (cfg.download_path)
    # return os.path.join (cfg.download_path, audio.default_filename), audio.default_filename[:-4]
    return Track(
        title=title_audio,
        performer=performer,
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
