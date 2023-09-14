import os
import json
from googleapiclient.discovery import build


api_key: str = os.getenv('YT_API_KEY')
youtube = build('youtube', 'v3', developerKey=api_key)


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""

        self.__channel_id = channel_id

        channel = youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()

        self.title = channel["items"][0]["snippet"]["title"]
        self.description = channel["items"][0]["snippet"]["description"]
        self.url = f"https://www.youtube.com/channel/{self.channel_id}"
        self.subscriber_count = int(channel["items"][0]["statistics"]["subscriberCount"])
        self.video_count = int(channel["items"][0]["statistics"]["videoCount"])
        self.view_count = int(channel["items"][0]["statistics"]["viewCount"])

    def __str__(self) -> str:
        """ отображает информацию об объекте класса"""
        return f"{self.title}({self.url})"

    def __add__(self, other) -> int:
        """ складывет количество подписчиков канала"""
        return self.subscriber_count + other.subscriber_count

    def __sub__(self, other) -> int:
        """ вычитает количество подписчиков канала"""
        return self.subscriber_count - other.subscriber_count

    def __gt__(self, other) -> bool:
        """ возвращает резуллльтат сравнения больше"""
        return self.subscriber_count > other.subscriber_count

    def __ge__(self, other) -> bool:
        """ возвращает результат сравнения больше или равно"""
        return self.subscriber_count >= other.subscriber_count

    def __lt__(self, other) -> bool:
        """ возвращает результат сравнения меньше"""
        return self.subscriber_count < other.subscriber_count

    def __le__(self, other) -> bool:
        """ возвращает результат сравнения меньше или равно"""
        return self.subscriber_count <= other.subscriber_count

    @classmethod
    def get_service(cls):
        """возвращает объект для работы с YouTube API"""
        return youtube

    @property
    def channel_id(self) -> str:
        return self.__channel_id

    def print_info(self):
        """Выводит в консоль информацию о канале."""
        channel = youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        print(json.dumps(channel, indent=2, ensure_ascii=False))

    def to_json(self, file_name):
        """сохраняет в файл значения атрибутов экземпляра `Channel`"""
        data_channel = {
            'id': self.__channel_id,
            'title': self.title,
            'url': self.url,
            'description': self.description,
            'subscriber_count': self.subscriber_count,
            'video_count': self.video_count,
            'view_count': self.view_count
        }
        with open(file_name, 'w', encoding='UTF-8') as file:
            json.dump(data_channel, file, ensure_ascii=False)
