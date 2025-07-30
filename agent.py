"""AI Village Simulation with OpenRouter integration."""

import uuid
import json
from typing import List, Dict, Any, Optional
from config import OPENROUTER_API_KEY, DEFAULT_MODEL
from openrouter_client import OpenRouterClient

class Perception:
    """Handles how an agent perceives its environment."""
    def __init__(self):
        pass

    def perceive(self, environment):
        """Simulates the agent perceiving the environment."""
        # Simple perception - in a real implementation, this would process the environment
        return f"Perceived environment: {environment}"


class Memory:
    """Manages the agent's memory."""
    def __init__(self):
        self.memories = []

    def add_memory(self, memory):
        """Adds a memory to the agent's memory."""
        self.memories.append(memory)
        return f"Added to memory: {memory}"

    def retrieve_memories(self, query):
        """Retrieves relevant memories based on a query."""
        # Simple retrieval - just return recent memories
        return "\n".join([f"- {m}" for m in self.memories[-5:]])  # Return last 5 memories


class Planner:
    """Handles the agent's planning and decision-making using OpenRouter."""
    def __init__(self, client=None, model: str = None):
        self.client = client or OpenRouterClient()
        self.model = model or DEFAULT_MODEL

    def plan(self, perceived_info, memories):
        """Develops a plan using OpenRouter based on perceived information and memories."""
        try:
            # Prepare the prompt
            prompt = f"""You are an AI agent in a village simulation. Your task is to decide on the next action.
            
            Current situation: {perceived_info}
            
            Relevant memories:
            {memories}
            
            What should you do next? Respond with just one concise sentence describing your next action."""
            
            # Get response from OpenRouter
            response = self.client.chat_completion(
                messages=[{"role": "user", "content": prompt}],
                model=self.model,
                temperature=0.7,
                max_tokens=100
            )
            
            # Extract the plan from the response
            plan = response.get('choices', [{}])[0].get('message', {}).get('content', 'No plan generated')
            print(f"🤖 Generated plan: {plan}")
            return plan
            
        except Exception as e:
            print(f"❌ Error in planning: {str(e)}")
            return f"Default plan due to error: {str(e)}"


class Executor:
    """Executes the agent's plans."""
    def __init__(self):
        pass

    def execute(self, plan, environment):
        """Executes a given plan within the environment."""
        print(f"🏃 Executing: {plan}")
        return f"Executed: {plan}"


class Lifecycle:
    """Manages the agent's lifecycle (e.g., age, energy)."""
    def __init__(self):
        self.age = 0
        self.energy = 100

    def update(self):
        """Updates the agent's lifecycle state."""
        self.age += 1
        self.energy = max(0, self.energy - 1)  # Decrease energy, but don't go below 0
        return f"Age: {self.age}, Energy: {self.energy}"


class Interaction:
    """Handles interactions with other agents or the environment."""
    def __init__(self):
        pass

    def interact(self, target, action):
        """Simulates interaction with a target."""
        result = f"Interacted with {target} using {action}"
        print(f"🤝 {result}")
        return result


class Agent:
    """Base class for all agents in the simulation."""
    
    def __init__(self, agent_id=None, model: str = None):
        self.agent_id = agent_id if agent_id is not None else str(uuid.uuid4())
        self.model = model or DEFAULT_MODEL
        self.perception = Perception()
        self.memory = Memory()
        self.planner = Planner(OpenRouterClient(), self.model)
        self.executor = Executor()
        self.lifecycle = Lifecycle()
        self.interaction = Interaction()
        print(f"👤 Agent created with ID: {self.agent_id} using model: {self.model}")

    def step(self, environment):
        """Represents one step in the agent's simulation."""
        try:
            # Perception
            perceived_info = self.perception.perceive(environment)
            print(f"👀 Perceived: {perceived_info}")
            
            # Memory
            self.memory.add_memory(perceived_info)
            relevant_memories = self.memory.retrieve_memories("what to do next?")
            
            # Planning
            plan = self.planner.plan(perceived_info, relevant_memories)
            
            # Execution
            result = self.executor.execute(plan, environment)
            
            # Update lifecycle
            self.lifecycle.update()
            
            # Add result to memory
            self.memory.add_memory(f"Action result: {result}")
            
            return {
                "agent_id": self.agent_id,
                "perception": perceived_info,
                "plan": plan,
                "result": result,
                "status": "success"
            }
            
        except Exception as e:
            error_msg = f"Error in agent {self.agent_id} step: {str(e)}"
            print(f"❌ {error_msg}")
            return {
                "agent_id": self.agent_id,
                "status": "error",
                "error": error_msg
            }


# Example usage
if __name__ == "__main__":
    print("🚀 Starting AI Village Simulation with OpenRouter")
    
    # Create an agent
    agent = Agent(model="openai/gpt-3.5-turbo")  # You can change the model here
    
    # Run a few simulation steps
    for i in range(3):
        print(f"\n--- Step {i+1} ---")
        result = agent.step("a peaceful village with a market and houses")
        print(f"Step result: {json.dumps(result, indent=2)}")
    
    print("\n🏁 Simulation complete!")
