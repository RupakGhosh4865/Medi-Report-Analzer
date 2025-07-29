# 🧠 MediDiagnose AI - Advanced Medical Diagnostic Platform

**MediDiagnose AI** is an advanced medical diagnostic platform that leverages artificial intelligence to analyze patient reports and provide comprehensive health assessments. The platform employs specialized AI agents simulating **cardiologists**, **psychologists**, and **pulmonologists** to deliver expert analysis, culminating in a **multidisciplinary team diagnosis**.

<img width="1914" height="927" alt="Image" src="https://github.com/user-attachments/assets/0d58f74d-29d3-47dc-ac3b-67ac89de7871" />

<img width="1919" height="862" alt="Image" src="https://github.com/user-attachments/assets/8b6e4cba-e777-4020-95bb-48b33faf1db5" />

<img width="1908" height="959" alt="Image" src="https://github.com/user-attachments/assets/7b3b5d98-f4de-4703-a670-4b2cd6f0401b" />

<img width="1919" height="968" alt="Image" src="https://github.com/user-attachments/assets/d6ded123-cb0c-45a2-bfac-bfe29951c327" />

## 🚀 Key Features

- **🧠 AI-Powered Specialist Analysis** - Three specialized AI agents provide expert insights
- **🔬 Multidisciplinary Diagnosis** - Integrated team analysis identifies key health issues
- **📄 Comprehensive Reporting** - Detailed specialist reports with actionable recommendations
- **📥 PDF & Text Processing** - Automatically extracts and analyzes medical reports
- **💻 Professional UI** - Clean, intuitive interface designed for healthcare professionals
- **📤 Export Capabilities** - Download full diagnostic reports in text format

## 🛠️ Technology Stack

| Component           | Purpose                          |
|---------------------|----------------------------------|
| Streamlit           | Web application framework        |
| Google Gemini API   | Advanced AI analysis engine      |
| PyMuPDF (fitz)      | PDF text extraction              |
| Python              | Backend programming language     |

## 🧪 Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/medidiagnose-ai.git
cd medidiagnose-ai
```

### 2. Create a virtual environment

```bash
# For Linux/macOS:
python -m venv venv
source venv/bin/activate

# For Windows:
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Create a file at `.streamlit/secrets.toml` with the following content:

```toml
GEMINI_API_KEY = "your_gemini_api_key_here"
```

### 5. Run the application

```bash
streamlit run app.py
```

## ☁️ Deployment

### ✅ Option 1: Streamlit Sharing (Recommended)

1. Create an account at [share.streamlit.io](https://share.streamlit.io)
2. Connect your GitHub repository
3. Add your `GEMINI_API_KEY` in the Secrets section
4. Click Deploy

### 🐳 Option 2: Docker Deployment

```bash
# Build the Docker image
docker build -t medidiagnose-ai .

# Run the container
docker run -p 8501:8501 -e GEMINI_API_KEY=your_api_key medidiagnose-ai
```

Then open: http://localhost:8501

### 🖥️ Option 3: Traditional Server Deployment

1. Install Python 3.8+ and all dependencies
2. Run:
   ```bash
   streamlit run app.py
   ```
3. For production, configure Nginx or any reverse proxy

## ⚙️ Configuration

| Variable          | Description                        | Default  |
|-------------------|------------------------------------|----------|
| GEMINI_API_KEY    | Google Gemini API key             | Required |
| ANALYSIS_TIMEOUT  | Timeout for AI analysis (seconds) | 300      |
| MAX_FILE_SIZE     | Maximum upload file size          | 10MB     |

## 📋 Usage

1. Upload a medical report (PDF or text format)
2. Click **Start Analysis**
3. View individual specialist reports:
   - Cardiologist AI Report
   - Psychologist AI Report
   - Pulmonologist AI Report
4. Review the final multidisciplinary diagnosis
5. Download the full report for patient records

## 🤝 Contributing

We welcome contributions! Here's how:

```bash
# Fork the repository
# Create a new feature branch
git checkout -b feature/your-feature

# Commit your changes
git commit -am "Add some feature"

# Push to GitHub
git push origin feature/your-feature

# Open a Pull Request
```

## 📄 License

MediDiagnose AI is released under the MIT License.

## ⚠️ Disclaimer

- This application is for **educational and research purposes only**
- It does **not** provide medical advice, diagnosis, or treatment
- Always consult with qualified healthcare professionals for any medical concerns

---

**MediDiagnose AI** — Revolutionizing medical diagnostics through AI-powered analysis.
