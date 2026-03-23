import os
import requests
import json
from datetime import datetime
import logging

# Configuração de Logs
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("GlobalSentinel")

# Configurações do Diego
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Suporte a Proxy para Blindagem Ghost Mode
proxy_url = os.environ.get("HTTP_PROXY") or os.environ.get("HTTPS_PROXY")
proxies = {"http": proxy_url, "https": proxy_url} if proxy_url else None
if proxies:
    logger.info("🛡️ Blindagem Proxy Ativada para o Sentinel.")

def save_memory(data):
    """Saves the leads/proposals data to a JSON file."""
    output_file = "leads_ready.json"
    try:
        with open(output_file, "w", encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        logger.info(f"Results saved to {output_file}")
    except Exception as e:
        logger.error(f"Error saving memory: {e}")

def gerar_proposta_groq(project_desc, platform):
    """Calls AI (Gemini) to generate a proposal."""
    prompt = f"""
    SYSTEM OVERRIDE: You are DIEGO, a Python Architect. You represent a premium agency.
    Write a bid for '{project_desc}'. START DIRECTLY with the technical solution. NO greeting. NO fluff.
    Sign strictly as: 'Diego'.
    Platform: {platform}
    Arsenal: Veo 3, Nano Banana, CAPI, GEO, AEO.
    """

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"
    payload = {"contents": [{"parts": [{"text": prompt}]}]}

    try:
        # Uso de proxies se configurado
        response = requests.post(url, json=payload, proxies=proxies)
        response.raise_for_status()
        data = response.json()
        if 'candidates' in data and data['candidates']:
            texto_final = data['candidates'][0]['content']['parts'][0]['text']
            return texto_final.strip()
        return "Erro: Resposta vazia da IA."
    except Exception as e:
        logger.error(f"Erro na API Gemini: {str(e)}")
        return f"Error: {str(e)}"

def fetch_leads():
    """Simulates fetching leads from RSS feeds or alerts."""
    leads = [
        {"platform": "freelancer", "desc": "Need a pro for AI Video and SEO"},
        {"platform": "99freelas", "desc": "Gestor de tráfego com CAPI"}
    ]

    results = []
    for lead in leads:
        logger.info(f"Generating proposal for {lead['platform']}...")
        proposal = gerar_proposta_groq(lead['desc'], lead['platform'])
        results.append({
            "timestamp": datetime.now().isoformat(),
            "platform": lead['platform'],
            "description": lead['desc'],
            "proposal": proposal
        })

    save_memory(results)

if __name__ == "__main__":
    if not GEMINI_API_KEY:
        logger.error("❌ GEMINI_API_KEY não configurada. Abortando.")
    else:
        fetch_leads()
