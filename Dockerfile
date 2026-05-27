FROM python:3.12-slim

# Evita arquivos .pyc e permite logs em tempo real
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Instala dependências do sistema necessárias para MoviePy e OpenCV
RUN apt-get update && apt-get install -y --no-install-recommends     build-essential     ffmpeg     libsm6     libxext6     && rm -rf /var/lib/apt/lists/*

# Instala dependências do Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código fonte
COPY . .

# Comando padrão: Inicia o Cloud Factory (Modo VPS 24/7)
CMD ["python", "cloud_factory.py"]
