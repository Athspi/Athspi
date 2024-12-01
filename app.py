import streamlit as st
import os
import subprocess
import tempfile
import shutil

# Set page configuration
st.set_page_config(
    page_title="AI-Powered Terminal Chat",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# CSS and customizations
hide_streamlit_style = """
    <style>
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Full-screen terminal styling */
    .block-container {
        padding: 0;
        margin: 0;
    }
    iframe {
        border: none;
    }
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Function to execute Python commands
def execute_command(command, working_dir):
    try:
        result = subprocess.run(
            command,
            shell=True,
            cwd=working_dir,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        return result.stdout, result.stderr
    except Exception as e:
        return "", f"Error executing command: {e}"

# Manage temporary files
if "temp_dir" not in st.session_state:
    st.session_state.temp_dir = tempfile.mkdtemp()

temp_dir = st.session_state.temp_dir

# Embed HTML terminal
def render_terminal():
    html_code = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>AI-Powered Terminal Chat</title>
        <style>
            body, html {
                margin: 0;
                padding: 0;
                height: 100%;
                overflow: hidden;
                font-family: 'Courier New', monospace;
                background-color: #000;
                color: #0f0;
            }
            #terminal {
                height: calc(100% - 60px);
                width: 100%;
                overflow-y: auto;
                padding: 20px;
                box-sizing: border-box;
            }
            #input-area {
                height: 60px;
                width: 100%;
                display: flex;
                padding: 10px;
                box-sizing: border-box;
                background-color: #111;
                align-items: center;
            }
            #user-input {
                flex-grow: 1;
                background-color: #000;
                border: 2px solid #0f0;
                color: #0f0;
                font-family: 'Courier New', monospace;
                font-size: 16px;
                padding: 10px;
                border-radius: 5px 0 0 5px;
                outline: none;
            }
            #send-btn {
                width: 80px;
                height: 42px;
                background-color: #0f0;
                color: #000;
                border: none;
                cursor: pointer;
                font-family: 'Courier New', monospace;
                font-size: 16px;
                font-weight: bold;
                border-radius: 0 5px 5px 0;
                transition: background-color 0.3s;
            }
            #send-btn:hover {
                background-color: #00ff00;
            }
        </style>
    </head>
    <body>
        <div id="terminal"></div>
        <div id="input-area">
            <input type="text" id="user-input" placeholder="Enter your command..." aria-label="Enter your command">
            <button id="send-btn">Send</button>
        </div>
        <script>
            const terminal = document.getElementById('terminal');
            const userInput = document.getElementById('user-input');
            const sendBtn = document.getElementById('send-btn');

            function addLine(text, isUser = false) {
                const lineElement = document.createElement('div');
                if (isUser) {
                    lineElement.textContent = '> ' + text;
                    lineElement.style.color = '#ff0';
                } else {
                    lineElement.textContent = text;
                }
                terminal.appendChild(lineElement);
                terminal.scrollTop = terminal.scrollHeight;
            }

            function processCommand(command) {
                addLine(command, true);
                fetch('/run_command', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ command: command })
                })
                .then(response => response.json())
                .then(data => {
                    addLine(data.output);
                });
            }

            sendBtn.addEventListener('click', () => {
                const command = userInput.value.trim();
                if (command) {
                    processCommand(command);
                    userInput.value = '';
                }
            });

            userInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    sendBtn.click();
                }
            });

            addLine("Welcome to the AI-Powered Terminal Chat!");
            addLine("Type 'help' for available commands.");
        </script>
    </body>
    </html>
    """
    st.components.v1.html(html_code, height=800)

# Render terminal
render_terminal()

# Execute Python commands from user input
command_input = st.text_input("Python Command:", "")
if st.button("Run Command"):
    stdout, stderr = execute_command(command_input, temp_dir)
    st.text_area("Output:", value=stdout + stderr, height=300)

# Clear temporary files
if st.button("Clear Temp Files"):
    shutil.rmtree(temp_dir)
    st.session_state.temp_dir = tempfile.mkdtemp()
    st.success("Temporary files cleared!")
