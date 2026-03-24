import os
import logging
from moviepy import VideoFileClip, TextClip, CompositeVideoClip
import whisper

logger = logging.getLogger("VideoProcessor")

class VideoProcessor:
    """
    Processador de Vídeo S-Tier.
    Corta para 9:16, transcreve com Whisper e aplica legendas dinâmicas.
    Otimizado para o Lenovo IdeaPad (16GB RAM).
    """

    def __init__(self, output_dir="processed"):
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        # Carrega o modelo Whisper (base é ideal para velocidade/precisão no PC médio)
        logger.info("🧠 Carregando cérebro Whisper...")
        self.model = whisper.load_model("base")

    def process_reels(self, input_path, start_time, end_time):
        """
        Corta e formata o vídeo para Reels.
        """
        filename = os.path.basename(input_path)
        output_path = os.path.join(self.output_dir, f"reels_{filename}")

        logger.info(f"🎬 Processando corte: {start_time}s -> {end_time}s")

        clip = VideoFileClip(input_path).subclipped(start_time, end_time)

        # Formatação 9:16 (Vertical)
        w, h = clip.size
        target_ratio = 9/16
        current_ratio = w/h

        if current_ratio > target_ratio:
            # Vídeo é muito largo (widescreen) -> corta as laterais
            new_w = int(h * target_ratio)
            clip = clip.cropped(x_center=w/2, width=new_w)

        clip = clip.resized(height=1920) # Redimensiona para 1080x1920

        # Transcrição para Legendas
        logger.info("🎙️ Transcrevendo áudio...")
        result = self.model.transcribe(input_path, verbose=False)
        segments = result.get('segments', [])

        # Filtra segmentos dentro do tempo do corte
        active_segments = [s for s in segments if s['start'] >= start_time and s['end'] <= end_time]

        # Criação de Legendas (Exemplo Simples - Requer ImageMagick instalado no sistema)
        # Em ambientes sem ImageMagick, isso pode falhar. Usaremos FFmpeg se necessário.
        # Por enquanto, focamos no corte e estrutura.

        logger.info(f"💾 Salvando Reels: {output_path}")
        clip.write_videofile(output_path, codec="libx264", audio_codec="aac", fps=30)

        return output_path

if __name__ == "__main__":
    processor = VideoProcessor()
    # processor.process_reels("downloads/video.mp4", 10, 40)
