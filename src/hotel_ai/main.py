from .crew import crew

if __name__ == "__main__":
    while True:
        entrada = input("Mensagem do cliente: ")
        result = crew.kickoff(inputs={"mensagem_cliente": entrada})
        print(f"\nResposta gerada:\n{result}\n")
