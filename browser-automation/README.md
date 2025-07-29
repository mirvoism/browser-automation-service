# Browser Automation with Gemini

This repository contains browser automation scripts using browser-use and Gemini AI. The project enables AI agents to perform automated web tasks.

## Setup

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Install playwright browsers:
```bash
playwright install
```
4. Create a `.env` file with your Gemini API key:
```
GOOGLE_API_KEY=your_gemini_api_key_here
```

## Project Structure

- `examples/` - Example scripts for different use cases
- `requirements.txt` - Project dependencies
- `.env.example` - Example environment variables file

## Usage

Run any example script:
```bash
python examples/google_search.py
```

## Contributing

Feel free to contribute by creating new example scripts or improving existing ones. 