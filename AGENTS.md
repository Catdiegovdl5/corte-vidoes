# Proposals Architect S-Tier - AGENTS.md

## Persona
Your role is to analyze project descriptions and generate proposals using **Reverse Engineering** to focus on the client's pain points.

## Technical Arsenal
Whenever relevant, incorporate the following:
- **Video:** Pipeline Veo 3 + Nano Banana (Fidelidade 4K) + ElevenLabs (Sound Design).
- **Traffic:** CAPI (Conversions API) + GTM Server-Side + Estratégia de Atribuição Avançada.
- **SEO:** GEO (Generative Engine Optimization) + AEO (Answer Engine Optimization) + Knowledge Graph @graph.
- **Content:** Técnica Nugget (Answer-First) + Information Gain (E-E-A-T).

## Platform Differentiation Filters
- **Freelancer.com:**
  - Focus: Speed and Technical Response.
  - Features: Tables for "Test Keywords" or "Milestones".
  - Language: English.
- **99Freelas:**
  - Focus: ROI and Consultancy.
  - Features: Partner tone, mention "Projeto Piloto".
  - Language: Portuguese.
- **Upwork:**
  - Focus: Seniority and Case Studies.
  - Features: Deep technical responses to "Screening Questions".
  - Language: English.

## Automation Tool
Use `src/proposal_generator.py` to automate the generation of these proposals.
To run it:
```bash
python3 src/proposal_generator.py --platform <platform> --description "<project_description>"
```

## Global Sentinel (Automated Workflow)
The system is equipped with a Global Sentinel (`sentinel.py`) that runs automatically via GitHub Actions every 15 minutes.

### How it works:
1. **GitHub Action:** Scans feeds and alerts (simulated in `sentinel.py`).
2. **Jules (Gemini API):** Processes leads and generates proposals using the S-Tier Technical Arsenal.
3. **Commit:** Results are saved to `leads_ready.json` in the repository.
4. **Opal Dashboard:** You can connect your Opal Dashboard to the raw JSON URL of `leads_ready.json`:
   `https://raw.githubusercontent.com/<USER>/<REPO>/main/leads_ready.json`

### Setup:
- Add your `GEMINI_API_KEY` to GitHub Repository Secrets.
- Ensure the GitHub Action has write permissions to the repository.

## Trincheira 2: Ascensão à Nuvem (Cloud Edition)
O arsenal está pronto para operação autônoma 24/7.
- **Workflow:** GitHub Actions configurado para varredura a cada 15 min (\`.github/workflows/sentinel.yml\`).
- **Container:** \`Dockerfile\` universal para deploy em VPS.
- **Blindagem Ghost Mode:** Suporte a Proxy Residencial em todos os módulos de rede.
- **Secrets:** Chaves de API e tokens centralizados via Env Vars (ver \`guia_segredos_cloud.md\`).

## Projeto Jumbo: Operação Raiam Santos (Fábrica de Cortes)
O arsenal agora inclui uma linha de produção automatizada para o canal do Raiam Santos.
- **Hunter:** \`src/youtube_hunter.py\` (yt-dlp para caçar vídeos virais).
- **Processor:** \`src/video_processor.py\` (Whisper + MoviePy para cortes 9:16 e legendas).
- **Style:** \`src/caption_generator.py\` (Persona Diego refinada para tom provocativo/Raiam).
- **Orchestrator:** \`start_jumbo_factory.py\` (Comando único para rodar toda a fábrica).

### Comando Master para o Lenovo IdeaPad:
\`\`\`bash
python3 start_jumbo_factory.py
\`\`\`

## Arsenal de Vídeo: Ultra-Intelligence (Cortes do Raiam)
O sistema agora possui visão computacional e análise semântica.
- **AI Analyst:** \`src/ai_analyst.py\` (Identifica momentos de alto impacto via LLM).
- **Auto-Reframe:** \`src/video_processor.py\` (Detecta o rosto do Raiam via MediaPipe e mantém centralizado em 9:16).
- **Workflow:** Download -> Transcrição -> Análise Semântica -> Auto-Reframe -> Legenda Viral.
