
from sdk.anchor_client import AnchorZKClient

def test_anchor_mock_storage():
    anchor = AnchorZKClient()
    agent_id = "tavernkeeper"
    memory = "Brewed Elven Wine at 3PM"

    hash1 = anchor.store_proof(agent_id, memory)
    assert anchor.verify_proof(agent_id, memory)
    assert not anchor.verify_proof(agent_id, memory + "tampered")

    print("✅ Anchor zkVerifier mock passed:", hash1)
