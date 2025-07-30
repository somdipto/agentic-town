"""Test script for the AI Village Simulation with OpenRouter."""

import time
from agent import Agent

def run_simulation(steps=3, model="openai/gpt-3.5-turbo"):
    """Run a simple simulation with one agent.
    
    Args:
        steps: Number of simulation steps to run
        model: The AI model to use (default: gpt-3.5-turbo)
    """
    print("🚀 Starting AI Village Simulation")
    print(f"📊 Using model: {model}")
    
    # Create an agent
    print("\n👤 Creating agent...")
    agent = Agent(model=model)
    
    # Environment description
    environment = "a peaceful village with a market, houses, and a central square"
    
    # Run simulation steps
    print(f"\n🏃 Running {steps} simulation steps...")
    for step in range(1, steps + 1):
        print(f"\n--- Step {step}/{steps} ---")
        try:
            result = agent.step(environment)
            print(f"✅ Step {step} completed successfully!")
            print(f"   Plan: {result['plan']}")
            print(f"   Result: {result['result']}")
        except Exception as e:
            print(f"❌ Error in step {step}: {str(e)}")
        
        # Add a small delay between steps
        if step < steps:
            time.sleep(2)  # 2-second delay between steps
    
    print("\n🏁 Simulation complete!")

if __name__ == "__main__":
    # You can change the model here if needed
    # Available models: https://openrouter.ai/models
    MODEL = "openai/gpt-3.5-turbo"  # Fast and cost-effective
    # MODEL = "anthropic/claude-3-opus"  # More powerful but slower
    # MODEL = "google/gemini-pro"  # Alternative model
    
    run_simulation(steps=3, model=MODEL)
