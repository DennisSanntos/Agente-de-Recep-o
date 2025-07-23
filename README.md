# Hotel AI - Agente de Recepção Inteligente

Projeto construído com [CrewAI](https://github.com/joaomdmoura/crewai) para automatizar o atendimento de hóspedes via Telegram.

## Funcionalidades

- Classificação de mensagens por departamento e nível de complexidade
- Registro de solicitações no Baserow por meio de uma ferramenta personalizada
- Geração de respostas personalizadas ao cliente
- Integração com Telegram para recebimento e envio de mensagens
- Suporte a mensagens de voz com transcrição automática via OpenAI Whisper
- Buffer de 15&nbsp;segundos para agrupar mensagens antes do processamento
- Configuração de agentes e tarefas por arquivos YAML
- Execução da pipeline de agentes em sequência com CrewAI

## Como usar

1. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

2. Defina as variáveis de ambiente obrigatórias:

   - `TELEGRAM_BOT_TOKEN` – token do bot do Telegram
   - `OPENAI_API_KEY` – chave da OpenAI para transcrição de áudio
   - `BASEROW_API_TOKEN` – token para registrar solicitações no Baserow

3. Execute localmente para testes rápidos:

   ```bash
   python src/hotel_ai/main.py
   ```

4. Para rodar o servidor de webhook:

   ```bash
   gunicorn src.hotel_ai.webhook_server:app
   ```
