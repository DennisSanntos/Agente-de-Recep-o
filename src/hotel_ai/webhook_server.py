from flask import Flask, request
from flask_cors import CORS
from src.hotel_ai.crew import crew
from src.hotel_ai.telegram_bot import send_message
import os

app = Flask(__name__)
CORS(app)

# Armazena update_ids já processados (só durante o uptime atual do app)
processed_updates = set()

@app.route("/webhook", methods=["POST"])
def telegram_webhook():
    data = request.get_json()
    update_id = data.get("update_id")

    # Evita reprocessar a mesma mensagem
    if update_id in processed_updates:
        print(f"⚠️ Ignorando update_id já processado: {update_id}")
        return "Duplicate update", 200
    processed_updates.add(update_id)

    message = data.get("message", {})
    chat_id = message.get("chat", {}).get("id")
    text = message.get("text")

    if not text or not chat_id:
        return "No message", 400

    print(f"📩 Mensagem recebida: {text}")

    try:
        # Executa CrewAI com a mensagem recebida
        result = crew.kickoff(inputs={"mensagem_cliente": text})

        # Envia resposta gerada ao cliente
        send_message(chat_id, result.final_output)
        return "OK", 200

    except Exception as e:
        print(f"❌ Erro no processamento: {e}")
        return "Erro interno", 500
