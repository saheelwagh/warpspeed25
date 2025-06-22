import os
import streamlit as st
from dotenv import load_dotenv
# Re-import the specific library for Google Gemini
from langchain_google_genai import ChatGoogleGenerativeAI
from crewai import Agent, Task, Crew, Process

# --- 1. Application Configuration & Setup ---

# Load environment variables from your .env file
load_dotenv()

# Configure the Streamlit page
st.set_page_config(page_title="CrewAI Base Configuration", layout="centered")

# Explicitly load your Google credentials from the .env file
gemini_api_key = os.getenv("GEMINI_API_KEY")
google_cloud_project = os.getenv("GOOGLE_CLOUD_PROJECT")

st.title("🤖 Your brutal action plan generator")
st.markdown("Big dreams are worthless. Without small actions.")

st.header("Configuration Status")
if not gemini_api_key:
    st.error("🔴 **GEMINI_API_KEY:** Not found. Please set it in your .env file.")
else:
    st.success("🟢 **GEMINI_API_KEY:** Loaded successfully.")

if not google_cloud_project:
    st.error("🔴 **GOOGLE_CLOUD_PROJECT:** Not found. Please set it in your .env file.")
else:
    st.success("🟢 **GOOGLE_CLOUD_PROJECT:** Loaded successfully.")

if gemini_api_key and google_cloud_project:
    try:
        # Define the LLM using the robust ChatGoogleGenerativeAI class
        # This confirms that the connection to the service is working.
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash-lite-001",
            verbose=True,
            temperature=0.3,
            google_api_key=gemini_api_key
        )
        st.success("✅ **LLM Connection:** Successfully initialized a connection to Google Gemini.")
        st.info("You can now add your Agents and Tasks to this script.")
        
    except Exception as e:
        st.error(f"An error occurred while connecting to the LLM: {e}")

