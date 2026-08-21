md


🧂 SaltGuard AI
Agariya Worker Welfare Suite --- Challenge 11

SaltGuard AI is an AI-powered welfare platform designed to support
Agariya (salt pan) workers with health-risk guidance, fair salt-price
analysis, and welfare-scheme discovery. The application is built with
Python and Streamlit, integrates IBM watsonx.ai, and includes a Langflow
agent pipeline.

✨ Features
🩺 Health & Hazard Triage
Accepts worker symptoms in English, Hindi, or Gujarati

Considers current heat index and hours worked

Generates a severity level: Critical / High / Moderate / Low

Provides immediate first-aid guidance and referral recommendations

💰 Salt Fair-Price Advisor
Supports multiple salt grades

Takes tonnage, production region, moisture content, and offered
price

Generates an estimated fair market rate

Calculates total fair value

Assesses potential exploitation risk

Provides recommended actions and potential buyer/procurement
channels

📋 Welfare Scheme Matcher
Uses worker profile information such as age, category, gender, BPL
status, housing, equipment, experience, and health conditions

Generates relevant Gujarat and central government welfare schemes

Shows expected benefits and basic application guidance

🔗 Langflow Agent Pipeline
Provides a general-purpose welfare query interface

Sends requests to the local saltguard-agent Langflow flow

Uses IBM Granite/watsonx.ai as a fallback when Langflow is
unavailable

🏗️ Architecture
User
  │
  ▼
Streamlit Dashboard
  │
  ├── Health & Hazard Triage
  ├── Salt Fair-Price Advisor
  ├── Welfare Scheme Matcher
  │
  └── Langflow Agent
          │
          ▼
     IBM watsonx.ai
          │
          ▼
   Foundation Model / Granite Integration
The Langflow runner communicates with the local endpoint:

http://127.0.0.1:7860/api/v1/run/saltguard-agent
If Langflow is offline or returns an unexpected response, the
application falls back to the IBM watsonx.ai model wrapper.

🛠️ Technology Stack
Python

Streamlit

IBM watsonx.ai

IBM Granite / watsonx.ai foundation-model integration

Langflow

Requests

python-dotenv

Pandas

NumPy

Plotly

Folium

Streamlit-Folium

Pillow

📁 Project Structure
SaltGuardAI/
│
├── app.py
├── ibm_granite.py
├── langflow_agent.py
├── requirements.txt
├── .gitignore
├── .env                 # Local secrets — do not commit
└── README.md
File Roles
app.py - Main Streamlit application - Defines the dashboard and
four application tabs - Handles user inputs and sends prompts to the AI
layer

ibm_granite.py - IBM watsonx.ai model wrapper - Loads API
credentials from environment variables - Creates the model inference
client - Includes retry handling for rate-limit errors

langflow_agent.py - Connects the application to the local Langflow
pipeline - Sends chat requests to saltguard-agent - Falls back to IBM
watsonx.ai if Langflow is unavailable

requirements.txt - Contains the Python dependencies required by
the project

⚙️ Setup
1. Clone the repository
git clone <your-repository-url>
cd SaltGuardAI
2. Create a virtual environment
python -m venv venv
Activate it on Windows:

venv\Scripts\activate
3. Install dependencies
pip install -r requirements.txt
4. Configure IBM watsonx.ai
Create a .env file in the project directory:

IBM_API_KEY=your_ibm_api_key
IBM_PROJECT_ID=your_ibm_project_id
IBM_WML_URL=https://us-south.ml.cloud.ibm.com
WATSONX_MODEL_ID=your_model_id
Never commit the .env file or expose your API key publicly.

5. Run Langflow
Start Langflow locally:

python -m langflow run
Make sure the saltguard-agent flow is available at the configured
Langflow endpoint.

6. Run SaltGuard AI
streamlit run app.py
The Streamlit application will open in your browser.

🔐 Security
API credentials are loaded from environment variables rather than being
hard-coded into the application.

Recommended .gitignore entries:

.env
venv/
__pycache__/
*.pyc
Do not upload your IBM API key, project credentials, or other secrets to
GitHub.

🔄 Langflow Fallback
SaltGuard AI is designed to remain usable when Langflow is unavailable.

User Query
    │
    ▼
Langflow Pipeline
    │
    ├── Available ──► Langflow Response
    │
    └── Unavailable ──► IBM watsonx.ai Fallback
The fallback also handles connection errors, timeouts, HTTP errors, and
unexpected Langflow response structures.

⚠️ Important Note
The Health & Hazard Triage module is an AI assistance tool and not a
replacement for professional medical care. Serious or emergency
conditions should be referred to qualified medical professionals.

🎯 Project Goal
SaltGuard AI aims to provide Agariya workers with a single, accessible
AI platform for:

Safer Health Decisions • Fairer Salt Pricing • Better Welfare Access

Challenge
Challenge 11 --- AI-Based Salt Pan Worker (Agariya) Welfare & Safety
Platform

Domain: Social Governance

