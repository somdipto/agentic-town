#!/usr/bin/env python3
"""
AI Town - A virtual town where AI characters live, chat and socialize.
Inspired by a16z-infra/ai-town and convex.dev/ai-town
"""

import json
import uuid
import random
import time
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
import threading
import requests
from dataclasses import dataclass, asdict
from enum import Enum

class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)
    STAY = (0, 0)

class BuildingType(Enum):
    HOUSE = "house"
    CAFE = "cafe"
    PARK = "park"
    SHOP = "shop"
    OFFICE = "office"

@dataclass
class Position:
    x: int
    y: int
    
    def distance_to(self, other: 'Position') -> float:
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5
    
    def move_towards(self, target: 'Position', max_distance: int = 1) -> 'Position':
        """Move towards target position by max_distance units."""
        dx = target.x - self.x
        dy = target.y - self.y
        distance = (dx ** 2 + dy ** 2) ** 0.5
        
        if distance <= max_distance:
            return target
        
        if distance == 0:
            return self
            
        dx = int(round(dx / distance * max_distance))
        dy = int(round(dy / distance * max_distance))
        
        return Position(self.x + dx, self.y + dy)

@dataclass
class Conversation:
    speaker: str
    message: str
    timestamp: datetime
    location: Position

@dataclass
class Memory:
    content: str
    importance: float  # 0-1 scale
    timestamp: datetime
    location: Optional[Position] = None
    related_agents: List[str] = None
    
    def __post_init__(self):
        if self.related_agents is None:
            self.related_agents = []

class Building:
    def __init__(self, building_id: str, building_type: BuildingType, position: Position, size: Tuple[int, int]):
        self.id = building_id
        self.type = building_type
        self.position = position
        self.size = size
        self.occupants: List[str] = []
        self.description = self._generate_description()
    
    def _generate_description(self) -> str:
        descriptions = {
            BuildingType.HOUSE: "A cozy house with a small garden",
            BuildingType.CAFE: "A bustling cafe with the aroma of fresh coffee",
            BuildingType.PARK: "A peaceful park with trees and benches",
            BuildingType.SHOP: "A local shop selling various goods",
            BuildingType.OFFICE: "A modern office building"
        }
        return descriptions.get(self.type, "A building")
    
    def get_bounds(self) -> Tuple[int, int, int, int]:
        """Return (min_x, min_y, max_x, max_y)"""
        return (self.position.x, self.position.y, 
                self.position.x + self.size[0], self.position.y + self.size[1])
    
    def contains_position(self, pos: Position) -> bool:
        min_x, min_y, max_x, max_y = self.get_bounds()
        return min_x <= pos.x < max_x and min_y <= pos.y < max_y

class World:
    def __init__(self, width: int = 50, height: int = 50):
        self.width = width
        self.height = height
        self.buildings: List[Building] = []
        self.agents: Dict[str, 'AIAgent'] = {}
        self.conversations: List[Conversation] = []
        self.time = datetime.now()
        
        self._initialize_world()
    
    def _initialize_world(self):
        """Initialize the world with buildings and paths."""
        # Add some buildings
        buildings_data = [
            ("house1", BuildingType.HOUSE, Position(5, 5), (3, 3)),
            ("house2", BuildingType.HOUSE, Position(15, 8), (3, 3)),
            ("cafe1", BuildingType.CAFE, Position(10, 15), (4, 3)),
            ("park1", BuildingType.PARK, Position(20, 20), (5, 5)),
            ("shop1", BuildingType.SHOP, Position(8, 25), (3, 3)),
            ("office1", BuildingType.OFFICE, Position(25, 10), (4, 4)),
        ]
        
        for building_id, building_type, position, size in buildings_data:
            self.buildings.append(Building(building_id, building_type, position, size))
    
    def add_agent(self, agent: 'AIAgent'):
        """Add an agent to the world."""
        self.agents[agent.id] = agent
        # Place agent near a random building
        if self.buildings:
            building = random.choice(self.buildings)
            agent.position = Position(
                building.position.x + random.randint(0, building.size[0] - 1),
                building.position.y + random.randint(0, building.size[1] - 1)
            )
    
    def get_building_at(self, position: Position) -> Optional[Building]:
        """Get the building at a specific position."""
        for building in self.buildings:
            if building.contains_position(position):
                return building
        return None
    
    def get_nearby_agents(self, position: Position, radius: int = 5) -> List['AIAgent']:
        """Get agents within radius of position."""
        nearby = []
        for agent in self.agents.values():
            if agent.position.distance_to(position) <= radius:
                nearby.append(agent)
        return nearby
    
    def is_valid_position(self, position: Position) -> bool:
        """Check if position is within world bounds."""
        return 0 <= position.x < self.width and 0 <= position.y < self.height
    
    def get_world_state(self) -> Dict[str, Any]:
        """Get the current state of the world for frontend."""
        return {
            "width": self.width,
            "height": self.height,
            "buildings": [
                {
                    "id": b.id,
                    "type": b.type.value,
                    "position": {"x": b.position.x, "y": b.position.y},
                    "size": b.size,
                    "description": b.description,
                    "occupants": b.occupants
                }
                for b in self.buildings
            ],
            "agents": [
                {
                    "id": a.id,
                    "name": a.name,
                    "position": {"x": a.position.x, "y": a.position.y},
                    "mood": a.mood,
                    "current_action": a.current_action
                }
                for a in self.agents.values()
            ],
            "conversations": [
                {
                    "speaker": c.speaker,
                    "message": c.message,
                    "timestamp": c.timestamp.isoformat(),
                    "location": {"x": c.location.x, "y": c.location.y}
                }
                for c in self.conversations[-10:]  # Last 10 conversations
            ],
            "time": self.time.isoformat()
        }

class OpenRouterClient:
    """Client for OpenRouter API integration."""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://openrouter.ai/api/v1"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "HTTP-Referer": "http://localhost:5000",
            "X-Title": "AI Town"
        }
    
    def chat_completion(self, messages: List[Dict[str, str]], model: str = "openai/gpt-3.5-turbo") -> str:
        """Get chat completion from OpenRouter."""
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers={**self.headers, "Content-Type": "application/json"},
                json={
                    "model": model,
                    "messages": messages,
                    "temperature": 0.7,
                    "max_tokens": 150
                }
            )
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            return f"[Error: {str(e)}]"

class AIAgent:
    """An AI agent that can move, think, and interact in the world."""
    
    def __init__(self, agent_id: str, name: str, personality: str, api_key: str):
        self.id = agent_id
        self.name = name
        self.personality = personality
        self.position = Position(0, 0)
        self.mood = "neutral"
        self.current_action = "standing"
        self.energy = 100
        self.hunger = 0
        self.memories: List[Memory] = []
        self.relationships: Dict[str, float] = {}  # agent_id -> relationship_score
        self.goals: List[str] = []
        self.conversation_history: List[Conversation] = []
        
        self.llm_client = OpenRouterClient(api_key)
        self.last_action_time = time.time()
    
    def add_memory(self, content: str, importance: float = 0.5, location: Optional[Position] = None, related_agents: List[str] = None):
        """Add a memory to the agent's memory."""
        memory = Memory(
            content=content,
            importance=importance,
            timestamp=datetime.now(),
            location=location,
            related_agents=related_agents or []
        )
        self.memories.append(memory)
        
        # Keep only important memories (limit to 50 most important)
        self.memories.sort(key=lambda m: (m.importance, m.timestamp), reverse=True)
        self.memories = self.memories[:50]
    
    def get_relevant_memories(self, context: str, limit: int = 5) -> List[str]:
        """Get relevant memories based on context."""
        # Simple relevance scoring based on keyword matching
        relevant = []
        for memory in self.memories:
            score = 0
            context_words = context.lower().split()
            memory_words = memory.content.lower().split()
            
            for word in context_words:
                if word in memory_words:
                    score += 1
            
            if score > 0:
                relevant.append((memory, score))
        
        relevant.sort(key=lambda x: (x[1], x[0].importance), reverse=True)
        return [mem.content for mem, _ in relevant[:limit]]
    
    def decide_next_action(self, world: World) -> str:
        """Use LLM to decide next action."""
        # Get context
        nearby_agents = world.get_nearby_agents(self.position, radius=3)
        current_building = world.get_building_at(self.position)
        
        context = f"""
        You are {self.name}, a {self.personality} AI agent in AI Town.
        Current location: {current_building.type.value if current_building else 'outside'}
        Current mood: {self.mood}
        Energy: {self.energy}
        Hunger: {self.hunger}
        Nearby agents: {[a.name for a in nearby_agents if a.id != self.id]}
        """
        
        # Get relevant memories
        relevant_memories = self.get_relevant_memories(context)
        
        prompt = f"""
        {context}
        
        Recent memories:
        {chr(10).join(f"- {mem}" for mem in relevant_memories[-3:])}
        
        Based on your personality ({self.personality}), current state, and memories, what should you do next?
        Respond with a simple action description like "go to cafe", "talk to Alice", "rest at home", etc.
        """
        
        messages = [
            {"role": "system", "content": f"You are {self.name}, a {self.personality} AI agent. Be concise and natural."},
            {"role": "user", "content": prompt}
        ]
        
        response = self.llm_client.chat_completion(messages)
        return response.strip()
    
    def generate_conversation(self, other_agent: 'AIAgent', world: World) -> str:
        """Generate conversation with another agent."""
        context = f"""
        You are {self.name} talking to {other_agent.name}.
        Your personality: {self.personality}
        Their personality: {other_agent.personality}
        Current location: {world.get_building_at(self.position).type.value if world.get_building_at(self.position) else 'outside'}
        
        Your relationship: {"friendly" if self.relationships.get(other_agent.id, 0) > 0 else "neutral"}
        """
        
        recent_memories = self.get_relevant_memories(f"conversation with {other_agent.name}")
        
        prompt = f"""
        {context}
        
        Start a natural conversation. Keep it brief (1-2 sentences).
        Recent memories: {recent_memories[-2:] if recent_memories else "None"}
        """
        
        messages = [
            {"role": "system", "content": f"You are {self.name}. Be conversational and natural."},
            {"role": "user", "content": prompt}
        ]
        
        return self.llm_client.chat_completion(messages)
    
    def move_towards(self, target: Position, world: World) -> bool:
        """Move towards a target position."""
        new_pos = self.position.move_towards(target)
        
        if world.is_valid_position(new_pos):
            # Check if new position is occupied by another agent
            for agent in world.agents.values():
                if agent.id != self.id and agent.position.x == new_pos.x and agent.position.y == new_pos.y:
                    return False
            
            self.position = new_pos
            return True
        return False
    
    def update(self, world: World):
        """Update agent state and decide next action."""
        current_time = time.time()
        
        # Update basic needs
        self.hunger = min(100, self.hunger + 0.1)
        self.energy = max(0, self.energy - 0.05)
        
        # Decide action every 2 seconds
        if current_time - self.last_action_time > 2:
            action = self.decide_next_action(world)
            self.current_action = action
            
            # Parse and execute action
            self._execute_action(action, world)
            self.last_action_time = current_time
    
    def _execute_action(self, action: str, world: World):
        """Execute the decided action."""
        action = action.lower()
        
        if "go to" in action:
            # Find target building
            target_type = None
            for building_type in BuildingType:
                if building_type.value in action:
                    target_type = building_type
                    break
            
            if target_type:
                # Find nearest building of target type
                buildings = [b for b in world.buildings if b.type == target_type]
                if buildings:
                    target = min(buildings, key=lambda b: self.position.distance_to(b.position))
                    self.move_towards(target.position, world)
                    self.current_action = f"going to {target_type.value}"
        
        elif "talk to" in action or "chat with" in action:
            # Find nearby agents to talk to
            nearby = world.get_nearby_agents(self.position, radius=2)
            if nearby:
                target = random.choice([a for a in nearby if a.id != self.id])
                conversation = self.generate_conversation(target, world)
                
                # Add conversation to both agents
                conv = Conversation(
                    speaker=self.name,
                    message=conversation,
                    timestamp=datetime.now(),
                    location=self.position
                )
                
                world.conversations.append(conv)
                self.conversation_history.append(conv)
                target.conversation_history.append(conv)
                
                # Update relationships
                self.relationships[target.id] = self.relationships.get(target.id, 0) + 0.1
                target.relationships[self.id] = target.relationships.get(self.id, 0) + 0.1
                
                self.add_memory(f"Talked to {target.name}: {conversation}", importance=0.7, related_agents=[target.id])
        
        elif "rest" in action or "sleep" in action:
            building = world.get_building_at(self.position)
            if building and building.type == BuildingType.HOUSE:
                self.energy = min(100, self.energy + 10)
                self.current_action = "resting"
                self.add_memory("Rested at home", importance=0.3)
        
        elif "eat" in action:
            self.hunger = max(0, self.hunger - 20)
            self.current_action = "eating"
            self.add_memory("Ate some food", importance=0.4)
        
        # Add memory of current action
        self.add_memory(f"I decided to: {action}", importance=0.5)

class AITownSimulation:
    """Main simulation controller."""
    
    def __init__(self, api_key: str):
        self.world = World()
        self.api_key = api_key
        self.running = False
        self.simulation_thread = None
        self.update_callbacks = []
    
    def add_agent(self, name: str, personality: str) -> str:
        """Add a new agent to the simulation."""
        agent_id = str(uuid.uuid4())
        agent = AIAgent(agent_id, name, personality, self.api_key)
        self.world.add_agent(agent)
        return agent_id
    
    def start(self):
        """Start the simulation."""
        if not self.running:
            self.running = True
            self.simulation_thread = threading.Thread(target=self._simulation_loop)
            self.simulation_thread.daemon = True
            self.simulation_thread.start()
    
    def stop(self):
        """Stop the simulation."""
        self.running = False
    
    def _simulation_loop(self):
        """Main simulation loop."""
        while self.running:
            # Update all agents
            for agent in list(self.world.agents.values()):
                agent.update(self.world)
            
            # Update world time
            self.world.time = datetime.now()
            
            # Notify callbacks
            for callback in self.update_callbacks:
                callback(self.world.get_world_state())
            
            time.sleep(1)  # Update every second
    
    def get_world_state(self) -> Dict[str, Any]:
        """Get current world state."""
        return self.world.get_world_state()

if __name__ == "__main__":
    # Example usage
    api_key = "your-openrouter-api-key-here"
    town = AITownSimulation(api_key)
    
    # Add some agents
    town.add_agent("Alice", "friendly and outgoing")
    town.add_agent("Bob", "quiet and thoughtful")
    town.add_agent("Charlie", "energetic and curious")
    
    # Start simulation
    town.start()
    
    try:
        while True:
            state = town.get_world_state()
            print(f"\nTime: {state['time']}")
            for agent in state['agents']:
                print(f"{agent['name']}: {agent['current_action']} at ({agent['position']['x']}, {agent['position']['y']})")
            time.sleep(2)
    except KeyboardInterrupt:
        town.stop()
        print("\nSimulation stopped.")
