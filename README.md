# 🧂 SaltGuard AI — Agariya Worker Welfare Suite

> **Challenge 11 · IBM University Engagement · Edument Foundation**
> AI-powered health triage, fair-price advisory, welfare scheme matching, and Langflow pipeline integration for salt pan workers in Gujarat, India.

[![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.61-red?logo=streamlit)](https://streamlit.io)
[![IBM watsonx.ai](https://img.shields.io/badge/IBM-watsonx.ai-0f62fe?logo=ibm)](https://www.ibm.com/watsonx)
[![Langflow](https://img.shields.io/badge/Langflow-1.11-purple)](https://langflow.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green)](LICENSE)

---

## 📌 Problem Statement

Agariya workers are a marginalised community of salt pan labourers in the Rann of Kutch, Gujarat. They face:

- **Extreme heat exposure** (heat index often exceeding 45°C) with no on-site medical support
- **Price exploitation** by middlemen who purchase salt at a fraction of fair market value
- **Zero awareness** of government welfare schemes they are legally entitled to

SaltGuard AI addresses all three problems in a single, multilingual web app powered by **IBM Granite LLM** on **watsonx.ai**.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         SaltGuard AI                            │
│                                                                 │
│  ┌──────────┐    ┌─────────────┐    ┌──────────────────────┐   │
│  │ Streamlit│───▶│ GraniteAgent│───▶│  IBM watsonx.ai      │   │
│  │ Frontend │    │ (wrapper)   │    │  granite-3-2-8b      │   │
│  └──────────┘    └─────────────┘    └──────────────────────┘   │
│        │                                                        │
│        │         ┌─────────────────────────────────────────┐   │
│        └────────▶│  Langflow Agent  (local / optional)     │   │
│                  │  http://127.0.0.1:7860                   │   │
│                  │  Falls back to Granite if offline        │   │
│                  └─────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

| Layer | Technology |
|---|---|
| Frontend UI | Streamlit (dark theme) |
| LLM | IBM Granite 3.2 8B Instruct via watsonx.ai |
| Agentic Pipeline | Langflow `saltguard-agent` flow |
| Environment Config | python-dotenv |
| Visualisation | Plotly, Folium, streamlit-folium |

---

## ✨ Features

### 🩺 Tab 1 — Health & Hazard Triage Agent
- Enter worker symptoms in **English, Hindi, or Gujarati**
- Input heat index (°C) and hours worked
- Granite returns:
  - **Severity Level** — Critical / High / Moderate / Low (with colour badge)
  - **Likely Condition** — brief AI diagnosis
  - **Immediate First Aid** — 3–5 numbered steps for on-site supervisor
  - **Referral Needed** — Yes/No with reason

### 💰 Tab 2 — Salt Fair-Price Advisor
- Input salt grade, tonnage, production region, moisture %, and middleman's offered price
- Granite returns:
  - **Fair Market Rate** (₹/MT range based on Indian salt market)
  - **Total Fair Value** (with calculation)
  - **Exploitation Risk** assessment
  - **Recommended Actions** for the worker / cooperative
  - **Key Buyers** — legitimate bulk buyers or government procurement channels

### 📋 Tab 3 — Welfare Scheme Matcher
- Input worker profile: age, caste category, gender, BPL card, equipment ownership, health conditions
- Granite lists **all eligible Gujarat state + central government schemes** with:
  - Scheme name and benefit
  - How to apply (one sentence)
  - Profile tags shown as pills

### 🔗 Tab 4 — Langflow Agent Pipeline
- Live status indicator (● Online / ● Offline)
- Routes any free-text query through the local **Langflow `saltguard-agent` flow**
- Automatically falls back to IBM Granite if Langflow is not running

---

## 🚀 Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/jeetlohe/SaltGuardAI.git
cd SaltGuardAI
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure environment variables
Create a `.env` file in the `SaltGuardAI` directory:
```env
IBM_API_KEY=your_ibm_cloud_api_key
IBM_PROJECT_ID=your_watsonx_project_id
IBM_WML_URL=https://us-south.ml.cloud.ibm.com
WATSONX_MODEL_ID=ibm/granite-3-2-8b-instruct
```

Get your credentials from [IBM watsonx.ai](https://www.ibm.com/watsonx) → My Projects → Manage → Access.

### 4. Run the app
```bash
streamlit run app.py
```

Opens at **http://localhost:8501**

### 5. (Optional) Start Langflow
```bash
python -m langflow run
```
Then import the `saltguard-agent` flow at **http://localhost:7860**.
If Langflow is offline, Tab 4 automatically falls back to Granite.

---

## 📁 Project Structure

```
SaltGuardAI/
├── app.py               # Streamlit UI — all 4 tabs, CSS, layout
├── ibm_granite.py       # GraniteAgent wrapper (watsonx.ai ModelInference)
├── langflow_agent.py    # Langflow pipeline runner with Granite fallback
├── requirements.txt     # Python dependencies
├── .env                 # Credentials (gitignored)
└── README.md            # This file
```

---

## 🔧 Configuration Reference

| Variable | Default | Description |
|---|---|---|
| `IBM_API_KEY` | — | IBM Cloud API key (**required**) |
| `IBM_PROJECT_ID` | — | watsonx.ai project ID (**required**) |
| `IBM_WML_URL` | `https://us-south.ml.cloud.ibm.com` | watsonx.ai endpoint |
| `WATSONX_MODEL_ID` | `ibm/granite-3-2-8b-instruct` | Granite model ID |

---

## 🛡️ Rate Limit Handling

The `GraniteAgent` automatically retries on IBM watsonx.ai **429 / consumption_limit_reached** errors with exponential back-off:

| Attempt | Wait |
|---|---|
| 1 | immediate |
| 2 | 5 s |
| 3 | 15 s |
| 4 | 30 s |
| 5 | 60 s |

---

## 🌐 Multilingual Support

Triage prompts accept input in:
- 🇮🇳 **Gujarati** — ચક્કર આવે છે, ઘણો પરસેવો થઈ રહ્યો છે
- 🇮🇳 **Hindi** — चक्कर आ रहा है, बहुत पसीना आ रहा है
- 🌍 **English** — Dizziness, heavy sweating, leg cramps

All AI responses are returned in English for supervisor readability.

---

## 📜 License

MIT License © 2025 Jeet Lohe

---

## 🙏 Acknowledgements

- **IBM watsonx.ai** — Granite 3.2 LLM
- **Langflow** — Open-source visual AI pipeline builder
- **Streamlit** — Rapid Python web UI framework
- **Edument Foundation / IBM University Engagement** — Challenge 11 organisers
- Inspired by the real struggles of **Agariya salt pan workers** in Gujarat, India 🧂
