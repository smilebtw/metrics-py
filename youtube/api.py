from googleapiclient.discovery import build
import googleapiclient.errors
from datetime import datetime

class YoutubeAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.youtube = build('youtube', 'v3', developerKey=api_key)

    def get_channel_info(self, channel_id):
        try:
            response = self.youtube.channels().list(
                part='snippet,statistics',
                id=channel_id
            ).execute()

            channel_info = response['items'][0]
            name = channel_info['snippet']['title']
            views = int(channel_info['statistics'].get('viewCount', 0))
            subscribers = int(channel_info['statistics'].get('subscriberCount', 0))
            return dict({"channelId": channel_id, "channelName": name, "channelViews": views, "channelSubscribers": subscribers})

        except googleapiclient.errors.HttpError as e:
            print('Erro ao obter informações do canal:', e)
            return None

    def get_videos(self, channel_id):
        try:
            videos = []
            next_page_token = None

            while True:
                response = self.youtube.search().list(
                    part='id,snippet',
                    channelId=channel_id,
                    type='video',
                    maxResults=50,
                    pageToken=next_page_token
                ).execute()

                for item in response['items']:
                    video_url_id = item['id']['videoId']
                    title = item['snippet']['title']
                    published_at = datetime.strptime(item['snippet']['publishedAt'], "%Y-%m-%dT%H:%M:%SZ")
                    video = dict({"videoId": video_url_id, "videoTitle": title, "publishedAt": published_at})
                    videos.append(video)

                next_page_token = response.get('nextPageToken')
                if not next_page_token:
                    break

            return videos

        except googleapiclient.errors.HttpError as e:
            print('Erro ao obter os vídeos:', e)
            return []

    def get_video_metrics(self, video_id):
        try:
            response = self.youtube.videos().list(
                part='statistics',
                id=video_id
            ).execute()

            video_stats = response['items'][0]['statistics']
            video_views = int(video_stats.get('viewCount', 0))
            video_likes = int(video_stats.get('likeCount', 0))
            video_comments = int(video_stats.get('commentCount', 0))

            return dict({"videoViews": video_views, "videoLikes": video_likes, "videoComments": video_comments})
            
        except googleapiclient.errors.HttpError as e:
            print('Erro ao obter as métricas do vídeo:', e)
            return None
