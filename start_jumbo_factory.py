import os
import logging
from src.youtube_hunter import YoutubeHunter
from src.video_processor import VideoProcessor
from src.caption_generator import CaptionGenerator
from src.ai_analyst import AIAnalyst
from src.instagram_uploader import InstagramUploader

# Configuração Master de Log
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("JumboFactory")

def run_factory():
    """
    Orquestrador Ultra-Intelligence do Projeto Jumbo.
    Fábrica de Cortes Virais: Raiam Santos Edition.
    """
    logger.info("🦅 Operação Ultra-Intelligence Iniciada!")

    hunter = YoutubeHunter()
    processor = VideoProcessor()
    analyst = AIAnalyst()
    caption_gen = CaptionGenerator()

    # 1. Caçar Vídeos
    top_videos = hunter.get_viral_videos(limit=1) # Foca em um por vez para máxima precisão

    for video in top_videos:
        logger.info(f"🎯 Alvo Detectado: {video['title']}")

        # 2. Download do bruto
        video_path = hunter.download_video(video['url'])

        # 3. Transcrição Completa
        logger.info("🎙️ Transcrevendo para análise semântica...")
        transcript = processor.transcribe_full(video_path)

        # 4. Detecção de Momentos Virais via IA
        logger.info("🧠 Identificando momentos de 'Choque de Realidade'...")
        viral_moments = analyst.identify_viral_moments(transcript.get('segments', []))

        for i, moment in enumerate(viral_moments):
            logger.info(f"🔥 Processando Clip {i+1}: {moment['reason']}")

            # 5. Corte Inteligente + Auto-Reframe (Foco no Rosto)
            reels_path = processor.process_reels(
                video_path,
                start_time=moment['start'],
                end_time=moment['end'],
                viral_reason=moment['reason']
            )

            # 6. Gerar Legenda Magnética
            caption = caption_gen.generate_caption(moment['reason'], video['title'])
            logger.info(f"✍️ Legenda Gerada para o Clip {i+1}: {caption}")

            logger.info(f"🚀 REELS PRONTO: {reels_path}")

    logger.info("✅ Operação S-Tier Concluída!")

if __name__ == "__main__":
    run_factory()
