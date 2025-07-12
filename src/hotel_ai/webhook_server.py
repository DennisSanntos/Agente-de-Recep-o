from flask import Flask, request
from flask_cors import CORS
from src.hotel_ai.crew import crew
from src.hotel_ai.telegram_bot import send_message
import os
import requests
import threading
import time
import openai

app = Flask(__name__)
CORS(app)

# Armazena update_ids já processados
processed_updates = set()

# Buffer de mensagens por chat_id
message_buffer = {}
buffer_timers = {}

# Configurações
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WHISPER_MODEL = "whisper-1"  # Whisper API
BUFFER_TIMEOUT = 15  # segundos

# 📥 Baixa o arquivo de áudio do Telegram
def download_voice_file(file_id):
    file_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getFile?file_id={file_id}"
    file_info = requests.get(file_url).json()
    file_path = file_info["result"]["file_path"]
    file_download_url = f"https://api.telegram.org/file/bot{TELEGRAM_BOT_TOKEN}/{file_path}"
    response = requests.get(file_download_url)
    return response.content

# 🎙️ Transcreve o áudio usando OpenAI Whisper API
def transcribe_audio(audio_bytes):
    audio_file = ("audio.ogg", audio_bytes)
    response = openai.Audio.transcribe(
        model=WHISPER_MODEL,
        file=audio_file,
        response_format="text"
    )
    return response.strip()

# 🚀 Processa o buffer quando o tempo expira
def process_buffer(chat_id):
    messages = message_buffer.get(chat_id, [])
    if not messages:
        return

    full_message = " ".join(messages)
    print(f"💬 Processando mensagem composta: {full_message}")

    try:
        result = crew.kickoff(inputs={"mensagem_cliente": full_message})
        
        # ✅ Usa 'result.output' (v0.13.4)
        response_text = result.output

        send_message(chat_id, response_text)
    except Exception as e:
        print(f"❌ Erro ao processar buffer: {e}")
        send_message(chat_id, "Ocorreu um erro ao processar sua solicitação.")

    # Limpa buffers
    message_buffer.pop(chat_id, None)
    buffer_timers.pop(chat_id, None)


@app.route("/webhook", methods=["POST"])
def telegram_webhook():
    data = request.get_json()
    update_id = data.get("update_id")

    # 🔁 Evita reprocessamento
    if update_id in processed_updates:
        print(f"⚠️ Ignorando update_id já processado: {update_id}")
        return "Duplicate update", 200
    processed_updates.add(update_id)

    message = data.get("message", {})
    chat_id = message.get("chat", {}).get("id")

    if not chat_id:
        return "Missing chat_id", 400

    try:
        if "text" in message:
            text = message["text"]
            print(f"📝 Texto recebido: {text}")

        elif "voice" in message:
            print("🎤 Mensagem de voz recebida")
            file_id = message["voice"]["file_id"]
            audio_bytes = download_voice_file(file_id)
            text = transcribe_audio(audio_bytes)
            print(f"📝 Transcrição: {text}")

        else:
            print("⚠️ Tipo de mensagem não suportado")
            return "Unsupported message type", 200

        # ⏳ Adiciona mensagem ao buffer
        if chat_id not in message_buffer:
            message_buffer[chat_id] = []
        message_buffer[chat_id].append(text)

        # Reinicia o timer
        if chat_id in buffer_timers:
            buffer_timers[chat_id].cancel()

        timer = threading.Timer(BUFFER_TIMEOUT, process_buffer, args=[chat_id])
        buffer_timers[chat_id] = timer
        timer.start()

        return "Mensagem recebida", 200

    except Exception as e:
        print(f"❌ Erro no webhook: {e}")
        return "Erro interno", 500
