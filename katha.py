import streamlit as st
import time
import os
from dotenv import load_dotenv
load_dotenv()
# Re-import the specific library for Google Gemini
from langchain_google_genai import ChatGoogleGenerativeAI
from crewai import Agent, Task, Crew, Process

# --- Configuration & Setup ---

# Load environment variables
gemini_api_key = os.getenv("GEMINI_API_KEY")
google_cloud_project = os.getenv("GOOGLE_CLOUD_PROJECT")

# Page Configuration
st.set_page_config(
    page_title="Weaver",
    page_icon="✍️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Terminal Status Checks (Formerly Streamlit Success/Error Messages) ---
# These messages will now print to your terminal, not the webpage.
if not gemini_api_key:
    print("ERROR: GEMINI_API_KEY not found in .env file.")
else:
    print("INFO: GEMINI_API_KEY loaded successfully.")

if not google_cloud_project:
    print("ERROR: GOOGLE_CLOUD_PROJECT not found in .env file.")
else:
    print("INFO: GOOGLE_CLOUD_PROJECT loaded successfully.")

# --- Custom CSS ---
st.markdown("""
<style>
    /* Main container styling */
    .stApp {
        background-color: #FFFFFF;
        color: #333333;
    }
    /* Title styling */
    h1 {
        color: #2c3e50;
        font-weight: bold;
        text-align: center;
    }
    /* Subheader styling */
    .st-emotion-cache-1y4p8pa {
        text-align: center;
        color: #7f8c8d;
    }
    /* Main headers for sections */
    h2 {
        color: #34495e;
        border-bottom: 2px solid #bdc3c7;
        padding-bottom: 5px;
        margin-top: 2em;
    }
    /* Button styling */
    .stButton>button {
        background-color: #2c3e50;
        color: white;
        border-radius: 8px;
        border: 1px solid #2c3e50;
        padding: 10px 24px;
        font-size: 16px;
        font-weight: bold;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #34495e;
        border: 1px solid #34495e;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# --- Header Section ---
st.title("Weaver ✍️")
st.subheader("Transform your daily thoughts into beautiful narratives.")
st.write("---")

# --- Main Application Logic & Input ---
if 'narrative_generated' not in st.session_state:
    st.session_state.narrative_generated = False

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.header("Turn Your Reflections into a Content Piece")
    st.markdown("""
    Prepare your journal entry in a `.txt` or `.md` file using the **Bullet Journal method**. Our AI understands this syntax to weave your unique story.
    
    - **Tasks:** Start with `•` 
    - **Events:** Start with `○` 
    - **Notes/Thoughts:** Start with `—` 
    - **Priority:** Mark any bullet with `*` 
    - **Inspiration:** Mark any bullet with `!` 
    """)

    uploaded_file = st.file_uploader(
        "Upload your journal entry",
        type=['txt', 'md'],
        accept_multiple_files=False
    )

    if uploaded_file is not None:
        user_log_input = uploaded_file.getvalue().decode("utf-8")
        
        with st.expander("Preview your uploaded log"):
            st.text(user_log_input)

        if st.button("Weave My Reflection"):
            st.session_state.narrative_generated = True
            
            with st.spinner("✍️ Weaver is interpreting your log and crafting your narrative..."):
                # This is where you will eventually kick off your crew
                time.sleep(4) # Simulating AI work
            
            # Replaced st.success and st.balloons with a print statement
            print("SUCCESS: Narrative has been generated.")
    
# --- Output Section ---
if st.session_state.narrative_generated:
    # We keep the 'col2' context to ensure the output is also centered
    with st.columns([1, 2, 1])[1]: 
        st.header("Your Woven Narrative")
        
        # This will be replaced with the actual output from your agent
        st.markdown("""
        > *Today was defined by a major breakthrough, a priority insight that shifted my entire focus. The decision to pivot to a new, more personal idea felt deeply authentic—a true moment of inspiration that cast a new light on everything. It even seemed to make the morning coffee taste that much better.*

        > *With this new creative energy comes a clear intention: I need to outline the new app structure. A key event is already on the books—the 10 AM team meeting, where this exciting new path can be shared and solidified.*
        """)