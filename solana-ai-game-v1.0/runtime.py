
from fastapi import FastAPI, Request
from planner.planner import dispatch

app = FastAPI()

@app.post("/mcp/context")
async def mcp_entry(req: Request):
    body = await req.json()
    agent = body.get("agent")
    player = body.get("player", "anonymous")
    result = dispatch(agent, player)
    return result
