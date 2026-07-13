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
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');
    
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

# PRE-INDEXED FALLBACK SLATE FOR UPCOMING TOURNAMENT GAMES
UPCOMING_MARQUEE_GAMES = [
    {"id": "mq_eng_arg", "label": "🏆 [WORLD CUP KNOCKOUT] England vs Argentina (Elite Stage)", "ta": "England", "tb": "Argentina", "sa": 0, "sb": 0, "status": "Scheduled"},
    {"id": "mq_fra_esp", "label": "🏆 [EURO CHAMPIONSHIP] France vs Spain (Finals Slate)", "ta": "France", "tb": "Spain", "sa": 0, "sb": 0, "status": "Scheduled"}
]

# RENDER SEPARATED TAB MODULES FOR CLEAN SPORT SEPARATION
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

# STAKE PARSER SELECTION MODES
with st.expander("📋 Stake.com Smart Paste Clipboard Parser", expanded=False):
    raw_pasted_blob = st.text_area("Paste event overview raw text straight from Stake:")
    scanned_odds = []
    if raw_pasted_blob:
        scanned_odds = [float(val) for val in re.findall(r"\b\d+\.\d{2}\b", raw_pasted_blob)]
        if len(scanned_odds) >= 4: st.success(f"Parsed array matching layout slots: {scanned_odds[:4]}")

# 3. CONTROL RISK PANEL PARAMETERS
st.markdown('<div class="talox-workspace-card">', unsafe_allow_html=True)
st.markdown('<div class="talox-card-header">⚙️ Portfolio Liquidity & Safeguard Rules</div>', unsafe_allow_html=True)
col_wallet, col_safeguard = st.columns(2)
with col_wallet:
    bankroll = st.number_input("Total Allocation Bankroll ($)", min_value=5.0, value=30.0, step=5.0)
with col_safeguard:
    protection_ratio = st.slider("Downside Capital Protection Floor (%)", min_value=10, max_value=100, value=90) / 100.0
st.markdown('</div>', unsafe_allow_html=True)

# MAP AND POPULATE INPUT VARIABLES
base_o1 = scanned_odds[1] if len(scanned_odds) > 1 else 3.00   # 90M Full-Time Draw Line
base_o2 = scanned_odds[6] if len(scanned_odds) > 6 else 1.59   # Total Under 2.5 Line
base_o3 = scanned_odds[2] if len(scanned_odds) > 2 else 1.75   # Team A To Advance Line
base_o4 = scanned_odds[3] if len(scanned_odds) > 3 else 2.04   # Team B To Advance Line

st.markdown('<div class="talox-workspace-card">', unsafe_allow_html=True)
st.markdown('<div class="talox-card-header">📈 Core Market Matrix Line Inputs</div>', unsafe_allow_html=True)
col_l1, col_l2 = st.columns(2)
with col_l1:
    o1 = st.number_input("Slot 1 Core: 90M Full-Time Draw", value=float(base_o1), step=0.01)
    o3 = st.number_input(f"Slot 3 Floor: {team_a} To Advance", value=float(base_o3), step=0.01)
with col_l2:
    o2 = st.number_input("Slot 2 Core: Asian Total Under 2.5", value=float(base_o2), step=0.01)
    o4 = st.number_input(f"Slot 4 Floor: {team_b} To Advance", value=float(base_o4), step=0.01)
st.markdown('</div>', unsafe_allow_html=True)

# 4. BALANCED MATHEMATICAL ASSET RECOVERY CALCULATION LOOPS
target_hedged_recovery = bankroll * protection_ratio

# Hedges track separately because tournament rules dictate only ONE team can advance!
stake3 = round(target_hedged_recovery / o3, 2)
stake4 = round(target_hedged_recovery / o4, 2)
remaining_working_capital = bankroll - stake3 - stake4

if remaining_working_capital > 0:
    stake1 = round(remaining_working_capital * 0.40, 2)
    stake2 = round(remaining_working_capital * 0.60, 2)
else:
    # Auto-Balance Safety sub-routine to keep active lanes open
    stake1 = round(bankroll * 0.15, 2)
    stake2 = round(bankroll * 0.25, 2)
    stake3 = round((bankroll * 0.35) / o3, 2)
    stake4 = round((bankroll * 0.25) / o4, 2)

# 5. EXECUTABLE ALLOCATION WORKING SLIPS VISUALIZER
st.subheader("📋 Executable Optimization Slips")
def print_executable_slip(title, market_label, odds, final_wager):
    st.markdown(f"""
        <div class="betting-slip-module">
            <div><div class="slip-text-main">{title}</div><div class="slip-text-sub">{market_label}</div></div>
            <div style="display:flex; align-items:center; gap:14px;"><span class="slip-odds-badge">@{odds:.2f}</span><span class="slip-stake-display">${final_wager:.2f}</span></div>
        </div>
    """, unsafe_allow_html=True)

print_executable_slip("Slot 1 Core Allocation", "90 Minute Regular Time Full-Time Match Draw", o1, stake1)
print_executable_slip("Slot 2 Core Allocation", "Asian Total Goals Volume Under 2.5 Line", o2, stake2)
print_executable_slip("Slot 3 Floor Allocation", f"{team_a} Tournament Outright To Advance Hedge", o3, stake3)
print_executable_slip("Slot 4 Floor Allocation", f"{team_b} Tournament Outright To Advance Hedge", o4, stake4)

# 6. HIGH-CLARITY TRANSPARENT SCENARIO LEDGER MATRIX (Solves Confusion)
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

# ACCURATE MULTI-BET STACKED MATHEMATICAL VALUES
# Scenario A (Low Scoring Draw 0-0, 1-1): Slot 1 and Slot 2 cash. 
# In tournament play, either Team A or Team B must also advance. The matrix tracks using the minimum line to establish an absolute safety baseline.
min_advancement_yield = min(stake3 * o3, stake4 * o4)
wallet_a = (stake1 * o1) + (stake2 * o2) + min_advancement_yield

# Scenario B (Home Defensive Under-Win 1-0, 2-0): Slot 2 and Slot 3 cash.
wallet_b = (stake2 * o2) + (stake3 * o3)

# Scenario C (Away Defensive Under-Win 0-1, 0-2): Slot 2 and Slot 4 cash.
wallet_c = (stake2 * o2) + (stake4 * o4)

# Scenario D (Home Outlier Blast 3-0, 3-1): Only Slot 3 cashes.
wallet_d = (stake3 * o3)

# Scenario E (Away Outlier Blast 0-3, 1-3): Only Slot 4 cashes.
wallet_e = (stake4 * o4)

print_transparent_scenario_ledger("🎯 Scenario A: Tactical Low Scoring Tie (0-0, 1-1 Regular Time)", [1, 2, "3 or 4"], [], wallet_a)
print_transparent_scenario_ledger(f"🛡️ Scenario B: Home Defensive Match Profile ({team_a} Wins 1-0, 2-0)", [2, 3], [1, 4], wallet_b)
print_transparent_scenario_ledger(f"🛡️ Scenario C: Away Defensive Match Profile ({team_b} Wins 0-1, 0-2)", [2, 4], [1, 3], wallet_c)
print_transparent_scenario_ledger(f"⚠️ Scenario D: Outlier High-Scoring Disruption ({team_a} Blowout 3-0+)", [3], [1, 2, 4], wallet_d)
print_transparent_scenario_ledger(f"⚠️ Scenario E: Outlier High-Scoring Disruption ({team_b} Blowout 0-3+)", [4], [1, 2, 3], wallet_e)

# 7. INTEGRATED EXPERT GEMINI COGNITIVE INTERFACE DECK
st.markdown("---")
st.subheader("🧠 Gemini Core Intelligence Matrix Hub")

# CONFIGURATION INGESTION MODES VIA SIDEBAR / APP OVERLAYS
with st.expander("🔑 AI Synthesis Configuration (Gemini Engine Integration)", expanded=False):
    ai_secret_key = st.text_input("Provide your Google Gemini API Key:", type="password")
    confidence_bias = st.slider("Target Model Confidence Threshold (%)", min_value=10, max_value=100, value=85)

if not ai_secret_key:
    st.info("💡 Input your Gemini API key in the configuration deck component above to unlock real-time predictive rationales.")
else:
    if st.button("Generate Matrix AI Prediction Rationale"):
        with st.spinner("Processing scenario parameters through predictive modeling pathways..."):
            
            # Construct a clean analytical prompt mapping matrix statistics
            synthesis_prompt = f"""
            You are TALOX AI, an expert quantitative sports risk analyst.
            Synthesize a risk profile overview based on these active market parameters:
            - Fixture Context: {team_a} vs {team_b} (Current Status: {match_status})
            - Target Base Bankroll: ${bankroll}
            - Slot 1 Odds (Draw): {o1} (Allocation Stake: ${stake1})
            - Slot 2 Odds (Under 2.5): {o2} (Allocation Stake: ${stake2})
            - Slot 3 Odds ({team_a} Advance): {o3} (Allocation Stake: ${stake3})
            - Slot 4 Odds ({team_b} Advance): {o4} (Allocation Stake: ${stake4})
            
            Format your final response cleanly with these explicit Markdown sections:
            1. **Predictive Core Rationale**: Break down the structural logic behind allocating capital into these exact defensive lines.
            2. **Confidence Metric Evaluation**: Detail the model confidence parameters based on market distributions.
            3. **Risk Profile Variance**: Identify outlier game scripts that require active monitoring.
            
            Keep your analysis highly professional, precise, and objective. Avoid generic introductory text.
            """
            
            try:
                # Direct HTTP Request payload mapping to the Google Gemini AI Studio endpoint
                endpoint_target = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={ai_secret_key}"
                request_payload = {"contents": [{"parts": [{"text": synthesis_prompt}]}]}
                request_headers = {"Content-Type": "application/json"}
                
                api_response = requests.post(endpoint_target, data=json.dumps(request_payload), headers=request_headers, timeout=12)
                
                if api_response.status_code == 200:
                    ai_content = api_response.json()['candidates'][0]['content']['parts'][0]['text']
                    st.markdown(f"""
                        <div class="talox-workspace-card" style="border-color:#a855f7; background:#0c091a;">
                            <div class="talox-card-header" style="color:#c084fc;">🔮 Gemini Real-Time Synthesis Deck</div>
                            <div style="font-size:0.88rem; line-height:1.6; color:#cbd5e1;">{ai_content}</div>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.error(f"Gemini interface connectivity error. Server code: {api_response.status_code}")
            except Exception as system_fault:
                st.error(f"AI Matrix configuration anomaly identified: {str(system_fault)}")
