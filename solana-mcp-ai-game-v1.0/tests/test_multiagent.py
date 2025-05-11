
from memory.graph import MemoryGraph

def test_memory_sharing():
    mem = MemoryGraph()
    mem.add_memory("town-square", "thief", "stole a purse")
    mem.add_memory("town-square", "guard", "noticed suspicious movement")
    recent = mem.get_recent("town-square")
    assert len(recent) == 2
    assert recent[0]["agent"] == "thief"
    print("✅ Multi-agent memory test passed")
