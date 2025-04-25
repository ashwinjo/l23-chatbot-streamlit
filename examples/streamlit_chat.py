"""
Streamlit chat example using MCPAgent with built-in conversation memory.

This example demonstrates how to use the MCPAgent with its built-in
conversation history capabilities for better contextual interactions in a Streamlit app.

Special thanks to https://github.com/microsoft/playwright-mcp for the server.
"""

import asyncio
import atexit
import streamlit as st
import base64
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from mcp_use import MCPAgent, MCPClient

# App title and description - must be first Streamlit command
st.set_page_config(page_title="MCP Chat", layout="wide")

# Load environment variables for API keys
load_dotenv()

# Function to set background using a local image file
def add_bg_from_local_file():
    local_image_path = "/Users/ashwjosh/mcp-use/examples/Keysight_Colorado_Springs.jpeg"
    try:
        if os.path.exists(local_image_path):
            with open(local_image_path, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode()
                
                # Set the background with CSS and enhanced styling for Keysight corporate look
                st.markdown(
                    f"""
                    <style>
                    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');
                    
                    .stApp {{
                        background-image: url("data:image/png;base64,{encoded_string}");
                        background-size: cover;
                        background-position: center;
                        background-repeat: no-repeat;
                        font-family: 'Roboto', sans-serif;
                    }}
                    
                    /* Main title styling */
                    h1 {{
                        color: #003366 !important;
                        font-weight: 700 !important;
                        font-size: 2.5rem !important;
                        margin-bottom: 1.5rem !important;
                        padding: 10px 15px !important;
                        background-color: rgba(255, 255, 255, 0.85) !important;
                        border-radius: 8px !important;
                        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1) !important;
                        display: inline-block !important;
                    }}
                    
                    /* Subtitle styling */
                    .stMarkdown p {{
                        color: #333333 !important;
                        font-weight: 500 !important;
                        font-size: 1.1rem !important;
                        background-color: rgba(255, 255, 255, 0.85) !important;
                        padding: 10px 15px !important;
                        border-radius: 8px !important;
                        margin-bottom: 20px !important;
                        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1) !important;
                    }}
                    
                    /* Chat messages styling */
                    .stChatMessage {{
                        background-color: rgba(255, 255, 255, 0.9) !important;
                        border-radius: 12px !important;
                        padding: 15px !important;
                        margin-bottom: 15px !important;
                        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.08) !important;
                        border-left: 4px solid #003366 !important;
                    }}
                    
                    /* User message specific styling */
                    [data-testid="stChatMessageContent"] {{
                        font-size: 1rem !important;
                        line-height: 1.5 !important;
                        color: #333333 !important;
                    }}
                    
                    /* Chat input styling */
                    .stChatInput {{
                        background-color: rgba(255, 255, 255, 0.9) !important;
                        border-radius: 8px !important;
                        padding: 5px !important;
                        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1) !important;
                        margin-top: 20px !important;
                    }}
                    
                    /* Buttons styling */
                    .stButton button {{
                        background-color: #003366 !important;
                        color: white !important;
                        font-weight: 500 !important;
                        border-radius: 6px !important;
                        padding: 5px 15px !important;
                        border: none !important;
                        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1) !important;
                        transition: all 0.3s ease !important;
                    }}
                    
                    .stButton button:hover {{
                        background-color: #004b87 !important;
                        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15) !important;
                    }}
                    
                    /* Error message styling */
                    .stAlert {{
                        background-color: rgba(255, 255, 255, 0.9) !important;
                        border-radius: 8px !important;
                        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1) !important;
                    }}
                    </style>
                    """,
                    unsafe_allow_html=True
                )
        else:
            st.error(f"Background image file not found: {local_image_path}")
            # Fallback to a solid gradient background
            apply_fallback_bg()
    except Exception as e:
        st.error(f"Error loading background image: {e}")
        apply_fallback_bg()

def apply_fallback_bg():
    # Fallback to a solid gradient background if image loading fails
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');
        
        .stApp {
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            font-family: 'Roboto', sans-serif;
        }
        
        /* Main title styling */
        h1 {
            color: white !important;
            font-weight: 700 !important;
            font-size: 2.5rem !important;
            margin-bottom: 1.5rem !important;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2) !important;
        }
        
        /* Subtitle styling */
        .stMarkdown p {
            color: white !important;
            font-weight: 500 !important;
            font-size: 1.1rem !important;
            background-color: rgba(255, 255, 255, 0.1) !important;
            padding: 10px 15px !important;
            border-radius: 8px !important;
            margin-bottom: 20px !important;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1) !important;
        }
        
        /* Chat messages styling */
        .stChatMessage {
            background-color: rgba(255, 255, 255, 0.9) !important;
            border-radius: 12px !important;
            padding: 15px !important;
            margin-bottom: 15px !important;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1) !important;
        }
        
        /* User message specific styling */
        [data-testid="stChatMessageContent"] {
            font-size: 1rem !important;
            line-height: 1.5 !important;
            color: #333333 !important;
        }
        
        /* Chat input styling */
        .stChatInput {
            background-color: rgba(255, 255, 255, 0.9) !important;
            border-radius: 8px !important;
            padding: 5px !important;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1) !important;
            margin-top: 20px !important;
        }
        
        /* Buttons styling */
        .stButton button {
            background-color: #ffffff !important;
            color: #1e3c72 !important;
            font-weight: 500 !important;
            border-radius: 6px !important;
            padding: 5px 15px !important;
            border: none !important;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1) !important;
            transition: all 0.3s ease !important;
        }
        
        .stButton button:hover {
            background-color: #f0f0f0 !important;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15) !important;
        }
        
        /* Error message styling */
        .stAlert {
            background-color: rgba(255, 255, 255, 0.9) !important;
            border-radius: 8px !important;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1) !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# Apply background image from local file
add_bg_from_local_file()

st.title("Keysight L23 MCP Agent")
st.markdown("Chat with Keysight L23 Infrastructure.")

# Config file path
config_file = "browser_mcp.json"

# Set up a persistent event loop for the app
if "loop" not in st.session_state:
    st.session_state.loop = asyncio.new_event_loop()
    asyncio.set_event_loop(st.session_state.loop)

# Session state variables
if "messages" not in st.session_state:
    st.session_state.messages = []

if "agent" not in st.session_state:
    st.session_state.agent = None

if "client" not in st.session_state:
    st.session_state.client = None
    
# Initialize agent once at startup rather than on each interaction
if "initialized" not in st.session_state:
    try:
        # Use run_until_complete instead of asyncio.run to use the persistent loop
        def init_agent():
            async def _init():
                client = MCPClient.from_config_file(config_file)
                llm = ChatOpenAI(model="gpt-4o-mini")
                agent = MCPAgent(
                    llm=llm,
                    client=client,
                    max_steps=15,
                    memory_enabled=True,
                )
                return client, agent
            
            return st.session_state.loop.run_until_complete(_init())
        
        st.session_state.client, st.session_state.agent = init_agent()
        st.session_state.initialized = True
    except Exception as e:
        st.error(f"Failed to initialize agent: {e}")

def run_async(coro):
    """Run an async coroutine in the persistent event loop."""
    return st.session_state.loop.run_until_complete(coro)

async def cleanup():
    """Close all MCP sessions."""
    if st.session_state.client and st.session_state.client.sessions:
        await st.session_state.client.close_all_sessions()
        st.session_state.client = None
        st.session_state.agent = None
        st.session_state.initialized = False

# Register cleanup on exit
def on_exit():
    if st.session_state.client and st.session_state.client.sessions:
        run_async(cleanup())

atexit.register(on_exit)

async def get_agent_response(user_input):
    """Get response from agent and update conversation."""
    # Check for clear history command
    if user_input.lower() == "clear":
        st.session_state.agent.clear_conversation_history()
        st.session_state.messages = []
        return "Conversation history cleared."
    
    try:
        # Run the agent with the user input (memory handling is automatic)
        response = await st.session_state.agent.run(user_input)
        return response
    except Exception as e:
        return f"Error: {e}"

# Display conversation history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Get user input
user_input = st.chat_input("Type your message here...")

# Process user input and generate response
if user_input and st.session_state.initialized:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # Display assistant response with a spinner while processing
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            # Get response using our persistent event loop
            response = run_async(get_agent_response(user_input))
            st.markdown(response)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

# Handle cleanup on session end
if st.session_state.client:
    st.sidebar.button("End Session", on_click=lambda: run_async(cleanup())) 