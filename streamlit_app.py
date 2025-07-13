import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai
import json
import re
import base64
import PyPDF2
import docx
import pandas as pd
from io import BytesIO
import tempfile
from pathlib import Path
import zipfile
import time

# Load environment variables
load_dotenv()

# Configure Gemini
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    st.error("Please set GEMINI_API_KEY in your .env file")
    st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

# Streamlit app configuration
st.set_page_config(
    page_title="QE Test Automation Suite",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
:root {
    --primary: #1e3a8a;
    --secondary: #2ecc71;
    --dark: #2b2b2b;
    --light: #f8f8f8;
    --gray: #e0e0e0;
    --warning: #ff9800;
}
.header {
    color: var(--primary);
    padding: 15px 0;
    border-bottom: 3px solid var(--primary);
    margin-bottom: 20px;
}
.sidebar .sidebar-content {
    background-color: #f0f7ff;
}
.stButton>button {
    background-color: var(--primary);
    color: white;
    border-radius: 8px;
    padding: 12px 28px;
    font-weight: bold;
    transition: all 0.3s;
}
.stButton>button:hover {
    background-color: #152c6e;
    transform: scale(1.05);
}
.stTextArea textarea {
    border: 2px solid var(--primary) !important;
    border-radius: 8px;
    padding: 12px;
}
.success-box {
    background-color: #e6f7e9;
    border-left: 5px solid var(--secondary);
    padding: 20px;
    margin: 25px 0;
    border-radius: 0 10px 10px 0;
}
.test-case-card {
    border: 1px solid var(--gray);
    border-radius: 10px;
    padding: 20px;
    margin: 15px 0;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    background-color: #ffffff;
    transition: transform 0.3s;
}
.test-case-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 6px 12px rgba(0,0,0,0.15);
}
.test-case-card h4 {
    color: var(--primary);
    border-bottom: 1px solid var(--gray);
    padding-bottom: 12px;
    margin-top: 0;
}
.highlight {
    background-color: #fffacd;
    padding: 4px 8px;
    border-radius: 5px;
    font-weight: bold;
}
.footer {
    text-align: center;
    padding: 25px;
    color: #666;
    font-size: 0.95rem;
    margin-top: 40px;
    border-top: 1px solid var(--gray);
}
.traceability-matrix {
    margin-top: 35px;
    border: 1px solid var(--gray);
    border-radius: 10px;
    padding: 20px;
    background-color: #f9f9f9;
}
.traceability-matrix h3 {
    color: var(--primary);
    margin-top: 0;
}
.search-results {
    background-color: #f0f8ff;
    padding: 20px;
    border-radius: 10px;
    margin: 15px 0;
}
.automation-code {
    background-color: var(--dark);
    color: var(--light);
    padding: 20px;
    border-radius: 10px;
    margin: 20px 0;
    font-family: 'Fira Code', monospace;
    overflow-x: auto;
}
.code-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 15px;
    padding-bottom: 10px;
    border-bottom: 1px solid #444;
}
.code-header h3 {
    color: var(--secondary);
    margin: 0;
}
.code-container {
    max-height: 500px;
    overflow-y: auto;
}
.btn-download {
    background-color: var(--secondary) !important;
    margin: 5px;
}
.btn-download:hover {
    background-color: #27ae60 !important;
}
.btn-generate {
    background-color: #9b59b6 !important;
}
.btn-generate:hover {
    background-color: #8e44ad !important;
}
.tab-content {
    padding: 20px 0;
}
.file-info {
    background-color: #e3f2fd;
    padding: 15px;
    border-radius: 8px;
    margin: 10px 0;
}
.form-section {
    border: 1px solid #ddd;
    border-radius: 10px;
    padding: 20px;
    margin: 15px 0;
    background-color: #f9f9f9;
}
.form-header {
    background-color: #1e3a8a;
    color: white;
    padding: 10px 15px;
    border-radius: 8px 8px 0 0;
    margin: -20px -20px 20px -20px;
}
.attachment-preview {
    max-width: 200px;
    max-height: 150px;
    border-radius: 5px;
    margin: 5px;
}
.framework-file {
    background-color: #e8f4f8;
    border-left: 4px solid #1e3a8a;
    padding: 15px;
    margin: 10px 0;
    border-radius: 4px;
}
.file-name {
    font-weight: bold;
    color: #1e3a8a;
}
.test-case-container {
    max-height: 600px;
    overflow-y: auto;
    padding: 15px;
    border: 1px solid #e0e0e0;
    border-radius: 10px;
    margin: 15px 0;
}
.bulk-actions {
    display: flex;
    gap: 10px;
    margin-bottom: 20px;
    padding: 15px;
    background-color: #f8f9fa;
    border-radius: 8px;
}
.toast {
    position: fixed;
    top: 20px;
    right: 20px;
    padding: 15px 25px;
    background-color: #2ecc71;
    color: white;
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    z-index: 1000;
    animation: fadeInOut 3s ease-in-out;
}
@keyframes fadeInOut {
    0% { opacity: 0; transform: translateY(-20px); }
    10% { opacity: 1; transform: translateY(0); }
    90% { opacity: 1; transform: translateY(0); }
    100% { opacity: 0; transform: translateY(-20px); }
}
.draggable-item {
    padding: 12px;
    margin: 8px 0;
    background-color: #f8f9fa;
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    cursor: grab;
    transition: all 0.2s;
}
.draggable-item:hover {
    background-color: #e9ecef;
    transform: translateY(-2px);
}
.draggable-item.dragging {
    opacity: 0.5;
    border: 2px dashed #1e3a8a;
}
.combined-toggle {
    background-color: #e3f2fd;
    padding: 15px;
    border-radius: 10px;
    margin-bottom: 20px;
}
</style>
<link href="https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

# App header
st.markdown('<div class="header"><h1>🤖 QE Test Automation Suite</h1></div>', unsafe_allow_html=True)
st.markdown("Generate professional test cases and enterprise-grade Selenium automation code")

# Initialize session state
if 'test_cases' not in st.session_state:
    st.session_state.test_cases = []
if 'automation_code' not in st.session_state:
    st.session_state.automation_code = {}
if 'current_tc_id' not in st.session_state:
    st.session_state.current_tc_id = ""
if 'framework_generated' not in st.session_state:
    st.session_state.framework_generated = False
if 'framework_code' not in st.session_state:
    st.session_state.framework_code = {}
if 'file_content' not in st.session_state:
    st.session_state.file_content = ""
if 'show_toast' not in st.session_state:
    st.session_state.show_toast = False
if 'toast_message' not in st.session_state:
    st.session_state.toast_message = ""
if 'toast_time' not in st.session_state:
    st.session_state.toast_time = 0
if 'selected_test_cases' not in st.session_state:
    st.session_state.selected_test_cases = []
if 'editing_test_case' not in st.session_state:
    st.session_state.editing_test_case = None
if 'test_cases_str' not in st.session_state:
    st.session_state.test_cases_str = ""
if 'generation_mode' not in st.session_state:
    st.session_state.generation_mode = "combined"  # combined or separate
    
# Create a copy for form manipulation
manual_test_case_form = {
    "id": "TC_MANUAL_001",
    "title": "",
    "preconditions": [],
    "test_data": [],
    "test_steps": [],
    "expected_results": [],
    "priority": "Medium",
    "attachments": []
}

# File processing functions
def extract_text_from_txt(file):
    return file.read().decode("utf-8")

def extract_text_from_pdf(file):
    text = ""
    pdf_reader = PyPDF2.PdfReader(file)
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def extract_text_from_docx(file):
    doc = docx.Document(BytesIO(file.read()))
    return "\n".join([para.text for para in doc.paragraphs])

def extract_text_from_csv(file):
    df = pd.read_csv(file)
    return df.to_markdown()

def extract_text_from_xlsx(file):
    df = pd.read_excel(file)
    return df.to_markdown()

FILE_PROCESSORS = {
    "text/plain": extract_text_from_txt,
    "application/pdf": extract_text_from_pdf,
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": extract_text_from_docx,
    "text/csv": extract_text_from_csv,
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": extract_text_from_xlsx
}

# Function to generate test cases with Gemini
def generate_test_cases_from_prompt(prompt, num_cases, priority):
    try:
        prompt_template = f"""
        You are a senior QA engineer with 15+ years of experience. 
        Generate {num_cases} comprehensive test cases based on the following requirements:
        
        {prompt}
        
        Instructions:
        - Default Priority: {priority}
        - Format test cases in JSON with this structure:
        {{
            "test_cases": [
                {{
                    "id": "TC_001",
                    "title": "Test case title",
                    "preconditions": ["Precondition 1", "Precondition 2"],
                    "test_data": ["Data 1", "Data 2"],
                    "test_steps": ["Step 1", "Step 2", "Step 3"],
                    "expected_results": ["Expected result 1", "Expected result 2"],
                    "priority": "High/Medium/Low",
                    "attachments": []
                }}
            ]
        }}
        """
        
        response = model.generate_content(prompt_template)
        json_match = re.search(r'\{[\s\S]*\}', response.text)
        if json_match:
            json_str = json_match.group()
            data = json.loads(json_str)
            return data.get("test_cases", [])
        return []
    except Exception as e:
        st.error(f"Error generating test cases: {str(e)}")
        return []

# Function to generate Java Selenium code for a test case
def generate_test_case_automation_code(test_case):
    try:
        prompt_template = f"""
        You are a super senior QA automation engineer with over 30 years of enterprise experience. 
        Write complete, production-grade Selenium test automation code in Java using TestNG and Page Object Model.
        
        Based on the following test case:
        - Title: {test_case['title']}
        - Steps: 
        {chr(10).join(test_case['test_steps'])}
        - Expected Results: 
        {chr(10).join(test_case['expected_results'])}
        
        Generate the following:
        
        1. Page Object class for the relevant page(s)
        2. Test class that extends BaseTest
        3. Any necessary helper classes
        
        Use the following enterprise standards:
        - Java 17
        - Selenium WebDriver
        - TestNG
        - Page Object Model with @FindBy annotations
        - Factory Pattern for WebDriver
        - Singleton for configuration
        - Log4j2 logging
        - Allure reporting annotations
        - Explicit waits with WebDriverWait
        - Meaningful assertions
        - Thread-safe implementation
        
        Output the code in the following format:
        
        // FILE: src/main/java/com/qa/pages/[PageName]Page.java
        [Java code here]
        
        // FILE: src/test/java/com/qa/tests/[TestName]Test.java
        [Java code here]
        """
        
        response = model.generate_content(prompt_template)
        return response.text
    except Exception as e:
        st.error(f"Error generating automation code: {str(e)}")
        return ""

# Function to generate combined Java Selenium code for multiple test cases
def generate_combined_automation_code(test_cases):
    try:
        test_cases_str = "\n\n".join(
            [f"Test Case {idx+1}: {tc['title']}\n"
             f"Steps:\n{chr(10).join(tc['test_steps'])}\n"
             f"Expected Results:\n{chr(10).join(tc['expected_results'])}"
             for idx, tc in enumerate(test_cases)]
        )
        
        prompt_template = f"""
        You are a super senior QA automation engineer with over 30 years of enterprise experience. 
        Write complete, production-grade Selenium test automation code in Java using TestNG and Page Object Model.
        
        Create a SINGLE test class that includes test methods for the following test cases:
        
        {test_cases_str}
        
        Generate the following:
        
        1. Page Object classes for the relevant page(s)
        2. A single test class that extends BaseTest and contains multiple @Test methods (one for each test case above)
        3. Any necessary helper classes
        
        Use the following enterprise standards:
        - Java 17
        - Selenium WebDriver
        - TestNG
        - Page Object Model with @FindBy annotations
        - Factory Pattern for WebDriver
        - Singleton for configuration
        - Log4j2 logging
        - Allure reporting annotations
        - Explicit waits with WebDriverWait
        - Meaningful assertions
        - Thread-safe implementation
        
        Output the code in the following format:
        
        // FILE: src/main/java/com/qa/pages/[PageName]Page.java
        [Java code here]
        
        // FILE: src/test/java/com/qa/tests/GeneratedTestSuite.java
        [Java code for the combined test suite]
        """
        
        response = model.generate_content(prompt_template)
        return response.text
    except Exception as e:
        st.error(f"Error generating combined automation code: {str(e)}")
        return ""

# Function to parse generated code
def parse_generated_code(code):
    files = {}
    current_file = None
    current_content = []
    
    for line in code.split('\n'):
        if line.startswith("// FILE: "):
            if current_file:
                files[current_file] = "\n".join(current_content)
                current_content = []
            current_file = line.split("// FILE: ")[1].strip()
        elif current_file:
            current_content.append(line)
    
    if current_file and current_content:
        files[current_file] = "\n".join(current_content)
    
    return files

# Function to show toast notification
def show_toast(message):
    st.session_state.show_toast = True
    st.session_state.toast_message = message
    st.session_state.toast_time = time.time()  # Record display time

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Test Case Generator", "Test Automation"])

# Home Page
if page == "Home":
    st.markdown("""
    ## Welcome to the QE Test Automation Suite
    
    This enterprise-grade tool helps quality engineers:
    
    - 🧪 Generate comprehensive test cases from requirements
    - 🤖 Create production-ready Java Selenium automation code
    - 🏗️ Build complete automation frameworks
    - 📊 Follow industry best practices and patterns
    
    ### Get Started
    
    1. Go to **Test Case Generator** to create new test cases
    2. Visit **Test Automation** to generate Java Selenium code
    """)
    
    st.image("https://cdn-icons-png.flaticon.com/512/1046/1046784.png", width=200)
    
    st.markdown("---")
    st.markdown("""
    <div class="footer">QE Test Automation Suite | Powered by Gemini 1.5 Flash</div>
    """, unsafe_allow_html=True)

# Test Case Generator Page
elif page == "Test Case Generator":
    with st.sidebar:
        st.header("Configuration")
        module_name = st.text_input("**Module Name**", value="AUTH", 
                                  help="Used in test case IDs (e.g., TC_AUTH_001)")
        
        priority = st.selectbox(
            "**Default Priority**",
            ["High", "Medium", "Low"],
            index=1
        )
        
        st.markdown("---")
        st.markdown("**About**")
        st.markdown("Create professional test cases using AI")
    
    st.subheader("🧪 Test Case Generator")
    
    tab1, tab2 = st.tabs(["Manual Creation", "Generate from Requirements"])
    
    with tab1:
        st.subheader("Create Manual Test Case")
        with st.form("manual_test_case_form", clear_on_submit=False):
            st.markdown('<div class="form-section">', unsafe_allow_html=True)
            st.markdown('<div class="form-header"><h4>Test Case Details</h4></div>', unsafe_allow_html=True)
            
            title = st.text_input("Test Scenario*", placeholder="User login with valid credentials")
            
            col1, col2 = st.columns(2)
            with col1:
                preconditions = st.text_area("Preconditions", 
                                           placeholder="1. User is registered\n2. Application is running", 
                                           height=100)
            with col2:
                test_data = st.text_area("Test Data", 
                                       placeholder="Username: testuser\nPassword: Test@123", 
                                       height=100)
            
            steps = st.text_area("Test Steps*", 
                                placeholder="1. Navigate to login page\n2. Enter username\n3. Enter password\n4. Click login button", 
                                height=150)
            
            expected = st.text_area("Expected Results*", 
                                  placeholder="1. User is redirected to dashboard\n2. Welcome message is displayed", 
                                  height=100)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="form-section">', unsafe_allow_html=True)
            st.markdown('<div class="form-header"><h4>Attachments</h4></div>', unsafe_allow_html=True)
            attachments = st.file_uploader("Upload files (screenshots, documents)", 
                                         type=['png', 'jpg', 'jpeg', 'txt', 'pdf'], 
                                         accept_multiple_files=True)
            
            # Display attachments preview
            if attachments:
                st.subheader("Attachment Preview")
                cols = st.columns(4)
                for i, file in enumerate(attachments):
                    if file.type.startswith('image'):
                        with cols[i % 4]:
                            st.image(file, caption=file.name, width=100)
                    else:
                        with cols[i % 4]:
                            st.info(f"📄 {file.name}")
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            submitted = st.form_submit_button("Save Test Case", use_container_width=True)
            
            if submitted:
                if not title or not steps or not expected:
                    st.error("Please fill in all required fields (marked with *)")
                else:
                    # Process attachments
                    attachments_data = []
                    for file in attachments:
                        if file.type.startswith('image'):
                            content = base64.b64encode(file.read()).decode('utf-8')
                            attachments_data.append({
                                "name": file.name,
                                "type": file.type,
                                "content": content
                            })
                        else:
                            attachments_data.append({
                                "name": file.name,
                                "type": file.type,
                                "content": file.read()
                            })
                    
                    # Create test case object
                    test_case = {
                        "id": f"TC_{module_name}_{len(st.session_state.test_cases) + 1}",
                        "title": title,
                        "preconditions": [p.strip() for p in preconditions.split('\n') if p.strip()],
                        "test_data": [d.strip() for d in test_data.split('\n') if d.strip()],
                        "test_steps": [s.strip() for s in steps.split('\n') if s.strip()],
                        "expected_results": [e.strip() for e in expected.split('\n') if e.strip()],
                        "priority": priority,
                        "attachments": attachments_data,
                        "selected": False
                    }
                    
                    # Save to session state
                    st.session_state.test_cases.append(test_case)
                    show_toast("✅ Test case saved successfully!")
    
    with tab2:
        st.subheader("Generate Test Cases from Requirements")
        user_story = st.text_area(
            "Enter your user story or requirements:",
            height=250,
            placeholder="As a registered user, I want to log in to the application so that I can access my dashboard...",
            label_visibility="collapsed"
        )
        
        num_test_cases = st.slider(
            "Number of Test Cases to Generate (1-50)",
            min_value=1,
            max_value=50,
            value=10,
            step=1
        )
        
        if st.button("Generate Test Cases", use_container_width=True):
            if user_story:
                with st.spinner(f"Generating {num_test_cases} professional test cases..."):
                    generated_cases = generate_test_cases_from_prompt(user_story, num_test_cases, priority)
                    
                    if generated_cases:
                        # Assign unique IDs
                        for i, tc in enumerate(generated_cases):
                            tc["id"] = f"TC_{module_name}_G{len(st.session_state.test_cases) + i + 1}"
                            tc["selected"] = False
                            # Ensure attachments field exists
                            if "attachments" not in tc:
                                tc["attachments"] = []
                        
                        st.session_state.test_cases.extend(generated_cases)
                        show_toast(f"✅ Successfully generated {len(generated_cases)} test cases!")
                    else:
                        st.error("Failed to generate test cases. Please try again with more specific requirements.")
            else:
                st.warning("Please enter requirements to generate test cases")
    
    # Bulk actions
    if st.session_state.test_cases:
        st.subheader("Test Case Management")
        
        # Bulk actions container
        with st.container():
            st.markdown('<div class="bulk-actions">', unsafe_allow_html=True)
            
            # Select all checkbox
            all_selected = all(tc.get('selected', False) for tc in st.session_state.test_cases)
            select_all = st.checkbox("Select All", value=all_selected, key="select_all")
            
            # Update all test cases based on Select All
            if select_all:
                for tc in st.session_state.test_cases:
                    tc['selected'] = True
            elif not select_all and all_selected:
                for tc in st.session_state.test_cases:
                    tc['selected'] = False
            
            # Copy all button
            if st.button("Copy All Test Cases", key="copy_all"):
                # Create a copyable string of all test cases
                test_cases_str = "\n\n".join(
                    [f"ID: {tc['id']}\nTitle: {tc['title']}\nPriority: {tc['priority']}\n\nSteps:\n" + 
                     "\n".join([f"- {step}" for step in tc['test_steps']]) +
                     "\n\nExpected Results:\n" + 
                     "\n".join([f"- {result}" for result in tc['expected_results']])
                    for tc in st.session_state.test_cases]
                )
                
                st.session_state.test_cases_str = test_cases_str
                st.rerun()  # FIXED: Changed from experimental_rerun to rerun
            
            # Generate automation for selected
            selected_count = sum(1 for tc in st.session_state.test_cases if tc.get('selected', False))
            if selected_count > 0:
                if st.button(f"Generate Automation for {selected_count} Test Cases", key="gen_selected"):
                    st.session_state.selected_test_cases = [
                        tc for tc in st.session_state.test_cases if tc.get('selected', False)
                    ]
                    st.experimental_set_query_params(page="Test Automation")
                    st.rerun()
            else:
                st.button("Generate Automation (Select Test Cases)", disabled=True)
            
            # Delete selected button
            if st.button("Delete Selected", key="delete_selected"):
                st.session_state.test_cases = [
                    tc for tc in st.session_state.test_cases if not tc.get('selected', False)
                ]
                show_toast(f"✅ Deleted {selected_count} test cases")
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Test case container with scroll
        st.markdown('<div class="test-case-container">', unsafe_allow_html=True)
        
        # Display all test cases
        for idx, test_case in enumerate(st.session_state.test_cases):
            with st.container():
                col1, col2, col3 = st.columns([1, 10, 2])
                
                with col1:
                    # Checkbox for selection
                    selected = st.checkbox("", 
                                         value=test_case.get('selected', False), 
                                         key=f"select_{test_case['id']}",
                                         label_visibility="collapsed")
                    
                    # Update selection state
                    test_case['selected'] = selected
                
                with col2:
                    # Test case card
                    with st.expander(f"{test_case['id']}: {test_case['title']}", expanded=False):
                        st.markdown(f"**Priority:** `{test_case['priority']}`")
                        
                        if test_case['preconditions']:
                            st.markdown("**Preconditions:**")
                            for pre in test_case['preconditions']:
                                st.markdown(f"- {pre}")
                        
                        if test_case.get('test_data'):
                            st.markdown("**Test Data:**")
                            for data in test_case['test_data']:
                                st.markdown(f"- {data}")
                        
                        st.markdown("**Steps:**")
                        for step in test_case['test_steps']:
                            st.markdown(f"- {step}")
                        
                        st.markdown("**Expected Results:**")
                        for result in test_case['expected_results']:
                            st.markdown(f"- {result}")
                        
                        if test_case.get('attachments'):
                            st.markdown("**Attachments:**")
                            for attachment in test_case['attachments']:
                                if attachment['type'].startswith('image'):
                                    st.image(base64.b64decode(attachment['content']), caption=attachment['name'], use_column_width=True)
                                else:
                                    st.download_button(
                                        label=f"Download {attachment['name']}",
                                        data=attachment['content'],
                                        file_name=attachment['name'],
                                        mime=attachment['type'],
                                        key=f"attach_{test_case['id']}_{attachment['name']}"
                                    )
                
                with col3:
                    # Edit button
                    if st.button("✏️ Edit", key=f"edit_{test_case['id']}"):
                        st.session_state.editing_test_case = test_case
                        st.session_state.editing_index = idx
                    
                    # Generate automation for single test case
                    if st.button("🤖 Generate", key=f"gen_single_{test_case['id']}"):
                        st.session_state.selected_test_cases = [test_case]
                        st.experimental_set_query_params(page="Test Automation")
                        st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    else:
        st.info("No test cases created yet. Create or generate test cases to get started.")
    
    # Copy all test cases modal
    if st.session_state.test_cases_str:
        st.text_area("Copy all test cases", 
                    st.session_state.test_cases_str, 
                    height=300)
        if st.button("Close", key="close_copy"):
            st.session_state.test_cases_str = ""
            st.rerun()
    
    # Edit test case modal
    if st.session_state.editing_test_case:
        test_case = st.session_state.editing_test_case
        idx = st.session_state.editing_index
        
        with st.form(f"edit_form_{test_case['id']}"):
            st.subheader(f"Editing: {test_case['id']}")
            
            title = st.text_input("Test Scenario*", value=test_case['title'])
            
            col1, col2 = st.columns(2)
            with col1:
                preconditions = st.text_area("Preconditions", 
                                           value="\n".join(test_case['preconditions']), 
                                           height=100)
            with col2:
                test_data = st.text_area("Test Data", 
                                       value="\n".join(test_case.get('test_data', [])), 
                                       height=100)
            
            steps = st.text_area("Test Steps*", 
                                value="\n".join(test_case['test_steps']), 
                                height=150)
            
            expected = st.text_area("Expected Results*", 
                                  value="\n".join(test_case['expected_results']), 
                                  height=100)
            
            priority = st.selectbox(
                "Priority",
                ["High", "Medium", "Low"],
                index=["High", "Medium", "Low"].index(test_case['priority'])
            )
            
            # Form actions
            col1, col2 = st.columns(2)
            with col1:
                if st.form_submit_button("Save Changes", use_container_width=True):
                    # Update test case
                    st.session_state.test_cases[idx] = {
                        "id": test_case['id'],
                        "title": title,
                        "preconditions": [p.strip() for p in preconditions.split('\n') if p.strip()],
                        "test_data": [d.strip() for d in test_data.split('\n') if d.strip()],
                        "test_steps": [s.strip() for s in steps.split('\n') if s.strip()],
                        "expected_results": [e.strip() for e in expected.split('\n') if e.strip()],
                        "priority": priority,
                        "attachments": test_case.get('attachments', []),  # FIXED: Use get with default
                        "selected": test_case.get('selected', False)
                    }
                    st.session_state.editing_test_case = None
                    show_toast("✅ Test case updated successfully!")
                    st.rerun()  # FIXED: Changed from experimental_rerun to rerun
            
            with col2:
                if st.form_submit_button("Cancel", use_container_width=True):
                    st.session_state.editing_test_case = None
                    st.rerun()  # FIXED: Changed from experimental_rerun to rerun

# Test Automation Page
elif page == "Test Automation":
    st.subheader("🤖 Java Selenium Automation Generator")
    
    if st.session_state.selected_test_cases:
        st.success(f"Generating automation code for {len(st.session_state.selected_test_cases)} test cases")
        
        # Generation mode selection
        st.markdown('<div class="combined-toggle">', unsafe_allow_html=True)
        st.radio(
            "Generation Mode:",
            ["Combined Test Suite", "Separate Test Classes"],
            key="generation_mode",
            horizontal=True
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Generate automation code
        if st.button("Generate Automation Code", key="generate_automation", use_container_width=True):
            with st.spinner("Generating production-ready Java Selenium code..."):
                st.session_state.automation_code = {}
                
                if st.session_state.generation_mode == "Combined Test Suite":
                    # Generate combined test suite
                    automation_code = generate_combined_automation_code(st.session_state.selected_test_cases)
                    if automation_code:
                        st.session_state.automation_code["combined"] = parse_generated_code(automation_code)
                        show_toast("✅ Combined test suite generated successfully!")
                else:
                    # Generate separate files for each test case
                    for test_case in st.session_state.selected_test_cases:
                        automation_code = generate_test_case_automation_code(test_case)
                        st.session_state.automation_code[test_case['id']] = parse_generated_code(automation_code)
                    show_toast("✅ Automation code generated successfully!")
        
        if st.session_state.automation_code:
            # Combined Test Suite View
            if st.session_state.generation_mode == "Combined Test Suite" and "combined" in st.session_state.automation_code:
                st.markdown("### 🧩 Combined Test Suite")
                
                # Display automation code
                st.subheader("Generated Automation Code")
                
                for file_name, content in st.session_state.automation_code["combined"].items():
                    with st.expander(f"📄 {file_name}"):
                        st.code(content, language='java')
                
                # Create a zip file for download
                zip_buffer = BytesIO()
                with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED, False) as zip_file:
                    for file_name, content in st.session_state.automation_code["combined"].items():
                        zip_file.writestr(file_name, content)
                
                zip_buffer.seek(0)
                st.download_button(
                    label="Download Combined Test Suite",
                    data=zip_buffer,
                    file_name="CombinedTestSuite.zip",
                    mime="application/zip",
                    use_container_width=True
                )
                
                # Display test cases in suite
                st.markdown("### Test Cases in this Suite")
                for test_case in st.session_state.selected_test_cases:
                    with st.expander(f"{test_case['id']}: {test_case['title']}"):
                        st.markdown(f"**Priority:** `{test_case['priority']}`")
                        st.markdown("**Steps:**")
                        for step in test_case['test_steps']:
                            st.markdown(f"- {step}")
                        
                        st.markdown("**Expected Results:**")
                        for result in test_case['expected_results']:
                            st.markdown(f"- {result}")
            
            # Separate Files View
            elif st.session_state.generation_mode == "Separate Test Classes":
                # Tabs for each test case
                tabs = st.tabs([f"Test Case: {tc['id']}" for tc in st.session_state.selected_test_cases])
                
                for idx, test_case in enumerate(st.session_state.selected_test_cases):
                    with tabs[idx]:
                        st.markdown(f"### {test_case['title']}")
                        st.markdown(f"**ID:** {test_case['id']} | **Priority:** `{test_case['priority']}`")
                        
                        # Display test case details
                        with st.expander("Test Case Details", expanded=False):
                            st.markdown("**Steps:**")
                            for step in test_case['test_steps']:
                                st.markdown(f"- {step}")
                            
                            st.markdown("**Expected Results:**")
                            for result in test_case['expected_results']:
                                st.markdown(f"- {result}")
                        
                        # Display automation code
                        if test_case['id'] in st.session_state.automation_code:
                            st.subheader("Generated Automation Code")
                            
                            for file_name, content in st.session_state.automation_code[test_case['id']].items():
                                with st.expander(f"📄 {file_name}"):
                                    st.code(content, language='java')
                            
                            # Create a zip file for download
                            zip_buffer = BytesIO()
                            with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED, False) as zip_file:
                                for file_name, content in st.session_state.automation_code[test_case['id']].items():
                                    zip_file.writestr(file_name, content)
                            
                            zip_buffer.seek(0)
                            st.download_button(
                                label=f"Download Code for {test_case['id']}",
                                data=zip_buffer,
                                file_name=f"{test_case['id']}_automation.zip",
                                mime="application/zip",
                                use_container_width=True
                            )
                        else:
                            st.info("Click 'Generate Automation Code' to create Java code")
        else:
            st.info("Click the button above to generate automation code")
    else:
        st.info("No test cases selected for automation")
        st.markdown("Go to **Test Case Generator** to create and select test cases")
        if st.button("Go to Test Case Generator"):
            st.experimental_set_query_params(page="Test Case Generator")
            st.rerun()

# Toast notification
if st.session_state.get('show_toast'):
    # Show toast if less than 3 seconds have passed
    if time.time() - st.session_state.get('toast_time', 0) < 3:
        st.markdown(f'<div class="toast">{st.session_state.toast_message}</div>', unsafe_allow_html=True)
    else:
        # Automatically hide after 3 seconds
        st.session_state.show_toast = False

# Footer
st.markdown("---")
st.markdown('<div class="footer">QE Test Automation Suite | Powered by Gemini 1.5 Flash</div>', 
            unsafe_allow_html=True)
