import os
import streamlit as st
from crewai import Agent, Task, Crew, Process, LLM
from langchain_groq import ChatGroq
from dotenv import load_dotenv

# --- Load Environment Variables ---
load_dotenv()
st.title("🚀 Final Build: Pip + Venv + Groq")

# --- API Key Check ---
api_key = os.environ.get("GROQ_API_KEY")
if not api_key:
    st.error("🔴 GROQ_API_KEY NOT FOUND. Please check your .env file.")
    st.stop()
else:
    st.success("✅ GROQ_API_KEY found.")

# --- LLM Configuration: The Wrapping Method ---
# This is the most stable pattern to solve the library conflicts.
try:
    # 1. Create the LangChain Groq object
    langchain_groq_llm = ChatGroq(
        model_name="llama3-8b-8192",
        groq_api_key=api_key
    )

    # 2. Wrap the LangChain object in CrewAI's LLM class for compatibility
    crewai_llm = LLM(model="llama3-8b-8192", llm=langchain_groq_llm)

    st.success("✅ LLM configured and wrapped for CrewAI.")

except Exception as e:
    st.error(f"🔴 Error configuring LLM: {e}")
    st.stop()


# --- Main App Logic ---
topic = st.text_input("Enter a topic:", "a stable and working environment")

if st.button("Run Final Test"):
    with st.spinner("🚀 Agents launching... This is the final test."):
        try:
            # Create an agent using the wrapped LLM
            final_agent = Agent(
                role="Stability Engineer",
                goal=f"Confirm the system is fully operational by writing about {topic}.",
                backstory="I am an AI agent that only runs on stable, correctly configured systems.",
                llm=crewai_llm,
                verbose=True
            )

            # Create a task
            final_task = Task(
                description=f"Write a success message about {topic}.",
                expected_output="A single paragraph celebrating success.",
                agent=final_agent
            )

            # Create and run the crew
            final_crew = Crew(agents=[final_agent], tasks=[final_task], verbose=True)
            result = final_crew.kickoff()

            st.success("IT'S WORKING! The agent crew ran successfully.")
            st.markdown("---")
            st.markdown("### ✅ Agent Confirmation Message:")
            st.write(result)

        except Exception as e:
            st.error(f"An error occurred while running the crew: {e}")