
import json
from llm.decoder import mock_llm_decision
from tools.executor import ToolChainExecutor
from sdk.anchor_client import AnchorZKClient
import yaml

def test_full_agent_flow():
    with open("context/input.json") as f:
        context = json.load(f)
    agent = "tavernkeeper"
    skill = mock_llm_decision(agent, context)

    with open("config/skills.yaml") as f:
        skills = {s["name"]: s for s in yaml.safe_load(f)["skills"]}
    executor = ToolChainExecutor(skills)
    result = executor.execute(skill["action"], "Alice")

    zk = AnchorZKClient()
    proof = zk.store_proof(agent, str(result))
    assert zk.verify_proof(agent, str(result))
    print("✅ [FLOW TEST] PASS:", result)
