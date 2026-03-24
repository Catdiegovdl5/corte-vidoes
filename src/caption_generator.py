import os
import requests
import json
import logging

logger = logging.getLogger("CaptionBrain")

class CaptionGenerator:
    """
    Inteligência do Diego para copywriting de Reels.
    Usa LLaMA 3/Gemini para criar legendas de alta retenção.
    Focado agora no objetivo: CAMPEONATO DE CORTES (RAIAM STYLE).
    """

    def __init__(self, api_key=None):
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")

    def generate_caption(self, video_topic, video_title=""):
        """
        Gera uma legenda magnética baseada no tópico do vídeo.
        Otimizada para viralizar no estilo provocativo do Raiam Santos.
        """
        if not self.api_key:
            logger.warning("⚠️ API Key ausente. Usando legenda padrão 'Fallback'.")
            return f"Confira este corte épico sobre {video_topic}! 🏆 #Cortes #Viral"

        prompt = f"""
        Aja como Diego, Especialista em Viralização de Cortes e Tráfego Orgânico.
        Crie uma legenda para um Instagram Reel que é um CORTE do canal do RAIAM SANTOS.

        TÓPICO: "{video_topic}"
        TÍTULO ORIGINAL: "{video_title}"

        DIRETRIZES S-TIER (RAIAM STYLE):
        1. Gancho (Hook): Use uma frase de "choque de realidade" ou polêmica sobre dinheiro, mindset ou sucesso.
        2. Retenção: Mencione que a verdade dói, mas precisa ser dita. O final é onde ele solta a bomba.
        3. CTAs: Desafie a pessoa a discordar nos comentários ou a seguir para sair da mediocridade.
        4. Hashtags: #raiamsantos #nomadedigital #cortesdoraiam #marketingdigital #liberdadefinanceira #diego.
        5. Tom: Provocador, arrogante (no estilo mentor), rápido e focado em escala.

        RESTRIÇÕES:
        - Máximo 400 caracteres.
        - Sem emojis genéricos, use fogo, troféu e cifrão.
        - Idioma: Português (Brasil).

        SAÍDA: Apenas o texto da legenda.
        """

        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={self.api_key}"
        payload = {"contents": [{"parts": [{"text": prompt}]}]}

        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            data = response.json()
            if 'candidates' in data and data['candidates']:
                return data['candidates'][0]['content']['parts'][0]['text'].strip()
            return f"🏆 Raiam mandou a real sobre {video_topic}. #Cortes #Viral"
        except Exception as e:
            logger.error(f"Erro ao gerar legenda: {e}")
            return f"A verdade sobre {video_topic} que ninguém te conta. 🔥"

if __name__ == "__main__":
    gen = CaptionGenerator()
    print(gen.generate_caption("Por que ser CLT é burrice", "Papo Reto sobre Carreira"))
