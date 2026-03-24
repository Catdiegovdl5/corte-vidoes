import os
import logging
from moviepy import VideoFileClip
import whisper
import cv2
import mediapipe as mp
import numpy as np

logger = logging.getLogger("VideoProcessor")

class VideoProcessor:
    """
    Processador de Vídeo Ultra-Intelligence.
    Corta vídeos baseados em IA, detecta o rosto e faz auto-reframe para o Raiam.
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

    def process_reels(self, input_path, start_time, end_time, viral_reason=""):
        """
        Corta o vídeo e aplica auto-reframe focado no rosto detectado.
        """
        filename = os.path.basename(input_path)
        output_path = os.path.join(self.output_dir, f"viral_{start_time}_{filename}")

        logger.info(f"🎬 Processando Momento Viral: {viral_reason}")

        clip = VideoFileClip(input_path).subclipped(start_time, end_time)

        # Analisa o primeiro frame para achar o rosto
        sample_frame = clip.get_frame(0)
        face_x_percent = self.get_face_center(sample_frame)

        w, h = clip.size
        target_ratio = 9/16
        new_w = int(h * target_ratio)

        # Calcula o centro do crop baseado na detecção do rosto
        center_x = int(face_x_percent * w)

        # Garante que o crop não saia das bordas
        x1 = max(0, center_x - new_w // 2)
        if x1 + new_w > w:
            x1 = w - new_w

        logger.info(f"🎯 Auto-Reframe: Focando em X={center_x} (Crop: {x1} a {x1+new_w})")

        clip_cropped = clip.cropped(x1=x1, y1=0, width=new_w, height=h)
        clip_final = clip_cropped.resized(height=1920)

        logger.info(f"💾 Exportando corte inteligente: {output_path}")
        clip_final.write_videofile(output_path, codec="libx264", audio_codec="aac", fps=30, logger=None)

        return output_path

    def transcribe_full(self, input_path):
        """Retorna a transcrição completa para análise da IA."""
        return self.model.transcribe(input_path, verbose=False)

if __name__ == "__main__":
    # Teste de carga: processor = VideoProcessor()
    pass
