
import hashlib

class MemoryZK:
    def __init__(self):
        self._memory = {}

    def store(self, key, data):
        hashed = hashlib.sha256(data.encode()).hexdigest()
        self._memory[key] = hashed
        return hashed

    def verify(self, key, compare_data):
        compare_hash = hashlib.sha256(compare_data.encode()).hexdigest()
        return self._memory.get(key) == compare_hash
