import streamlit as st
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from crewai import Agent, Task, Crew, Process
from crewai_tools import FileReadTool # Import the pre-built tool

# --- Configuration & Setup ---
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

# --- Page Configuration & CSS ---
st.set_page_config(page_title="Weaver", page_icon="✍️", layout="wide", initial_sidebar_state="collapsed")
st.markdown("""
<style>
    /* ... Your existing CSS goes here ... */
    .stApp { background-color: #FFFFFF; color: #333333; }
    h1 { color: #2c3e50; font-weight: bold; text-align: center; }
    .st-emotion-cache-1y4p8pa { text-align: center; color: #7f8c8d; }
    h2 { color: #34495e; border-bottom: 2px solid #bdc3c7; padding-bottom: 5px; margin-top: 2em; }
    .stButton>button { background-color: #2c3e50; color: white; border-radius: 8px; border: 1px solid #2c3e50; padding: 10px 24px; font-size: 16px; font-weight: bold; width: 100%; }
    .stButton>button:hover { background-color: #34495e; border: 1px solid #34495e; color: white; }
</style>
""", unsafe_allow_html=True)


# --- LLM Initialization ---
# We only proceed if the API key is available
if gemini_api_key:
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-lite-001", google_api_key=gemini_api_key)
else:
    llm = None


# --- Header Section ---
st.title("Weaver ✍️")
st.subheader("Transform your daily thoughts into beautiful narratives.")
st.write("---")


# --- Main Application ---
if 'narrative' not in st.session_state:
    st.session_state.narrative = ""

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.header("Turn Your Reflections into a Content Piece")
    st.markdown("""
    Prepare your journal entry in a `.txt` or `.md` file using the **Bullet Journal method**. Our AI understands this syntax to weave your unique story.
    - **Tasks:** `•` | **Events:** `○` | **Notes:** `—` | **Priority:** `*` | **Inspiration:** `!` 
    """)

    uploaded_file = st.file_uploader("Upload your journal entry", type=['txt', 'md'])

    if uploaded_file is not None:
        # Create a temporary path to save the file
        temp_file_path = os.path.join(".", uploaded_file.name)
        
        # Save the uploaded file to the temporary path
        with open(temp_file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        with st.expander("Preview your uploaded log"):
            st.text(uploaded_file.getvalue().decode("utf-8"))

        if st.button("Weave My Reflection"):
            if not llm:
                st.error("Gemini API Key is not configured. Please check your .env file.")
            else:
                with st.spinner("✍️ Weaver is interpreting your log and crafting your narrative..."):
                    # --- Agent & Task Definition ---
                    
                    # 1. Instantiate the pre-built tool
                    file_read_tool = FileReadTool()

                    # 2. Define the "Journalist" Agent
                    journalist_agent = Agent(
                        role="Empathetic Journal Weaver",
                        goal="To read a user's bullet journal entry from a file and transform it into a beautiful, first-person narrative that captures the essence of their day.",
                        backstory=(
                            "You are a master storyteller with a deep understanding of human emotion and the art of journaling. "
                            "You can find the hidden story in simple notes and weave them together into a compelling and reflective piece of writing."
                        ),
                        llm=llm,
                        tools=[file_read_tool],
                        verbose=True,
                        allow_delegation=False,
                    )

                    # 3. Define the Weaving Task
                    # 3. Define the Weaving Task (Corrected)
                    weaving_task = Task(
                        # Add 'f' to make this an f-string and insert the variable directly
                        description=f"""
                        You must read the user's journal entry from the file located at: '{temp_file_path}'.
                        Interpret the entry based on the Bullet Journal method (`•` Tasks, `○` Events, `—` Notes, `*` Priority, `!` Inspiration).
                        Do not just list the items. Weave them into a cohesive, first-person narrative. 
                        Capture the underlying mood and themes of the day. The final output should be a formatted markdown text.
                        """,
                        expected_output=(
                            "A beautifully written, reflective narrative in markdown format. It should feel like a personal story, not a summary."
                        ),
                        agent=journalist_agent
                        # The 'context' parameter has been removed
                    )
                    # 4. Create and Kick off the Crew
                    story_crew = Crew(
                        agents=[journalist_agent],
                        tasks=[weaving_task],
                        process=Process.sequential,
                        verbose=True,
                    )

                    narrative_result = story_crew.kickoff()
                    st.session_state.narrative = narrative_result

                    # Clean up the temporary file
                    os.remove(temp_file_path)

# --- Output Section ---
if st.session_state.narrative:
    with st.columns([1, 2, 1])[1]:
        st.header("Your Woven Narrative")
        st.markdown(st.session_state.narrative)