# Complete Setup Guide

## 🌐 Google Gemini Version Setup

### Prerequisites
- Python 3.8 or higher
- Google Cloud account (for Gemini API)

### Step-by-Step Setup

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd ai-browser-automation
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Playwright Browsers**
   ```bash
   playwright install
   ```

5. **Get Gemini API Key**
   - Visit https://makersuite.google.com/app/apikey
   - Create a new API key
   - Copy the key

6. **Configure Environment**
   ```bash
   cp .env.example .env
   # Edit .env and add your API key
   ```

7. **Test Installation**
   ```bash
   python examples/google_search.py
   ```

## 🏠 Mac Studio Version Setup

### Prerequisites
- Mac Studio with Ollama installed
- Tailscale for network access
- Models: llama4:scout, maverick

### Step-by-Step Setup

1. **Verify Mac Studio Connection**
   ```bash
   curl https://matiass-mac-studio.tail174e9b.ts.net/v1/models
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements-macstudio.txt
   ```

3. **Test LLM Connection**
   ```bash
   python llm_speed_test.py
   ```

4. **Run Production Agent**
   ```bash
   python production_visual_agent.py
   ```

## 🚀 First Automation Test

### Google Gemini Version
```bash
python examples/google_search.py
```

### Mac Studio Version
```bash
python examples/google_search_macstudio.py
```

## 🔧 Troubleshooting

### Common Issues

#### "No module named 'browser_use'"
```bash
pip install browser-use>=0.1.37
```

#### "Playwright browsers not found"
```bash
playwright install
```

#### "API key not valid"
- Check your .env file
- Verify API key at Google AI Studio

#### "Mac Studio connection failed"
- Verify Tailscale is running
- Check Mac Studio is awake
- Test with: `curl <mac-studio-url>/v1/models`

### Performance Optimization

#### For Google Gemini
- Use shorter prompts for faster responses
- Implement proper rate limiting
- Cache results when possible

#### For Mac Studio
- Ensure Mac Studio doesn't sleep
- Use appropriate model for task complexity
- Monitor temperature settings

## 📊 Monitoring and Logging

### Enable Debug Logging
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Save Automation Sessions
```python
agent = Agent(
    task="...",
    save_conversation_path="./logs/session.json"
)
```

### Performance Monitoring
```python
agent = Agent(
    task="...",
    calculate_cost=True  # Track token usage
)
```

## 🎯 Next Steps

1. **Try Basic Examples**: Start with simple Google searches
2. **Customize Tasks**: Modify examples for your specific needs
3. **Advanced Features**: Explore multi-model workflows
4. **Production Deployment**: Set up proper error handling and monitoring 