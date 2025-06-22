import os
import streamlit as st
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from crewai.tools import BaseTool
# Import the specific library for Groq
from langchain_groq import ChatGroq

# --- 1. Application Configuration & Setup ---

# Load environment variables from your .env file
load_dotenv()

# Configure the Streamlit page
st.set_page_config(page_title="Gig Work Bot with AI Crew", layout="wide")

# Explicitly load your credentials from the .env file
groq_api_key = os.getenv("GROQ_API_KEY")

# Stop the app if credentials are not found, with a helpful message
if not groq_api_key:
    st.error("🔴 GROQ_API_KEY not found. Please set it in your .env file.")
    st.stop()


# --- 2. Placeholder Tools for the Gig Workflow ---

class TaskPostingTool(BaseTool):
    name: str = "Task Posting Tool"
    description: str = "Posts a new gig task to the platform."
    def _run(self, argument: str) -> str:
        print(f"--- Posting Task: {argument} ---")
        return f"Task '{argument}' has been successfully posted."

class TaskExecutionTool(BaseTool):
    name: str = "Task Execution Tool"
    description: str = "Simulates the work being done for a given task."
    def _run(self, argument: str) -> str:
        print(f"--- Executing Task: {argument} ---")
        return f"Completed work for '{argument}': A detailed summary of recent AI advancements."

class VerificationTool(BaseTool):
    name: str = "Work Verification Tool"
    description: str = "Verifies if the completed work meets the task requirements."
    def _run(self, argument: str) -> str:
        print(f"--- Verifying Work: {argument} ---")
        return "Verification Status: Approved"

class PaymentTool(BaseTool):
    name: str = "Payment Processing Tool"
    description: str = "Processes payment to a contributor for a completed and verified task."
    def _run(self, argument: str) -> str:
        print(f"--- Processing Payment for: {argument} ---")
        return f"Payment of $15 processed successfully for task '{argument}'."


# --- 3. Crew Setup Function ---

def setup_crew(gig_description: str):
    """
    Sets up the Gig Work Bot crew using the robust ChatGroq class.
    """
    
    # Define the LLM using the ChatGroq class.
    # We use a fast and capable model available on Groq.
    llm = ChatGroq(
        temperature=0.3,
        groq_api_key=groq_api_key,
        model_name="groq/llama3-8b-819" # A popular and fast model
    )

    # Instantiate the tools
    task_tool = TaskPostingTool()
    execution_tool = TaskExecutionTool()
    verification_tool = VerificationTool()
    payment_tool = PaymentTool()

    # Define the agents for the new crew
    project_manager = Agent(
        role='Project Manager',
        goal=f'Define the gig task "{gig_description}", find a contributor, and manage the workflow.',
        backstory='An experienced project manager skilled in breaking down tasks and delegating effectively.',
        verbose=True,
        tools=[task_tool],
        llm=llm
    )
    gig_worker = Agent(
        role='Gig Worker',
        goal='Execute the assigned task to the highest standard and submit it for verification.',
        backstory='A skilled freelancer specializing in digital tasks, known for reliability and attention to detail.',
        verbose=True,
        tools=[execution_tool],
        llm=llm
    )
    qa_specialist = Agent(
        role='Quality Assurance Specialist',
        goal='Rigorously check the submitted work against the original requirements and approve or reject it.',
        backstory='A meticulous QA professional with an uncompromising eye for detail and quality.',
        verbose=True,
        tools=[verification_tool],
        llm=llm
    )
    payment_processor = Agent(
        role='Payment Processor',
        goal='Process payments to contributors for successfully verified tasks.',
        backstory='An automated financial system that ensures prompt and accurate payments upon task approval.',
        verbose=True,
        tools=[payment_tool],
        llm=llm
    )

    # Define the tasks for the new crew
    task_definition = Task(
        description=f'Define and post the gig task: "{gig_description}".',
        expected_output='A confirmation that the task has been posted.',
        agent=project_manager
    )
    task_execution = Task(
        description='Execute the gig task that was just posted.',
        expected_output='The completed work, ready for verification.',
        agent=gig_worker
    )
    task_verification = Task(
        description='Verify the completed work against the task requirements. Use the verification tool.',
        expected_output="A verification status report, either 'Approved' or 'Rejected'.",
        agent=qa_specialist
    )
    task_payment = Task(
        description='If the work was approved, use the payment tool to process payment to the contributor.',
        expected_output='A payment confirmation receipt or a message stating no payment was made.',
        agent=payment_processor
    )
    
    # Assemble and return the crew
    return Crew(
        agents=[project_manager, gig_worker, qa_specialist, payment_processor],
        tasks=[task_definition, task_execution, task_verification, task_payment],
        process=Process.sequential,
        verbose=True
    )

# --- 4. Streamlit User Interface ---

st.title("🤖 Gig Work Bot")
st.markdown("""
This application simulates a gig workflow using a team of AI agents.
Enter a task description, and the AI crew will manage it from posting to payment.
""")

# User input for the gig description
gig_description = st.text_input(
    "Enter the gig task you want to delegate:",
    "Create a one-paragraph summary of the latest AI news."
)

if st.button("Start Gig Workflow", type="primary"):
    if not gig_description:
        st.warning("Please enter a gig description.")
        st.stop()
        
    # Create the crew object with the user's input
    gig_crew = setup_crew( gig_description)

    # Run the crew in a spinner to show activity
    with st.spinner("The AI crew is managing the gig..."):
        try:
            # Kick off the crew
            result = gig_crew.kickoff()
            # Store the result in the session state
            st.session_state.result = result
        except Exception as e:
            st.error(f"An error occurred: {e}")
            st.session_state.result = None

# Display the final result if it exists
if 'result' in st.session_state and st.session_state.result:
    st.markdown("---")
    st.markdown("### Final Workflow Outcome:")
    with st.container(border=True):
        st.markdown(st.session_state.result)
