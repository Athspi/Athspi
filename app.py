import streamlit as st
import os
import subprocess
import tempfile
import shutil

# Set Streamlit page configuration
st.set_page_config(
    page_title="AI Terminal in Streamlit",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Hide Streamlit branding and styling for terminal look
hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
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

# Initialize a temporary directory for the session
if "temp_dir" not in st.session_state:
    st.session_state.temp_dir = tempfile.mkdtemp()

temp_dir = st.session_state.temp_dir

# Function to execute commands
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

# Render terminal UI
def render_terminal():
    html_code = """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body, html {
                margin: 0; padding: 0; height: 100%; background-color: black; color: #0f0;
                font-family: "Courier New", monospace; overflow: hidden;
            }
            .terminal-container {
                height: calc(100% - 50px); width: 100%; overflow-y: auto; padding: 10px;
            }
            .terminal-input {
                height: 50px; width: 100%; background-color: #000; color: #0f0;
                font-family: "Courier New", monospace; font-size: 16px; padding: 10px;
                border: none; outline: none; box-sizing: border-box;
            }
        </style>
    </head>
    <body>
        <div class="terminal-container" id="terminal"></div>
        <input class="terminal-input" id="terminal-input" placeholder="Type a command here..." autofocus />
        <script>
            const terminal = document.getElementById('terminal');
            const input = document.getElementById('terminal-input');
            function addLine(text) {
                const div = document.createElement('div');
                div.textContent = text;
                terminal.appendChild(div);
                terminal.scrollTop = terminal.scrollHeight;
            }
            input.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    const command = input.value;
                    input.value = '';
                    addLine('> ' + command);
                    fetch('/streamlit/command', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ command })
                    })
                    .then(res => res.json())
                    .then(data => {
                        addLine(data.stdout || '');
                        addLine(data.stderr || '');
                    });
                }
            });
            addLine('Welcome to the AI Terminal!');
            addLine('Type your command and press Enter.');
        </script>
    </body>
    </html>
    """
    st.components.v1.html(html_code, height=600)

# Render terminal UI
render_terminal()

# Execute Python commands
if "command" not in st.session_state:
    st.session_state.command = ""

st.session_state.command = st.text_input("Enter a Python command:")
if st.button("Run Command"):
    stdout, stderr = execute_command(st.session_state.command, temp_dir)
    st.text_area("Command Output", value=stdout + stderr, height=300)

# Upload/Download files
uploaded_file = st.file_uploader("Upload a file to process")
if uploaded_file:
    file_path = os.path.join(temp_dir, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())
    st.success(f"Uploaded file saved to {file_path}")

# Show available files for download
if os.listdir(temp_dir):
    st.markdown("### Available Files for Download:")
    for file_name in os.listdir(temp_dir):
        file_path = os.path.join(temp_dir, file_name)
        with open(file_path, "rb") as f:
            st.download_button(
                label=f"Download {file_name}",
                data=f,
                file_name=file_name,
            )

# Clear temporary files
if st.button("Clear Temporary Files"):
    shutil.rmtree(temp_dir)
    os.mkdir(temp_dir)
    st.success("Temporary files cleared!")
