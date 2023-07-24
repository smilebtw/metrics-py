from database.models import Channel, Video, VideoMetrics, ChannelMetrics
from database.database import session
from datetime import datetime, timezone
from youtube.api import YoutubeAPI
from sqlalchemy import func, and_
import multiprocessing
from itertools import cycle

# pode pegar as chaves no arquivo api_keys.txt ou algo do tipo, mesma coisa para os ids dos canais
API_KEYS = [] 
CHANNEL_IDS = []

def process_channel(args):
    channel_id, api_key_cycle = args

    sucess = False
    while not sucess:
        try:
            api_key = next(api_key_cycle)
            api = YoutubeAPI(api_key)

            channel_info = api.get_channel_info(channel_id)

            channel = session.query(Channel).filter(Channel.channelId == channel_id).first()
            if channel is None:
                # o channelLabel pode ser pego de acordo com o channelId que for passado, por exemplo
                # podemos ter 2 txt, um com os ids dos canais de esquerda e outro com os ids dos canais de direita
                channel = Channel(channelId=channel_info['channelId'], channelName=channel_info['channelName'], channelLabel='Direita')
                session.add(channel)
                session.commit()
                print("Channel adicionado: ", channel.channelName)
            else:
                print("Canal já esta cadastrado, atualizando: ", channel.channelName)

            videos = api.get_videos(channel_id)

            for video in videos:
                video['channelId'] = channel_id
                video = Video(**video)
                if session.query(Video).filter(Video.videoId == video.videoId).first() is None:
                    session.add(video)

                createdAt = session.query(VideoMetrics.createdAt).filter(VideoMetrics.videoId == video.videoId).order_by(VideoMetrics.createdAt.desc()).first()

                if session.query(VideoMetrics).filter(VideoMetrics.videoId == video.videoId).first() is None or createdAt[0].date() < datetime.now(timezone.utc).date():
                    video_metrics = api.get_video_metrics(video.videoId)
                    video_metrics['videoId'] = video.videoId
                    video_metrics['channelId'] = channel_id
                    video_metrics = VideoMetrics(**video_metrics)
                    session.add(video_metrics)

            session.commit()

            total_comments_likes = session.query(
                func.sum(VideoMetrics.videoComments).label('total_comments'),
                func.sum(VideoMetrics.videoLikes).label('total_likes')
            ).filter(
                VideoMetrics.channelId == channel_id
            ).first()

            if total_comments_likes.total_comments is None:
                total_comments = 0
            else:
                total_comments = total_comments_likes.total_comments

            if total_comments_likes.total_likes is None:
                total_likes = 0
            else:
                total_likes = total_comments_likes.total_likes

            channel_metrics = session.query(ChannelMetrics).filter(
                ChannelMetrics.channelId == channel_id,
                func.date(ChannelMetrics.metricsDate) == datetime.now(timezone.utc).date()
            ).first()

            if channel_metrics is None:
                channel_metrics = ChannelMetrics(
                    channelId=channel_id,
                    views=channel_info['channelViews'],
                    subscribers=channel_info['channelSubscribers'],
                    likes=total_likes,
                    comments=total_comments,
                )
                session.add(channel_metrics)

            session.commit()
            sucess = True

            print("Canal atualizado: ", channel.channelName)
        except Exception as e:
            print(f"Erro ao processar o canal {channel_id} com a chave {api_key}: {e}")

            if api_key == API_KEYS[-1]:
                print(f"Todas as API keys foram testadas para o canal {channel_id}, não foi possível processá-lo.")
                return None

            continue

if __name__ == "__main__":
    api_key_cycle = cycle(API_KEYS)

    num_processes = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(processes=num_processes)

    channel_api_key_pairs = [(channel_id, api_key_cycle) for channel_id in CHANNEL_IDS]

    pool.map(process_channel, channel_api_key_pairs)

    pool.close()
    pool.join()

    print("Todos os canais foram processados.")

