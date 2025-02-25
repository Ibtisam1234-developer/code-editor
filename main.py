import streamlit as st
import requests
import json
import subprocess
import sys
import time
import google.generativeai as genai

# Configure Gemini AI
API_KEY = "AIzaSyBymOuraxBaTfeWM5dAGLldWNUq7bEm5oY"  # Replace with your actual API key
genai.configure(api_key=API_KEY)

def query_ai(prompt):
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt)
        return response.text if response else "No response from AI."
    except Exception as e:
        return f"\n[AI Error] {str(e)}\n"

def run_code(code):
    try:
        exec_output = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True)
        return exec_output.stdout + exec_output.stderr
    except Exception as e:
        return str(e)

def run_terminal_command(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.stdout + result.stderr
    except Exception as e:
        return str(e)

st.title("AI-Powered Code Editor")

uploaded_file = st.file_uploader("Upload a Python file", type=["py"])
if uploaded_file:
    code = uploaded_file.read().decode("utf-8")
else:
    code = ""  # Default empty code

code = st.text_area("Write your Python code:", code, height=400)

# Save As Feature
def save_file(content):
    with open("saved_code.py", "w") as f:
        f.write(content)
    return "File saved as saved_code.py"

if st.button("Save As"):
    save_message = save_file(code)
    st.success(save_message)

if st.button("Run Code"):
    output = run_code(code)
    st.subheader("Output:")
    st.code(output, language="python")

# AI Assistant Sidebar
st.sidebar.title("AI Assistant")
ai_query = st.sidebar.text_area("Ask AI anything:")
if st.sidebar.button("Get AI Response"):
    with st.spinner("AI is thinking..."):
        ai_response = query_ai(ai_query)
    st.sidebar.text_area("AI Response:", ai_response, height=200)

# Terminal Section
st.sidebar.title("Terminal")
terminal_command = st.sidebar.text_input("Enter a command:")
if st.sidebar.button("Run Command"):
    terminal_output = run_terminal_command(terminal_command)
    st.sidebar.text_area("Terminal Output:", terminal_output, height=200)
