import streamlit as st

# Set page configuration
st.set_page_config(
    page_title="AI-Powered Terminal",
    layout="wide",  # Use the entire width
    initial_sidebar_state="collapsed",
)

# Hide Streamlit branding and make the terminal full screen
hide_streamlit_style = """
    <style>
    /* Hide Streamlit elements */
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

# Embed HTML in Streamlit
def render_terminal():
    html_code = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>AI-Powered Terminal Chat (Fast Typing)</title>
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
            .line {
                margin: 5px 0;
                overflow: hidden;
                white-space: nowrap;
            }
            .typed {
                overflow: hidden;
                white-space: nowrap;
                animation: typing 0.5s steps(30, end);
            }
            @keyframes typing {
                from { width: 0; }
                to { width: 100%; }
            }
            @media (max-width: 768px) {
                #terminal {
                    font-size: 14px;
                }
                #user-input, #send-btn {
                    font-size: 14px;
                }
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

            function typeWriter(text, lineElement, index = 0) {
                if (index < text.length) {
                    lineElement.textContent += text.charAt(index);
                    setTimeout(() => typeWriter(text, lineElement, index + 1), Math.random() * 10 + 5); // Faster typing speed
                } else {
                    lineElement.classList.remove('typed');
                    terminal.scrollTop = terminal.scrollHeight;
                }
            }

            function addLine(text, isUser = false) {
                const lineElement = document.createElement('div');
                lineElement.classList.add('line', 'typed');
                if (isUser) {
                    lineElement.style.color = '#ff0';
                    lineElement.textContent = '> ' + text;
                    terminal.appendChild(lineElement);
                    terminal.scrollTop = terminal.scrollHeight;
                } else {
                    terminal.appendChild(lineElement);
                    typeWriter(text, lineElement);
                }
            }

            function toggleFullScreen() {
                if (!document.fullscreenElement) {
                    document.documentElement.requestFullscreen();
                    addLine("Entering fullscreen mode...");
                } else {
                    if (document.exitFullscreen) {
                        document.exitFullscreen();
                        addLine("Exiting fullscreen mode...");
                    }
                }
            }

            function processCommand(command) {
                addLine(command, true);
                
                setTimeout(() => {
                    switch(command.toLowerCase()) {
                        case 'help':
                            addLine("Available commands: help, download, clear, cs (toggle fullscreen)");
                            break;
                        case 'download':
                            addLine("Initiating download sequence...");
                            setTimeout(() => {
                                addLine("File downloaded successfully!");
                            }, 1000); // Faster download simulation
                            break;
                        case 'clear':
                            terminal.innerHTML = '';
                            break;
                        case 'cs':
                            toggleFullScreen();
                            break;
                        default:
                            addLine("Unknown command. Type 'help' for available commands.");
                    }
                }, 200); // Faster response time
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

            // Initial messages
            addLine("Welcome to the AI-Powered Terminal Chat!");
            addLine("Type 'help' for available commands.");
        </script>
    </body>
    </html>
    """
    st.components.v1.html(html_code, height=800)

# Render the full-screen terminal
render_terminal()
