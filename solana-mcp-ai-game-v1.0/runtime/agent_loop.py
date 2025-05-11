
from llm.decoder import mock_llm_decision
from tools.executor import ToolChainExecutor
from sdk.anchor_client import AnchorZKClient
from memory.graph import MemoryGraph
import yaml
import json
import random

def simulate_agents():
    agents = ["thief", "guard"]
    context = {"env": "town-square", "time": "14:00"}
    mem = MemoryGraph()

    with open("config/skills.yaml") as f:
        skills = {s["name"]: s for s in yaml.safe_load(f)["skills"]}
    executor = ToolChainExecutor(skills)
    zk = AnchorZKClient()

    logs = []

    for _ in range(3):
        for agent in agents:
            skill = mock_llm_decision(agent, context)
            result = executor.execute(skill["action"], agent)
            proof = zk.store_proof(agent, str(result))
            mem.add_memory("town-activity", agent, result)

            logs.append({
                "agent": agent,
                "skill": skill["action"],
                "params": skill["params"],
                "zk_hash": proof,
                "time": time.strftime("%H:%M:%S")
            })
    with open("data/log.jsonl", "w") as f:
        for log in logs:
            f.write(json.dumps(log) + "\n")
