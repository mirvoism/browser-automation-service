# Browser Automation with Mac Studio LLM

This version of the browser automation project uses your local Mac Studio LLM endpoint (Ollama) instead of Google's Gemini API.

## Prerequisites

1. **Mac Studio Setup**: Your Mac Studio should be running Ollama with Tailscale Serve enabled
2. **Tailscale Access**: Your MacBook must be connected to the same Tailscale network
3. **Available Models**: DeepSeek R1, Qwen 3 (32B), Qwen 2.5

## Setup

1. Install dependencies for Mac Studio version:
```bash
pip install -r requirements-macstudio.txt
```

2. Install playwright browsers:
```bash
playwright install
```

3. Verify Mac Studio connectivity:
```bash
curl -s https://matiass-mac-studio.tail174e9b.ts.net/v1/models
```

4. (Optional) Set environment variables:
```bash
export OPENAI_API_BASE="https://matiass-mac-studio.tail174e9b.ts.net/v1"
export OPENAI_API_KEY="ollama"
```

## Available Models

- `llama4:scout` - **🏆 RECOMMENDED** - Llama 4 optimized for exploration/search tasks
- `maverick` - **🥈 STRONG CHOICE** - Specialized model, excellent for complex reasoning
- `deepseek-r1` - DeepSeek Reasoning model, great for logical tasks
- `qwen3:32b` - Qwen 3 32B parameter model, large context window
- `qwen25` - Qwen 2.5 model, balanced performance

## Usage

Run Mac Studio examples:
```bash
# Basic examples
python examples/google_search_macstudio.py
python examples/superbowl_search_macstudio.py  
python example_macstudio.py

# Advanced examples
python examples/model_comparison_test.py
python examples/multi_model_workflow.py
```

## Model Performance Notes

- **Llama4:scout**: 🏆 **Best for browser automation** - Optimized for exploration and search tasks, excellent at navigating websites
- **maverick**: 🥈 **Excellent reasoning** - Strong performance on complex multi-step tasks and decision making  
- **DeepSeek R1**: Good reasoning capabilities, reliable for logical tasks
- **Qwen 3 32B**: Large context window, good for detailed extraction tasks
- **Local Processing**: No API rate limits, full privacy, faster response times

## Troubleshooting

1. **Connection Issues**: Ensure Tailscale is running and connected
2. **Model Errors**: Check available models with `/v1/models` endpoint
3. **Performance**: Llama4:scout recommended for best browser automation results

## Testing Your Setup

Run the model comparison test to see performance on your specific tasks:
```bash
python examples/model_comparison_test.py
```

Or test connectivity:
```bash
python test_macstudio_connection.py
```

## Advanced Features

- **Model Selection Guide**: See `model_selection_guide.md` for detailed recommendations
- **Multi-Model Workflows**: Use different models for different parts of complex tasks
- **Performance Testing**: Compare models with built-in benchmarking tools

## Advantages of Mac Studio Version

- ✅ **No API Costs**: Free local processing
- ✅ **Privacy**: All data stays local
- ✅ **No Rate Limits**: Run as many automations as needed
- ✅ **Custom Models**: Full control over model selection
- ✅ **Offline Capable**: Works without internet (except for web browsing) 