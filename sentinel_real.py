import time
import logging
import os
import threading
import json
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from groq import Groq
from freelancersdk.session import Session
from freelancersdk.resources.projects.projects import search_projects
from freelancersdk.resources.projects.helpers import create_search_projects_filter
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger("JulesV17_Groq")

# Carrega chaves do arquivo .env IMEDIATAMENTE (apenas para rodar local)
load_dotenv()

# Suporte a Proxy para Blindagem Ghost Mode
proxy_url = os.environ.get("HTTP_PROXY") or os.environ.get("HTTPS_PROXY")
proxies = {"http": proxy_url, "https": proxy_url} if proxy_url else None
if proxies:
    logger.info("🛡️ Blindagem Proxy Ativada para o Sentinel Real.")

# DIAGNOSTIC PROTOCOL: Verificar Variaveis
def check_env_var(name):
    val = os.environ.get(name)
    if not val:
        logger.error(f"❌ ERRO CRITICO: Variável {name} não encontrada no .env ou sistema")
        return None
    return val

TG_TOKEN = check_env_var("TG_TOKEN")
CHAT_ID = check_env_var("TG_CHAT_ID")
FLN_TOKEN = check_env_var("FLN_OAUTH_TOKEN")
GROQ_API_KEY = check_env_var("GROQ_API_KEY")

bot = telebot.TeleBot(TG_TOKEN) if TG_TOKEN else None
try:
    client_groq = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None
except Exception as e:
    logger.error(f"Erro ao inicializar Groq: {e}")
    client_groq = None

memory_lock = threading.Lock()
MEMORY_FILE = "memory.json"

def escape_html(text):
    if not text: return ""
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def load_memory():
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r", encoding='utf-8') as f:
                return json.load(f)
        except: pass
    return {"current_mission": "corte podcast campeonato videos"}

memory = load_memory()

def gerar_proposta_diego(titulo, desc):
    if not client_groq: return "⚠️ Erro: Groq não configurado."

    # PROMPT DIEGO S-TIER: FOCO CAMPEONATO DE CORTES + FULL ARSENAL
    prompt = f"""Role: Diego, Solutions Architect. Create a technical bid for: {titulo}.
    Description: {desc}.

    SPECIAL FOCUS: O cliente busca vencer um CAMPEONATO DE CORTES.
    Destaque experiência com retenção, hooks virais e pipeline de edição em massa.

    Rules: NO markdown, plain text only, be direct, sign 'Diego'.
    Include MUST-HAVE Technical Arsenal (AGENTS.md):
    - Video: Pipeline Veo 3 + Nano Banana + ElevenLabs.
    - Traffic: CAPI + GTM Server-Side.
    - SEO: GEO + AEO + Knowledge Graph.
    - Content: Técnica Nugget + Information Gain.
    """

    try:
        chat_completion = client_groq.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
            temperature=0.5,
        )
        content = chat_completion.choices[0].message.content
        return content.replace("**", "").replace("###", "").strip()
    except Exception as e:
        return f"Erro Groq: {str(e)}"

def scan_radar():
    logger.info(f"📡 Varrendo mercado por Cortes...")
    query = memory.get("current_mission", "corte podcast campeonato videos")

    if not FLN_TOKEN:
         logger.error("❌ ERRO: FLN_OAUTH_TOKEN ausente. Radar abortado.")
         return

    try:
        session = Session(oauth_token=FLN_TOKEN, url="https://www.freelancer.com")
        search_filter = create_search_projects_filter(sort_field='time_updated', project_types=['fixed'])

        result = search_projects(session, query=query, search_filter=search_filter)

        if result and 'projects' in result:
            for p in result['projects'][:2]:
                pid = str(p.get('id'))

                with memory_lock:
                    if pid in memory: continue

                title = p.get('title')
                seo_url = p.get('seo_url')
                project_link = f"https://www.freelancer.com/projects/{seo_url}" if seo_url else f"https://www.freelancer.com/projects/{pid}"

                logger.info(f"Processando alvo: {title}")
                raw_text = gerar_proposta_diego(title, p.get('preview_description', ''))

                safe_title = escape_html(title)
                safe_text = escape_html(raw_text)

                if bot:
                    markup = InlineKeyboardMarkup()
                    markup.add(InlineKeyboardButton("🔗 Abrir Projeto", url=project_link))
                    markup.add(InlineKeyboardButton("Gerar Nova", callback_data=f"regen_{pid}"))

                    bot.send_message(
                        CHAT_ID,
                        f"🎯 <b>NOVO ALVO ENCONTRADO (CORTES)</b>\n\n📝 <b>Projeto:</b> {safe_title}\n💰 {p.get('budget', {}).get('minimum', '?')} USD\n\n{safe_text}",
                        parse_mode="HTML",
                        reply_markup=markup
                    )

                with memory_lock:
                    memory[pid] = True
                    with open(MEMORY_FILE, "w", encoding='utf-8') as f: json.dump(memory, f)

                time.sleep(2)
    except Exception as e:
        logger.error(f"Erro no Radar (Geral): {e}")

if __name__ == "__main__":
    logger.info("🤖 Jules V17 (Cortes Edition) ONLINE")
    if bot:
        threading.Thread(target=bot.infinity_polling, kwargs={'timeout': 10, 'long_polling_timeout': 5}, daemon=True).start()

    while True:
        scan_radar()
        time.sleep(60)
