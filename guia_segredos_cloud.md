# 🗝️ Guia de Segredos do Arsenal S-Tier (Cloud Edition)

Para que a operação funcione 24/7 na Nuvem (GitHub Actions + VPS), as seguintes variáveis de ambiente devem ser configuradas:

## 1. Inteligência Artificial (Diego's Brain)
- \`GEMINI_API_KEY\`: Chave da API do Google AI Studio (Pro ou Flash).
- \`GROQ_API_KEY\`: Chave da API da Groq (para LLaMA 3 ultra-rápido).

## 2. Comunicação e Comando (Telegram)
- \`TG_TOKEN\`: Token do Bot (via @BotFather).
- \`TG_CHAT_ID\`: ID do seu chat ou grupo de comando.

## 3. Fontes de Leads (Freelancer.com / Meta)
- \`FLN_OAUTH_TOKEN\`: Token de acesso OAuth da Freelancer.com.
- \`INSTAGRAM_ACCESS_TOKEN\`: Token de usuário com permissão \`instagram_basic\` e \`instagram_content_publish\`.
- \`INSTAGRAM_USER_ID\`: ID da conta comercial do Instagram vinculada à página do Facebook.

## 4. Blindagem Ghost (Proxy)
- \`HTTP_PROXY\`: Formato \`http://usuario:senha@ip:porta\`.
- \`HTTPS_PROXY\`: Formato \`http://usuario:senha@ip:porta\`.

> **Nota:** No GitHub Actions, configure em *Settings > Secrets and variables > Actions*. Na VPS, utilize um arquivo \`.env\` blindado.
