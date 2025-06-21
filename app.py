import os
import streamlit as st
from crewai import Agent, Task, Crew, Process
from langchain_groq import ChatGroq
from dotenv import load_dotenv

# --- Step 1: Load Environment Variables ---
load_dotenv()

# --- Streamlit Frontend ---
st.title("🔑 API Key Diagnostic Tool")
st.markdown(f"**Location:** Madel, Goa, India | **Time:** {os.getenv('CURRENT_TIME_IST', 'Now')}")

# --- Step 2: API KEY DIAGNOSTIC ---
st.subheader("API Key Status")
api_key = os.environ.get("GROQ_API_KEY")

if api_key:
    st.success("✅ GROQ_API_KEY was found in the environment.")
    # Display a redacted version of the key for verification
    st.text(f"Key being used: {api_key[:7]}...{api_key[-4:]}")
else:
    st.error("🔴 GROQ_API_KEY NOT FOUND. Please check your .env file.")
    st.stop()


# --- Step 3: Configure the LLM ---
# We are going back to the stable LangChain Groq class and passing the key directly.
try:
    llm = ChatGroq(
        model_name="llama3-8b-8192",
        temperature=0.7,
        groq_api_key=api_key # We pass the key directly here
    )
    st.success("✅ LLM configured successfully.")

except Exception as e:
    st.error(f"🔴 Error configuring the LLM: {e}")
    st.stop()


# --- Main App Logic ---
topic = st.text_input("Enter a topic for the agent:", "finally fixing this API key issue")

if st.button("Run Agent Crew"):
    if not topic:
        st.warning("Please enter a topic.")
    else:
        with st.spinner("🚀 Agent is running..."):
            try:
                # Agent and Task setup remains the same
                final_agent = Agent(
                    role="System Administrator",
                    goal=f"Confirm the API connection is working by writing about {topic}.",
                    backstory="You are an expert in resolving API authentication issues.",
                    llm=llm,
                    verbose=True
                )
                final_task = Task(
                    description=f"Write a short, successful confirmation message about {topic}.",
                    expected_output="A single success paragraph.",
                    agent=final_agent
                )
                final_crew = Crew(agents=[final_agent], tasks=[final_task], verbose=True)

                result = final_crew.kickoff()

                st.success("IT WORKS! The agent returned a result.")
                st.markdown("---")
                st.markdown("### ✅ Agent Confirmation Message:")
                st.write(result)

            except Exception as e:
                st.error(f"An error occurred while running the crew: {e}")