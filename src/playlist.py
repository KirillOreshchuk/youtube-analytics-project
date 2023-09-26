import os
import datetime
import isodate

from googleapiclient.discovery import build


class PlayList:

    __api_key: str = os.getenv('YT_API_KEY')
    __youtube = build('youtube', 'v3', developerKey=__api_key)

    def __init__(self, playlist_id: str):
        """
        Инициализатор класса PlayList
        """
        self.__playlist_id = playlist_id
        self.__playlists_info = self.__youtube.playlists().list(id=playlist_id,
                                                                part='contentDetails,snippet',
                                                                maxResults=50,
                                                                ).execute()
        self.__playlist_video = self.__youtube.playlistItems().list(playlistId=self.__playlist_id,
                                                                    part='contentDetails,snippet',
                                                                    maxResults=50,
                                                                    ).execute()

        video_ids: list[str] = [video['contentDetails']['videoId'] for video in self.__playlist_video['items']]

        self.title = self.__playlists_info["items"][0]["snippet"]["title"]
        self.url = f"https://www.youtube.com/playlist?list={self.__playlist_id}"

        self.__video_response = self.__youtube.videos().list(part='contentDetails,statistics',
                                                             id=','.join(video_ids)
                                                             ).execute()

    @property
    def total_duration(self):
        """
        Возвращает объект класса `datetime.timedelta` с суммарной длительностью плейлиста
        """
        total_duration = datetime.timedelta()
        video_response = self.__video_response

        for video in video_response['items']:
            # YouTube video duration is in ISO 8601 format
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total_duration += duration

        return total_duration

    def show_best_video(self):
        """
        Возвращает ссылку на самое популярное видео из плейлиста (по количеству лайков)
        """
        video_list = self.__video_response
        high_likes = 0
        top_video = None

        for i in range(len(video_list)):
            like_count = int(video_list["items"][i]["statistics"]["likeCount"])
            if like_count > high_likes:
                high_likes = like_count
                top_video = video_list["items"][i]["id"]

        return f"https://youtu.be/{top_video}"
