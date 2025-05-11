
import hashlib

class AnchorZKClient:
    def __init__(self):
        self.chain_memory = {}

    def store_proof(self, agent_id, memory_str):
        digest = hashlib.sha256(memory_str.encode()).hexdigest()
        self.chain_memory[agent_id] = digest
        return digest

    def verify_proof(self, agent_id, value):
        digest = hashlib.sha256(value.encode()).hexdigest()
        return self.chain_memory.get(agent_id) == digest
