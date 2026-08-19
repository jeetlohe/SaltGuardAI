"""
SaltGuard AI — Agariya Worker Welfare Suite
Challenge 11: AI-powered health triage, fair-price advisory, welfare scheme
matching, and Langflow pipeline integration for salt pan workers.
"""

import os
import streamlit as st
from pathlib import Path
from dotenv import load_dotenv
from ibm_granite import GraniteAgent
from langflow_agent import run_langflow_pipeline

# Load .env from the SaltGuardAI folder regardless of cwd
load_dotenv(dotenv_path=Path(__file__).parent / ".env", override=True)

# ── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SaltGuard AI",
    page_icon="🧂",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Global Dark-Mode CSS ──────────────────────────────────────────────────────
st.markdown("""
<style>
  /* ── Base ── */
  html, body, [data-testid="stAppViewContainer"] {
    background-color: #0d1117;
    color: #e6edf3;
    font-family: -apple-system, "Segoe UI", system-ui, sans-serif;
  }
  [data-testid="stSidebar"] { background-color: #161b22; }

  /* ── Headings ── */
  h1 { color: #58a6ff; letter-spacing: -0.5px; }
  h2, h3 { color: #79c0ff; }

  /* ── Tabs ── */
  [data-testid="stTabs"] button {
    color: #8b949e;
    font-weight: 600;
    font-size: 0.9rem;
    padding: 0.5rem 1.2rem;
    border-radius: 6px 6px 0 0;
  }
  [data-testid="stTabs"] button[aria-selected="true"] {
    color: #58a6ff;
    border-bottom: 2px solid #58a6ff;
    background: #161b22;
  }

  /* ── Cards ── */
  .sg-card {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 10px;
    padding: 1.2rem 1.5rem;
    margin-bottom: 1rem;
  }
  .sg-card-title {
    font-size: 0.78rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #8b949e;
    margin-bottom: 0.3rem;
  }
  .sg-card-value {
    font-size: 1.6rem;
    font-weight: 700;
    color: #e6edf3;
  }

  /* ── Severity badges ── */
  .badge {
    display: inline-block;
    padding: 0.25rem 0.75rem;
    border-radius: 999px;
    font-size: 0.85rem;
    font-weight: 700;
  }
  .badge-critical  { background:#3d0000; color:#ff7b72; border:1px solid #ff7b72; }
  .badge-high      { background:#2d1a00; color:#ffa657; border:1px solid #ffa657; }
  .badge-moderate  { background:#2c2200; color:#e3b341; border:1px solid #e3b341; }
  .badge-low       { background:#003820; color:#3fb950; border:1px solid #3fb950; }

  /* ── Inputs ── */
  [data-testid="stTextInput"] input,
  [data-testid="stTextArea"] textarea,
  [data-testid="stNumberInput"] input,
  [data-testid="stSelectbox"] select {
    background-color: #161b22 !important;
    color: #e6edf3 !important;
    border: 1px solid #30363d !important;
    border-radius: 6px !important;
  }

  /* ── Buttons ── */
  [data-testid="stButton"] > button {
    background: #1f6feb;
    color: #ffffff;
    border: none;
    border-radius: 6px;
    font-weight: 600;
    padding: 0.45rem 1.4rem;
    transition: background 0.2s;
  }
  [data-testid="stButton"] > button:hover {
    background: #388bfd;
  }

  /* ── Dividers ── */
  hr { border-color: #30363d; }

  /* ── Response box ── */
  .sg-response {
    background: #161b22;
    border-left: 3px solid #58a6ff;
    border-radius: 6px;
    padding: 1rem 1.2rem;
    white-space: pre-wrap;
    font-size: 0.95rem;
    line-height: 1.65;
    color: #e6edf3;
  }

  /* ── Scheme pill ── */
  .scheme-pill {
    display: inline-block;
    background: #1f2d3d;
    border: 1px solid #388bfd;
    color: #79c0ff;
    border-radius: 20px;
    padding: 0.2rem 0.9rem;
    margin: 0.25rem;
    font-size: 0.83rem;
    font-weight: 600;
  }

  /* ── Price table ── */
  .price-row {
    display: flex;
    justify-content: space-between;
    padding: 0.5rem 0;
    border-bottom: 1px solid #30363d;
    font-size: 0.93rem;
  }
  .price-label { color: #8b949e; }
  .price-value { color: #3fb950; font-weight: 700; }
</style>
""", unsafe_allow_html=True)

# ── Helpers ───────────────────────────────────────────────────────────────────

@st.cache_resource(show_spinner=False)
def load_granite() -> GraniteAgent | None:
    """Instantiate GraniteAgent once and cache it for the session."""
    try:
        return GraniteAgent()
    except Exception as exc:
        st.warning(f"⚙️ IBM Granite not initialised: {exc}", icon="⚙️")
        return None


def ask_granite(agent: GraniteAgent | None, prompt: str) -> str:
    if agent is None:
        return "⚠️ IBM Granite credentials not configured. Fill IBM_API_KEY and IBM_PROJECT_ID in .env."
    try:
        return agent.generate_response(prompt)
    except Exception as exc:
        if "429" in str(exc) or "consumption_limit_reached" in str(exc):
            return "⚠️ IBM watsonx.ai free-tier rate limit reached (max 10 concurrent requests). Please wait 30–60 seconds and try again."
        return f"⚠️ Error from IBM watsonx.ai: {exc}"


def severity_badge(level: str) -> str:
    cls = {"critical": "badge-critical", "high": "badge-high",
           "moderate": "badge-moderate", "low": "badge-low"}.get(level.lower(), "badge-low")
    return f'<span class="badge {cls}">{level.upper()}</span>'


# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("# 🧂 SaltGuard AI")
st.markdown("### Agariya Worker Welfare Suite &nbsp;·&nbsp; Challenge 11")
st.divider()

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "🩺 Health & Hazard Triage",
    "💰 Salt Fair-Price Advisor",
    "📋 Welfare Scheme Matcher",
    "🔗 Langflow Agent",
])

granite = load_granite()

# ─────────────────────────────────────────────────────────────────────────────
# TAB 1 — Health & Hazard Triage Agent
# ─────────────────────────────────────────────────────────────────────────────
with tab1:
    st.markdown("## 🩺 Health & Hazard Triage Agent")
    st.markdown(
        "Describe the worker's symptoms in **Gujarati, Hindi, or English**. "
        "The agent returns a severity risk level and immediate first-aid guidance."
    )
    st.divider()

    col_l, col_r = st.columns([1, 1], gap="large")

    with col_l:
        st.markdown("#### Worker Details")
        worker_id   = st.text_input("Worker ID / Name", placeholder="e.g. W-1042 or Ramji Bhai")
        language    = st.selectbox("Input Language", ["English", "Hindi", "Gujarati"])
        symptoms    = st.text_area(
            "Describe symptoms",
            placeholder=(
                "e.g. 'Dizziness, heavy sweating, cramps in legs since 2 hours' "
                "/ 'ચક્કર આવે છે, ઘણો પરસેવો થઈ રહ્યો છે' "
                "/ 'चक्कर आ रहा है, बहुत पसीना आ रहा है'"
            ),
            height=140,
        )
        heat_index  = st.number_input("Current Heat Index (°C)", min_value=20.0, max_value=60.0, value=38.0, step=0.5)
        hours_worked = st.slider("Hours Worked Today", min_value=1, max_value=14, value=6)

        triage_btn = st.button("🩺 Run Triage", key="triage", use_container_width=True)

    with col_r:
        st.markdown("#### Triage Report")
        if triage_btn:
            if not symptoms.strip():
                st.error("Please enter symptoms before running triage.")
            else:
                prompt = f"""You are SaltGuard AI, a medical triage assistant for Agariya (salt pan) workers in Gujarat, India.
A worker has reported the following:

Worker ID      : {worker_id or 'Unknown'}
Language used  : {language}
Symptoms       : {symptoms}
Current Heat Index: {heat_index}°C
Hours worked today: {hours_worked}

Respond strictly in English with:
1. SEVERITY LEVEL: one of [Critical / High / Moderate / Low]
2. LIKELY CONDITION: brief diagnosis (1 sentence)
3. IMMEDIATE FIRST AID: 3–5 numbered steps the on-site supervisor can take right now
4. REFERRAL NEEDED: Yes or No, with reason

Keep the response concise and actionable."""

                with st.spinner("Analysing symptoms with IBM Granite…"):
                    response = ask_granite(granite, prompt)

                # Parse severity for badge
                level = "moderate"
                for lvl in ["critical", "high", "moderate", "low"]:
                    if lvl in response.lower():
                        level = lvl
                        break

                st.markdown(
                    f"**Severity** &nbsp; {severity_badge(level)}",
                    unsafe_allow_html=True,
                )
                st.markdown(f'<div class="sg-response">{response}</div>', unsafe_allow_html=True)
        else:
            st.markdown(
                '<div class="sg-card"><div class="sg-card-title">Awaiting Input</div>'
                '<div style="color:#8b949e;font-size:0.9rem;">Fill in the worker details on the left and click <strong>Run Triage</strong>.</div></div>',
                unsafe_allow_html=True,
            )

    st.divider()
    st.markdown(
        "ℹ️ *This tool is an AI assistant. Always consult a medical professional for serious conditions.*"
    )


# ─────────────────────────────────────────────────────────────────────────────
# TAB 2 — Salt Fair-Price Advisor
# ─────────────────────────────────────────────────────────────────────────────
with tab2:
    st.markdown("## 💰 Salt Fair-Price Advisor")
    st.markdown(
        "Enter the salt grade and tonnage to get **fair market rates** and "
        "identify potential middleman exploitation."
    )
    st.divider()

    col_l2, col_r2 = st.columns([1, 1], gap="large")

    with col_l2:
        st.markdown("#### Salt Details")
        salt_grade    = st.selectbox(
            "Salt Grade",
            ["Industrial Grade (Low)", "Edible / Food Grade (Medium)",
             "Pharmaceutical Grade (High)", "Vacuum Evaporated (Premium)"],
        )
        tonnage       = st.number_input("Tonnage (MT)", min_value=0.5, max_value=5000.0, value=10.0, step=0.5)
        salt_region   = st.selectbox(
            "Production Region",
            ["Rann of Kutch, Gujarat", "Little Rann of Kutch", "Sambhar Lake, Rajasthan", "Coastal Andhra Pradesh"],
        )
        moisture_pct  = st.slider("Moisture Content (%)", min_value=0.0, max_value=10.0, value=3.0, step=0.5)
        offered_price = st.number_input(
            "Price Offered by Middleman (₹/MT)",
            min_value=0.0, max_value=10000.0, value=800.0, step=50.0,
        )

        price_btn = st.button("💰 Analyse Price", key="price", use_container_width=True)

    with col_r2:
        st.markdown("#### Market Rate Report")
        if price_btn:
            prompt = f"""You are SaltGuard AI, a fair-trade advisor for Agariya (salt pan) workers in Gujarat, India.

Salt Details:
- Grade        : {salt_grade}
- Tonnage      : {tonnage} MT
- Region       : {salt_region}
- Moisture     : {moisture_pct}%
- Offered Price: ₹{offered_price}/MT

Respond with:
1. FAIR MARKET RATE: estimated range in ₹/MT based on current Indian salt market
2. TOTAL FAIR VALUE: fair rate × tonnage (show calculation)
3. EXPLOITATION RISK: assess whether the offered price is fair, low, or exploitative
4. RECOMMENDED ACTION: 2–3 practical steps the worker/cooperative can take
5. KEY BUYERS: 2 legitimate bulk buyers or government procurement channels in India

Be concise, factual, and worker-focused."""

            with st.spinner("Fetching market intelligence via IBM Granite…"):
                response = ask_granite(granite, prompt)

            st.markdown(f'<div class="sg-response">{response}</div>', unsafe_allow_html=True)

            # Quick summary cards
            st.divider()
            sc1, sc2, sc3 = st.columns(3)
            with sc1:
                st.markdown('<div class="sg-card"><div class="sg-card-title">Grade</div>'
                            f'<div class="sg-card-value" style="font-size:1rem;">{salt_grade.split("(")[0].strip()}</div></div>',
                            unsafe_allow_html=True)
            with sc2:
                st.markdown(f'<div class="sg-card"><div class="sg-card-title">Tonnage</div>'
                            f'<div class="sg-card-value">{tonnage} MT</div></div>',
                            unsafe_allow_html=True)
            with sc3:
                st.markdown(f'<div class="sg-card"><div class="sg-card-title">Offered Price</div>'
                            f'<div class="sg-card-value" style="color:#ffa657;">₹{offered_price}/MT</div></div>',
                            unsafe_allow_html=True)
        else:
            st.markdown(
                '<div class="sg-card"><div class="sg-card-title">Awaiting Input</div>'
                '<div style="color:#8b949e;font-size:0.9rem;">Fill in salt details on the left and click <strong>Analyse Price</strong>.</div></div>',
                unsafe_allow_html=True,
            )


# ─────────────────────────────────────────────────────────────────────────────
# TAB 3 — Welfare Scheme Matcher
# ─────────────────────────────────────────────────────────────────────────────
with tab3:
    st.markdown("## 📋 Welfare Scheme Matcher")
    st.markdown(
        "Enter worker profile details to identify eligible **Gujarat state government "
        "subsidies, schemes, and entitlements**."
    )
    st.divider()

    col_l3, col_r3 = st.columns([1, 1], gap="large")

    with col_l3:
        st.markdown("#### Worker Profile")
        worker_age      = st.number_input("Age (years)", min_value=18, max_value=70, value=35)
        caste_category  = st.selectbox(
            "Caste Category",
            ["General", "OBC (Other Backward Class)", "SC (Scheduled Caste)", "ST (Scheduled Tribe)"],
        )
        gender          = st.selectbox("Gender", ["Male", "Female", "Other"])
        bpl_card        = st.checkbox("BPL (Below Poverty Line) Card Holder")
        has_equipment   = st.checkbox("Owns Salt Harvesting Equipment")
        has_housing     = st.checkbox("Owns Permanent Housing")
        years_in_trade  = st.slider("Years in Salt Farming", min_value=0, max_value=40, value=5)
        health_issue    = st.multiselect(
            "Known Health Conditions",
            ["None", "Skin Disease", "Eye Problems", "Joint Pain", "Respiratory Issues", "Diabetes"],
            default=["None"],
        )

        scheme_btn = st.button("📋 Find Eligible Schemes", key="scheme", use_container_width=True)

    with col_r3:
        st.markdown("#### Eligible Schemes & Benefits")
        if scheme_btn:
            profile_str = f"""
Worker Profile:
- Age             : {worker_age} years
- Caste Category  : {caste_category}
- Gender          : {gender}
- BPL Card        : {'Yes' if bpl_card else 'No'}
- Owns Equipment  : {'Yes' if has_equipment else 'No'}
- Owns Housing    : {'Yes' if has_housing else 'No'}
- Years in Trade  : {years_in_trade}
- Health Issues   : {', '.join(health_issue)}"""

            prompt = f"""You are SaltGuard AI, a welfare expert for Agariya (salt pan) workers in Gujarat, India.

{profile_str}

List ALL Gujarat state and central government schemes this worker is likely eligible for.
For each scheme provide:
- SCHEME NAME
- BENEFIT: what the worker receives (money, equipment, housing, insurance, etc.)
- HOW TO APPLY: one sentence

Include schemes from: Gujarat Salt Industry, BOCW (Building & Other Construction Workers), PM-JAY, PM Awas Yojana, NFBS, equipment subsidies, and any relevant SC/ST/OBC schemes.
Format clearly. Be specific to Gujarat."""

            with st.spinner("Matching schemes via IBM Granite…"):
                response = ask_granite(granite, prompt)

            st.markdown(f'<div class="sg-response">{response}</div>', unsafe_allow_html=True)

            # Quick profile pills
            st.divider()
            st.markdown("**Profile Tags:**")
            tags = [
                caste_category.split("(")[0].strip(),
                gender,
                f"Age {worker_age}",
                "BPL" if bpl_card else "Non-BPL",
                "Equipment Owner" if has_equipment else "No Equipment",
                f"{years_in_trade}y experience",
            ]
            pills_html = "".join(f'<span class="scheme-pill">{t}</span>' for t in tags)
            st.markdown(pills_html, unsafe_allow_html=True)
        else:
            st.markdown(
                '<div class="sg-card"><div class="sg-card-title">Awaiting Input</div>'
                '<div style="color:#8b949e;font-size:0.9rem;">Fill in the worker profile on the left and click <strong>Find Eligible Schemes</strong>.</div></div>',
                unsafe_allow_html=True,
            )



# ─────────────────────────────────────────────────────────────────────────────
# TAB 4 — Langflow Agent Pipeline
# ─────────────────────────────────────────────────────────────────────────────
with tab4:
    st.markdown("## 🔗 Langflow Agent Pipeline")
    st.markdown("Send any query through your **local Langflow `saltguard-agent` flow**.")
    st.divider()

    # Live status check
    import requests as _req
    try:
        _ping = _req.get("http://127.0.0.1:7860/api/v1/version", timeout=2)
        lf_online = _ping.status_code == 200
    except Exception:
        lf_online = False

    status_html = (
        '<span style="color:#3fb950;font-weight:700;">● Online</span>'
        if lf_online else
        '<span style="color:#f85149;font-weight:700;">● Offline</span>'
        ' &nbsp;<span style="color:#8b949e;font-size:0.85rem;">'
        '— start Langflow with: <code>python -m langflow run</code></span>'
    )
    st.markdown(f"**Langflow Status:** {status_html}", unsafe_allow_html=True)
    st.divider()

    lf_prompt = st.text_area(
        "Enter your query",
        placeholder="Ask anything about salt pan worker welfare, health, pricing, or schemes…",
        height=140,
    )
    lf_btn = st.button("🔗 Run Langflow Pipeline", key="langflow_run", use_container_width=True)

    if lf_btn:
        if not lf_prompt.strip():
            st.error("Please enter a query first.")
        else:
            source = "Langflow Pipeline" if lf_online else "IBM Granite (Langflow offline)"
            with st.spinner(f"Running via {source}…"):
                result = run_langflow_pipeline(lf_prompt)
            label = (
                '<span style="color:#3fb950">Langflow Pipeline</span>'
                if lf_online else
                '<span style="color:#ffa657">IBM Granite (fallback)</span>'
            )
            st.markdown(f"**Response via:** {label}", unsafe_allow_html=True)
            st.markdown(f'<div class="sg-response">{result}</div>', unsafe_allow_html=True)


# ── Footer ────────────────────────────────────────────────────────────────────
st.divider()
st.markdown(
    '<p style="text-align:center;color:#484f58;font-size:0.78rem;">'
    "SaltGuard AI &nbsp;·&nbsp; Agariya Worker Welfare Suite &nbsp;·&nbsp; Challenge 11 &nbsp;·&nbsp; "
    "Powered by IBM watsonx.ai</p>",
    unsafe_allow_html=True,
)
