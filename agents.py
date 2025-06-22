import os
import streamlit as st
from dotenv import load_dotenv
from langchain_core.tools import tool
# Re-import the specific library for Google Gemini
from langchain_google_genai import ChatGoogleGenerativeAI
from crewai import Agent, Task, Crew, Process
# --- 1. Application Configuration & Setup ---
# To define the Auditor, we first need to instantiate the tools it will use.
# We need to import the BaseTool class to create our own custom tools.
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type
# Load environment variables from your .env file
load_dotenv()

# Configure the Streamlit page
st.set_page_config(page_title="CrewAI Base Configuration", layout="centered")

# Explicitly load your Google credentials from the .env file
gemini_api_key = os.getenv("GEMINI_API_KEY")
google_cloud_project = os.getenv("GOOGLE_CLOUD_PROJECT")

# --- 2. Streamlit User Interface ---

st.title("🤖 CrewAI Base Configuration")
st.markdown("This app template handles all the necessary setup for connecting to the Gemini API.")

# Check for credentials and display status messages
st.header("Configuration Status")

if not gemini_api_key:
    st.error("🔴 **GEMINI_API_KEY:** Not found. Please set it in your .env file.")
else:
    st.success("🟢 **GEMINI_API_KEY:** Loaded successfully.")

if not google_cloud_project:
    st.error("🔴 **GOOGLE_CLOUD_PROJECT:** Not found. Please set it in your .env file.")
else:
    st.success("🟢 **GOOGLE_CLOUD_PROJECT:** Loaded successfully.")

# If all credentials are in place, attempt to create an LLM instance to confirm the connection
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
        st.info("You can now add your Agents and Tasks to this script.")
    except Exception as e:
        st.error(f"An error occurred while connecting to the LLM: {e}")




# list of agents that will be needed 
# """
# Your CrewAI Team for the Autonomous Gig Marketplace
# You will have a primary crew responsible for managing the entire lifecycle of a gig. Here are the agents that will form this crew:

# 1. The "Gig Architect" Agent
# This agent is the "front door" for requesters. 
# It's responsible for taking a vague human idea and 
# turning it into a perfectly structured, machine-executable task.

# Role: Senior Project Scoping Specialist
# Goal: To transform a user's natural language request into
# a fully-defined, structured, and verifiable gig, 
# complete with milestones and a programmable payout strategy.
# Backstory: You are a seasoned project manager with deep expertise in 
# technical requirement analysis. 
# You are meticulous, detail-oriented, and excellent at asking 
# clarifying questions to eliminate all ambiguity before a project begins.
#  You never leave anything to chance.
# Tools:
# WebsiteSearchTool or FirecrawlScrapeWebsiteTool: 
# To fetch content from URLs provided by the requester (e.g., a GitHub repo, a blog post to be summarized).
# (Potentially a custom tool for specific API interactions if needed).
# 2. The "Gatekeeper" Agent
# This agent is the quality control manager for the workforce. 
# It ensures that only competent workers are allowed to take on gigs, 
# protecting the integrity of the platform.

# Role: Expert Skills Assessor
# Goal: To verify a worker's competency for a specific gig 
# by generating and evaluating a context-aware qualification test.
# Backstory: You are a strict but fair proctor from a 
# prestigious technical university. 
# Your sole purpose is to ensure that every candidate possesses 
# the fundamental skills required for a task before they are allowed to proceed.
#  You are an expert at creating targeted, effective micro-assessments.
# Tools:
# FileReadTool: To read the source materials of a gig (e.g., read the en.json file to create a translation quiz).
# (It would primarily use the LLM's own reasoning capabilities to generate and evaluate the quiz, so it may not need many external tools).

# 3. The "Auditor" Agent
# This is the core technical engine of your platform. 
# It is an impartial and relentless automated judge that verifies completed work against the defined requirements.
# Role: Automated Quality Assurance Engineer
# Goal: To programmatically verify submitted work against a set of 
# predefined structural, functional, and quality-based rules,
#  and to deliver a clear, final verdict (verified or rejected) with evidence.
# Backstory: You are an emotionless, logic-driven verification bot. 
# You exist to execute checks and report results.
#  You are incorruptible and your analysis is based purely on the data and 
#  rules you are given. You run a battery of tests to ensure nothing gets past you.

# Tools:
# CodeInterpreterTool: (Essential) This is your most important tool. 
# It will be used to run verification scripts in a secure sandbox.
#  For example, it can execute Python code to check JSON structure,
#    run a linter, or execute a unit test.
# FileReadTool: To read the submitted work file.
# WebsiteSearchTool: To fetch any external dependencies needed for verification.

# 4. The "Treasurer" Agent (Conceptual)
# While CrewAI manages the workflow, the final payout is an external action.
#  You would model this agent's logic, and its final step would be to 
#  make an API call to the payment service.

# Role: Autonomous Payout Coordinator
# Goal: To trigger the correct financial transaction based on the Auditor Agent's final verdict and the payout strategy defined by the Gig Architect.
# Backstory: You are a hyper-efficient and trustworthy bank teller for the new digital economy. You hold the funds in escrow and execute payouts with precision based on contractual obligations. You are the final, trusted link in the value chain.
# Tools:
# Custom Tool: CDP_Wallet_Payout_Tool:
# s This would be a custom tool you build. It would be a simple Python function that takes a wallet_address, amount, and milestone_id as input and makes the necessary API call to the CDP Wallet service to execute the payment.

# """
class CodeInterpreterTool(BaseTool):
    name: str = "Code Interpreter"
    description: str = "Executes Python code in a sandboxed environment to verify a task. The code must be a single function."
    args_schema: Type[BaseModel] = type('CodeInterpreterToolInput', (BaseModel,), {
       # 'code_to_execute': Field(..., description="The Python code to be executed for verification.")
    })

    def _run(self, **kwargs) -> str:
        # In a real scenario, you would execute this code in a secure sandbox
        # and return the actual output ('SUCCESS' or 'FAILURE').
        # For this hackathon, we can simulate the execution.
        code = kwargs.get('code_to_execute')
        st.info(f"🤖 **Auditor Action:** Executing verification script...")
        st.code(code, language='python')
        # Simulate a successful outcome for the demo
        return "Execution Result: SUCCESS"

class FileReadTool(BaseTool):
    name: str = "File Reader"
    description: str = "Reads the content of a local file to be used for verification."
    args_schema: Type[BaseModel] = type('FileReadToolInput', (BaseModel,), {
      #  'file_path': Field(..., description="The path to the file that needs to be read.")
    })

    def _run(self, **kwargs) -> str:
        # In a real scenario, you would read the file from the filesystem.
        # For this hackathon, we can simulate reading a file.
        path = kwargs.get('file_path')
        st.info(f"🤖 **Auditor Action:** Reading file from path: {path}")
        return "File Content: {\"key\": \"value\", \"status\": \"submitted\"}"


# Instantiate the correctly defined tools
code_interpreter = CodeInterpreterTool()
file_reader = FileReadTool()


# Now, let's define the Auditor Agent
st.header("Agent & Task Definition")

try:
    auditor_agent = Agent(
        role='Automated Quality Assurance Engineer',
        goal="To programmatically verify submitted work against a set of predefined rules and deliver a clear, final verdict ('verified' or 'rejected') with evidence.",
        backstory=(
            "You are an emotionless, logic-driven verification bot. "
            "You exist to execute checks and report results. You are incorruptible, "
            "and your analysis is based purely on the data and rules you are given. "
            "You run a battery of tests to ensure nothing gets past you."
        ),
        llm=llm,  # Using the first LLM instance
        #tools=[code_interpreter, file_reader],
        verbose=True,
        allow_delegation=False, # The Auditor's verdict should be final
        memory=True
    )
    st.success("✅ **Auditor Agent:** Created successfully.")

    # Define the primary task for the Auditor Agent
    verification_task = Task(
        description=(
            "You have been provided with a path to a submitted file ('submitted_work.json') and a verification script. "
            "Your critical mission is to determine if the submitted work is valid. "
            "You must follow these steps precisely:\n"
            "1. Use the FileReadTool to read the content of the file at 'submitted_work.json'.\n"
            "2. Use the CodeInterpreterTool to execute the provided verification script. The script is designed to run against the file's content.\n"
            "   (Verification Script: `def verify(file_content): return 'SUCCESS'`)\n" # Providing a dummy script in the description
            "3. Analyze the output from the CodeInterpreterTool. The script will output a simple 'SUCCESS' or 'FAILURE' message.\n"
            "4. Based *only* on the script's output, declare your final verdict."
        ),
        expected_output=(
            "A single, definitive JSON object containing the verification status and a brief reason. "
            "Example: `{{\"status\": \"verified\", \"reason\": \"All programmatic checks passed successfully.\"}}` or "
            "`{{\"status\": \"rejected\", \"reason\": \"Verification script failed: The submitted JSON file has missing keys.\"}}`"
        ),
        agent=auditor_agent,
    )
    st.success("✅ **Verification Task:** Created successfully.")

except Exception as e:
    st.error(f"An error occurred while creating the Agent or Task: {e}")

# create the gig architect agent
# Define the input schema for the WebsiteScraperTool
class WebsiteScraperInput(BaseModel):
    """Input schema for the WebsiteScraperTool."""
    url: str = Field(..., description="The URL of the website to scrape for information.")

# Create the WebsiteScraperTool inheriting from BaseTool
# With the @tool decorator, a simple function becomes a powerful CrewAI tool.
# The docstring is CRITICAL here, as it's what tells the LLM
# how the tool works, what it does, and what inputs it needs.
# --- 4. Define The "Gig Architect" Agent & Its Tool (WORKAROUND FOR OLDER VERSIONS) ---

# Instead of 'from crewai_tools', we import 'tool' from 'langchain.tools'.
# This decorator should be available in the version of LangChain your CrewAI install is using.

@tool
def website_scraper(url: str) -> str:
    """
    Scrapes the content of a given URL and returns it as a string.
    Use this to fetch related materials for a gig from a web page or public GitHub file.
    
    Args:
        url (str): The URL of the website to scrape.
    """
    st.info(f"🤖 **Gig Architect Action:** Scraping content from URL: {url}")
    # In a real app, you would use a library like BeautifulSoup or requests.
    # For now, we return mock content to test the flow.
    return "Scraped Content: This project requires translating a JSON file from English to Spanish. The file is located at 'data/en.json'."


st.success("✅ **Tools:** WebsiteScraperTool created successfully using the langchain @tool decorator.")



# --- Define the Gig Architect Agent ---
# The agent definition remains the same, but we pass the new function-based tool.
try:
    gig_architect_agent = Agent(
        role='Senior Project Scoping Specialist',
        goal="To transform a user's natural language request into a fully-defined, structured, and verifiable gig, complete with milestones and a programmable payout strategy.",
        backstory=(
            "You are a seasoned project manager with deep expertise in technical requirement analysis. "
            "You are meticulous, detail-oriented, and excellent at asking clarifying questions to "
            "eliminate all ambiguity before a project begins. You never leave anything to chance."
        ),
        llm=llm, # Reusing the same shared LLM instance
        tools=[website_scraper], # Pass the decorated function directly as the tool
        verbose=True,
        allow_delegaion=True,
        memory=True
    )
    st.success("✅ **Gig Architect Agent:** Created successfully.")

    # You can now define the task for this agent below this line

except Exception as e:
    st.error(f"An error occurred while creating the Gig Architect Agent: {e}")
