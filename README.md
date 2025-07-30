# 🤖 AI Town - Virtual AI Community

A real-time virtual town where AI agents live, chat, and socialize. Inspired by [a16z-infra/ai-town](https://github.com/a16z-infra/ai-town) and [convex.dev/ai-town](https://convex.dev/ai-town).

## 🌟 Features

- **Real-time AI Agents**: Watch AI agents move around, interact, and have conversations
- **Dynamic World**: Buildings, parks, cafes, and houses where agents can go
- **Memory System**: Agents remember past interactions and use them to guide future behavior
- **Relationship Building**: Agents form relationships based on interactions
- **Web Interface**: Beautiful real-time web dashboard with live updates
- **WebSocket Support**: Real-time updates via Socket.IO
- **REST API**: Full REST API for programmatic access

## 🏗️ Architecture

```
AI Town/
├── ai_town.py          # Core simulation engine
├── town_server.py      # Flask web server with WebSocket support
├── templates/
│   └── town.html       # Real-time web interface
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Get OpenRouter API Key

1. Go to [OpenRouter](https://openrouter.ai)
2. Sign up for an account
3. Get your API key from the dashboard

### 3. Set Environment Variables

Create a `.env` file:
```bash
OPENROUTER_API_KEY=your_api_key_here
SECRET_KEY=your_secret_key_here
PORT=5000
DEBUG=True
```

### 4. Run the Server

```bash
python town_server.py
```

### 5. Open Your Browser

Navigate to `http://localhost:5000` to see AI Town in action!

## 🎮 Usage

### Web Interface
- **Start Simulation**: Click "Start Simulation" with your API key
- **Add Agents**: Create new AI agents with custom names and personalities
- **Watch Interactions**: See agents move around and have conversations in real-time
- **Monitor Activity**: View agent status and recent conversations in the sidebar

### API Endpoints

#### Start Simulation
```javascript
// WebSocket
socket.emit('start_simulation', {api_key: 'your_key'});
```

#### Add Agent
```javascript
// WebSocket
socket.emit('add_agent', {
    name: 'Alice',
    personality: 'friendly and outgoing'
});

// REST API
POST /api/agents
{
    "name": "Alice",
    "personality": "friendly and outgoing"
}
```

#### Get World State
```javascript
// WebSocket
socket.on('world_update', (state) => {
    console.log(state);
});

// REST API
GET /api/world
```

## 🏙️ World Details

### Buildings
- **Houses**: Where agents rest and recover energy
- **Cafes**: Social hubs where agents meet and chat
- **Parks**: Relaxation areas for agents
- **Shops**: Places for agents to get food and supplies
- **Offices**: Work areas for agents

### Agent Behaviors
- **Movement**: Agents navigate the world using pathfinding
- **Conversations**: AI-powered conversations using OpenRouter
- **Memory**: Agents remember interactions and locations
- **Relationships**: Agents form positive/negative relationships
- **Needs**: Agents have energy, hunger, and social needs

## 🛠️ Development

### Project Structure
```
ai_town.py          # Core simulation classes
├── World           # Manages the virtual world
├── AIAgent         # Individual AI agents
├── Building        # World buildings
└── AITownSimulation # Main simulation controller

town_server.py      # Web server
├── REST API        # HTTP endpoints
├── WebSocket       # Real-time updates
└── Web Interface   # Frontend serving
```

### Adding New Features

#### New Building Types
```python
# In ai_town.py
class BuildingType(Enum):
    # Add new types
    GYM = "gym"
    LIBRARY = "library"
```

#### New Agent Behaviors
```python
# In AIAgent class
def _execute_action(self, action: str, world: World):
    if "exercise" in action:
        # Add new behavior
        self.energy = min(100, self.energy + 15)
        self.current_action = "exercising"
```

## 🔧 Configuration

### Environment Variables
- `OPENROUTER_API_KEY`: Your OpenRouter API key (required)
- `SECRET_KEY`: Flask secret key (optional)
- `PORT`: Server port (default: 5000)
- `DEBUG`: Debug mode (default: False)

### Simulation Parameters
- World size: 50x50 grid
- Update interval: 1 second
- Memory limit: 50 memories per agent
- Conversation radius: 2 cells

## 🐛 Troubleshooting

### Common Issues

1. **API Key Issues**
   - Ensure your OpenRouter API key is valid
   - Check rate limits on your OpenRouter account

2. **Port Already in Use**
   ```bash
   # Kill process on port 5000
   lsof -ti:5000 | xargs kill -9
   ```

3. **WebSocket Connection Issues**
   - Check browser console for errors
   - Ensure server is running on correct port
   - Try refreshing the page

4. **Python Dependencies**
   ```bash
   # If you have issues with eventlet
   pip uninstall eventlet
   pip install eventlet==0.33.3
   ```

## 📊 Monitoring

### Logs
- Server logs are printed to console
- Agent actions and conversations are logged
- WebSocket events are tracked

### Performance
- Monitor memory usage with many agents
- API calls are rate-limited by OpenRouter
- Consider upgrading OpenRouter plan for more agents

## 🎯 Future Enhancements

- [ ] Weather system affecting agent behavior
- [ ] Day/night cycle
- [ ] More complex building interactions
- [ ] Agent emotions and mood visualization
- [ ] Persistent world state
- [ ] Agent customization (appearance, traits)
- [ ] Social events and gatherings
- [ ] Economic system
- [ ] Mobile-responsive interface
- [ ] Agent profiles and detailed stats

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

MIT License - feel free to use for any purpose!

## 🙏 Acknowledgments

- Inspired by [a16z-infra/ai-town](https://github.com/a16z-infra/ai-town)
- Built with [OpenRouter](https://openrouter.ai) for AI capabilities
- Powered by [Flask](https://flask.palletsprojects.com/) and [Socket.IO](https://socket.io/)
