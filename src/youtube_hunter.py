import yt_dlp
import os
import logging
import json

logger = logging.getLogger("YoutubeHunter")

class YoutubeHunter:
    """
    Caçador de Vídeos Virais do Raiam Santos.
    Focado em identificar os vídeos com maior potencial de 'cortes' baseados em views e data.
    """

    def __init__(self, output_dir="downloads"):
        self.channel_url = "https://www.youtube.com/@nomadedigitalraiam/videos"
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def get_viral_videos(self, limit=5):
        """
        Analisa o canal e retorna os 'top' vídeos recentes/virais.
        """
        logger.info(f"🕵️ Analisando canal do Raiam: {self.channel_url}")

        ydl_opts = {
            'quiet': True,
            'extract_flat': True,
            'force_generic_extractor': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                info = ydl.extract_info(self.channel_url, download=False)
                entries = info.get('entries', [])

                # Ordenar por views (simulado, extração básica do YouTube pode variar)
                # Na prática, pegamos os mais recentes e o usuário define o alvo
                videos = []
                for entry in entries[:limit*2]: # Pega um buffer maior
                    videos.append({
                        'title': entry.get('title'),
                        'url': f"https://www.youtube.com/watch?v={entry.get('id')}",
                        'id': entry.get('id')
                    })

                logger.info(f"✅ Encontrados {len(videos)} vídeos potenciais.")
                return videos[:limit]
            except Exception as e:
                logger.error(f"Erro ao caçar vídeos: {e}")
                return []

    def download_video(self, video_url):
        """
        Baixa o vídeo na melhor qualidade para processamento (MP4).
        """
        output_path = os.path.join(self.output_dir, '%(id)s.%(ext)s')
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': output_path,
            'merge_output_format': 'mp4',
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            logger.info(f"📥 Baixando vídeo: {video_url}")
            info = ydl.extract_info(video_url, download=True)
            file_path = ydl.prepare_filename(info)
            logger.info(f"✅ Download concluído: {file_path}")
            return file_path

if __name__ == "__main__":
    hunter = YoutubeHunter()
    top_videos = hunter.get_viral_videos(limit=1)
    if top_videos:
        print(f"Alvo detectado: {top_videos[0]['title']}")
        # hunter.download_video(top_videos[0]['url'])
