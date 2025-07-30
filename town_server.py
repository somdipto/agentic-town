#!/usr/bin/env python3
"""
AI Town Web Server - Real-time web interface for AI Town simulation
"""

from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import json
import os
from dotenv import load_dotenv
from ai_town import AITownSimulation
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-here')
CORS(app)

# Initialize SocketIO
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

# Global simulation instance
simulation = None

@app.route('/')
def index():
    """Serve the main AI Town interface."""
    return render_template('town.html')

@app.route('/api/world')
def get_world():
    """Get current world state as JSON."""
    if simulation:
        return jsonify(simulation.get_world_state())
    return jsonify({"error": "Simulation not running"}), 503

@app.route('/api/agents', methods=['POST'])
def add_agent():
    """Add a new agent to the simulation."""
    if not simulation:
        return jsonify({"error": "Simulation not running"}), 503
    
    data = request.json
    name = data.get('name', 'Anonymous')
    personality = data.get('personality', 'neutral')
    
    agent_id = simulation.add_agent(name, personality)
    logger.info(f"Added agent: {name} ({agent_id})")
    
    return jsonify({"agent_id": agent_id, "name": name, "personality": personality})

@app.route('/api/agents')
def list_agents():
    """List all agents in the simulation."""
    if simulation:
        state = simulation.get_world_state()
        return jsonify({"agents": state.get('agents', [])})
    return jsonify({"agents": []})

@socketio.on('connect')
def handle_connect():
    """Handle client connection."""
    logger.info('Client connected')
    if simulation:
        # Send initial world state
        emit('world_update', simulation.get_world_state())

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection."""
    logger.info('Client disconnected')

@socketio.on('start_simulation')
def handle_start_simulation(data):
    """Start the simulation."""
    global simulation
    
    if simulation is None:
        api_key = data.get('api_key', os.getenv('OPENROUTER_API_KEY'))
        if not api_key:
            emit('error', {'message': 'OpenRouter API key required'})
            return
        
        simulation = AITownSimulation(api_key)
        
        # Add some default agents
        default_agents = [
            ("Alice", "friendly and outgoing, loves meeting new people"),
            ("Bob", "quiet and thoughtful, enjoys reading and coffee"),
            ("Charlie", "energetic and curious, always exploring"),
            ("Diana", "caring and helpful, likes to assist others"),
            ("Eve", "creative and artistic, enjoys the park")
        ]
        
        for name, personality in default_agents:
            simulation.add_agent(name, personality)
        
        # Set up update callback for WebSocket
        def on_world_update(state):
            socketio.emit('world_update', state)
        
        simulation.update_callbacks.append(on_world_update)
        simulation.start()
        
        emit('simulation_started', {'message': 'AI Town simulation started'})
        logger.info("Simulation started")
    else:
        emit('simulation_already_running', {'message': 'Simulation already running'})

@socketio.on('stop_simulation')
def handle_stop_simulation():
    """Stop the simulation."""
    global simulation
    if simulation:
        simulation.stop()
        simulation = None
        emit('simulation_stopped', {'message': 'AI Town simulation stopped'})
        logger.info("Simulation stopped")

@socketio.on('add_agent')
def handle_add_agent(data):
    """Add agent via WebSocket."""
    if simulation:
        name = data.get('name', 'Anonymous')
        personality = data.get('personality', 'neutral')
        agent_id = simulation.add_agent(name, personality)
        emit('agent_added', {'agent_id': agent_id, 'name': name, 'personality': personality})

@socketio.on('get_world_state')
def handle_get_world_state():
    """Send current world state to client."""
    if simulation:
        emit('world_update', simulation.get_world_state())

def create_app():
    """Application factory for deployment."""
    return app

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('DEBUG', 'False').lower() == 'true'
    
    logger.info(f"Starting AI Town server on port {port}")
    socketio.run(app, host='0.0.0.0', port=port, debug=debug)
