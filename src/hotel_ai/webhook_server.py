from flask import Flask, request
from flask_cors import CORS  # 🔥 Importa o CORS
from src.hotel_ai.crew import crew
from src.hotel_ai.telegram_bot import send_message
import os

app = Flask(__name__)
CORS(app)  # 🔥 Ativa o CORS para todas as rotas

@app.route("/webhook", methods=["POST"])
def telegram_webhook():
    data = request.get_json()
    message = data.get("message", {})
    chat_id = message.get("chat", {}).get("id")
    text = message.get("text")

    if not text or not chat_id:
        return "No message", 400

    print(f"📩 Mensagem recebida: {text}")

    # Executa CrewAI com a mensagem recebida
    result = crew.kickoff(inputs={"mensagem_cliente": text})

    # Envia resposta gerada ao cliente
    send_message(chat_id, result.output)

    return "OK", 200
