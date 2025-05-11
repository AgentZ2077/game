# 🧠 Solana-MCP: Modular AI Agent Runtime for On-Chain Games

Solana-MCP is a modular, composable runtime for AI agents in Web3 games.  
It enables autonomous NPCs to interact with players, generate quests, manage inventory, and write blockchain-proofed memory — all powered by large language models and verified via zk proofs.

> “We’re not building a game. We’re building the operating system for all AI games.”

---

## 🎮 Project Vision

In the AI + Web3 future, games will no longer be hardcoded scripts. NPCs will:
- Think like real agents using LLMs
- Read/write on-chain memory
- Interact with each other
- Mint items, generate quests, and trade autonomously

Solana-MCP provides the **standard protocol runtime** for this new generation of AI-driven games — starting with Solana.

---

## ✨ Key Features

| Module            | Description                                                                 |
|-------------------|-----------------------------------------------------------------------------|
| 🤖 Agent Runtime   | Multi-agent orchestration (thief, guard, tavernkeeper, miner...)            |
| 🧠 MemoryGraph     | Shared DAG-style memory for cross-agent communication                       |
| 📡 MCP Interface   | Unified API between agents and Solana blockchain via structured calls       |
| 📜 zkVerifier      | Anchor-compatible Solana contract for on-chain behavior verification         |
| 🧪 Toolchain       | Structured Prompt decoder + Pydantic schema for function-calling LLMs       |
| 📊 UI Runtime      | Frontend timeline viewer with zk stats and agent logs (Chart.js)            |

---

## 📦 Directory Structure

```bash
.
├── api/              # FastAPI server for frontend log access
├── frontend/         # Web UI to visualize agent timeline + zk analytics
├── llm/              # LLM decoder using schema validation
├── memory/           # DAG-based memory graph manager
├── programs/zkVerifier  # Anchor contract for zk proof verification
├── runtime/          # Agent loop simulation with MCP logic
├── sdk/              # Mock client for zkVerifier program
├── tests/            # pytest-based flow test suite
└── data/             # Behavior logs (JSONL)
