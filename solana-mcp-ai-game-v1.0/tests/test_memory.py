
from memory.zk_memory import MemoryZK

def test_memory_hashing():
    zk = MemoryZK()
    h1 = zk.store("agent1", "Alice likes elven_wine")
    assert zk.verify("agent1", "Alice likes elven_wine")
    assert not zk.verify("agent1", "Wrong memory")
