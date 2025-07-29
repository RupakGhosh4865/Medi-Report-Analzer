import streamlit as st
import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import PyPDF2  # For PDF processing
import google.generativeai as genai
from io import BytesIO

# Set page configuration
st.set_page_config(
    page_title="MediDiagnose AI",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for styling - enhanced for better visibility
st.markdown("""
<style>
    /* Main container */
    .main {
        background-color: #f8f9fa;
        color: #333333; /* Dark text for better contrast */
    }
    
    /* Header styling */
    .header {
        background: linear-gradient(135deg, #1a6fb0, #0d47a1);
        color: white;
        padding: 2rem 1rem;
        border-radius: 0 0 10px 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
    }
    
    /* Upload area styling */
    .upload-area {
        border: 2px dashed #1a6fb0;
        border-radius: 10px;
        padding: 3rem;
        text-align: center;
        background-color: #e8f4ff;
        transition: all 0.3s ease;
        margin-bottom: 2rem;
        color: #333333; /* Dark text */
    }
    
    .upload-area:hover {
        background-color: #d0e8ff;
        border-color: #0d47a1;
    }
    
    /* Specialist cards */
    .specialist-card {
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        background: white;
        color: #333333; /* Dark text */
    }
    
    .cardio-card {
        border-left: 4px solid #e53935;
    }
    
    .psycho-card {
        border-left: 4px solid #43a047;
    }
    
    .pulmo-card {
        border-left: 4px solid #1e88e5;
    }
    
    /* Analysis status */
    .analysis-status {
        padding: 1rem;
        border-radius: 10px;
        background: #e3f2fd;
        margin: 1rem 0;
        text-align: center;
        color: #333333; /* Dark text */
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 1rem;
        margin-top: 2rem;
        color: #757575;
        font-size: 0.9rem;
    }
    
    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #1a6fb0, #0d47a1);
        color: white;
        border: none;
        border-radius: 5px;
        padding: 0.5rem 1.5rem;
        font-weight: 600;
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, #0d47a1, #1a6fb0);
        color: white;
    }
    
    /* Text elements */
    h1, h2, h3, h4, h5, h6, p {
        color: #333333 !important; /* Dark text for all elements */
    }
</style>
""", unsafe_allow_html=True)

# Agent class definition
class Agent:
    def __init__(self, medical_report=None, role=None, extra_info=None):
        self.medical_report = medical_report
        self.role = role
        self.extra_info = extra_info
        self.prompt_template = self.create_prompt_template()
        
        # Configure Gemini API
        self.api_key = "AIzaSyByuy7KuEzsniA91qvHcUF2R-0lT43a76U"  # Your Gemini API key
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        
    def create_prompt_template(self):
        if self.role == "MultidisciplinaryTeam":
            return f"""
                You are a multidisciplinary team of healthcare professionals.
                Review the patient's medical reports from three specialists and:
                1. Identify 3 possible health issues
                2. For each issue, provide:
                   - Reason based on the reports
                   - Potential impact on patient health
                3. Format as bullet points
                
                **Cardiologist Report:**
                {self.extra_info.get('cardiologist_report', 'N/A')}
                
                **Psychologist Report:**
                {self.extra_info.get('psychologist_report', 'N/A')}
                
                **Pulmonologist Report:**
                {self.extra_info.get('pulmonologist_report', 'N/A')}
            """
        else:
            role_specific = {
                "Cardiologist": f"""
                    You are a cardiologist. Review this patient's cardiac workup:
                    {self.medical_report}
                    
                    Focus on:
                    - Subtle signs of cardiac issues
                    - Potential arrhythmias or structural abnormalities
                    - Connection to patient symptoms
                    
                    Recommendations:
                    - Further cardiac testing needed
                    - Monitoring requirements
                    - Management strategies if issues identified
                    
                    Format:
                    1. Possible causes
                    2. Recommended next steps
                """,
                "Psychologist": f"""
                    You are a psychologist. Review this patient's report:
                    {self.medical_report}
                    
                    Focus on:
                    - Mental health issues (anxiety, depression, trauma)
                    - Impact on patient's well-being
                    
                    Recommendations:
                    - Therapeutic interventions
                    - Counseling approaches
                    - Other psychological support
                    
                    Format:
                    1. Possible mental health issues
                    2. Recommended next steps
                """,
                "Pulmonologist": f"""
                    You are a pulmonologist. Review this patient's report:
                    {self.medical_report}
                    
                    Focus on:
                    - Respiratory issues (asthma, COPD, infections)
                    - Impact on breathing function
                    
                    Recommendations:
                    - Pulmonary function tests
                    - Imaging studies
                    - Treatment interventions
                    
                    Format:
                    1. Possible respiratory issues
                    2. Recommended next steps
                """
            }
            return role_specific[self.role]

    def run(self):
        try:
            response = self.model.generate_content(
                contents=self.prompt_template,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.3,
                    max_output_tokens=1000
                )
            )
            return response.text.strip()
        except Exception as e:
            return f"Error: {str(e)}"

# Specialized agent classes
class Cardiologist(Agent):
    def __init__(self, medical_report):
        super().__init__(medical_report, "Cardiologist")

class Psychologist(Agent):
    def __init__(self, medical_report):
        super().__init__(medical_report, "Psychologist")

class Pulmonologist(Agent):
    def __init__(self, medical_report):
        super().__init__(medical_report, "Pulmonologist")

class MultidisciplinaryTeam(Agent):
    def __init__(self, cardiologist_report, psychologist_report, pulmonologist_report):
        extra_info = {
            "cardiologist_report": cardiologist_report,
            "psychologist_report": psychologist_report,
            "pulmonologist_report": pulmonologist_report
        }
        super().__init__(role="MultidisciplinaryTeam", extra_info=extra_info)

# Function to extract text from PDF
def extract_text_from_pdf(uploaded_file):
    try:
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        text = ""
        for page in range(len(pdf_reader.pages)):
            text += pdf_reader.pages[page].extract_text()
        return text
    except Exception as e:
        st.error(f"Error reading PDF: {str(e)}")
        return ""

# Function to process uploaded file
def process_uploaded_file(uploaded_file):
    if uploaded_file is not None:
        try:
            # For text files
            if uploaded_file.type == "text/plain":
                return uploaded_file.read().decode("utf-8")
            
            # For PDF files
            elif uploaded_file.type == "application/pdf":
                return extract_text_from_pdf(uploaded_file)
                
            # For other file types
            else:
                st.error("Unsupported file type. Please upload a PDF or text file.")
                return ""
        except Exception as e:
            st.error(f"Error processing file: {str(e)}")
            return ""
    return ""

# Function to run analysis
def run_analysis():
    if not st.session_state.medical_report:
        st.error("Please upload a medical report first")
        return
    
    # Create status container
    status_container = st.empty()
    
    # Show initial status
    status_container.markdown("""
    <div class="analysis-status">
        <h3>Consulting Cardiologist AI, Psychologist AI, and Pulmonologist AI...</h3>
        <p>Our AI specialists are analyzing your report. This may take a few moments.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create agents
    agents = {
        "Cardiologist": Cardiologist(st.session_state.medical_report),
        "Psychologist": Psychologist(st.session_state.medical_report),
        "Pulmonologist": Pulmonologist(st.session_state.medical_report)
    }
    
    # Function to run each agent
    def get_response(agent_name, agent):
        return agent_name, agent.run()
    
    # Run agents concurrently
    st.session_state.reports = {}
    with ThreadPoolExecutor() as executor:
        futures = {executor.submit(get_response, name, agent): name for name, agent in agents.items()}
        
        # Update status as each agent completes
        for i, future in enumerate(as_completed(futures)):
            agent_name, response = future.result()
            st.session_state.reports[agent_name] = response
            
            # Update status
            progress = (i + 1) / len(agents) * 100
            status_container.markdown(f"""
            <div class="analysis-status">
                <h3>Analysis in Progress ({int(progress)}% complete)</h3>
                <p>{agent_name} analysis complete</p>
                <div style="height: 10px; background: #e0e0e0; border-radius: 5px; margin-top: 10px;">
                    <div style="height: 100%; width: {progress}%; background: #1a6fb0; border-radius: 5px;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            time.sleep(1)  # Simulate processing time
    
    # Run multidisciplinary team
    team_agent = MultidisciplinaryTeam(
        st.session_state.reports["Cardiologist"],
        st.session_state.reports["Psychologist"],
        st.session_state.reports["Pulmonologist"]
    )
    st.session_state.final_diagnosis = team_agent.run()
    st.session_state.analysis_complete = True
    
    # Clear status container
    status_container.empty()

# Main application
def main():
    # Main header
    st.markdown("""
    <div class="header">
        <h1 style="text-align: center; margin-bottom: 0.5rem;">MediDiagnose AI</h1>
        <h3 style="text-align: center; font-weight: 300;">Advanced Medical Diagnostic Platform</h3>
    </div>
    """, unsafe_allow_html=True)

    # File upload section
    st.markdown("## Upload Medical Report")
    st.markdown("Upload your medical report for comprehensive AI analysis")

    st.markdown("""
    <div class="upload-area">
        <h3>Drag & drop your medical report here</h3>
        <p>or click to browse files</p>
        <p><small>Supported formats: PDF, TXT</small></p>
        <p><small>Maximum file size: 10MB</small></p>
    </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Upload Medical Report", 
        type=["pdf", "txt"],
        label_visibility="collapsed"
    )

    # Initialize session state
    if 'medical_report' not in st.session_state:
        st.session_state.medical_report = ""
    if 'analysis_complete' not in st.session_state:
        st.session_state.analysis_complete = False
    if 'reports' not in st.session_state:
        st.session_state.reports = {}
    if 'final_diagnosis' not in st.session_state:
        st.session_state.final_diagnosis = ""

    # Process file when uploaded
    if uploaded_file:
        processed_text = process_uploaded_file(uploaded_file)
        if processed_text:
            st.session_state.medical_report = processed_text
            st.success("Medical report processed successfully!")
            
            # Show analysis button
            if st.button("Start Analysis", use_container_width=True):
                run_analysis()

    # Display specialist reports if available
    if st.session_state.reports:
        st.markdown("## Specialist Analysis Reports")
        
        # Cardiologist report
        with st.expander("### Cardiologist AI Report", expanded=True):
            st.markdown(f"""
            <div class="specialist-card cardio-card">
                <p>{st.session_state.reports['Cardiologist']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Psychologist report
        with st.expander("### Psychologist AI Report", expanded=True):
            st.markdown(f"""
            <div class="specialist-card psycho-card">
                <p>{st.session_state.reports['Psychologist']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Pulmonologist report
        with st.expander("### Pulmonologist AI Report", expanded=True):
            st.markdown(f"""
            <div class="specialist-card pulmo-card">
                <p>{st.session_state.reports['Pulmonologist']}</p>
            </div>
            """, unsafe_allow_html=True)

    # Display final diagnosis if available
    if st.session_state.analysis_complete:
        st.markdown("## Final Diagnosis")
        st.markdown(f"""
        <div style="background: #e8f5e9; padding: 1.5rem; border-radius: 10px; border-left: 4px solid #43a047;">
            <h3 style="color: #2e7d32;">Multidisciplinary Team Analysis</h3>
            <p>{st.session_state.final_diagnosis}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Create downloadable report
        report_content = f"MediDiagnose AI Report\n{'='*30}\n\n"
        report_content += "Cardiologist Report:\n" + st.session_state.reports['Cardiologist'] + "\n\n"
        report_content += "Psychologist Report:\n" + st.session_state.reports['Psychologist'] + "\n\n"
        report_content += "Pulmonologist Report:\n" + st.session_state.reports['Pulmonologist'] + "\n\n"
        report_content += "Final Diagnosis:\n" + st.session_state.final_diagnosis
        
        # Download button for diagnosis
        st.download_button(
            label="Download Full Report",
            data=report_content,
            file_name="medical_diagnosis_report.txt",
            mime="text/plain"
        )

    # Footer
    st.markdown("""
    <div class="footer">
        <p>© 2024 MediDiagnose AI Advanced Medical Diagnostic Platform</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()