import asyncio
from datetime import datetime

import streamlit as st

from config import GROUP_ID, INCIDENT_ID, get_graphiti_client
from incident_data import INCIDENT_EVENTS

# ---------------------------------------------------------------------------
st.set_page_config(
    page_title=f"{INCIDENT_ID} — Arclight",
    page_icon="\U0001f6e1\ufe0f",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# CSS
# ---------------------------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600&display=swap');

:root {
    --bg-primary:   #06080f;
    --bg-secondary: #0b0f1a;
    --bg-card:      #0f1320;
    --bg-elevated:  #141926;
    --border:       #1c2235;
    --border-hover: #2a3350;
    --text-primary: #e8ecf4;
    --text-secondary: #8891a5;
    --text-muted:   #555d73;
    --accent-blue:  #4f8ff7;
    --accent-purple:#8b7cf7;
    --accent-green: #34d399;
    --accent-red:   #f06060;
    --accent-amber: #f0a030;
    --accent-cyan:  #22d3ee;
}

html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
}

/* ---- app background ---- */
.stApp { background: var(--bg-primary); }
.main .block-container { padding: 1.2rem 2rem 2rem; max-width: 1440px; }
#MainMenu, footer, header { visibility: hidden; }

/* ---- sidebar ---- */
section[data-testid="stSidebar"] {
    background: var(--bg-secondary);
    border-right: 1px solid var(--border);
}
section[data-testid="stSidebar"] .stMarkdown p,
section[data-testid="stSidebar"] .stMarkdown h1,
section[data-testid="stSidebar"] .stMarkdown h2,
section[data-testid="stSidebar"] .stMarkdown h3 { color: var(--text-secondary); }
section[data-testid="stSidebar"] [data-testid="stSidebarCollapsedControl"] { color: var(--text-muted); }

/* ---- tabs ---- */
.stTabs [data-baseweb="tab-list"] {
    gap: 2px;
    background: var(--bg-secondary);
    border-radius: 12px;
    padding: 4px;
    border: 1px solid var(--border);
}
.stTabs [data-baseweb="tab"] {
    border-radius: 10px;
    color: var(--text-muted);
    font-weight: 600;
    font-size: 0.82rem;
    padding: 10px 22px;
    letter-spacing: 0.01em;
    background: transparent;
    border-bottom: none !important;
}
.stTabs [aria-selected="true"] {
    background: var(--bg-elevated) !important;
    color: var(--text-primary) !important;
    box-shadow: 0 1px 4px rgba(0,0,0,0.3);
}
.stTabs [data-baseweb="tab-border"],
.stTabs [data-baseweb="tab-highlight"] { display: none; }

/* ---- metrics ---- */
div[data-testid="stMetric"] {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 18px 20px;
    transition: border-color 0.2s;
}
div[data-testid="stMetric"]:hover { border-color: var(--border-hover); }
div[data-testid="stMetric"] label {
    color: var(--text-muted) !important;
    font-size: 0.72rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.06em;
    text-transform: uppercase;
}
div[data-testid="stMetric"] [data-testid="stMetricValue"] {
    color: var(--text-primary) !important;
    font-weight: 800 !important;
    font-size: 1.5rem !important;
    letter-spacing: -0.02em;
}

/* ---- buttons ---- */
.stButton > button {
    border-radius: 10px;
    font-weight: 600;
    font-size: 0.82rem;
    border: 1px solid var(--border);
    transition: all 0.15s ease;
    letter-spacing: 0.01em;
}
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #4f8ff7, #6366f1);
    border: none;
    color: #fff;
    box-shadow: 0 2px 8px rgba(79,143,247,0.15);
}
.stButton > button[kind="primary"]:hover {
    background: linear-gradient(135deg, #6ba3ff, #818cf8);
    box-shadow: 0 4px 20px rgba(79,143,247,0.25);
    transform: translateY(-1px);
}
.stButton > button:not([kind="primary"]) {
    background: var(--bg-elevated);
    color: var(--text-secondary);
}
.stButton > button:not([kind="primary"]):hover {
    background: var(--border);
    color: var(--text-primary);
}

/* ---- text input ---- */
.stTextInput input {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text-primary) !important;
    font-size: 0.85rem;
    padding: 10px 14px !important;
}
.stTextInput input::placeholder { color: var(--text-muted) !important; }
.stTextInput input:focus {
    border-color: var(--accent-blue) !important;
    box-shadow: 0 0 0 3px rgba(79,143,247,0.1) !important;
}

/* ---- expanders ---- */
[data-testid="stExpander"] {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 12px;
}

/* ---- markdown ---- */
.stMarkdown p, .stMarkdown li { color: var(--text-secondary); }
.stMarkdown h1, .stMarkdown h2, .stMarkdown h3 { color: var(--text-primary); }
.stMarkdown code {
    background: var(--bg-elevated);
    color: var(--accent-blue);
    padding: 2px 7px;
    border-radius: 5px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.85em;
}
hr { border-color: var(--border) !important; }

/* ---- scrollbar ---- */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 10px; }
::-webkit-scrollbar-thumb:hover { background: var(--border-hover); }

/* ---- progress ---- */
.stProgress > div > div { background: linear-gradient(90deg, var(--accent-blue), var(--accent-purple)) !important; }

/* ---- alerts ---- */
div[data-testid="stAlert"] { border-radius: 12px; }

/* ===== CUSTOM COMPONENTS ===== */

/* ---- top bar ---- */
.top-bar {
    background: linear-gradient(135deg, var(--bg-secondary) 0%, var(--bg-card) 100%);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 28px 32px;
    margin-bottom: 12px;
    position: relative;
    overflow: hidden;
}
.top-bar::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, var(--accent-blue), var(--accent-purple), var(--accent-cyan));
}
.top-bar-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 16px;
}
.top-bar-left { display: flex; align-items: center; gap: 16px; }
.top-bar-title {
    font-size: 1.35rem;
    font-weight: 800;
    color: var(--text-primary);
    letter-spacing: -0.03em;
}
.top-bar-badges { display: flex; gap: 8px; flex-wrap: wrap; }
.top-bar-status {
    display: flex;
    align-items: center;
    gap: 20px;
    font-size: 0.78rem;
    color: var(--text-muted);
}
.top-bar-status-item { display: flex; align-items: center; gap: 6px; }
.status-dot {
    width: 8px; height: 8px;
    border-radius: 50%;
    display: inline-block;
}
.status-dot-green { background: var(--accent-green); box-shadow: 0 0 6px var(--accent-green); }
.status-dot-red   { background: var(--accent-red); box-shadow: 0 0 6px var(--accent-red); }

/* ---- badges ---- */
.b {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    padding: 4px 12px;
    border-radius: 8px;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.04em;
}
.b-crit { background: rgba(240,96,96,0.12); color: #f87171; border: 1px solid rgba(240,96,96,0.2); }
.b-ok   { background: rgba(52,211,153,0.1); color: #34d399; border: 1px solid rgba(52,211,153,0.2); }
.b-svc  { background: rgba(79,143,247,0.1); color: #7cb3ff; border: 1px solid rgba(79,143,247,0.15); }
.b-dur  { background: var(--bg-elevated); color: var(--text-secondary); border: 1px solid var(--border); }
.b-id   {
    background: var(--bg-elevated);
    color: var(--text-primary);
    border: 1px solid var(--border);
    font-family: 'JetBrains Mono', monospace;
    font-weight: 600;
    font-size: 0.74rem;
}

/* ---- timeline ---- */
.tl-event {
    display: flex;
    gap: 16px;
    padding: 14px 18px;
    border-left: 2px solid var(--border);
    margin-left: 8px;
    position: relative;
    transition: background 0.15s;
}
.tl-event:hover { background: var(--bg-card); border-radius: 0 12px 12px 0; }
.tl-event::before {
    content: '';
    position: absolute;
    left: -6px;
    top: 18px;
    width: 10px;
    height: 10px;
    border-radius: 50%;
    z-index: 1;
}
.tl-event-info::before    { background: var(--accent-green); }
.tl-event-warning::before { background: var(--accent-amber); }
.tl-event-critical::before {
    background: var(--accent-red);
    box-shadow: 0 0 8px rgba(240,96,96,0.5);
    animation: pulse-red 2s ease-in-out infinite;
}
@keyframes pulse-red {
    0%, 100% { box-shadow: 0 0 4px rgba(240,96,96,0.3); }
    50%      { box-shadow: 0 0 12px rgba(240,96,96,0.6); }
}
.tl-event:last-child { border-left-color: transparent; }

.tl-time {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.76rem;
    font-weight: 600;
    color: var(--text-muted);
    width: 44px;
    flex-shrink: 0;
    padding-top: 2px;
}
.tl-body { flex: 1; min-width: 0; }
.tl-head { display: flex; align-items: center; gap: 8px; flex-wrap: wrap; margin-bottom: 3px; }
.tl-src {
    display: inline-block;
    padding: 2px 8px;
    border-radius: 5px;
    font-size: 0.66rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.06em;
}
.tl-sev {
    display: inline-block;
    padding: 2px 7px;
    border-radius: 5px;
    font-size: 0.64rem;
    font-weight: 700;
    letter-spacing: 0.04em;
}
.tl-sev-info     { background: rgba(52,211,153,0.1); color: var(--accent-green); }
.tl-sev-warning  { background: rgba(240,160,48,0.12); color: var(--accent-amber); }
.tl-sev-critical { background: rgba(240,96,96,0.12); color: var(--accent-red); }
.tl-actor { font-weight: 700; color: var(--text-primary); font-size: 0.84rem; }
.tl-msg { color: var(--text-secondary); font-size: 0.82rem; line-height: 1.55; }

.tl-phase-marker {
    display: flex;
    align-items: center;
    gap: 10px;
    margin: 20px 0 4px;
    padding-left: 20px;
}
.tl-phase-line { width: 24px; height: 1px; background: var(--border-hover); }
.tl-phase-label {
    font-size: 0.68rem;
    font-weight: 800;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.12em;
}

/* ---- investigation cards ---- */
.inv-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 20px 24px;
    margin-bottom: 10px;
    transition: all 0.15s;
    position: relative;
}
.inv-card:hover { border-color: var(--border-hover); transform: translateY(-1px); box-shadow: 0 4px 20px rgba(0,0,0,0.2); }
.inv-card::before {
    content: '';
    position: absolute;
    left: 0; top: 12px; bottom: 12px;
    width: 3px;
    border-radius: 3px;
    background: linear-gradient(180deg, var(--accent-blue), var(--accent-purple));
}
.inv-idx {
    font-size: 0.66rem;
    font-weight: 800;
    color: var(--accent-blue);
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 8px;
}
.inv-fact {
    color: var(--text-primary);
    font-size: 0.9rem;
    font-weight: 500;
    line-height: 1.6;
}
.inv-meta {
    margin-top: 12px;
    display: flex;
    gap: 6px;
    flex-wrap: wrap;
}
.inv-tag {
    background: var(--bg-elevated);
    border: 1px solid var(--border);
    padding: 3px 10px;
    border-radius: 6px;
    font-size: 0.72rem;
    font-family: 'JetBrains Mono', monospace;
    color: var(--text-muted);
}

/* ---- entity cards ---- */
.ent-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
.ent-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 20px 22px;
    transition: all 0.15s;
}
.ent-card:hover { border-color: var(--border-hover); transform: translateY(-1px); }
.ent-icon {
    width: 36px; height: 36px;
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1rem;
    margin-bottom: 12px;
    font-weight: 700;
    color: #fff;
}
.ent-name { color: var(--text-primary); font-weight: 700; font-size: 0.92rem; margin-bottom: 6px; }
.ent-summary { color: var(--text-secondary); font-size: 0.8rem; line-height: 1.55; }

/* ---- report ---- */
.rpt {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 24px 28px;
    margin-bottom: 12px;
}
.rpt-title {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 0.72rem;
    font-weight: 800;
    color: var(--accent-blue);
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 16px;
    padding-bottom: 12px;
    border-bottom: 1px solid var(--border);
}
.rpt-title-dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: var(--accent-blue);
}
.rpt-kv {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 0;
    border-bottom: 1px solid rgba(28,34,53,0.6);
    font-size: 0.86rem;
}
.rpt-kv:last-child { border-bottom: none; }
.rpt-k { color: var(--text-muted); font-weight: 500; }
.rpt-v { color: var(--text-primary); font-weight: 600; font-family: 'JetBrains Mono', monospace; font-size: 0.84rem; }

.rpt-step {
    display: flex;
    gap: 14px;
    margin-bottom: 14px;
    align-items: flex-start;
}
.rpt-step-num {
    width: 28px; height: 28px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.72rem;
    font-weight: 800;
    flex-shrink: 0;
    border: 1.5px solid var(--border);
    color: var(--accent-blue);
    background: var(--bg-elevated);
}
.rpt-step-text { color: var(--text-secondary); font-size: 0.86rem; line-height: 1.5; padding-top: 3px; }

.rpt-person {
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 12px 0;
    border-bottom: 1px solid rgba(28,34,53,0.5);
}
.rpt-person:last-child { border-bottom: none; }
.rpt-avatar {
    width: 38px; height: 38px;
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.82rem;
    font-weight: 800;
    color: #fff;
    flex-shrink: 0;
}
.rpt-person-info { flex: 1; }
.rpt-person-name { color: var(--text-primary); font-weight: 700; font-size: 0.88rem; }
.rpt-person-role { color: var(--text-muted); font-size: 0.76rem; margin-top: 1px; }
.rpt-person-action { color: var(--text-secondary); font-size: 0.78rem; text-align: right; line-height: 1.5; }

.rpt-stat {
    text-align: center;
    padding: 16px 12px;
    background: var(--bg-primary);
    border-radius: 12px;
    border: 1px solid var(--border);
}
.rpt-stat-val {
    font-size: 1.6rem;
    font-weight: 900;
    letter-spacing: -0.03em;
    font-family: 'Inter', sans-serif;
}
.rpt-stat-label {
    font-size: 0.66rem;
    font-weight: 700;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-top: 4px;
}

/* ---- empty state ---- */
.empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 80px 20px;
    text-align: center;
}
.empty-icon {
    width: 64px; height: 64px;
    border-radius: 18px;
    background: var(--bg-card);
    border: 1px solid var(--border);
    display: flex; align-items: center; justify-content: center;
    font-size: 1.8rem;
    margin-bottom: 20px;
}
.empty-title { color: var(--text-secondary); font-size: 0.95rem; font-weight: 600; }
.empty-desc  { color: var(--text-muted); font-size: 0.82rem; margin-top: 6px; max-width: 340px; line-height: 1.5; }

/* ---- sidebar custom ---- */
.sb-brand {
    display: flex; align-items: center; gap: 12px;
    padding-bottom: 20px;
    margin-bottom: 20px;
    border-bottom: 1px solid var(--border);
}
.sb-logo {
    width: 36px; height: 36px;
    border-radius: 10px;
    background: linear-gradient(135deg, #4f8ff7, #8b7cf7);
    display: flex; align-items: center; justify-content: center;
    font-weight: 900; font-size: 15px; color: #fff;
    box-shadow: 0 2px 10px rgba(79,143,247,0.25);
}
.sb-name { font-size: 1rem; font-weight: 800; color: var(--text-primary); letter-spacing: -0.02em; }
.sb-sub  { font-size: 0.66rem; color: var(--text-muted); font-weight: 600; letter-spacing: 0.02em; }

.sb-section {
    font-size: 0.66rem;
    font-weight: 800;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.12em;
    margin: 24px 0 10px;
}
.sb-ctx {
    font-size: 0.8rem;
    color: var(--text-muted);
    line-height: 1.8;
}
.sb-ctx strong { color: var(--text-secondary); font-weight: 600; }

/* ---- query pill ---- */
.q-pill {
    background: var(--bg-elevated);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 12px 16px;
    margin-bottom: 14px;
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 0.82rem;
    color: var(--text-secondary);
}
.q-pill-icon {
    width: 28px; height: 28px;
    border-radius: 8px;
    background: linear-gradient(135deg, rgba(79,143,247,0.15), rgba(139,124,247,0.15));
    display: flex; align-items: center; justify-content: center;
    font-size: 0.8rem;
    flex-shrink: 0;
}
.q-pill strong { color: var(--text-primary); }

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Async helpers
# ---------------------------------------------------------------------------

def run_async(coro):
    loop = asyncio.new_event_loop()
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()


async def _search_graph(query: str, num_results: int = 10):
    client = await get_graphiti_client()
    try:
        return await client.search(query, num_results=num_results, group_ids=[GROUP_ID])
    finally:
        await client.close()


async def _search_entities(query: str, num_results: int = 10):
    from graphiti_core.search.search_config_recipes import NODE_HYBRID_SEARCH_RRF
    client = await get_graphiti_client()
    try:
        config = NODE_HYBRID_SEARCH_RRF.model_copy(deep=True)
        config.limit = num_results
        return (await client._search(query, config=config, group_ids=[GROUP_ID])).nodes
    finally:
        await client.close()

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

SRC = {
    "git":     ("Git",     "#a78bfa"),
    "ci":      ("CI/CD",   "#818cf8"),
    "deploy":  ("Deploy",  "#4f8ff7"),
    "monitor": ("Monitor", "#22d3ee"),
    "alert":   ("Alert",   "#f06060"),
    "slack":   ("Slack",   "#34d399"),
}
DOT = {"info": "#34d399", "warning": "#f0a030", "critical": "#f06060"}
PHASES = {"DEPLOYMENT": 0, "DETECTION": 4, "RESPONSE": 6, "REMEDIATION": 9, "RECOVERY": 11}
DUR = int((INCIDENT_EVENTS[-1].timestamp - INCIDENT_EVENTS[0].timestamp).total_seconds() / 60)

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------

with st.sidebar:
    st.markdown(
        '<div class="sb-brand">'
        '<div class="sb-logo">A</div>'
        '<div><div class="sb-name">Arclight</div>'
        '<div class="sb-sub">Incident Response Platform</div></div>'
        '</div>',
        unsafe_allow_html=True,
    )

    st.markdown('<div class="sb-section">Knowledge Graph Search</div>', unsafe_allow_html=True)
    user_query = st.text_input("q", placeholder="What caused the error rate spike?", label_visibility="collapsed")
    run_custom = st.button("Search Graph", type="primary", use_container_width=True)

    st.markdown('<div class="sb-section">Quick Investigations</div>', unsafe_allow_html=True)
    ca, cb = st.columns(2)
    with ca:
        q_root   = st.button("Root Cause",  use_container_width=True)
        q_people = st.button("People",      use_container_width=True)
    with cb:
        q_tl     = st.button("Timeline",    use_container_width=True)
        q_chg    = st.button("Changes",     use_container_width=True)

    st.markdown('<div class="sb-section">Incident Context</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="sb-ctx">'
        f'<strong>ID</strong> &nbsp;<code>{INCIDENT_ID}</code><br>'
        f'<strong>Date</strong> &nbsp;Nov 15 2024<br>'
        f'<strong>Window</strong> &nbsp;14:10 – 14:30 UTC<br>'
        f'<strong>Service</strong> &nbsp;payment-api<br>'
        f'<strong>Commander</strong> &nbsp;Bob<br>'
        f'<strong>Episodes</strong> &nbsp;{len(INCIDENT_EVENTS)} ingested'
        f'</div>',
        unsafe_allow_html=True,
    )

# resolve query
aq = None
if run_custom and user_query.strip():
    aq = user_query.strip()
elif q_root:   aq = "What was the root cause of the payment-api incident?"
elif q_tl:     aq = "What is the full timeline of the payment-api incident?"
elif q_people: aq = "Which people were involved in the payment-api incident and what did each person do?"
elif q_chg:    aq = "What code or configuration changes happened before the payment-api outage started?"

if aq:
    with st.spinner("Querying knowledge graph..."):
        try:
            st.session_state["last_query"]   = aq
            st.session_state["last_results"] = run_async(_search_graph(aq))
        except Exception as e:
            st.toast(f"Query failed: {e}", icon="\u26a0\ufe0f")

# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------

st.markdown(
    f"""
    <div class="top-bar">
        <div class="top-bar-row">
            <div class="top-bar-left">
                <div class="top-bar-title">Incident Investigation</div>
                <div class="top-bar-badges">
                    <span class="b b-id">{INCIDENT_ID}</span>
                    <span class="b b-crit">P1 CRITICAL</span>
                    <span class="b b-svc">payment-api</span>
                    <span class="b b-dur">{DUR} min</span>
                    <span class="b b-ok">RESOLVED</span>
                </div>
            </div>
            <div class="top-bar-status">
                <div class="top-bar-status-item"><span class="status-dot status-dot-green"></span>Neo4j Connected</div>
                <div class="top-bar-status-item"><span class="status-dot status-dot-green"></span>Graph Ready</div>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

m1, m2, m3, m4, m5, m6 = st.columns(6)
m1.metric("Time to Detect",  "6 min")
m2.metric("Time to Resolve", "20 min")
m3.metric("Error Rate Peak", "42%")
m4.metric("Revenue Impact",  "$2.3K/min")
m5.metric("Events Ingested", str(len(INCIDENT_EVENTS)))
m6.metric("Services Hit",    "1")

st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Tabs
# ---------------------------------------------------------------------------

t1, t2, t3, t4 = st.tabs(["Timeline", "Investigation", "Entities", "Report"])

# ---- TIMELINE -------------------------------------------------------------
with t1:
    for i, ev in enumerate(INCIDENT_EVENTS):
        for pn, pi in PHASES.items():
            if i == pi:
                st.markdown(
                    f'<div class="tl-phase-marker"><div class="tl-phase-line"></div>'
                    f'<span class="tl-phase-label">{pn}</span></div>',
                    unsafe_allow_html=True,
                )

        sl, sc = SRC.get(ev.source, (ev.source, "#555d73"))

        st.markdown(
            f'<div class="tl-event tl-event-{ev.severity}">'
            f'<div class="tl-time">{ev.timestamp.strftime("%H:%M")}</div>'
            f'<div class="tl-body">'
            f'<div class="tl-head">'
            f'<span class="tl-src" style="background:{sc}18;color:{sc};">{sl}</span>'
            f'<span class="tl-sev tl-sev-{ev.severity}">{ev.severity.upper()}</span>'
            f'<span class="tl-actor">{ev.actor}</span></div>'
            f'<div class="tl-msg">{ev.message}</div>'
            f'</div></div>',
            unsafe_allow_html=True,
        )

# ---- INVESTIGATION --------------------------------------------------------
with t2:
    st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
    lq = st.session_state.get("last_query")
    lr = st.session_state.get("last_results")

    if lq and lr is not None:
        n = len(lr)
        st.markdown(
            f'<div class="q-pill">'
            f'<div class="q-pill-icon">\U0001f50d</div>'
            f'<div><strong>{lq}</strong><br><span style="font-size:0.76rem;color:var(--text-muted);">{n} finding{"s" if n != 1 else ""} from knowledge graph</span></div>'
            f'</div>',
            unsafe_allow_html=True,
        )
        for idx, edge in enumerate(lr, 1):
            tags = ""
            if hasattr(edge, "valid_at") and edge.valid_at:
                tags += f'<span class="inv-tag">valid {edge.valid_at}</span>'
            if hasattr(edge, "invalid_at") and edge.invalid_at:
                tags += f'<span class="inv-tag">invalid {edge.invalid_at}</span>'
            if hasattr(edge, "episodes") and edge.episodes:
                tags += f'<span class="inv-tag">{len(edge.episodes)} episodes</span>'

            st.markdown(
                f"""
                <div class="inv-card">
                    <div class="inv-idx">Finding {idx:02d}</div>
                    <div class="inv-fact">{edge.fact}</div>
                    {"<div class='inv-meta'>" + tags + "</div>" if tags else ""}
                </div>
                """,
                unsafe_allow_html=True,
            )
    else:
        st.markdown(
            '<div class="empty-state">'
            '<div class="empty-icon">\U0001f50d</div>'
            '<div class="empty-title">No investigation results yet</div>'
            '<div class="empty-desc">Search the knowledge graph using the sidebar or click a quick investigation button to start</div>'
            '</div>',
            unsafe_allow_html=True,
        )

# ---- ENTITIES -------------------------------------------------------------
with t3:
    st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

    EQ = ["payment-api service", "Alice engineer", "Bob engineer", "rate limiter configuration", "PagerDuty alert"]
    ENT_COLORS = ["#4f8ff7", "#a78bfa", "#22d3ee", "#f0a030", "#f06060", "#34d399", "#818cf8", "#f472b6"]

    if st.button("Load Entities from Knowledge Graph", type="primary"):
        all_ent = []
        prog = st.progress(0, text="Searching...")
        for j, eq in enumerate(EQ):
            try:
                nodes = run_async(_search_entities(eq, num_results=3))
                for nd in nodes:
                    all_ent.append({"name": getattr(nd, "name", str(nd)), "summary": getattr(nd, "summary", "")})
            except Exception:
                pass
            prog.progress((j + 1) / len(EQ), text=f"Searching: {eq}")
        prog.empty()
        seen = set()
        uniq = []
        for e in all_ent:
            if e["name"] not in seen:
                seen.add(e["name"])
                uniq.append(e)
        if uniq:
            st.session_state["entities"] = uniq

    ents = st.session_state.get("entities", [])
    if ents:
        st.markdown(
            f'<div class="q-pill">'
            f'<div class="q-pill-icon">\U0001f310</div>'
            f'<div><strong>{len(ents)} entities</strong> discovered in the knowledge graph</div>'
            f'</div>',
            unsafe_allow_html=True,
        )
        cards = ""
        for k, e in enumerate(ents):
            c = ENT_COLORS[k % len(ENT_COLORS)]
            initial = e["name"][0].upper() if e["name"] else "?"
            cards += (
                f'<div class="ent-card">'
                f'<div class="ent-icon" style="background:{c};">{initial}</div>'
                f'<div class="ent-name">{e["name"]}</div>'
                f'<div class="ent-summary">{e["summary"] or "No summary available"}</div>'
                f'</div>'
            )
        st.markdown(f'<div class="ent-grid">{cards}</div>', unsafe_allow_html=True)
    else:
        st.markdown(
            '<div class="empty-state">'
            '<div class="empty-icon">\U0001f310</div>'
            '<div class="empty-title">Entity graph not loaded</div>'
            '<div class="empty-desc">Click the button above to extract and display entities from the knowledge graph</div>'
            '</div>',
            unsafe_allow_html=True,
        )

# ---- REPORT ---------------------------------------------------------------
with t4:
    st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

    # Summary
    st.markdown(
        f"""
        <div class="rpt">
            <div class="rpt-title"><span class="rpt-title-dot"></span>Incident Summary</div>
            <div class="rpt-kv"><span class="rpt-k">Incident ID</span><span class="rpt-v">{INCIDENT_ID}</span></div>
            <div class="rpt-kv"><span class="rpt-k">Severity</span><span class="rpt-v" style="color:var(--accent-red);">P1 Critical</span></div>
            <div class="rpt-kv"><span class="rpt-k">Service</span><span class="rpt-v">payment-api</span></div>
            <div class="rpt-kv"><span class="rpt-k">Commander</span><span class="rpt-v">Bob</span></div>
            <div class="rpt-kv"><span class="rpt-k">Duration</span><span class="rpt-v">{DUR}m &nbsp;(14:10 – 14:30 UTC)</span></div>
            <div class="rpt-kv"><span class="rpt-k">Status</span><span class="rpt-v" style="color:var(--accent-green);">Resolved</span></div>
            <div class="rpt-kv"><span class="rpt-k">Est. Revenue Impact</span><span class="rpt-v" style="color:var(--accent-amber);">~$46,800</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    rc1, rc2 = st.columns(2)

    with rc1:
        st.markdown(
            """
            <div class="rpt">
                <div class="rpt-title"><span class="rpt-title-dot"></span>Root Cause Analysis</div>
                <div style="color:var(--text-secondary);font-size:0.86rem;line-height:1.75;">
                    PR #482 reduced the <code>payment-api</code> rate-limiter threshold from
                    <strong style="color:var(--accent-green);">1,000</strong> to
                    <strong style="color:var(--accent-red);">100</strong> req/sec.
                    Production traffic exceeded the new limit, causing
                    <strong style="color:var(--text-primary);">42% HTTP 429</strong> errors
                    and <strong style="color:var(--accent-amber);">$2,340/min</strong> revenue loss.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            """
            <div class="rpt">
                <div class="rpt-title"><span class="rpt-title-dot"></span>Resolution</div>
                <div class="rpt-step">
                    <div class="rpt-step-num">1</div>
                    <div class="rpt-step-text">Bob identified misconfigured rate limiter via Datadog error-rate dashboard</div>
                </div>
                <div class="rpt-step">
                    <div class="rpt-step-num">2</div>
                    <div class="rpt-step-text">Alice pushed hotfix PR #483 reverting threshold to 1,000 req/sec</div>
                </div>
                <div class="rpt-step">
                    <div class="rpt-step-num">3</div>
                    <div class="rpt-step-text">v2.3.2 deployed to production at 14:27 UTC via rolling update</div>
                </div>
                <div class="rpt-step">
                    <div class="rpt-step-num" style="color:var(--accent-green);border-color:rgba(52,211,153,0.3);">&check;</div>
                    <div class="rpt-step-text">Error rate returned to 0.1% baseline by 14:29 UTC — recovery confirmed</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with rc2:
        st.markdown(
            """
            <div class="rpt">
                <div class="rpt-title"><span class="rpt-title-dot"></span>Personnel</div>
                <div class="rpt-person">
                    <div class="rpt-avatar" style="background:linear-gradient(135deg,#a78bfa,#818cf8);">A</div>
                    <div class="rpt-person-info"><div class="rpt-person-name">Alice</div><div class="rpt-person-role">Software Engineer</div></div>
                    <div class="rpt-person-action">Authored PR #482<br>Pushed hotfix #483</div>
                </div>
                <div class="rpt-person">
                    <div class="rpt-avatar" style="background:linear-gradient(135deg,#4f8ff7,#22d3ee);">B</div>
                    <div class="rpt-person-info"><div class="rpt-person-name">Bob</div><div class="rpt-person-role">Incident Commander</div></div>
                    <div class="rpt-person-action">Diagnosed root cause<br>Coordinated response</div>
                </div>
                <div class="rpt-person">
                    <div class="rpt-avatar" style="background:linear-gradient(135deg,#22d3ee,#34d399);">D</div>
                    <div class="rpt-person-info"><div class="rpt-person-name">Datadog</div><div class="rpt-person-role">Monitoring</div></div>
                    <div class="rpt-person-action">Detected spike<br>Confirmed recovery</div>
                </div>
                <div class="rpt-person">
                    <div class="rpt-avatar" style="background:linear-gradient(135deg,#f06060,#f0a030);">P</div>
                    <div class="rpt-person-info"><div class="rpt-person-name">PagerDuty</div><div class="rpt-person-role">Alerting</div></div>
                    <div class="rpt-person-action">Triggered P1 alert<br>Paged on-call</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            """
            <div class="rpt">
                <div class="rpt-title"><span class="rpt-title-dot"></span>Key Metrics</div>
                <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;">
                    <div class="rpt-stat"><div class="rpt-stat-val" style="color:var(--accent-red);">42%</div><div class="rpt-stat-label">Peak Error Rate</div></div>
                    <div class="rpt-stat"><div class="rpt-stat-val" style="color:var(--accent-amber);">$2.3K</div><div class="rpt-stat-label">Revenue Loss / min</div></div>
                    <div class="rpt-stat"><div class="rpt-stat-val" style="color:var(--accent-blue);">6m</div><div class="rpt-stat-label">Time to Detect</div></div>
                    <div class="rpt-stat"><div class="rpt-stat-val" style="color:var(--accent-green);">20m</div><div class="rpt-stat-label">Time to Resolve</div></div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    if st.button("Enrich Report with Graph Intelligence", type="primary"):
        with st.spinner("Querying knowledge graph..."):
            try:
                res = run_async(_search_graph("Summarize the complete incident including root cause, impact, and resolution"))
                if res:
                    items = "".join(
                        f'<div style="display:flex;gap:12px;margin-bottom:10px;">'
                        f'<span style="color:var(--accent-blue);font-size:1.1rem;line-height:1;flex-shrink:0;">&bull;</span>'
                        f'<span style="color:var(--text-secondary);font-size:0.86rem;line-height:1.55;">{e.fact}</span></div>'
                        for e in res
                    )
                    st.markdown(
                        f'<div class="rpt"><div class="rpt-title"><span class="rpt-title-dot"></span>Graph-Enriched Insights</div>{items}</div>',
                        unsafe_allow_html=True,
                    )
            except Exception as e:
                st.error(f"Enrichment failed: {e}")
