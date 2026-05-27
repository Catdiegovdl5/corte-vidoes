import os
import time
import requests
import logging

# Configuração de Logs
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("InstaCommander")

class InstagramUploader:
    """
    Comandante de Upload de Reels via Facebook Graph API.
    Focado em invisibilidade, velocidade e conformidade com o 'Sindicato Enterprise'.
    """

    def __init__(self, access_token=None, ig_user_id=None, proxy=None):
        self.access_token = access_token or os.environ.get("INSTAGRAM_ACCESS_TOKEN")
        self.ig_user_id = ig_user_id or os.environ.get("INSTAGRAM_USER_ID")
        self.base_url = "https://graph.facebook.com/v19.0"

        # Suporte a Proxy para Blindagem Ghost Mode
        self.proxies = None
        proxy_url = proxy or os.environ.get("HTTP_PROXY") or os.environ.get("HTTPS_PROXY")
        if proxy_url:
            self.proxies = {
                "http": proxy_url,
                "https": proxy_url
            }
            logger.info(f"🛡️ Blindagem Proxy Ativada para Upload.")

        if not self.access_token or not self.ig_user_id:
            logger.warning("⚠️ Credenciais da Meta ausentes. O modo 'Fantasma' pode falhar.")

    def upload_reels(self, video_url, caption):
        """
        Executa o protocolo de upload em 3 fases: Container -> Status -> Publish.
        """
        try:
            logger.info("🚀 Iniciando Protocolo de Upload: Trincheira 1")

            # Fase 1: Criar o Container de Mídia (Reels)
            container_id = self._create_container(video_url, caption)
            if not container_id:
                return False

            # Fase 2: Monitorar Processamento (Status Check)
            if not self._wait_for_processing(container_id):
                return False

            # Fase 3: Publicação Oficial (The "Go" Signal)
            media_id = self._publish_media(container_id)
            if media_id:
                logger.info(f"✅ MISSÃO CUMPRIDA! Reels publicado com sucesso. ID: {media_id}")
                return media_id

            return False

        except Exception as e:
            logger.error(f"❌ Falha Crítica no Comando: {str(e)}")
            return False

    def _create_container(self, video_url, caption):
        """Cria o container inicial para o vídeo."""
        url = f"{self.base_url}/{self.ig_user_id}/media"
        payload = {
            'media_type': 'REELS',
            'video_url': video_url,
            'caption': caption,
            'access_token': self.access_token
        }

        response = requests.post(url, data=payload, proxies=self.proxies)
        data = response.json()

        if 'id' in data:
            logger.info(f"📦 Container criado: {data['id']}")
            return data['id']
        else:
            logger.error(f"❌ Erro ao criar container: {data}")
            return None

    def _wait_for_processing(self, container_id):
        """Monitora o status do processamento do vídeo na Meta."""
        url = f"{self.base_url}/{container_id}"
        params = {
            'fields': 'status_code,status',
            'access_token': self.access_token
        }

        max_retries = 30
        for i in range(max_retries):
            response = requests.get(url, params=params, proxies=self.proxies)
            data = response.json()
            status = data.get('status_code')

            if status == 'FINISHED':
                logger.info("⚡ Processamento Finalizado (Status: FINISHED)")
                return True
            elif status == 'ERROR':
                logger.error(f"❌ Erro no processamento da Meta: {data}")
                return False

            logger.info(f"⏳ Processando... ({i+1}/{max_retries}) - Status: {status}")
            time.sleep(10)

        logger.error("❌ Timeout: O vídeo demorou demais para processar.")
        return False

    def _publish_media(self, container_id):
        """Publica o container processado."""
        url = f"{self.base_url}/{self.ig_user_id}/media_publish"
        payload = {
            'creation_id': container_id,
            'access_token': self.access_token
        }

        response = requests.post(url, data=payload, proxies=self.proxies)
        data = response.json()

        if 'id' in data:
            return data['id']
        else:
            logger.error(f"❌ Erro na publicação final: {data}")
            return None

if __name__ == "__main__":
    uploader = InstagramUploader()
