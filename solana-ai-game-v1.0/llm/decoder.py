
from pydantic import BaseModel, ValidationError
import random

class SkillCall(BaseModel):
    action: str
    params: dict

def mock_llm_decision(agent: str, context: dict) -> dict:
    # Simulate structured function call output
    options = {
        "tavernkeeper": {"action": "brew_item", "params": {"flavor": "elven"}},
        "miner": {"action": "mine", "params": {"location": "deep_cave"}},
        "thief": {"action": "steal", "params": {"target": "bag"}},
        "guard": {"action": "inspect", "params": {"area": "market"}}
    }
    output = options.get(agent, {"action": "noop", "params": {}})
    try:
        validated = SkillCall(**output)
        return validated.dict()
    except ValidationError as e:
        print("❌ Invalid Skill:", e)
        return {"action": "noop", "params": {}}
