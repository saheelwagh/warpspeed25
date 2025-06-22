import streamlit as st
import os
import time
from dotenv import load_dotenv
from litellm import completion
# --- 1. Load Environment Variables & LLM ---
load_dotenv()

# We need to import the necessary classes from crewai and langchain
from langchain_google_genai import ChatGoogleGenerativeAI
from crewai import Agent, Task, Crew, Process
# We'll import a tool for our writer agent to use
from crewai_tools import FileReadTool

# Explicitly load your Google credentials
gemini_api_key = os.getenv("GEMINI_API_KEY")

# Initialize LLM - we'll only proceed if the key is available
llm = None
if gemini_api_key:
    llm=ChatGoogleGenerativeAI(model="gemini-2.0-flash-lite-001",
                           verbose=True,
                           temperature=0.5,
                           google_api_key=os.getenv("GOOGLE_API_KEY"))
    llm2 = completion(
        model="gemini-2.0-flash-lite-001",
                           verbose=True,
                           temperature=0.5,
                           google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    print("INFO: LLM connection configured successfully.")
else:
    print("ERROR: GEMINI_API_KEY not found. LLM not loaded.")

# --- 2. Page Configuration & Styling ---
st.set_page_config(
    page_title="Content Engine - Upgrade",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for a polished dark mode theme
st.markdown("""
<style>
    .stApp {
        background-color: #0f172a; /* Dark Slate background */
        color: #e2e8f0; /* Light Slate text for good contrast */
    }
    .main-container {
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 80vh;
    }
    .paywall-box {
        background-color: #1e293b; /* Lighter Slate for the box */
        padding: 40px;
        border-radius: 15px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        text-align: center;
        max-width: 600px;
        border-top: 5px solid #3b82f6; /* Bright blue accent */
    }
    h1 {
        color: #ffffff;
        font-weight: bold;
    }
    h2 {
        color: #94a3b8;
    }
    .st-emotion-cache-1wivap2 {
        background-color: rgba(59, 130, 246, 0.1);
        border: 1px solid rgba(59, 130, 246, 0.5);
    }
    .stButton>button {
        background-color: #3b82f6;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 12px 28px;
        font-size: 18px;
        font-weight: bold;
        margin-top: 20px;
    }
    .stButton>button:hover {
        background-color: #60a5fa;
        color: white;
    }
</style>
""", unsafe_allow_html=True)


# --- 3. x402 Payment Simulation ---
# This function simulates the backend API protected by x402.
def simulate_x402_backend(headers=None):
    if headers and 'X-PAYMENT' in headers:
        print("BACKEND: Payment header received. Granting access.")
        return {'status_code': 200, 'message': 'Payment Verified'}
    else:
        print("BACKEND: No payment header. Demanding payment with 402.")
        return {'status_code': 402, 'message': 'Payment Required'}

# This function simulates the client-side logic to handle a 402 response.
def process_x402_payment():
    with st.spinner("Requesting access..."):
        time.sleep(1)
        initial_response = simulate_x402_backend()

    if initial_response['status_code'] == 402:
        with st.spinner("Payment Required. Simulating transaction..."):
            print("CLIENT: Received 402. Simulating payment signing.")
            time.sleep(2) # Simulate user signing/confirming
            
            # Retry request with a dummy payment header
            dummy_header = {'X-PAYMENT': 'dummy_signed_payload'}
            final_response = simulate_x402_backend(headers=dummy_header)

            if final_response['status_code'] == 200:
                print("CLIENT: Payment successful.")
                return True
            else:
                st.error("Payment failed after retry.")
                return False
    return False

# --- 4. UI Layout ---
if 'article' not in st.session_state:
    st.session_state.article = None

st.markdown('<div class="main-container">', unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="paywall-box">', unsafe_allow_html=True)
    
    st.title("You've Reached Your Weekly Limit")
    st.write("You've generated your 3 free articles for this week. Great job!")
    st.info("To continue creating, simply upload a topic or journal entry below.")
    
    st.header("Create Your Next Article")

    uploaded_file = st.file_uploader(
        "Upload a topic brief or journal entry (.txt or .md)",
        type=['txt', 'md'],
        label_visibility="collapsed"
    )

    if uploaded_file is not None:
        if st.button("💳 Generate Article for $0.50", key="generate_paid_article"):
            if not llm:
                st.error("LLM not configured. Please set your GEMINI_API_KEY in the .env file.")
            else:
                # Step 1: Process the payment
                payment_successful = process_x402_payment()

                # Step 2: If payment is successful, run the agent
                if payment_successful:
                    with st.spinner("Payment verified. Generating your article..."):
                        
                        # Save the uploaded file to a temporary path for the agent to use
                        temp_file_path = os.path.join(".", uploaded_file.name)
                        with open(temp_file_path, "wb") as f:
                            f.write(uploaded_file.getbuffer())

                        # Define the Article Writer Agent and its Task
                        file_read_tool = FileReadTool()
                        writer_agent = Agent(
                            role="Expert Content Writer",
                            goal="Read the content from the provided file path and expand it into a high-quality, engaging article.",
                            backstory="You are a renowned content writer, known for your ability to turn simple ideas into compelling stories.",
                            llm=llm2,
                            tools=[file_read_tool],
                            verbose=True
                        )
                        writing_task = Task(
                            description=f"Read the content from the file at '{temp_file_path}'. Use this content as the brief to write a full, engaging article. The article should be well-structured, informative, and at least 300 words long.",
                            expected_output="A complete article in markdown format.",
                            agent=writer_agent
                        )
                        
                        # Create and run the crew
                        writing_crew = Crew(
                            agents=[writer_agent],
                            tasks=[writing_task],
                            verbose=True
                        )
                        
                        article_result = writing_crew.kickoff()
                        st.session_state.article = article_result
                        
                        # Clean up the temp file
                        os.remove(temp_file_path)

                        st.success("Your new article has been generated!")
                        st.balloons()
            
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Display the final generated article if it exists
if st.session_state.article:
    st.markdown("---")
    st.header("Your Generated Article")
    st.markdown(st.session_state.article)

