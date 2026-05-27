import time
import logging
import os
from start_jumbo_factory import run_factory

# Configuração Master de Log para Cloud
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("CloudJumbo")

def cloud_scheduler():
    """
    Executa a Fábrica Jumbo em loop infinito para VPS/Ghost Mode.
    Frequência recomendada: 4x ao dia (6h em 6h).
    """
    interval_hours = int(os.environ.get("JUMBO_INTERVAL_HOURS", 6))
    interval_seconds = interval_hours * 3600

    logger.info(f"🚀 Cloud Factory Ativada! Operando em Ghost Mode 24/7.")
    logger.info(f"⏰ Frequência de Operação: A cada {interval_hours} horas.")

    while True:
        try:
            run_factory()
            logger.info(f"⏳ Missão concluída. Entrando em modo 'Sleep' por {interval_hours} horas.")
            time.sleep(interval_seconds)
        except Exception as e:
            logger.error(f"❌ Erro Crítico na Cloud Factory: {e}")
            logger.info("Retentando em 1 hora...")
            time.sleep(3600)

if __name__ == "__main__":
    cloud_scheduler()
