import streamlit as st
import os
import google.generativeai as genai
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure Gemini Pro API
API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-pro')

# Define banking services and required details
services = {
    "fixed_deposit": ["amount", "tenure"],
    "mutual_fund": ["amount", "investment_type"],
    "money_transfer": ["amount", "recipient_account", "bank_name"]
}

# Helper functions
def get_service_intent(user_query):
    """Identifies the banking service based on user's natural language query."""
    prompt = f"Identify the banking service from the user query: '{user_query}'. Return one of these categories: fixed_deposit, mutual_fund, money_transfer."
    response = model.generate_content(prompt)
    return response.text.strip().lower()

def extract_details(user_query, service_type):
    """Extracts initial details provided in the user's query for the specific service."""
    prompt = f"Extract details (like amount, recipient_account, bank_name, etc.) for '{service_type}' from this query: '{user_query}'. Return details as a JSON with only these fields: {services[service_type]}."
    response = model.generate_content(prompt)
    try:
        extracted_details = json.loads(response.text)
        # Ensure only expected fields are returned
        return {key: value for key, value in extracted_details.items() if key in services[service_type]}
    except json.JSONDecodeError:
        return {}

def request_missing_details(service_type, provided_details):
    """Prompts user only for genuinely missing details."""
    missing_fields = [field for field in services[service_type] if field not in provided_details]
    if missing_fields:
        prompt = f"Ask the user only for the following missing details: {', '.join(missing_fields)} for '{service_type}' service."
        response = model.generate_content(prompt)
        return response.text.strip()
    return ""

def confirm_details(service_type, details):
    """Generates a confirmation summary message for the user based on provided details."""
    prompt = f"Summarize the following details for '{service_type}' service: {details}. Confirm back in a concise, clear message."
    response = model.generate_content(prompt)
    return response.text.strip()

# Initialize conversation history in session state
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []

# Function to display chat history
def display_chat_history():
    for entry in st.session_state.conversation_history:
        st.write(entry["role"] + ": " + entry["message"])

# Streamlit App - Chat Interface
st.title("Banking Service Chatbot")

# Display chat history
display_chat_history()

# User input with clear after submission
user_input = st.text_input("You:", key="user_input", value="")

if st.button("Send"):
    if not user_input:
        st.error("Please enter a query.")
    else:
        # Add user input to conversation history
        st.session_state.conversation_history.append({"role": "User", "message": user_input})

        # Step 1: Identify Service Intent
        service_type = get_service_intent(user_input)
        
        if service_type not in services:
            response = "Sorry, I couldn't recognize the requested service. Please try again."
        else:
            # Step 2: Extract initial details
            provided_details = extract_details(user_input, service_type)

            # Step 3: Check and request missing details
            missing_info = request_missing_details(service_type, provided_details)
            if missing_info:
                response = f"I still need some more details to proceed: {missing_info}"
            else:
                # Step 4: Confirm details
                confirmation_message = confirm_details(service_type, provided_details)
                response = f"All details received! {confirmation_message}"

            # Add system response to conversation history
            st.session_state.conversation_history.append({"role": "System", "message": response})

# Display updated chat history
display_chat_history()
