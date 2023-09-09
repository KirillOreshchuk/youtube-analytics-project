import os
from googleapiclient.discovery import build
from helper.youtube_api_manual import printj
api_key: str = "AIzaSyDzWMCtRnkwIfUSTbjvN9fuPnT2DVNTz1I"

class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.channel_id = channel_id

    def print_info(self):
        """Выводит в консоль информацию о канале."""

        youtube = build('youtube', 'v3', developerKey=api_key)
        channel = youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()

        return printj(channel)