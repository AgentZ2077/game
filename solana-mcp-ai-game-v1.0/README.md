
# 🚀 Solana AI Game Protocol v1.0.0-alpha5

Final alpha release with full pipeline: Agent → Skill → zkVerifier → UI

## 🧠 Features

- Structured LLM Prompt decoder using `pydantic`
- zkVerifier Anchor contract (Rust) + mock SDK + IDL JSON
- MemoryGraph shared between agents
- Agent Loop simulates multi-agent game logic
- FastAPI backend serving agent zk logs
- Chart.js UI Timeline + zkHash analytics

## 🧪 Run Tests

```bash
pytest tests/test_multiagent.py
pytest tests/test_anchor.py
```

## 🔁 Run Simulation

```bash
python runtime/agent_loop.py
uvicorn api.server:app --reload
```

Then open `frontend/index.html` to visualize.

## 📜 Anchor zkVerifier Contract

```bash
cd programs/zkVerifier
anchor build
anchor deploy
```

IDL: `programs/zkVerifier/target/idl/zkVerifier.json`
