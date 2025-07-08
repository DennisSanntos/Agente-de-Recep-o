from .crew import crew

if __name__ == "__main__":
    result = crew.kickoff(inputs={
        "mensagem_cliente": "A luz do quarto 302 está piscando constantemente, por favor verifiquem."
    })

    print(result)
