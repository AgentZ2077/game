
from collections import defaultdict
import time
from typing import Dict, List, Any, Optional, Set, Tuple
from dataclasses import dataclass, field
import json
import logging
from datetime import datetime
import uuid

logger = logging.getLogger(__name__)

@dataclass
class MemoryEntry:
    agent_id: str
    content: Any
    timestamp: float = field(default_factory=time.time)
    entry_id: str = field(default_factory=lambda: uuid.uuid4().hex)
    tags: Set[str] = field(default_factory=set)
    references: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to serializable dictionary"""
        return {
            "id": self.entry_id,
            "agent": self.agent_id,
            "content": self.content,
            "timestamp": self.timestamp,
            "datetime": datetime.fromtimestamp(self.timestamp).isoformat(),
            "tags": list(self.tags),
            "references": self.references
        }

class MemoryGraph:
    """
    Advanced memory graph implementation with indexing, querying,
    and persistence capabilities.
    """
    def __init__(self, persist_path: Optional[str] = None):
        self._topics = defaultdict(list)
        self._agent_index = defaultdict(list)  # Agent -> entry_ids
        self._tag_index = defaultdict(set)     # Tag -> entry_ids
        self._entry_map = {}                   # entry_id -> Entry
        self._persist_path = persist_path
        
        if persist_path:
            self._load_from_disk()
    
    def add_memory(self, topic: str, agent: str, content: Any, 
                  tags: Optional[List[str]] = None) -> MemoryEntry:
        """Add a memory entry with optional tags"""
        tags = set(tags or [])
        entry = MemoryEntry(agent_id=agent, content=content, tags=tags)
        
        # Store in primary topic collection
        self._topics[topic].append(entry.entry_id)
        
        # Update indices
        self._agent_index[agent].append(entry.entry_id)
        for tag in tags:
            self._tag_index[tag].add(entry.entry_id)
        
        # Store the actual entry
        self._entry_map[entry.entry_id] = entry
        
        # Persist if configured
        if self._persist_path:
            self._persist_to_disk()
            
        logger.debug(f"Added memory: {topic} / {agent} / {entry.entry_id}")
        return entry
    
    def connect_memories(self, source_id: str, target_id: str) -> bool:
        """Create a reference between two memory entries"""
        if source_id not in self._entry_map or target_id not in self._entry_map:
            return False
            
        self._entry_map[source_id].references.append(target_id)
        if self._persist_path:
            self._persist_to_disk()
        return True
    
    def get_topic(self, topic: str) -> List[MemoryEntry]:
        """Get all memories for a topic"""
        entry_ids = self._topics.get(topic, [])
        return [self._entry_map[eid] for eid in entry_ids if eid in self._entry_map]
    
    def get_recent(self, topic: str, limit: int = 3) -> List[MemoryEntry]:
        """Get most recent memories for a topic"""
        entries = self.get_topic(topic)
        return sorted(entries, key=lambda x: x.timestamp, reverse=True)[:limit]
    
    def query(self, 
             topics: Optional[List[str]] = None,
             agents: Optional[List[str]] = None, 
             tags: Optional[List[str]] = None,
             time_range: Optional[Tuple[float, float]] = None,
             limit: int = 100) -> List[MemoryEntry]:
        """
        Advanced query with multiple filters
        Returns entries that match ALL specified criteria
        """
        # Start with all entry IDs
        result_set = set(self._entry_map.keys())
        
        # Filter by topic
        if topics:
            topic_entries = set()
            for topic in topics:
                topic_entries.update(self._topics.get(topic, []))
            result_set &= topic_entries
            
        # Filter by agent
        if agents:
            agent_entries = set()
            for agent in agents:
                agent_entries.update(self._agent_index.get(agent, []))
            result_set &= agent_entries
        
        # Filter by tag (require all tags)
        if tags:
            tag_entries = set.intersection(
                *[self._tag_index.get(tag, set()) for tag in tags]
            )
            result_set &= tag_entries
        
        # Convert to entries
        results = [self._entry_map[eid] for eid in result_set if eid in self._entry_map]
        
        # Filter by time range
        if time_range:
            start, end = time_range
            results = [e for e in results if start <= e.timestamp <= end]
        
        # Sort by timestamp (newest first) and limit
        results.sort(key=lambda x: x.timestamp, reverse=True)
        return results[:limit]
    
    def _persist_to_disk(self) -> None:
        """Save memory state to disk"""
        try:
            with open(self._persist_path, 'w') as f:
                export_data = {
                    "topics": {k: v for k, v in self._topics.items()},
                    "entries": {k: v.to_dict() for k, v in self._entry_map.items()}
                }
                json.dump(export_data, f)
        except Exception as e:
            logger.error(f"Failed to persist memory graph: {str(e)}")
    
    def _load_from_disk(self) -> None:
        """Load memory state from disk"""
        try:
            with open(self._persist_path, 'r') as f:
                data = json.load(f)
                
                # Restore topics
                self._topics = defaultdict(list, data.get("topics", {}))
                
                # Restore entries and rebuild indices
                for entry_id, entry_data in data.get("entries", {}).items():
                    entry = MemoryEntry(
                        entry_id=entry_id,
                        agent_id=entry_data["agent"],
                        content=entry_data["content"],
                        timestamp=entry_data["timestamp"],
                        tags=set(entry_data.get("tags", [])),
                        references=entry_data.get("references", [])
                    )
                    self._entry_map[entry_id] = entry
                    
                    # Rebuild indices
                    self._agent_index[entry.agent_id].append(entry_id)
                    for tag in entry.tags:
                        self._tag_index[tag].add(entry_id)
                        
            logger.info(f"Loaded memory graph from {self._persist_path}: "
                      f"{len(self._entry_map)} entries across {len(self._topics)} topics")
        except FileNotFoundError:
            logger.info(f"No existing memory file at {self._persist_path}, starting fresh")
        except Exception as e:
            logger.error(f"Failed to load memory graph: {str(e)}")
