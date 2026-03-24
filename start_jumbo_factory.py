import os
import logging
from src.youtube_hunter import YoutubeHunter
from src.video_processor import VideoProcessor
from src.caption_generator import CaptionGenerator
from src.instagram_uploader import InstagramUploader

# Configuração Master de Log
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("JumboFactory")

def run_factory():
    """
    Orquestrador Supremo do Projeto Jumbo: Cortes do Raiam.
    """
    logger.info("🏭 Fábrica Jumbo Iniciada: Operação Raiam Santos")

    hunter = YoutubeHunter()
    processor = VideoProcessor()
    caption_gen = CaptionGenerator()
    uploader = InstagramUploader()

    # 1. Caçar Vídeos
    top_videos = hunter.get_viral_videos(limit=3)

    for video in top_videos:
        logger.info(f"🎯 Alvo Detectado: {video['title']}")

        # 2. Download
        video_path = hunter.download_video(video['url'])

        # 3. Criar Cortes (Simulando um corte de 30 segundos no meio do vídeo)
        # Em uma versão avançada, a IA analisaria o áudio para achar o momento 'viral'.
        reels_path = processor.process_reels(video_path, start_time=60, end_time=90)

        # 4. Gerar Legenda Viral (Raiam Style)
        caption = caption_gen.generate_caption(video['title'], video['title'])
        logger.info(f"✍️ Legenda Gerada: {caption}")

        # 5. Upload (Trincheira 1 - Desativado por padrão para segurança)
        logger.info(f"🚀 Reels Pronto para Envio: {reels_path}")
        # uploader.upload_reels(reels_path, caption) # Requer URL pública para a API Graph

    logger.info("✅ Operação Jumbo Concluída com Sucesso!")

if __name__ == "__main__":
    run_factory()
