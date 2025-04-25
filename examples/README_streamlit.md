# Streamlit MCP Chat Application

This is a Streamlit version of the chat example using MCPAgent with built-in conversation memory.

## Requirements

- Python 3.9+
- All dependencies listed in requirements.txt

## Setup

1. Install required packages:
   ```
   pip install -r requirements.txt
   ```

2. Set up your environment variables in a `.env` file:
   ```
   OPENAI_API_KEY=your_openai_api_key
   # Add any other required environment variables
   ```

3. Modify the config file path in `streamlit_chat.py` if necessary:
   ```python
   config_file = "examples/browser_mcp.json"  # Update this to your config file path
   ```

## Running the Application

To run the Streamlit application:

```bash
streamlit run examples/streamlit_chat.py
```

The application will open in your default web browser. If it doesn't open automatically, you can access it at http://localhost:8501.

## Usage

- Type your message in the input box at the bottom of the screen
- Type 'clear' to clear the conversation history
- Click the "End Session" button in the sidebar to properly close all MCP sessions

## Features

- Interactive chat interface with Streamlit
- Persistent conversation history within a session
- Built-in conversation memory using MCPAgent
- Asynchronous processing of agent responses 