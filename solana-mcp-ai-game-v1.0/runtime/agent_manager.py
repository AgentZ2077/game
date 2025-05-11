import asyncio
import logging
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from planner.planner import dispatch

logger = logging.getLogger(__name__)

@dataclass
class AgentContext:
    player_id: str
    environment: Dict[str, Any]
    memory_access: List[str] = None

class AgentManager:
    """
    Manages the lifecycle and execution of game agents.
    Provides concurrent execution and dependency management.
    """
    def __init__(self, agent_config_path: str):
        """Initialize with configuration file path instead of raw list"""
        import yaml
        with open(agent_config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        self.agents = config.get('agents', {})
        self.dependencies = config.get('dependencies', {})
        self.execution_order = self._resolve_execution_order()
        self.results_cache = {}
        
    def _resolve_execution_order(self) -> List[str]:
        """Resolves agent execution order based on dependencies"""
        # Simple topological sort implementation
        visited = set()
        temp_mark = set()
        order = []
        
        def visit(agent):
            if agent in temp_mark:
                raise ValueError(f"Circular dependency detected involving {agent}")
            if agent not in visited:
                temp_mark.add(agent)
                for dep in self.dependencies.get(agent, []):
                    visit(dep)
                temp_mark.remove(agent)
                visited.add(agent)
                order.append(agent)
                
        for agent in self.agents:
            if agent not in visited:
                visit(agent)
                
        return list(reversed(order))
    
    async def run_agent(self, agent: str, context: AgentContext) -> Dict[str, Any]:
        """Execute an agent with proper context and error handling"""
        logger.info(f"Running agent {agent} for player {context.player_id}")
        try:
            result = await dispatch(agent, context.player_id, context.environment)
            self.results_cache[agent] = result
            logger.debug(f"Agent {agent} execution completed: {result}")
            return result
        except Exception as e:
            logger.error(f"Failed to execute agent {agent}: {str(e)}", exc_info=True)
            return {"error": str(e), "agent": agent}
    
    async def run_all(self, player_id: str, environment: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Execute all agents in dependency order with shared context
        Returns consolidated results
        """
        environment = environment or {}
        context = AgentContext(player_id=player_id, environment=environment)
        
        results = {}
        # Execute in dependency order, not randomly
        for agent in self.execution_order:
            results[agent] = await self.run_agent(agent, context)
            # Update environment with results for next agents
            context.environment.update({
                "latest_actions": {agent: results[agent]}
            })
            
        return {
            "player": player_id,
            "timestamp": asyncio.get_event_loop().time(),
            "results": results
        }
    
    async def run_selective(self, agents: List[str], player_id: str, 
                          environment: Dict[str, Any] = None) -> Dict[str, Any]:
        """Run a specific subset of agents"""
        environment = environment or {}
        context = AgentContext(player_id=player_id, environment=environment)
        
        tasks = [self.run_agent(agent, context) for agent in agents 
                if agent in self.agents]
        results = await asyncio.gather(*tasks)
        
        return {
            "player": player_id,
            "agents": agents,
            "results": dict(zip(agents, results))
        }
