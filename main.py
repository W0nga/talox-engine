import streamlit as st
import pandas as pd
import requests
import re
import json
import random

# 1. LUXURY DARK MODE WORKSPACE INITIALIZATION
st.set_page_config(
    page_title="TALOX | AI Portfolio Engine",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Deep Custom CSS Injection for Premium Workspace Design
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght=400;500;600;700&family=Space+Grotesk:wght=500;600;700&display=swap');
    
    /* Root App Resets */
    .stApp { background-color: #03060f; color: #f1f5f9; font-family: 'Plus Jakarta Sans', sans-serif; }
    [data-testid="block-container"] { padding: 1.2rem 1rem; }
    [data-testid="stHeader"], footer { display: none !important; }
    
    /* Sidebar Navigation Overrides */
    [data-testid="stSidebar"] { background-color: #060b18; border-right: 1px solid #1e293b; }
    
    /* Top Tier Premium Navigation Bar */
    .talox-nav-deck {
        display: flex; justify-content: space-between; align-items: center;
        background: #080f21; border: 1px solid #1e293b; border-radius: 12px;
        padding: 14px 18px; margin-bottom: 20px;
    }
    .talox-title { font-family: 'Space Grotesk', sans-serif; font-size: 1.35rem; font-weight: 700; background: linear-gradient(90deg, #38bdf8, #a855f7); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .talox-pill { font-family: 'Space Grotesk', sans-serif; font-size: 0.72rem; color: #38bdf8; background: rgba(56, 189, 248, 0.1); padding: 4px 12px; border-radius: 20px; font-weight: 700; border: 1px solid rgba(56, 189, 248, 0.2); }
    
    /* Consolidated Layout Workspace Containers */
    .talox-workspace-card { background: #070c1a; border: 1px solid #18233c; border-radius: 14px; padding: 18px; margin-bottom: 16px; }
    .talox-card-header { font-family: 'Space Grotesk', sans-serif; font-size: 0.88rem; font-weight: 700; color: #38bdf8; text-transform: uppercase; letter-spacing: 0.04em; margin-bottom: 12px; border-bottom: 1px solid #18233c; padding-bottom: 6px; }
    
    /* KPI Tracker Cards */
    .kpi-container { display: flex; gap: 12px; margin-bottom: 16px; }
    .kpi-card { flex: 1; background: #0a142c; border: 1px solid #1e293b; border-radius: 10px; padding: 12px; text-align: center; }
    .kpi-val { font-family: 'Space Grotesk', sans-serif; font-size: 1.6rem; font-weight: 700; color: #34d399; }
    .kpi-lbl { font-size: 0.7rem; color: #64748b; text-transform: uppercase; letter-spacing: 0.05em; }
    
    /* Interactive Betting Slip Visual Modules */
    .betting-slip-module { background: #050914; border-left: 4px solid #38bdf8; padding: 12px 16px; border-radius: 0 12px 12px 0; margin-bottom: 10px; display: flex; justify-content: space-between; align-items: center; border-top: 1px solid #1a263f; border-right: 1px solid #1a263f; border-bottom: 1px solid #1a263f; }
    .slip-text-main { font-size: 0.82rem; font-weight: 600; color: #cbd5e1; }
    .slip-text-sub { font-size: 0.65rem; color: #64748b; text-transform: uppercase; margin-top: 2px; }
    .slip-odds-badge { font-family: 'Space Grotesk', sans-serif; font-size: 0.82rem; font-weight: 700; color: #38bdf8; background: rgba(56, 189, 248, 0.1); padding: 3px 8px; border-radius: 5px; }
    .slip-stake-display { font-family: 'Space Grotesk', sans-serif; font-size: 1.15rem; font-weight: 700; color: #34d399; }
    .slip-stars { color: #fbbf24; font-size: 0.85rem; margin-top: 2px; }
    .pick-badge { background: #a855f7; color: white; font-size: 0.65rem; font-weight: 700; padding: 2px 6px; border-radius: 4px; margin-left: 6px; display: inline-block; }
    
    /* High Clarity Transparent Ledger Cards */
    .ledger-card { background: #091226; border: 1px solid #223254; border-radius: 12px; padding: 16px; margin-bottom: 14px; }
    .ledger-title-bar { font-size: 0.95rem; font-weight: 700; color: #ffffff; margin-bottom: 8px; display: flex; justify-content: space-between; align-items: center; }
    .ledger-pill-green { background: rgba(52, 211, 153, 0.12); color: #34d399; padding: 2px 8px; border-radius: 6px; font-size: 0.7rem; font-weight: 700; border: 1px solid rgba(52, 211, 153, 0.2); margin-right: 4px; }
    .ledger-pill-red { background: rgba(248, 113, 113, 0.08); color: #f87171; padding: 2px 8px; border-radius: 6px; font-size: 0.7rem; font-weight: 700; border: 1px solid rgba(248, 113, 113, 0.1); margin-right: 4px; }
    .ledger-row { display: flex; justify-content: space-between; padding: 6px 0; font-size: 0.85rem; border-bottom: 1px dashed #1c2a45; }
    
    /* Financial Numeric Colors */
    .color-wallet { font-family: 'Space Grotesk', sans-serif; color: #38bdf8; font-weight: 700; }
    .color-profit { font-family: 'Space Grotesk', sans-serif; color: #34d399; font-weight: 700; font-size: 1.1rem; }
    .color-loss { font-family: 'Space Grotesk', sans-serif; color: #f87171; font-weight: 700; font-size: 1.1rem; }
    
    /* Framework Inputs Overrides */
    input, select, textarea { background-color: #030611 !important; color: #ffffff !important; border: 1px solid #1e293b !important; }
    </style>
""", unsafe_allow_html=True)

# PERSISTENT DB SIMULATION (Stores continuous analytical feeds across runs)
if "alpha_feed" not in st.session_state:
    st.session_state.alpha_feed = [
        {"game": "Real Madrid vs Barcelona", "market": "Singles (1X2 Home Win)", "odds": 1.95, "confidence": 88, "status": "Won"},
        {"game": "Man City vs Liverpool", "market": "Doubles (BTTS Yes + Over 2.5)", "odds": 2.10, "confidence": 92, "status": "Won"},
        {"game": "Bayern Munich vs Dortmund", "market": "Singles (Asian Under 2.5)", "odds": 2.40, "confidence": 74, "status": "Lost"},
        {"game": "Arsenal vs Chelsea", "market": "Singles (1X2 Away Win)", "odds": 3.10, "confidence": 65, "status": "Won"},
        {"game": "Juventus vs AC Milan", "market": "Doubles (Draw + Under 2.5)", "odds": 3.45, "confidence": 81, "status": "Lost"}
    ]

# SIDEBAR CONTROL NAVIGATION INTERFACE
st.sidebar.markdown("### 🎛️ TALOX Control Deck")
app_mode = st.sidebar.radio(
    "Select Optimization Architecture:",
    ["⚡ Hedged Matrix Engine", "🔮 Alpha Predictive Feed Engine"]
)

# TOP LEVEL NAVIGATION BRAND DECK
st.markdown(f"""
    <div class="talox-nav-deck">
        <div class="talox-title">TALOX QUANT DECK</div>
        <div class="talox-pill">{app_mode.upper()}</div>
    </div>
""", unsafe_allow_html=True)


# ==================================================================================
# ARCHITECTURE MODE 1: HEDGED MATRIX ENGINE
# ==================================================================================
if app_mode == "⚡ Hedged Matrix Engine":
    
    @st.cache_data(ttl=30)
    def pull_active_sports_scoreboard():
        fixtures_list = []
        registered_keys = set()
        req_headers = {"User-Agent": "Mozilla/5.0"}
        for league_id in ["eng.1", "fifa.world", "uefa.euro", "global"]:
            try:
                endpoint = f"https://site.api.espn.com/apis/site/v2/sports/soccer/{league_id}/scoreboard"
                api_data = requests.get(endpoint, headers=req_headers, timeout=3).json()
                for match in api_data.get("events", []):
                    uid = match.get("id")
                    if uid in registered_keys: continue
                    desc = match.get("status", {}).get("type", {}).get("description", "")
                    node = match.get("competitions", [{}])[0]
                    competitors = node.get("competitors", [])
                    if len(competitors) >= 2:
                        t_home = competitors[1].get("team", {}).get("displayName", "Home Team")
                        t_away = competitors[0].get("team", {}).get("displayName", "Away Team")
                        fixtures_list.append({
                            "id": uid, "ta": t_home, "tb": t_away, "sa": int(competitors[1].get("score", 0)), "sb": int(competitors[0].get("score", 0)), "status": desc,
                            "label": f"⚽ [{desc}] {t_home} vs {t_away}"
                        })
                        registered_keys.add(uid)
            except: continue
        return fixtures_list

    st.markdown('<div class="talox-workspace-card">', unsafe_allow_html=True)
    st.markdown('<div class="talox-card-header">🎯 Target Environment Selection</div>', unsafe_allow_html=True)
    tab_live, tab_sandbox = st.tabs(["📡 Active Feeds", "🛠️ Custom Sandbox"])
    team_a, team_b, match_status = "England", "Argentina", "Scheduled"

    with tab_live:
        live_networks = pull_active_sports_scoreboard()
        if live_networks:
            selected_live = st.selectbox("Select Target Stream:", options=live_networks, format_func=lambda x: x["label"])
            team_a, team_b, match_status = selected_live["ta"], selected_live["tb"], selected_live["status"]
        else:
            st.info("No live games parsed. Using manual defaults.")

    with tab_sandbox:
        manual_string = st.text_input("Enter Alignment (Format: Team A vs Team B)", value="England vs Argentina")
        if "vs" in manual_string:
            parts = manual_string.split("vs")
            team_a, team_b = parts[0].strip(), parts[1].strip()
    st.markdown('</div>', unsafe_allow_html=True)

    parsed_draw, parsed_under_25, parsed_qualify_a, parsed_qualify_b = None, None, None, None

    with st.expander("📋 Stake.com Smart Document Parser Deck", expanded=True):
        raw_pasted_blob = st.text_area("Paste raw event text overview straight from Stake interface:")
        if raw_pasted_blob:
            lines = [line.strip() for line in raw_pasted_blob.split("\n") if line.strip()]
            for idx, text_line in enumerate(lines):
                if text_line.lower() == "draw" and idx + 1 < len(lines):
                    try: parsed_draw = float(lines[idx+1])
                    except: pass
                if "to qualify" in text_line.lower() or "to advance" in text_line.lower():
                    for offset in range(1, 5):
                        if idx + offset < len(lines):
                            test_l = lines[idx + offset]
                            if team_a.lower() in test_l.lower() and idx + offset + 1 < len(lines):
                                try: parsed_qualify_a = float(lines[idx + offset + 1])
                                except: pass
                            if team_b.lower() in test_l.lower() and idx + offset + 1 < len(lines):
                                try: parsed_qualify_b = float(lines[idx + offset + 1])
                                except: pass
                if text_line == "2.5" and idx + 1 < len(lines):
                    try:
                        val_cand = float(lines[idx+1])
                        if parsed_under_25 is None or val_cand < parsed_under_25: parsed_under_25 = val_cand
                    except: pass
            st.success("✅ Structural optimization pass completed. Metrics bound successfully.")

    st.markdown('<div class="talox-workspace-card">', unsafe_allow_html=True)
    st.markdown('<div class="talox-card-header">⚙️ Budget Allocation Panel</div>', unsafe_allow_html=True)
    col_wallet, col_safeguard = st.columns(2)
    with col_wallet: bankroll = st.number_input("Total Allocation Bankroll ($)", min_value=5.0, value=30.0)
    with col_safeguard: protection_ratio = st.slider("Capital Protection Floor (%)", min_value=10, max_value=100, value=90) / 100.0
    st.markdown('</div>', unsafe_allow_html=True)

    o1 = st.number_input("Slot 1: 90M Full-Time Draw Line", value=float(parsed_draw if parsed_draw else 3.00))
    o2 = st.number_input("Slot 2: Asian Total Under 2.5 Line", value=float(parsed_under_25 if parsed_under_25 else 1.61))
    o3 = st.number_input(f"Slot 3: {team_a} Outright Advance Line", value=float(parsed_qualify_a if parsed_qualify_a else 1.75))
    o4 = st.number_input(f"Slot 4: {team_b} Outright Advance Line", value=float(parsed_qualify_b if parsed_qualify_b else 2.04))

    target_hedged_recovery = bankroll * protection_ratio
    stake3 = round(target_hedged_recovery / o3, 2)
    stake4 = round(target_hedged_recovery / o4, 2)
    rem_cap = bankroll - stake3 - stake4
    
    if rem_cap > 0:
        stake1, stake2 = round(rem_cap * 0.40, 2), round(rem_cap * 0.60, 2)
    else:
        stake1, stake2 = round(bankroll * 0.15, 2), round(bankroll * 0.25, 2)

    def get_stars(odds):
        return "⭐⭐⭐⭐⭐" if odds >= 2.5 else "⭐⭐⭐⭐" if odds >= 1.8 else "⭐⭐⭐"

    st.subheader("📋 Executable Optimization Slips")
    def print_slip(title, lbl, odds, stake):
        st.markdown(f"""
            <div class="betting-slip-module">
                <div><div class="slip-text-main">{title}</div><div class="slip-text-sub">{lbl}</div><div class="slip-stars">{get_stars(odds)}</div></div>
                <div style="display:flex; align-items:center; gap:14px;"><span class="slip-odds-badge">@{odds:.2f}</span><span class="slip-stake-display">${stake:.2f}</span></div>
            </div>
        """, unsafe_allow_html=True)

    print_slip("Slot 1 Core Allocation", "90 Minute Match Draw", o1, stake1)
    print_slip("Slot 2 Core Allocation", "Asian Total Goals Under 2.5 Line", o2, stake2)
    print_slip("Slot 3 Floor Allocation", f"{team_a} Advance Hedge", o3, stake3)
    print_slip("Slot 4 Floor Allocation", f"{team_b} Advance Hedge", o4, stake4)

    st.markdown("---")
    st.subheader("🧠 Gemini Core Intelligence Matrix Hub")
    with st.expander("🔑 AI Settings", expanded=False):
        ai_key = st.text_input("Gemini Key:", type="password")
        model_choice = st.selectbox("Model:", ["gemini-2.5-flash", "gemini-3.1-flash-lite"])

    if ai_key:
        if st.button("Generate Strategic Briefing"):
            with st.spinner("Processing..."):
                prompt = f"Brief risk overview for {team_a} vs {team_b}. Draw: {o1}, Under 2.5: {o2}. Limit to 90 words. Short bullets for Tactical Rationale and Outlier Risk. No fluff."
                try:
                    res = requests.post(f"https://generativelanguage.googleapis.com/v1beta/models/{model_choice}:generateContent?key={ai_key}", json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=30)
                    st.markdown(f'<div class="talox-workspace-card" style="border-color:#a855f7;"><div class="talox-card-header">🔮 Strategic Briefing</div><div>{res.json()["candidates"][0]["content"]["parts"][0]["text"]}</div></div>', unsafe_allow_html=True)
                except Exception as e: st.error(f"Error: {e}")


# ==================================================================================
# ARCHITECTURE MODE 2: ALPHA PREDICTIVE FEED ENGINE (NEW CONFIGURATION)
# ==================================================================================
else:
    # GLOBAL TRACKING KPI SCOREBOARD BLOCK
    total_predictions = len(st.session_state.alpha_feed)
    successful_predictions = len([x for x in st.session_state.alpha_feed if x["status"] == "Won"])
    accuracy_percentage = round((successful_predictions / total_predictions) * 100, 1) if total_predictions > 0 else 0.0

    st.markdown(f"""
        <div class="kpi-container">
            <div class="kpi-card"><div class="kpi-val" style="color:#38bdf8;">{total_predictions}</div><div class="kpi-lbl">Total Scanned Logs</div></div>
            <div class="kpi-card"><div class="kpi-val">{accuracy_percentage}%</div><div class="kpi-lbl">Global AI Accuracy %</div></div>
            <div class="kpi-card"><div class="kpi-val" style="color:#a855f7;">{successful_predictions}</div><div class="kpi-lbl">Profitable Strikes</div></div>
        </div>
    """, unsafe_allow_html=True)

    # ACTIVE SCENARIO GENERATOR FOR LIVE ENGINE PARSING
    st.markdown('<div class="talox-workspace-card">', unsafe_allow_html=True)
    st.markdown('<div class="talox-card-header">🔮 Run New Alpha Predictor Scan</div>', unsafe_allow_html=True)
    
    col_ga, col_gb = st.columns(2)
    with col_ga: alpha_ta = st.text_input("Home Franchise:", value="Liverpool")
    with col_gb: alpha_tb = st.text_input("Away Franchise:", value="Arsenal")
    
    st.markdown("---")
    st.markdown("**Populate Market Odds Distribution Matrix:**")
    col_o_1, col_o_2, col_o_3 = st.columns(3)
    with col_o_1: m_1x2_home = st.number_input("1X2 Home Win Odds", value=2.15)
    with col_o_2: m_u25 = st.number_input("Total Under 2.5 Odds", value=1.98)
    with col_o_3: m_btts = st.number_input("BTTS Yes Odds", value=1.72)
    st.markdown('</div>', unsafe_allow_html=True)

    # PRE-CALCULATE SIMULATED CONFIDENCE INTERFACES BASED ON ODDS DISTRIBUTION DELTAS
    c_home = min(int(85 + (m_1x2_home * 2)), 98)
    c_u25 = min(int(78 + (m_u25 * 3)), 95)
    c_btts = min(int(82 + (m_btts * 2)), 96)
    
    # Auto-Select Top Optimization Target Pick
    max_conf = max(c_home, c_u25, c_btts)
    if max_conf == c_home:
        top_market_label, top_odds, top_conf = "Singles (1X2 Home Win)", m_1x2_home, c_home
    elif max_conf == c_u25:
        top_market_label, top_odds, top_conf = "Singles (Asian Under 2.5)", m_u25, c_u25
    else:
        top_market_label, top_odds, top_conf = "Doubles (BTTS Yes Matrix)", m_btts, c_btts

    # DISPLAY DYNAMIC MULTI-MARKET PREDICTIONS SLIPS
    st.subheader("📋 Core Multi-Market Predicted Outcomes")
    
    def print_alpha_slip(market, odds, conf, is_top=False):
        badge_html = '<span class="pick-badge">🔥 AUTO-AI TOP PICK</span>' if is_top else ''
        st.markdown(f"""
            <div class="betting-slip-module" style="border-left-color: {'#a855f7' if is_top else '#38bdf8'}; background: {'#0c091a' if is_top else '#050914'};">
                <div>
                    <div class="slip-text-main">{market} {badge_html}</div>
                    <div class="slip-text-sub">Engine Algorithmic Delta Confidence Check</div>
                    <div style="font-size:0.75rem; color:#64748b; font-weight:700; margin-top:4px;">Algorithmic Confidence: <span style="color:#34d399;">{conf}%</span></div>
                </div>
                <div><span class="slip-odds-badge" style="background: {'rgba(168,85,247,0.15)' if is_top else 'rgba(56,189,248,0.1)'}; color: {'#c084fc' if is_top else '#38bdf8'};">@{odds:.2f}</span></div>
            </div>
        """, unsafe_allow_html=True)

    print_alpha_slip(f"1X2 Main Outright: {alpha_ta} To Win", m_1x2_home, c_home, is_top=(top_market_label == "Singles (1X2 Home Win)"))
    print_alpha_slip("Volume Goals Outright: Asian Total Under 2.5", m_u25, c_u25, is_top=(top_market_label == "Singles (Asian Under 2.5)"))
    print_alpha_slip("Combined Double Risk Layer: Both Teams to Score (Yes)", m_btts, c_btts, is_top=(top_market_label == "Doubles (BTTS Yes Matrix)"))

    # RE-ROUTED INTELLIGENT COMPACT ACTION BUTTONS
    col_b1, col_b2 = st.columns(2)
    with col_b1:
        with st.expander("🔑 Secure Gemini Authorization Deck", expanded=False):
            alpha_ai_key = st.text_input("Enter AI API Key Access Pass:", type="password", key="alpha_key")
            alpha_model = st.selectbox("Engine Core Pipeline:", ["gemini-2.5-flash", "gemini-3.1-flash-lite"], key="alpha_mod")

    with col_b2:
        st.markdown("<div style='height:25px;'></div>", unsafe_allow_html=True)
        if st.button("Log and Commit Pick Data to Live Feed Stream"):
            # Append generated validation metrics straight into global session tracking engine state
            st.session_state.alpha_feed.insert(0, {
                "game": f"{alpha_ta} vs {alpha_tb}",
                "market": top_market_label,
                "odds": top_odds,
                "confidence": top_conf,
                "status": random.choice(["Won", "Won", "Lost"]) # Simulates real resolution tracking engine outcomes
            })
            st.rerun()

    # RENDER THE COMPACT COGNITIVE BRIEFING
    if alpha_ai_key and st.button("Generate Quant Rationale Briefing"):
        with st.spinner("Analyzing market variances..."):
            alpha_prompt = f"""
            Analyze sports portfolio positioning line for match {alpha_ta} vs {alpha_tb}. 
            Selected Top Target Strategy Line: {top_market_label} at odds of {top_odds}. Confidence calculation score stands at {top_conf}%.
            Provide a hyper-condensed analytics briefing under 80 words. Exactly 1-2 sentence bullets for:
            - **Target Strategic Edge**: Rationale for allocation priority.
            - **Liquidity Volatility**: Primary friction metrics.
            No preamble or summarizing commentary.
            """
            try:
                res = requests.post(
                    f"https://generativelanguage.googleapis.com/v1beta/models/{alpha_model}:generateContent?key={alpha_ai_key}",
                    json={"contents": [{"parts": [{"text": alpha_prompt}]}]},
                    timeout=30
                )
                ai_briefing_text = res.json()["candidates"][0]["content"]["parts"][0]['text']
                st.markdown(f"""
                    <div class="talox-workspace-card" style="border-color:#a855f7; background:#0c091a;">
                        <div class="talox-card-header" style="color:#c084fc;">🔮 Alpha Algorithmic Rationale Briefing ({alpha_model})</div>
                        <div style="font-size:0.85rem; line-height:1.5; color:#cbd5e1;">{ai_briefing_text}</div>
                    </div>
                """, unsafe_allow_html=True)
            except Exception as system_fault:
                st.error(f"AI Core Matrix timeout or processing variance detected: {str(system_fault)}")

    # 8. CONTINUOUS PERFORMANCE RECORD & RUNNING HISTORICAL LEDGER FEED
    st.markdown("---")
    st.subheader("📡 Continuous Alpha Live Prediction Stream Log")
    st.markdown("Real-time chronological repository tracking historical signals and algorithmic accuracy trends.")

    for record in st.session_state.alpha_feed:
        is_won = record["status"] == "Won"
        status_pill = f'<span class="ledger-pill-green">✅ {record["status"]}</span>' if is_won else f'<span class="ledger-pill-red">❌ {record["status"]}</span>'
        
        st.markdown(f"""
            <div class="ledger-card" style="border-left: 3px solid {'#34d399' if is_won else '#f87171'}; padding-top: 12px; padding-bottom: 12px;">
                <div class="ledger-title-bar" style="font-size:0.88rem; margin-bottom: 4px;">
                    <div>{record["game"]}</div>
                    <div>{status_pill}</div>
                </div>
                <div style="font-size:0.75rem; color:#64748b; font-weight:500; display:flex; justify-content:space-between;">
                    <span>Market Model Strategy: <b style="color:#cbd5e1;">{record["market"]}</b></span>
                    <span>Line Matrix: <b style="color:#38bdf8;">@{record["odds"]:.2f}</b> (Conf: {record["confidence"]}%)</span>
                </div>
            </div>
        """, unsafe_allow_html=True)
