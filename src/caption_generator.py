import os
import requests
import json
import logging

logger = logging.getLogger("CaptionBrain")

class CaptionGenerator:
    """
    Inteligência do Diego para copywriting de Reels.
    Usa LLaMA 3/Gemini para criar legendas de alta retenção.
    Focado agora no objetivo: CAMPEONATO DE CORTES.
    """

    def __init__(self, api_key=None):
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")

    def generate_caption(self, video_topic):
        """
        Gera uma legenda magnética baseada no tópico do vídeo.
        Otimizada para viralizar em Campeonatos de Cortes.
        """
        if not self.api_key:
            logger.warning("⚠️ API Key ausente. Usando legenda padrão 'Fallback'.")
            return f"Confira este corte épico sobre {video_topic}! 🏆 #Cortes #Viral"

        prompt = f"""
        Aja como Diego, Especialista em Viralização de Cortes e Tráfego.
        Crie uma legenda para um Instagram Reel que é um CORTE de um podcast ou live.
        O objetivo é vencer um CAMPEONATO DE CORTES (máximo engajamento e retenção).

        TÓPICO DO VÍDEO: "{video_topic}"

        DIRETRIZES S-TIER:
        1. Gancho (Hook): Comece com uma frase polêmica ou uma pergunta que force a pessoa a parar.
        2. Retenção: Use frases curtas e impacto imediato. Mencione que o final é a melhor parte.
        3. CTAs: Peça para a pessoa seguir o perfil de cortes para não perder os próximos rounds do campeonato.
        4. Hashtags: Use #campeonatodecortes #cortespodcast #marketingdigital #sucesso #diego.
        5. Tom: Provocador, rápido e focado em autoridade.

        RESTRIÇÕES:
        - Sem enrolação.
        - Máximo 400 caracteres.
        - Idioma: Português (Brasil).

        SAÍDA: Apenas o texto da legenda pronta para colar.
        """

        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={self.api_key}"
        payload = {"contents": [{"parts": [{"text": prompt}]}]}

        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            data = response.json()
            if 'candidates' in data and data['candidates']:
                return data['candidates'][0]['content']['parts'][0]['text'].strip()
            return f"🏆 O segredo sobre {video_topic} revelado. #Cortes #Viral"
        except Exception as e:
            logger.error(f"Erro ao gerar legenda: {e}")
            return f"Mais um corte pesado sobre {video_topic}. Acompanhe a saga."

if __name__ == "__main__":
    gen = CaptionGenerator()
    print(gen.generate_caption("Como ganhar o campeonato de cortes usando IA"))
