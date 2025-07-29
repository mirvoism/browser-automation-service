# AI Browser Automation with Visual Navigation

A comprehensive browser automation solution that uses AI for visual navigation, supporting both cloud and local LLM endpoints. Perfect for bypassing anti-bot protection on modern websites.

## 🎯 **Two Implementation Options**

### **1. Google Gemini API Version** ☁️
- Uses Google's Gemini 1.5 Flash model
- Cloud-based processing
- Quick setup and deployment
- Pay-per-use model

### **2. Mac Studio Local LLM Version** 🏠  
- Uses local Ollama with llama4:scout/maverick models
- 100% local processing via Tailscale
- Complete privacy and unlimited usage
- Zero API costs after setup

## 🛡️ **Why Visual AI Navigation?**

Traditional browser automation gets **instantly blocked** by modern anti-bot protection:
- ❌ Cloudflare detection
- ❌ reCAPTCHA challenges  
- ❌ Bot fingerprinting
- ❌ Behavioral analysis

**Visual AI Navigation** bypasses all protection by acting like a real human:
- ✅ Sees pages like humans do
- ✅ Makes natural decisions
- ✅ Uses realistic timing
- ✅ Adapts to any website design

## 🚀 **Quick Start**

### **Option A: Google Gemini (Cloud)**
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set up API key
echo "GOOGLE_API_KEY=your_key_here" > .env

# 3. Install browsers
playwright install

# 4. Run example
python examples/google_search.py
```

### **Option B: Mac Studio (Local)**
```bash
# 1. Install dependencies  
pip install -r requirements-macstudio.txt

# 2. Test Mac Studio connection
python llm_speed_test.py

# 3. Run production agent
python production_visual_agent.py
```

## 📁 **Project Structure**

```
├── 🌐 GOOGLE GEMINI VERSION
│   ├── examples/
│   │   ├── google_search.py           # Basic Google search
│   │   └── superbowl_search.py        # Sports data extraction
│   ├── example.py                     # Financial data example
│   ├── requirements.txt               # Gemini dependencies
│   └── .env.example                   # Environment template
│
├── 🏠 MAC STUDIO VERSION  
│   ├── examples/
│   │   ├── google_search_macstudio.py      # Local LLM search
│   │   ├── superbowl_search_macstudio.py   # Sports data (local)
│   │   ├── model_comparison_test.py        # Model performance
│   │   └── multi_model_workflow.py         # Strategic model use
│   ├── production_visual_agent.py     # Production-ready agent
│   ├── anti_bot_examples.py           # Anti-bot scenarios
│   ├── llm_speed_test.py              # Performance testing
│   ├── requirements-macstudio.txt     # Local LLM dependencies
│   └── model_selection_guide.md       # Model recommendations
│
├── 📚 DOCUMENTATION
│   ├── README_macstudio.md            # Mac Studio setup guide
│   ├── README_FINAL.md                # Complete documentation
│   └── docs/                          # Additional documentation
│
└── 📊 RESULTS & CONFIGS
    ├── results/                       # Automation results
    └── browser-automation/            # Additional configs
```

## 🏆 **Real-World Applications**

### **E-commerce Automation**
```python
# Bypass Amazon's sophisticated bot protection
await visual_search_task(
    "gaming laptop under $1000 Amazon",
    "top 3 laptops with prices and specifications"
)
```

### **Financial Data Extraction**  
```python
# Navigate protected financial sites
await visual_search_task(
    "Tesla stock price today",
    "current price, market cap, and recent news"
)
```

### **Social Media Monitoring**
```python
# Research on protected platforms
await visual_search_task(
    "AI automation discussions Twitter",
    "recent posts and trending opinions"
)
```

## ⚡ **Performance Comparison**

| Feature | Google Gemini | Mac Studio |
|---------|---------------|------------|
| **Setup Time** | 5 minutes | 30 minutes |
| **Response Speed** | 2-4 seconds | 2-3 seconds |
| **Privacy** | Cloud processing | 100% local |
| **Cost** | Pay per use | Free after setup |
| **Rate Limits** | Yes | None |
| **Customization** | Limited | Full control |

## 🛠️ **Advanced Features**

### **Multi-Model Strategy (Mac Studio)**
```python
# Use llama4:scout for navigation
scout_agent = Agent(task="Navigate to site", llm=scout_llm)

# Use maverick for complex reasoning  
maverick_agent = Agent(task="Extract complex data", llm=maverick_llm)
```

### **Anti-Bot Optimization**
```python
# Human-like behavior patterns
agent = Agent(
    task="Complete protected workflow",
    step_timeout=90,           # Patient timing
    retry_delay=5,             # Natural delays
    use_vision=True,           # Visual navigation
    extend_system_message="Act like a real human user"
)
```

## 🔧 **Configuration Options**

### **Browser Profiles**
- **Standard**: General web browsing
- **Anti-Bot**: Optimized for protected sites
- **Stealth**: Maximum evasion capabilities

### **Model Selection (Mac Studio)**
- **llama4:scout**: Best for navigation and search
- **maverick**: Best for complex reasoning and data extraction
- **Strategic switching**: Use both for optimal results

## 📈 **Getting Started Guide**

### **For Beginners**
1. Start with Google Gemini version for simplicity
2. Try basic examples first
3. Gradually increase task complexity

### **For Advanced Users**
1. Set up Mac Studio local environment
2. Experiment with model combinations
3. Build custom automation workflows

### **For Production Use**
1. Use Mac Studio version for privacy and scale
2. Implement proper error handling
3. Set up monitoring and logging

## 🤝 **Contributing**

We welcome contributions! Please see our contributing guidelines for:
- Code style and standards
- Testing requirements  
- Documentation updates
- Bug reports and feature requests

## 📜 **License**

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 **Support**

- **Issues**: Report bugs and request features via GitHub Issues
- **Discussions**: Join community discussions for help and ideas
- **Documentation**: Comprehensive guides in the `/docs` folder

## ⭐ **Star this repo** if you find it useful!

---

**Perfect for**: Web scraping, automated testing, data extraction, e-commerce monitoring, social media research, and any scenario requiring reliable browser automation that bypasses modern anti-bot protection. 