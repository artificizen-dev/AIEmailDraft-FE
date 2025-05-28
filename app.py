import streamlit as st
import requests
import json

# Set up page and colors
st.set_page_config(
    page_title="Email Drafting Tool",
    page_icon="📧",
    layout="wide",
    initial_sidebar_state="expanded"
)

PRIMARY_COLOR = "#4a4a9c"
SECONDARY_COLOR = "#4CAF50"
BACKGROUND_COLOR = "#f8f9fa"
TEXT_COLOR = "#333333"

# Inject your custom CSS for style
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

# API_BASE = "http://127.0.0.1:8000/api/services"
API_BASE = "https://fahriw32qr.us-east-1.awsapprunner.com/api/services"
DRAFT_URL = f"{API_BASE}/email-draft/"
REFACTOR_URL = f"{API_BASE}/email-refactor/"
SEND_URL = f"{API_BASE}/send-email/"

def update_final_edit(i):
    state = st.session_state["email_states"][i]
    to = st.session_state.get(f"to_{i}", "")
    subject = st.session_state.get(f"subject_{i}", "")
    body = st.session_state.get(f"body_{i}", "")
    state["final_edit"] = {"to": to, "subject": subject, "body": body}

def process_file(uploaded_file):
    files = {'file': (uploaded_file.name, uploaded_file, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')}
    with st.spinner('Processing your file...'):
        response = requests.post(DRAFT_URL, files=files)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error: API returned status code {response.status_code}")
        st.error(f"Response: {response.text}")
        return None

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

def display_email(email_data):
    if isinstance(email_data, str):
        try:
            email_data = json.loads(email_data)
        except Exception:
            st.error("Email data parse error.")
            return
    to_address = email_data.get("To") or email_data.get("to", "")
    subject = email_data.get("subject", "")
    body = email_data.get("body", "")
    body_html = body.replace('\n', '<br>')
    st.markdown(f"""
    <div class="email-card">
        <div class="recipient-line">To: {to_address}</div>
        <div class="subject-line">Subject: {subject}</div>
        <div class="email-body">{body_html}</div>
    </div>
    """, unsafe_allow_html=True)

st.title("📧 Email Drafting Tool")
st.markdown(f"""
<div style="padding: 15px; background-color: {PRIMARY_COLOR}; border-radius: 10px; margin-bottom: 25px;">
    <h3 style="color: white;">Upload your leads file to generate personalized email drafts</h3>
    <p style="color: #e0e0e0;">This tool helps you quickly create professional, personalized emails based on your lead data.</p>
</div>
""", unsafe_allow_html=True)

if "email_states" not in st.session_state:
    st.session_state["email_states"] = {}
if "results" not in st.session_state:
    st.session_state["results"] = None

with st.sidebar:
    st.markdown(f"""
    <div style="text-align: center; padding: 10px; margin-bottom: 20px;">
        <h2 style="color: {PRIMARY_COLOR};">📊 Lead Processor</h2>
    </div>
    """, unsafe_allow_html=True)
    st.header("Upload File")
    uploaded_file = st.file_uploader("Choose an XLSX file", type="xlsx")
    if st.button("🚀 Process File", type="primary", disabled=not uploaded_file):
        result = process_file(uploaded_file)
        if result and "Response" in result:
            st.session_state["results"] = result["Response"]
            st.session_state["email_states"] = {}
            st.success(f"Successfully processed {len(result['Response'])} leads!")
        else:
            st.session_state["results"] = None
            st.session_state["email_states"] = {}
    st.markdown("---")
    st.markdown(f"""
    <div style="background-color: #e8f5e9; padding: 15px; border-radius: 10px; margin-top: 20px;">
        <h3 style="color: {SECONDARY_COLOR};">About</h3>
        <p style="color: {TEXT_COLOR};">This tool helps you create personalized email drafts based on lead data.
        Simply upload your Excel file and click 'Process File' to get started.</p>
    </div>
    """, unsafe_allow_html=True)

if st.session_state["results"]:
    for i, item in enumerate(st.session_state["results"]):
        lead = item["lead_data"]
        draft = item["drafted_email"]
        if i not in st.session_state["email_states"]:
            st.session_state["email_states"][i] = {
                "editing": False,
                "llm_prompt": "",
                "llm_rewrite": None,
                "final_edit": None
            }
        state = st.session_state["email_states"][i]

        st.markdown(f"""
        <div class="section-header">
            <h3>Lead {i+1}: {lead['first_name']} {lead['last_name']} - {lead['company_name']}</h3>
        </div>
        """, unsafe_allow_html=True)
        col1, col2 = st.columns([1, 2])
        with col1:
            st.subheader("Lead Information")
            display_lead_data(lead)
        with col2:
            st.subheader("Drafted Email")
            edit_btn = st.button("Edit", key=f"edit_{i}")
            if edit_btn:
                # Only allow one editing row at a time
                for j, s in st.session_state["email_states"].items():
                    s["editing"] = False
                state["editing"] = True

            if state["editing"]:
                # Cancel button (only for the row being edited)
                cancel_btn = st.button("Cancel", key=f"cancel_{i}")
                if cancel_btn:
                    state["editing"] = False
                    state["llm_prompt"] = ""
                    state["final_edit"] = None

                state["llm_prompt"] = st.text_area(
                    "Describe your change (or leave blank to edit directly):",
                    value=state["llm_prompt"], key=f"prompt_{i}")

                if st.button("Process with LLM", key=f"process_{i}"):
                    refactor_payload = {
                        "original_email": state["llm_rewrite"] or draft,
                        "user_prompt": state["llm_prompt"]
                    }
                    with st.spinner("AI is rewriting your email..."):
                        response = requests.post(REFACTOR_URL, json=refactor_payload)
                    if response.status_code == 200:
                        rewritten = response.json()["rewritten_email"]
                        try:
                            rewritten = json.loads(rewritten)
                        except Exception:
                            pass
                        state["llm_rewrite"] = rewritten
                        st.success("LLM provided a new draft below. You can edit it before sending.")
                    else:
                        st.error("LLM call failed. Try again.")

                draft_to_edit = state["llm_rewrite"] or draft
                if isinstance(draft_to_edit, str):
                    try:
                        draft_to_edit = json.loads(draft_to_edit)
                    except Exception:
                        draft_to_edit = {"To": "", "subject": "", "body": draft_to_edit}

                to = st.text_input(
                    "To", 
                    value=draft_to_edit.get("To") or draft_to_edit.get("to", ""), 
                    key=f"to_{i}", 
                    on_change=update_final_edit, 
                    args=(i,)
                )
                subject = st.text_input(
                    "Subject", 
                    value=draft_to_edit.get("subject", ""), 
                    key=f"subject_{i}", 
                    on_change=update_final_edit, 
                    args=(i,)
                )
                body = st.text_area(
                    "Body", 
                    value=draft_to_edit.get("body", ""), 
                    key=f"body_{i}", 
                    height=200, 
                    on_change=update_final_edit, 
                    args=(i,)
                )

                if state["final_edit"] is None:
                    state["final_edit"] = {
                        "to": to,
                        "subject": subject,
                        "body": body
                    }

                if st.button("Send Email", key=f"send_{i}"):
                    send_payload = {"email_data": state["final_edit"]}
                    with st.spinner("Sending email..."):
                        resp = requests.post(SEND_URL, json=send_payload)
                    if resp.status_code == 200:
                        st.success("Email sent to client!")
                        state["editing"] = False
                    else:
                        st.error(f"Failed to send email: {resp.text}")
            else:
                display_email(state["llm_rewrite"] or draft)

        st.markdown("---")
else:
    st.markdown("""
    ### Welcome to the Email Drafting Tool

    This application helps you generate personalized email drafts based on your lead data.

    **Instructions:**
    1. Upload your Excel (.xlsx) file using the sidebar
    2. Click the "Process File" button
    3. View and copy or edit your personalized email drafts
    4. You can use the edit button to customize the draft for each lead and send directly to the client.
    """)
