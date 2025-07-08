from crewai import Agent, Task
import yaml
from pathlib import Path
from src.hotel_ai.tools.custom_tool import registrar_baserow

TOOLS = [registrar_baserow]

def load_yaml(path):
    with open(path, 'r') as file:
        return yaml.safe_load(file)

# Corrigindo o caminho dos arquivos YAML
CONFIG_DIR = Path(__file__).parent / "config"

agent_data = load_yaml(CONFIG_DIR / "agents.yaml")
task_data = load_yaml(CONFIG_DIR / "tasks.yaml")

agents = {
    name: Agent(
        role=cfg["role"],
        goal=cfg["goal"],
        backstory=cfg["backstory"],
        verbose=True,
        tools=TOOLS
    )
    for name, cfg in agent_data.items()
}

tasks = {
    name: Task(
        description=cfg["description"],
        expected_output=cfg["expected_output"],
        agent=agents[name.split("_task")[0]],
    )
    for name, cfg in task_data.items()
}
