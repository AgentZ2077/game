
from collections import defaultdict
import time

class MemoryGraph:
    def __init__(self):
        self.memory = defaultdict(list)

    def add_memory(self, topic, agent, content):
        entry = {
            "agent": agent,
            "content": content,
            "timestamp": time.strftime("%H:%M:%S")
        }
        self.memory[topic].append(entry)
        return entry

    def get_topic(self, topic):
        return self.memory.get(topic, [])

    def get_recent(self, topic, limit=3):
        return self.memory.get(topic, [])[-limit:]
