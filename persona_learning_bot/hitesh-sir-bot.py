import streamlit as st
import os
import sys
import subprocess
from dotenv import load_dotenv

# Relaunch script using Streamlit if run as a standard Python script directly
if not st.runtime.exists():
    print("Launching Hitesh Sir Multi-Persona Dashboard in Streamlit...")
    subprocess.run(["streamlit", "run", sys.argv[0]] + sys.argv[1:])
    sys.exit()

# Set Streamlit page configuration (must be called as the very first Streamlit command)
st.set_page_config(
    page_title="Chai aur Code Learning Portal",
    page_icon="☕",
    layout="wide"
)

# Load environment variables
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Prevent execution if no API key is provided
if not api_key:
    st.error("⚠️ Gemini API Key not found! Please define GEMINI_API_KEY in your .env file to proceed.")
    st.stop()

# Initialize Google GenAI client
from google import genai
client = genai.Client(api_key=api_key)

# Import and execute the dashboard rendering logic from dashboard.py
from dashboard import run_dashboard
run_dashboard(client)
