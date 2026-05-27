import os
import logging
from moviepy import VideoFileClip, clips_array, vfx
import whisper
import cv2
import mediapipe as mp
import numpy as np

logger = logging.getLogger("VideoProcessor")

class VideoProcessor:
    """
    Processador de Vídeo Ultra-Intelligence.
    Corta vídeos baseados em IA, detecta o rosto e aplica layouts inteligentes (Solo vs React).
    """

    def __init__(self, output_dir="processed"):
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        logger.info("🧠 Carregando Whisper e MediaPipe...")
        self.model = whisper.load_model("base")
        self.mp_face_detection = mp.solutions.face_detection
        self.face_detection = self.mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.5)

    def get_face_center(self, frame):
        """
        Detecta o rosto no frame e retorna a coordenada X central.
        """
        results = self.face_detection.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        if results.detections:
            # Pega a primeira detecção (presumivelmente o Raiam)
            bbox = results.detections[0].location_data.relative_bounding_box
            center_x = bbox.xmin + (bbox.width / 2)
            return center_x
        return 0.5 # Fallback para o centro real

    def process_reels(self, input_path, start_time, end_time, viral_reason="", content_type="solo"):
        """
        Corta o vídeo e aplica o layout inteligente baseado no tipo de conteúdo (Solo ou React).
        """
        filename = os.path.basename(input_path)
        output_path = os.path.join(self.output_dir, f"viral_{start_time}_{filename}")

        logger.info(f"🎬 Processando Momento Viral ({content_type}): {viral_reason}")

        clip = VideoFileClip(input_path).subclipped(start_time, end_time)

        if content_type == "react":
            # Layout de Reação: Raiam em cima (crop rosto) e conteúdo em baixo (full width)
            return self._create_react_layout(clip, output_path)
        else:
            # Layout Solo: Auto-Reframe Vertical
            return self._create_solo_layout(clip, output_path)

    def _create_solo_layout(self, clip, output_path):
        """Aplica o Auto-Reframe 9:16 focado no rosto."""
        sample_frame = clip.get_frame(0)
        face_x_percent = self.get_face_center(sample_frame)

        w, h = clip.size
        target_ratio = 9/16
        new_w = int(h * target_ratio)
        center_x = int(face_x_percent * w)

        x1 = max(0, center_x - new_w // 2)
        if x1 + new_w > w:
            x1 = w - new_w

        logger.info(f"🎯 Solo Reframe: Focando em X={center_x}")
        clip_final = clip.cropped(x1=x1, y1=0, width=new_w, height=h).resized(height=1920)
        clip_final.write_videofile(output_path, codec="libx264", audio_codec="aac", fps=30, logger=None)
        return output_path

    def _create_react_layout(self, clip, output_path):
        """Cria um layout empilhado (Split-Screen) para Reações."""
        # 1. PARTE SUPERIOR (Reactor/Raiam)
        # Vamos assumir 50% da altura do vídeo para o Reactor.
        sample_frame = clip.get_frame(0)
        face_x_percent = self.get_face_center(sample_frame)

        w, h = clip.size
        # Crop lateral para o reactor (1080x960)
        # Largura alvo para o reactor na metade superior: 1080
        # Altura alvo: 960

        reactor_crop_w = int(h * (1080/1920)) # Proporção correta para a metade
        center_x = int(face_x_percent * w)
        x1 = max(0, center_x - reactor_crop_w // 2)
        if x1 + reactor_crop_w > w: x1 = w - reactor_crop_w

        reactor_clip = clip.cropped(x1=x1, y1=0, width=reactor_crop_w, height=h).resized(height=960)

        # 2. PARTE INFERIOR (Conteúdo): Original full width mas redimensionado para preencher a largura
        content_clip = clip.resized(width=1080)

        # Empilhamento Vertical
        logger.info("📐 Layout Split-Screen: Raiam em cima + Vídeo reagido em baixo")
        final_clip = clips_array([[reactor_clip], [content_clip]])

        # Garante que o final tenha 1080x1920 (pode precisar de preenchimento ou redimensionamento)
        final_clip = final_clip.resized(height=1920)

        final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac", fps=30, logger=None)
        return output_path

    def transcribe_full(self, input_path):
        """Retorna a transcrição completa para análise da IA."""
        return self.model.transcribe(input_path, verbose=False)

if __name__ == "__main__":
    pass
