
import asyncio
from planner.planner import dispatch

class AgentManager:
    def __init__(self, agent_list):
        self.agents = agent_list

    async def run_agent(self, agent, player):
        print(f"Running {agent} for {player}...")
        result = dispatch(agent, player)
        print(f"{agent} result: {result}")

    async def run_all(self):
        await asyncio.gather(*[self.run_agent(agent, "Alice") for agent in self.agents])

# For test run
if __name__ == "__main__":
    manager = AgentManager(["tavernkeeper", "miner"])
    asyncio.run(manager.run_all())
