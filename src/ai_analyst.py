import os
import json
import logging
import requests

logger = logging.getLogger("AIAnalyst")

class AIAnalyst:
    """
    O Cérebro da Operação.
    Analisa a transcrição e identifica momentos virais (Raiam Style).
    """

    def __init__(self, api_key=None):
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")

    def identify_viral_moments(self, transcript_segments):
        """
        Recebe os segmentos do Whisper e retorna os melhores timestamps.
        """
        if not self.api_key:
            logger.warning("⚠️ API Key ausente. Usando fallback de tempo fixo.")
            return [{"start": 60, "end": 120, "reason": "Fixed fallback"}]

        # Prepara a transcrição com timestamps para a IA
        text_for_ai = ""
        for s in transcript_segments[:100]: # Limita para não estourar contexto
            text_for_ai += f"[{s['start']:.2f}s - {s['end']:.2f}s]: {s['text']}\n"

        prompt = f"""
        Aja como Diego, Diretor de Conteúdo Viral. Sua missão é analisar a transcrição de um vídeo do RAIAM SANTOS.
        Identifique os 3 momentos mais virais.

        Sua inteligência deve classificar cada momento em um de dois tipos:
        - 'solo': Monólogo de poder, lição direta, choque de realidade sem vídeo externo.
        - 'react': Raiam reagindo ou comentando sobre outro vídeo, pessoa ou conteúdo externo visível na tela.

        Critérios:
        1. CHOQUE DE REALIDADE: Mindset, dinheiro, críticas à mediocridade (Raiam Style).
        2. ALTA ENERGIA: Momentos de fala contínua, sem pausas longas.
        3. POLÊMICA: Assuntos que gerem comentários.

        Retorne APENAS um JSON no seguinte formato:
        [
            {{"start": 10.5, "end": 40.2, "reason": "Motivo", "type": "solo" | "react"}},
            ...
        ]

        TRANSCRIÇÃO:
        {text_for_ai}
        """

        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={self.api_key}"
        payload = {"contents": [{"parts": [{"text": prompt}]}]}

        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            data = response.json()
            if 'candidates' in data and data['candidates']:
                raw_json = data['candidates'][0]['content']['parts'][0]['text']
                # Limpeza simples de possíveis markdown na resposta
                raw_json = raw_json.replace("```json", "").replace("```", "").strip()
                return json.loads(raw_json)
            return []
        except Exception as e:
            logger.error(f"Erro na análise semântica: {e}")
            return [{"start": 30, "end": 90, "reason": "Error fallback"}]

if __name__ == "__main__":
    analyst = AIAnalyst()
    # test_segments = [{"start": 0, "end": 10, "text": "Vocês são preguiçosos"}]
    # print(analyst.identify_viral_moments(test_segments))
