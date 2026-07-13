import streamlit as st
import pandas as pd
import requests
import re
import json

# 1. LUXURY DARK MODE WORKSPACE INITIALIZATION
st.set_page_config(
    page_title="TALOX | AI Portfolio Engine",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Deep Custom CSS Injection to mimic custom-branded UI and build clear financial blocks
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght=400;500;600;700&family=Space+Grotesk:wght=500;600;700&display=swap');
    
    /* Root App Resets */
    .stApp { background-color: #03060f; color: #f1f5f9; font-family: 'Plus Jakarta Sans', sans-serif; }
    [data-testid="block-container"] { padding: 1.2rem 1rem; }
    [data-testid="stHeader"], footer { display: none !important; }
    
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
    
    /* Interactive Betting Slip Visual Modules */
    .betting-slip-module { background: #050914; border-left: 4px solid #38bdf8; padding: 12px 16px; border-radius: 0 12px 12px 0; margin-bottom: 10px; display: flex; justify-content: space-between; align-items: center; border-top: 1px solid #1a263f; border-right: 1px solid #1a263f; border-bottom: 1px solid #1a263f; }
    .slip-text-main { font-size: 0.82rem; font-weight: 600; color: #cbd5e1; }
    .slip-text-sub { font-size: 0.65rem; color: #64748b; text-transform: uppercase; margin-top: 2px; }
    .slip-odds-badge { font-family: 'Space Grotesk', sans-serif; font-size: 0.82rem; font-weight: 700; color: #38bdf8; background: rgba(56, 189, 248, 0.1); padding: 3px 8px; border-radius: 5px; }
    .slip-stake-display { font-family: 'Space Grotesk', sans-serif; font-size: 1.15rem; font-weight: 700; color: #34d399; }
    .slip-stars { color: #fbbf24; font-size: 0.85rem; margin-top: 2px; }
    
    /* High Clarity Transparent Ledger Cards */
    .ledger-card { background: #091226; border: 1px solid #223254; border-radius: 12px; padding: 16px; margin-bottom: 14px; }
    .ledger-title-bar { font-size: 0.95rem; font-weight: 700; color: #ffffff; margin-bottom: 8px; display: flex; justify-content: space-between; align-items: center; }
    .ledger-pill-green { background: rgba(52, 211, 153, 0.12); color: #34d399; padding: 2px 8px; border-radius: 6px; font-size: 0.7rem; font-weight: 700; border: 1px solid rgba(52, 211, 153, 0.2); margin-right: 4px; }
    .ledger-pill-red { background: rgba(248, 113, 113, 0.08); color: #f87171; padding: 2px 8px; border-radius: 6px; font-size: 0.7rem; font-weight: 700; border: 1px solid rgba(248, 113, 113, 0.1); margin-right: 4px; }
    .ledger-row { display: flex; justify-content: space-between; padding: 6px 0; font-size: 0.85rem; border-bottom: 1px dashed #1c2a45; }
    .ledger-row:last-of-type { border-bottom: none; }
    
    /* Financial Numeric Colors */
    .color-wallet { font-family: 'Space Grotesk', sans-serif; color: #38bdf8; font-weight: 700; }
    .color-profit { font-family: 'Space Grotesk', sans-serif; color: #34d399; font-weight: 700; font-size: 1.1rem; }
    .color-loss { font-family: 'Space Grotesk', sans-serif; color: #f87171; font-weight: 700; font-size: 1.1rem; }
    
    /* Streamlit Framework Resets */
    div[data-testid="stExpander"] { background: #070c1a; border: 1px solid #18233c; border-radius: 12px; }
    .stTabs [data-baseweb="tab"] { color: #64748b; font-family: 'Space Grotesk', sans-serif; font-size: 0.85rem; }
    .stTabs [aria-selected="true"] { color: #38bdf8 !important; border-bottom-color: #38bdf8 !important; }
    input { background-color: #030611 !important; color: #ffffff !important; border: 1px solid #1e293b !important; }
    </style>
""", unsafe_allow_html=True)

# TOP LEVEL STATUS BRAND DECK
st.markdown("""
    <div class="talox-nav-deck">
        <div class="talox-title">TALOX QUANT DECK</div>
        <div class="talox-pill">ALGORITHMIC V3.5</div>
    </div>
""", unsafe_allow_html=True)

# 2. SEPARATED ASSET FIXTURE PIPELINES (Handles Current Scores and Custom Fixtures)
@st.cache_data(ttl=30)
def pull_active_sports_scoreboard():
    fixtures_list = []
    registered_keys = set()
    req_headers = {"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0)"}
    for league_id in ["eng.1", "fifa.world", "uefa.euro", "global", "esp.1"]:
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
                    s_home = int(competitors[1].get("score", 0))
                    s_away = int(competitors[0].get("score", 0))
                    fixtures_list.append({
                        "id": uid, "ta": t_home, "tb": t_away, "sa": s_home, "sb": s_away, "status": desc,
                        "label": f"⚽ [{desc}] {t_home} {s_home}-{s_away} {t_away}"
                    })
                    registered_keys.add(uid)
        except Exception: continue
    return fixtures_list

UPCOMING_MARQUEE_GAMES = [
    {"id": "mq_eng_arg", "label": "🏆 [WORLD CUP KNOCKOUT] England vs Argentina", "ta": "England", "tb": "Argentina", "sa": 0, "sb": 0, "status": "Scheduled"},
    {"id": "mq_fra_esp", "label": "🏆 [EURO CHAMPIONSHIP] France vs Spain", "ta": "France", "tb": "Spain", "sa": 0, "sb": 0, "status": "Scheduled"}
]

st.markdown('<div class="talox-workspace-card">', unsafe_allow_html=True)
st.markdown('<div class="talox-card-header">🎯 Target Environment Selection</div>', unsafe_allow_html=True)
tab_live, tab_marquee, tab_sandbox = st.tabs(["📡 Live Data Feeds", "🏆 Marquee Tournament Fixtures", "🛠️ Custom Manual Sandbox"])

team_a, team_b, score_a, score_b, match_status = "England", "Argentina", 0, 0, "Scheduled"

with tab_live:
    live_networks = pull_active_sports_scoreboard()
    if live_networks:
        selected_live = st.selectbox("Select Running Live Network Stream:", options=live_networks, format_func=lambda x: x["label"])
        team_a, team_b, score_a, score_b, match_status = selected_live["ta"], selected_live["tb"], selected_live["sa"], selected_live["sb"], selected_live["status"]
    else:
        st.info("No active fixtures indexed on data streams at this moment.")

with tab_marquee:
    selected_mq = st.selectbox("Select Marquee Target Block:", options=UPCOMING_MARQUEE_GAMES, format_func=lambda x: x["label"])
    if selected_mq:
        team_a, team_b, score_a, score_b, match_status = selected_mq["ta"], selected_mq["tb"], selected_mq["sa"], selected_mq["sb"], selected_mq["status"]

with tab_sandbox:
    manual_string = st.text_input("Enter Custom Alignment (Format: Team A vs Team B)", value="England vs Argentina")
    if "vs" in manual_string:
        parts = manual_string.split("vs")
        team_a, team_b = parts[0].strip(), parts[1].strip()
st.markdown('</div>', unsafe_allow_html=True)

# ADVANCED STAKE STRUCTURAL PARSER WITH CLIPBOARD AND TEXT INGESTION
parsed_draw = None
parsed_under_25 = None
parsed_qualify_a = None
parsed_qualify_b = None

with st.expander("📋 Stake.com Smart Document & Text Parser Deck", expanded=True):
    uploaded_text_file = st.file_uploader("Upload Market Log Ingestion Sheet (.txt format):", type=["txt"])
    raw_pasted_blob = st.text_area("Or paste raw event text overview straight from Stake interface below:", height=150)
    
    combined_ingestion_text = ""
    if uploaded_text_file is not None:
        combined_ingestion_text = uploaded_text_file.read().decode("utf-8")
    elif raw_pasted_blob:
        combined_ingestion_text = raw_pasted_blob
        
    if combined_ingestion_text:
        lines = [line.strip() for line in combined_ingestion_text.split("\n") if line.strip()]
        
        # Stateful Structural Parser Optimization
        for idx, text_line in enumerate(lines):
            # 1. Capture exact match for Draw line
            if text_line.lower() == "draw" and idx + 1 < len(lines):
                try: parsed_draw = float(lines[idx+1])
                except: pass
            
            # 2. Capture Exact Match for To Qualify Lines
            if "to qualify" in text_line.lower():
                # Scan next 4 lines for structural pairs
                for offset in range(1, 5):
                    if idx + offset < len(lines):
                        test_l = lines[idx + offset]
                        if team_a.lower() in test_l.lower() and idx + offset + 1 < len(lines):
                            try: parsed_qualify_a = float(lines[idx + offset + 1])
                            except: pass
                        if team_b.lower() in test_l.lower() and idx + offset + 1 < len(lines):
                            try: parsed_qualify_b = float(lines[idx + offset + 1])
                            except: pass

            # 3. Capture Asian Under 2.5 Market lines cleanly
            if text_line == "2.5" and idx + 1 < len(lines):
                try:
                    val_candidate = float(lines[idx+1])
                    # In stake layouts, Under is usually the second occurrence or paired with lower odds
                    if parsed_under_25 is None or val_candidate < parsed_under_25:
                        parsed_under_25 = val_candidate
                except: pass

        st.success("✅ Structural optimization pass completed. Values successfully extracted.")

# 3. CONTROL RISK PANEL PARAMETERS
st.markdown('<div class="talox-workspace-card">', unsafe_allow_html=True)
st.markdown('<div class="talox-card-header">⚙️ Portfolio Liquidity & Safeguard Rules</div>', unsafe_allow_html=True)
col_wallet, col_safeguard = st.columns(2)
with col_wallet:
    bankroll = st.number_input("Total Allocation Bankroll ($)", min_value=5.0, value=30.0, step=5.0)
with col_safeguard:
    protection_ratio = st.slider("Downside Capital Protection Floor (%)", min_value=10, max_value=100, value=90) / 100.0
st.markdown('</div>', unsafe_allow_html=True)

# MAP AND POPULATE INPUT VARIABLES WITH INTELLIGENT PARSER FALLBACKS
base_o1 = parsed_draw if parsed_draw is not None else 3.00
base_o2 = parsed_under_25 if parsed_under_25 is not None else 1.61
base_o3 = parsed_qualify_a if parsed_qualify_a is not None else 1.75
base_o4 = parsed_qualify_b if parsed_qualify_b is not None else 2.04

st.markdown('<div class="talox-workspace-card">', unsafe_allow_html=True)
st.markdown('<div class="talox-card-header">📈 Core Market Matrix Line Inputs</div>', unsafe_allow_html=True)
col_l1, col_l2 = st.columns(2)
with col_l1:
    o1 = st.number_input("Slot 1 Core: 90M Full-Time Draw Line", value=float(base_o1), step=0.01)
    o3 = st.number_input(f"Slot 3 Floor: {team_a} To Advance", value=float(base_o3), step=0.01)
with col_l2:
    o2 = st.number_input("Slot 2 Core: Asian Total Under 2.5 Line", value=float(base_o2), step=0.01)
    o4 = st.number_input(f"Slot 4 Floor: {team_b} To Advance", value=float(base_o4), step=0.01)
st.markdown('</div>', unsafe_allow_html=True)

# 4. BALANCED MATHEMATICAL ASSET RECOVERY CALCULATION LOOPS
target_hedged_recovery = bankroll * protection_ratio
stake3 = round(target_hedged_recovery / o3, 2)
stake4 = round(target_hedged_recovery / o4, 2)
remaining_working_capital = bankroll - stake3 - stake4

if remaining_working_capital > 0:
    stake1 = round(remaining_working_capital * 0.40, 2)
    stake2 = round(remaining_working_capital * 0.60, 2)
else:
    stake1 = round(bankroll * 0.15, 2)
    stake2 = round(bankroll * 0.25, 2)
    stake3 = round((bankroll * 0.35) / o3, 2)
    stake4 = round((bankroll * 0.25) / o4, 2)

# Dynamic Confidence Evaluation Generator Loop (Out of 5 Stars)
def calculate_lane_stars(odds, priority_tier):
    if odds >= 2.50 and priority_tier == "core": return "⭐⭐⭐⭐⭐"
    elif odds >= 1.80: return "⭐⭐⭐⭐"
    elif odds >= 1.50: return "⭐⭐⭐"
    return "⭐⭐"

# 5. EXECUTABLE ALLOCATION WORKING SLIPS VISUALIZER
st.subheader("📋 Executable Optimization Slips")
def print_executable_slip(title, market_label, odds, final_wager, star_rating):
    st.markdown(f"""
        <div class="betting-slip-module">
            <div>
                <div class="slip-text-main">{title}</div>
                <div class="slip-text-sub">{market_label}</div>
                <div class="slip-stars">{star_rating}</div>
            </div>
            <div style="display:flex; align-items:center; gap:14px;"><span class="slip-odds-badge">@{odds:.2f}</span><span class="slip-stake-display">${final_wager:.2f}</span></div>
        </div>
    """, unsafe_allow_html=True)

print_executable_slip("Slot 1 Core Allocation", "90 Minute Regular Time Full-Time Match Draw", o1, stake1, calculate_lane_stars(o1, "core"))
print_executable_slip("Slot 2 Core Allocation", "Asian Total Goals Volume Under 2.5 Line", o2, stake2, calculate_lane_stars(o2, "core"))
print_executable_slip("Slot 3 Floor Allocation", f"{team_a} Tournament Outright To Advance Hedge", o3, stake3, calculate_lane_stars(o3, "floor"))
print_executable_slip("Slot 4 Floor Allocation", f"{team_b} Tournament Outright To Advance Hedge", o4, stake4, calculate_lane_stars(o4, "floor"))

# 6. HIGH-CLARITY TRANSPARENT SCENARIO LEDGER MATRIX
st.subheader("🎯 Exploded Portfolio Scenario Return Ledger")
st.markdown("Review the complete financial breakdown below. **Total Return** is the gross cash sent back to your wallet (including stake), and **Net Profit** is your actual clear yield.")

def print_transparent_scenario_ledger(title, active_slots, dead_slots, total_wallet_payout):
    net_pure_profit = total_wallet_payout - bankroll
    profit_css = "color-profit" if net_pure_profit >= 0 else "color-loss"
    sign_prefix = "+" if net_pure_profit >= 0 else ""
    
    active_badges = "".join([f'<span class="ledger-pill-green">✅ Slot {s}</span>' for s in active_slots])
    dead_badges = "".join([f'<span class="ledger-pill-red">❌ Slot {s}</span>' for s in dead_slots])
    
    st.markdown(f"""
        <div class="ledger-card">
            <div class="ledger-title-bar"><div>{title}</div></div>
            <div style="margin-bottom:12px; display:flex; flex-wrap:wrap; gap:4px;">{active_badges}{dead_badges}</div>
            <div class="ledger-row"><span>Total Capital Risked (Original Stake):</span><span style="font-weight:600; color:#cbd5e1;">${bankroll:.2f}</span></div>
            <div class="ledger-row"><span>Total Cash Returned to Wallet (Payout):</span><span class="color-wallet">${total_wallet_payout:.2f}</span></div>
            <div class="ledger-row" style="border-top:1px dashed #223254; margin-top:4px; padding-top:8px;">
                <span style="font-weight:700; color:#ffffff;">Net Financial Positioning (Clear Profit/Loss):</span>
                <span class="{profit_css}">{sign_prefix}${net_pure_profit:.2f}</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

min_advancement_yield = min(stake3 * o3, stake4 * o4)
wallet_a = (stake1 * o1) + (stake2 * o2) + min_advancement_yield
wallet_b = (stake2 * o2) + (stake3 * o3)
wallet_c = (stake2 * o2) + (stake4 * o4)
wallet_d = (stake3 * o3)
wallet_e = (stake4 * o4)

print_transparent_scenario_ledger("🎯 Scenario A: Tactical Low Scoring Tie (0-0, 1-1 Regular Time)", [1, 2, "3 or 4"], [], wallet_a)
print_transparent_scenario_ledger(f"🛡️ Scenario B: Home Defensive Match Profile ({team_a} Wins 1-0, 2-0)", [2, 3], [1, 4], wallet_b)
print_transparent_scenario_ledger(f"🛡️ Scenario C: Away Defensive Match Profile ({team_b} Wins 0-1, 0-2)", [2, 4], [1, 3], wallet_c)
print_transparent_scenario_ledger(f"⚠️ Scenario D: Outlier High-Scoring Disruption ({team_a} Blowout 3-0+)", [3], [1, 2, 4], wallet_d)
print_transparent_scenario_ledger(f"⚠️ Scenario E: Outlier High-Scoring Disruption ({team_b} Blowout 0-3+)", [4], [1, 2, 3], wallet_e)

# 7. INTEGRATED HYPER-CONCISE GEMINI INTERFACE DECK
st.markdown("---")
st.subheader("🧠 Gemini Core Intelligence Matrix Hub")

with st.expander("🔑 AI Synthesis Configuration (Gemini Engine Integration)", expanded=False):
    ai_secret_key = st.text_input("Provide your Google Gemini API Key:", type="password")
    model_choice = st.selectbox(
        "Target Gemini Model:", 
        options=["gemini-2.5-flash", "gemini-3.5-flash", "gemini-3.1-flash-lite"]
    )

if not ai_secret_key:
    st.info("💡 Input your Gemini API key in the configuration deck component above to unlock real-time predictive rationales.")
else:
    if st.button("Generate Matrix AI Prediction Rationale"):
        with st.spinner("Processing scenario parameters through predictive modeling pathways..."):
            
            # STRICT WORD COUNT AND FORMAT CONSTRAINTS TO ENFORCE A SHORT BULLETPROOF BRIEFING
            synthesis_prompt = f"""
            You are TALOX AI. Write a brief, hyper-condensed risk brief for:
            {team_a} vs {team_b}. 
            Total Allocation Bankroll: ${bankroll}.
            Slot 1 (Draw): {o1}. Slot 2 (Under 2.5): {o2}. Slot 3 ({team_a} Qualify): {o3}. Slot 4 ({team_b} Qualify): {o4}.
            
            CRITICAL INSTRUCTION: Your entire response must be under 120 words total. Do not include intros, conversational pleasantries, or conclusions. Use 2-3 sentence bullets for:
            - **Tactical Rationale**: Why this allocation setup makes sense.
            - **Outlier Risk**: The main dangerous script to monitor.
            """
            
            try:
                endpoint_target = f"https://generativelanguage.googleapis.com/v1beta/models/{model_choice}:generateContent?key={ai_secret_key}"
                request_payload = {"contents": [{"parts": [{"text": synthesis_prompt}]}]}
                request_headers = {"Content-Type": "application/json"}
                
                api_response = requests.post(endpoint_target, data=json.dumps(request_payload), headers=request_headers, timeout=30)
                
                if api_response.status_code == 200:
                    ai_content = api_response.json()['candidates'][0]['content']['parts'][0]['text']
                    st.markdown(f"""
                        <div class="talox-workspace-card" style="border-color:#a855f7; background:#0c091a;">
                            <div class="talox-card-header" style="color:#c084fc;">🔮 Gemini Strategic Briefing ({model_choice})</div>
                            <div style="font-size:0.88rem; line-height:1.5; color:#cbd5e1;">{ai_content}</div>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.error(f"Gemini interface connectivity error. Server code: {api_response.status_code}")
            except requests.exceptions.Timeout:
                st.error("⏳ Server response latency threshold reached. Try selecting 'gemini-3.1-flash-lite' for faster generation.")
            except Exception as system_fault:
                st.error(f"AI Matrix configuration anomaly identified: {str(system_fault)}")
