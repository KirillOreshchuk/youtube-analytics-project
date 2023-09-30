from src.video import Video

if __name__ == '__main__':
    broken_video = Video('broken_video_id')
    # изменил "title" на "video_title", потому что изначально определил переменную как "video_title"
    assert broken_video.video_title is None
    assert broken_video.like_count is None
