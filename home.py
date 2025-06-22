import os
import streamlit as st
from dotenv import load_dotenv

# create payout page with a title and description
st.title("Auto Payout System")
st.write("This page will handle the payout process for users.")  

# upload code file
uploaded_file = st.file_uploader("Upload your payout code file", type=["py"], key="code file")
if uploaded_file is not None:
    # Save the uploaded file to a temporary location
    with open("payout_code.py", "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success("File uploaded successfully!")

    # Execute the uploaded code file
    # check if file is a python file
    if uploaded_file.name.endswith(".py"):
        try:
            # Execute the uploaded code file
            exec(open("payout_code.py").read())
            st.success("Payout code executed successfully!")
        except Exception as e:
            st.error(f"Error executing payout code: {e}")

