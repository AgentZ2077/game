
# 🧠 Solana AI Game Protocol

> Modular AI + MCP Runtime for On-Chain Games  
> **Solana-native infrastructure powering AI agents** with verifiable behavior, composable toolchains, and zk memory validation.

---

## 🌐 Vision

We aim to create the **"Operating System for AI Games"**, not just a game.  
By combining MCP, AI Agent Runtime, and Solana’s high-throughput environment, we offer:

- 🧱 Modular game logic via on-chain contracts
- 🤖 Autonomous AI agents (Tavernkeeper, Miner, etc.)
- 🛠 Dynamic skill system (ToolChain)
- 🔐 Verifiable memory via zkVerifier (Anchor-based)

---

## 🔩 Protocol Architecture

```
Player → Agent Runtime → ToolChain → MCP Interface → Solana Contracts
```

- **Agent Runtime**: Handles decision loop and context
- **ToolChain**: Dynamically called skills (brew, mine, etc.)
- **MCP Interface**: Structured I/O between AI ↔ chain
- **Contracts**: Modular Solana programs for state, NFTs, and zk proof

---

## 🤖 AI Agents (Demo)

| Agent       | Description                                  |
|-------------|----------------------------------------------|
| 🧙‍♂️ `Tavernkeeper` | Offers drink, greets based on player data        |
| ⛏ `Miner`          | Mines random minerals and evaluates market price |

✅ Agents can be selected via `agent_registry.py` or frontend dropdown.

---

## 🛠 ToolChain Skills

| Skill              | Purpose                                      |
|--------------------|----------------------------------------------|
| `generate_greeting`| Personalized greeting per player             |
| `check_inventory`  | Simulated inventory query                    |
| `brew_item`        | Mint drink NFTs dynamically                  |
| `mine`             | Extract minerals and mint NFTs               |
| `evaluate_profit`  | Simulate market value (0.3 ~ 5 SOL)          |

---

## 🔐 zkVerifier (Solana Anchor)

📦 Path: `contracts/zk_verifier`  
Solana-native module for storing/verifying AI agent memory hashes.

### Rust API

```rust
pub fn store_memory_hash(ctx, hash: [u8; 32])     // Store hashed memory
pub fn verify_proof(ctx, provided: [u8; 32])      // Compare with on-chain hash
```

### Deploy with Anchor CLI

```bash
cd contracts/zk_verifier
anchor build
anchor deploy --provider.cluster devnet
```

---

## 🧪 Python SDK (zk.py)

Python utilities for interacting with zkVerifier contract.

```python
from sdk.zk import build_store_tx, build_verify_tx

tx1 = build_store_tx(client, signer, memory_data="playerX:used_elven_wine")
tx2 = build_verify_tx(client, signer, memory_data="playerX:used_elven_wine")
```

---

## 🚀 Run Locally

```bash
# Launch backend
uvicorn runtime.multi_agent_server:app --reload

# Open frontend
file://frontend/index.html
```

- Choose Agent (Tavernkeeper or Miner)
- Click "Send Context" to simulate decision + action
- Backend will simulate AI ↔ ToolChain ↔ MCP ↔ Solana flow

---

## 📦 File Structure

```
solana-ai-game/
├── runtime/            # AI Agent & ToolChain Runtime
│   ├── agent_registry.py
│   ├── tavernkeeper.py
│   ├── miner.py
│   └── toolchain.py
├── contracts/
│   └── zk_verifier/    # Anchor zk contract
├── sdk/
│   └── zk.py           # Python zkVerifier SDK
├── frontend/           # Simple demo HTML client
└── README.md
```

---

## 🧬 Next Steps

- [ ] Add more AI agents (e.g., Blacksmith, Guard, Oracle)
- [ ] Modular `modules/registry.json` for plug-and-play behaviors
- [ ] zkSNARK proof for off-chain LLM safety validation
- [ ] Solana NFT + compressed NFT integration
- [ ] PyPI / npm SDK publishing

---

© 2025 DrateRepare — Pioneering the AI x On-Chain Game World 🌐
