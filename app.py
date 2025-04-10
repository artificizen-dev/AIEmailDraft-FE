import streamlit as st
import pandas as pd
import requests
import json
from io import BytesIO

# Set page configuration
st.set_page_config(
    page_title="Email Drafting Tool",
    page_icon="📧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Define theme colors
PRIMARY_COLOR = "#4a4a9c"
SECONDARY_COLOR = "#4CAF50"
BACKGROUND_COLOR = "#f8f9fa"
TEXT_COLOR = "#333333"

# Custom CSS for styling
st.markdown("""
<style>
    .lead-card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        border-left: 5px solid #4CAF50;
        color: #333333;
    }
    .email-card {
        background-color: #f0f7ff;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 30px;
        border-left: 5px solid #2196F3;
        color: #333333;
    }
    .subject-line {
        font-weight: bold;
        color: #1a237e;
        margin-bottom: 10px;
        font-size: 16px;
    }
    .email-body {
        white-space: pre-line;
        font-family: Arial, sans-serif;
        color: #333333;
    }
    .section-header {
        background-color: #4a4a9c;
        color: white;
        padding: 12px;
        border-radius: 5px;
        margin-bottom: 15px;
    }
    .lead-name {
        color: #2e7d32;
        font-weight: bold;
        font-size: 18px;
    }
    .lead-info {
        color: #333333;
        margin-bottom: 6px;
    }
    .lead-label {
        font-weight: bold;
        color: #0d47a1;
    }
    .lead-value {
        color: #333333;
    }
    .notes-text {
        color: #555555;
        font-style: italic;
        background-color: #fffde7;
        padding: 10px;
        border-radius: 5px;
        margin-top: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Function to process the uploaded file
def process_file(uploaded_file):
    try:
        # API endpoint
        # api_url = "https://fahriw32qr.us-east-1.awsapprunner.com/api/services/email-draft/"
        api_url = "http://127.0.0.1:8000/api/services/email-draft/"
        
        # Prepare the file for upload
        files = {'file': (uploaded_file.name, uploaded_file, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')}
        
        # Make the API request
        with st.spinner('Processing your file...'):
            response = requests.post(api_url, files=files)
        
        # Check if request was successful
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error: API returned status code {response.status_code}")
            st.error(f"Response: {response.text}")
            return None
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return None

# Function to display lead data
def display_lead_data(lead_data):
    st.markdown(f"""
    <div class="lead-card">
        <h4 class="lead-name">{lead_data['first_name']} {lead_data['last_name']}</h4>
        <p class="lead-info"><span class="lead-label">Company:</span> <span class="lead-value">{lead_data['company_name']}</span></p>
        <p class="lead-info"><span class="lead-label">Title:</span> <span class="lead-value">{lead_data['job_title']}</span></p>
        <p class="lead-info"><span class="lead-label">Industry:</span> <span class="lead-value">{lead_data['industry']}</span></p>
        <p class="lead-info"><span class="lead-label">Lead Type:</span> <span class="lead-value">{lead_data['lead_type']}</span></p>
        <div class="notes-text">
            <span class="lead-label">Notes/Event:</span><br>
            {lead_data['notes_event']}
        </div>
    </div>
    """, unsafe_allow_html=True)

# Function to display drafted email
def display_email(drafted_email):
    # Check if drafted_email is a JSON string or already a dictionary
    if isinstance(drafted_email, str):
        try:
            # Parse the JSON string
            email_data = json.loads(drafted_email)
        except json.JSONDecodeError:
            # Fall back to the old method if JSON parsing fails
            lines = drafted_email.split('\n')
            subject = ""
            body = drafted_email
            
            if lines[0].startswith("Subject:"):
                subject = lines[0].replace("Subject:", "").strip()
                body = '\n'.join(lines[1:]).strip()
                
            email_data = {
                "To": "",  # We don't have this in the old format
                "subject": subject,
                "body": body
            }
    else:
        # Already a dictionary
        email_data = drafted_email
    
    # Extract the fields from the JSON object
    to_address = email_data.get("To", "")
    subject = email_data.get("subject", "")
    body = email_data.get("body", "")
    
    # Display the email with the recipient address included
    st.markdown(f"""
    <div class="email-card">
        <div class="recipient-line">To: {to_address}</div>
        <div class="subject-line">Subject: {subject}</div>
        <div class="email-body">{body}</div>
    </div>
    """, unsafe_allow_html=True)


# Main app header
st.title("📧 Email Drafting Tool")
st.markdown(f"""
<div style="padding: 15px; background-color: {PRIMARY_COLOR}; border-radius: 10px; margin-bottom: 25px;">
    <h3 style="color: white;">Upload your leads file to generate personalized email drafts</h3>
    <p style="color: #e0e0e0;">This tool helps you quickly create professional, personalized emails based on your lead data.</p>
</div>
""", unsafe_allow_html=True)

# Sidebar for file upload
with st.sidebar:
    st.markdown(f"""
    <div style="text-align: center; padding: 10px; margin-bottom: 20px;">
        <h2 style="color: {PRIMARY_COLOR};">📊 Lead Processor</h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.header("Upload File")
    st.markdown("Please upload an Excel file (.xlsx) containing lead data.")
    uploaded_file = st.file_uploader("Choose an XLSX file", type="xlsx")
    
    process_button = st.button("🚀 Process File", type="primary", disabled=not uploaded_file)
    
    if not uploaded_file:
        st.info("Please upload an XLSX file to continue.")
    
    st.markdown("---")
    st.markdown(f"""
    <div style="background-color: #e8f5e9; padding: 15px; border-radius: 10px; margin-top: 20px;">
        <h3 style="color: {SECONDARY_COLOR};">About</h3>
        <p style="color: {TEXT_COLOR};">This tool helps you create personalized email drafts based on lead data.
        Simply upload your Excel file and click 'Process File' to get started.</p>
    </div>
    """, unsafe_allow_html=True)

# Main content area
if process_button and uploaded_file is not None:
    # Process the file
    result = process_file(uploaded_file)
    
    if result and "Response" in result:
        # Display results
        st.success(f"Successfully processed {len(result['Response'])} leads!")
        
        # Display each lead and its drafted email
        for i, item in enumerate(result["Response"]):
            st.markdown(f"""
            <div class="section-header">
                <h3>Lead {i+1}: {item['lead_data']['first_name']} {item['lead_data']['last_name']} - {item['lead_data']['company_name']}</h3>
            </div>
            """, unsafe_allow_html=True)
            
            # Create two columns for lead data and email
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.subheader("Lead Information")
                display_lead_data(item["lead_data"])
            
            with col2:
                st.subheader("Drafted Email")
                display_email(item["drafted_email"])
                
            st.markdown("---")
    else:
        st.warning("No results returned from the API. Please check your file and try again.")
elif not uploaded_file and not process_button:
    # Show welcome message when app first loads
    st.markdown("""
    ### Welcome to the Email Drafting Tool
    
    This application helps you generate personalized email drafts based on your lead data.
    
    **Instructions:**
    1. Upload your Excel (.xlsx) file using the sidebar
    2. Click the "Process File" button
    3. View and copy your personalized email drafts
    4. It will only process the 4 rows of excel file because of testing purpose
    
    The tool will analyze your lead data and generate relevant email content for each lead.
    """)