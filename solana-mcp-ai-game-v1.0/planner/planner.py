
import yaml
from tools.executor import ToolChainExecutor

def dispatch(agent_type: str, player_id: str):
    with open("config/skills.yaml") as f:
        skills_config = {s["name"]: s for s in yaml.safe_load(f)["skills"]}
    with open("config/agent_rules.yaml") as f:
        rules = yaml.safe_load(f)["agents"]
    if agent_type not in rules:
        return {"error": "unknown agent"}
    chain = rules[agent_type].get("behavior", [])
    executor = ToolChainExecutor(skills_config)
    results = []
    for skill_name in chain:
        result = executor.execute(skill_name, player_id)
        results.append(result)
    return {"agent": agent_type, "player": player_id, "actions": results}
