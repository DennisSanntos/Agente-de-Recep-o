from crewai_tools import tool
import requests
import os

@tool("Registrar solicitação no Baserow")
def registrar_baserow(data: dict) -> str:
    """
    Registra uma nova solicitação na tabela do Baserow (ID: 599992).
    """
    token = os.getenv("BASEROW_API_TOKEN")
    if not token:
        return "Erro: variável de ambiente BASEROW_API_TOKEN não definida."

    url = "https://api.baserow.io/api/database/rows/table/599992/?user_field_names=false"

    payload = {
        "field_4858851": data.get("nome", "Não informado"),
        "field_4858852": data["mensagem"],
        "field_4858860": data["nivel"],
        "field_4858862": data["departamento"],
        "field_4858863": "Aberto"
    }

    headers = {
        "Authorization": f"Token {token}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        return "✅ Solicitação registrada com sucesso no Baserow."
    else:
        return f"❌ Erro ao registrar no Baserow: {response.text}"
