# 🚀 AI Town - Quick Start Guide

## 1. Get Started in 2 Minutes

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Get API Key
1. Visit [OpenRouter](https://openrouter.ai)
2. Sign up (free tier available)
3. Copy your API key

### Step 3: Configure
```bash
# Create .env file
echo "OPENROUTER_API_KEY=your_api_key_here" > .env
```

### Step 4: Run
```bash
./start_town.sh
```

### Step 5: Open Browser
Go to: `http://localhost:5000`

## 2. What You'll See

- **Live World**: 50x50 grid with buildings and AI agents
- **Real-time Movement**: Agents walk around and interact
- **Conversations**: AI agents chat with each other
- **Buildings**: Houses, cafes, parks, shops, offices
- **Agent Status**: See what each agent is doing

## 3. Try These Actions

1. **Add Agent**: Enter name + personality → "Add Agent"
2. **Watch**: See agents move and talk
3. **Monitor**: Check sidebar for conversations
4. **Experiment**: Try different personalities

## 4. Example Personalities

- "curious and friendly"
- "shy but intelligent"
- "outgoing entrepreneur"
- "quiet artist"
- "helpful neighbor"

## 5. Troubleshooting

**Port 5000 busy?** → Script will use 5001 automatically
**Missing packages?** → Script will install them
**No API key?** → Script will guide you

## 6. Demo Commands

```bash
# Quick test
python test_setup.py

# Manual start
python town_server.py

# With custom port
PORT=8080 python town_server.py
```

## 7. File Structure

```
ai_town.py      # Core simulation
town_server.py  # Web server
templates/      # Web interface
start_town.sh   # Easy startup
```

## 8. Next Steps

1. Add more agents
2. Try different personalities
3. Watch relationships form
4. Check console logs for details
5. Read README.md for advanced features

## 9. Live Demo

The simulation runs entirely in your browser with real-time updates via WebSocket. No external services needed except OpenRouter for AI conversations.

**Ready?** Run `./start_town.sh` now!
