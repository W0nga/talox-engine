import streamlit as st
import pandas as pd
import requests
import re

# 1. TRANSMUTE INTERFACE TO PREMIUM OLED-DARK VIEW
st.set_page_config(
    page_title="TALOX Quant Engine",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Bespoke UI Injection Stylesheet to strip Streamlit defaults and enforce native-app aesthetic
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;700&display=swap');
    
    /* Core Layout Customizations */
    .stApp { background-color: #05070a; color: #e2e8f0; font-family: 'Plus Jakarta Sans', sans-serif; }
    [data-testid="block-container"] { padding: 1.5rem 1rem; }
    [data-testid="stHeader"], footer { display: none !important; } /* Hides Streamlit branding */
    
    /* Title Banner Customization */
    .talox-brand-header {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.7rem;
        font-weight: 700;
        background: linear-gradient(90deg, #00bfff, #00ffaa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -0.03em;
        margin-bottom: 2px;
    }
    
    /* Premium Frost Glass Cards */
    .talox-card {
        background: linear-gradient(135deg, #0e131f 0%, #0c101a 100%);
        border: 1px solid #1e293b;
        border-radius: 14px;
        padding: 16px;
        margin-bottom: 12px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
    }
    
    /* Neon KPIs */
    .kpi-container { display: flex; gap: 10px; margin-bottom: 16px; }
    .kpi-box {
        flex: 1;
        background: #090d16;
        border: 1px solid #1a2333;
        border-radius: 12px;
        padding: 12px;
        text-align: center;
    }
    .kpi-label { font-size: 0.75rem; color: #64748b; text-transform: uppercase; font-weight: 600; }
    .kpi-val { font-family: 'Space Grotesk', sans-serif; font-size: 1.3rem; font-weight: 700; color: #ffaa00; margin-top: 4px; }
    
    /* Portfolio Custom Slip Modules */
    .slip-wrapper {
        background: #0d1220;
        border-left: 4px solid #00bfff;
        border-top: 1px solid #1e293b;
        border-right: 1px solid #1e293b;
        border-bottom: 1px solid #1e293b;
        border-radius: 4px 14px 14px 4px;
        padding: 14px;
        margin-bottom: 10px;
    }
    .slip-top { display: flex; justify-content: space-between; align-items: center; }
    .slip-tag { font-size: 0.75rem; color: #94a3b8; font-weight: 600; text-transform: uppercase; }
    .slip-odds { font-family: 'Space Grotesk', sans-serif; background: rgba(0, 191, 255, 0.15); color: #00bfff; font-size: 0.9rem; font-weight: 700; padding: 2px 8px; border-radius: 6px; }
    .slip-amt { font-family: 'Space Grotesk', sans-serif; font-size: 1.4rem; font-weight: 700; color: #00ffaa; margin-top: 6px; }
    
    /* Live Tracker State Items */
    .live-status-bar {
        display: flex; justify-content: space-between; align-items: center;
        background: rgba(255, 68, 68, 0.08); border: 1px solid rgba(255, 68, 68, 0.2);
        border-radius: 10px; padding: 10px 14px; margin-bottom: 16px;
    }
    .pulse-dot { width: 8px; height: 8px; background-color: #ff4444; border-radius: 50%; display: inline-block; margin-right: 6px; animate: pulse 1.5s infinite; }
    .badge-pass { background: rgba(0, 255, 170, 0.12); color: #00ffaa; border: 1px solid rgba(0, 255, 170, 0.3); padding: 4px 10px; border-radius: 6px; font-size: 0.8rem; font-weight: 700; }
    .badge-fail { background: rgba(255, 68, 68, 0.12); color: #ff4444; border: 1px solid rgba(255, 68, 68, 0.3); padding: 4px 10px; border-radius: 6px; font-size: 0.8rem; font-weight: 700; }
    
    /* Custom Scenario Grid Row */
    .matrix-row {
        display: flex; justify-content: space-between; align-items: center;
        background: #0a0e17; border: 1px solid #141b29; border-radius: 8px;
        padding: 12px; margin-bottom: 8px;
    }
    .yield-green { color: #00ffaa; font-family: 'Space Grotesk', sans-serif; font-weight: 700; }
    .yield-red { color: #ff4444; font-family: 'Space Grotesk', sans-serif; font-weight: 700; }
    
    /* Streamlit Components Dark Adjustment overrides */
    div[data-testid="stExpander"] { background: #0e131f; border: 1px solid #1e293b; border-radius: 12px; }
    div[data-widget="stSelectbox"] { background-color: #0e131f; }
    input { background-color: #070a12 !important; color: #ffffff !important; border: 1px solid #1e293b !important; }
    </style>
""", unsafe_allow_html=True)

# 2. DATA PIPELINE: AGGREGATE BROAD GLOBAL FIXTURES (Solves Missing Match Issue)
@st.cache_data(ttl=30)
def pull_global_live_data():
    target_leagues = ["eng.1", "fifa.world", "uefa.euro", "global", "esp.1", "ita.1"]
    discovered_fixtures = []
    registered_ids = set()
    req_headers = {"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15"}
    
    for league_slug in target_leagues:
        try:
            endpoint = f"https://site.api.espn.com/apis/site/v2/sports/soccer/{league_slug}/scoreboard"
            api_response = requests.get(endpoint, headers=req_headers, timeout=4)
            if api_response.status_code == 200:
                events_list = api_response.json().get("events", [])
                for match_node in events_list:
                    unique_id = match_node.get("id")
                    if unique_id in registered_ids:
                        continue
                    
                    match_title = match_node.get("name")
                    status_block = match_node.get("status", {})
                    current_status = status_block.get("type", {}).get("description", "")
                    game_clock = status_block.get("displayClock", "")
                    
                    competition_node = match_node.get("competitions", [{}])[0]
                    teams_array = competition_node.get("competitors", [])
                    
                    home_team, away_team = "Team A", "Team B"
                    home_score, away_score = 0, 0
                    
                    if len(teams_array) >= 2:
                        home_team = teams_array[1].get("team", {}).get("displayName", "Team A")
                        away_team = teams_array[0].get("team", {}).get("displayName", "Team B")
                        home_score = int(teams_array[1].get("score", 0))
                        away_score = int(teams_array[0].get("score", 0))
                    
                    time_prefix = f"⏱️ ({game_clock})" if current_status == "In Progress" else f"[{current_status}]"
                    menu_string = f"{time_prefix} {home_team} {home_score} - {away_score} {away_team}"
                    
                    discovered_fixtures.append({
                        "id": unique_id,
                        "display": menu_string,
                        "t_a": home_team, "t_b": away_team,
                        "s_a": home_score, "s_b": away_score,
                        "status": current_status
                    })
                    registered_ids.add(unique_id)
        except Exception:
            continue
    return discovered_fixtures

# 3. HELPER FUNCTION: STAKE PDF TEXT COPIER REGEX PARSER
def run_stake_text_parser(user_blob):
    found_decimals = re.findall(r"\b\d+\.\d{2}\b", user_blob)
    return [float(val) for val in found_decimals]

# --- UI APP RENDER ENGINE ---
st.markdown('<div class="talox-brand-header">TALOX QUANT MANAGEMENT</div>', unsafe_allow_html=True)
st.markdown('<div style="font-size:0.8rem; color:#64748b; margin-bottom:14px;">PRO-TIER ALGORITHMIC SEED PORTFOLIOS</div>', unsafe_allow_html=True)

# EXPANDER CAPABILITY: PASTE DIRECTLY FROM STAKE
with st.expander("📋 Stake.com Data Import Parser", expanded=False):
    raw_pasted_text = st.text_area("Paste text copied from your Stake interface page:")
    scanned_odds_array = []
    if raw_pasted_text:
        scanned_odds_array = run_stake_text_parser(raw_pasted_text)
        if len(scanned_odds_array) >= 4:
            st.success(f"Successfully extracted odds grid: {scanned_odds_array[:4]}")

# RECOVERY API INGESTION NODE
live_match_feed = pull_global_live_data()

if live_match_feed:
    selected_match_record = st.selectbox("Active Stream Event Target", options=live_match_feed, format_func=lambda x: x["display"])
    team_a = selected_match_record["t_a"]
    team_b = selected_match_record["t_b"]
    score_a = selected_match_record["s_a"]
    score_b = selected_match_record["s_b"]
    live_state = selected_match_record["status"]
else:
    st.warning("Data feeds inactive. Using standard fallback baseline.")
    team_a, team_b = "England", "Argentina"
    score_a, score_b = 0, 0
    live_state = "Scheduled"

# REAL-TIME KPI SYSTEM DATA LAYOUT
st.markdown('<div class="kpi-container">', unsafe_allow_html=True)
st.markdown(f"""
    <div class="kpi-box"><div class="kpi-label">Active Event Target</div><div class="kpi-val" style="color:#00bfff; font-size:1rem;">{team_a} vs {team_b}</div></div>
    <div class="kpi-box"><div class="kpi-label">Live Standing Score</div><div class="kpi-val" style="color:#ffffff;">{score_a} - {score_b}</div></div>
""", unsafe_allow_html=True)

# PORTFOLIO CAPITAL DISTRIBUTIONS VARIABLES INPUT
col_cap, col_floor = st.columns(2)
with col_cap:
    bankroll_allocation = st.number_input("Portfolio Bankroll Base ($)", min_value=5.0, value=30.0)
with col_floor:
    protection_target = st.slider("Downside Protection Floor (%)", min_value=50, max_value=100, value=95) / 100.0

# EXTRACT INITIAL ODDS FROM CLIPBOARD PARSER VS STAKE PARMS PDF DEFAULT
odds_s1 = scanned_odds_array[1] if len(scanned_odds_array) > 1 else 3.00  # Draw
odds_s2 = scanned_odds_array[6] if len(scanned_odds_array) > 6 else 1.59  # Under 2.5
odds_s3 = scanned_odds_array[2] if len(scanned_odds_array) > 2 else 1.75  # Qualify A
odds_s4 = scanned_odds_array[3] if len(scanned_odds_array) > 3 else 2.04  # Qualify B

# RENDER PARAMETERS METRIC INPUT CARDS
st.markdown('<div class="talox-card">', unsafe_allow_html=True)
st.markdown('<div style="font-size:0.85rem; font-weight:700; color:#94a3b8; margin-bottom:10px;">ADJUST MARKET ODDS MATRIX VALUES</div>', unsafe_allow_html=True)
c_odds1, c_odds2 = st.columns(2)
with c_odds1:
    o1 = st.number_input("Slot 1: Match Draw Line", value=float(odds_s1), step=0.01)
    o3 = st.number_input(f"Slot 3: {team_a} Floor Line", value=float(odds_s3), step=0.01)
with c_odds2:
    o2 = st.number_input("Slot 2: Total Under 2.5 Line", value=float(odds_s2), step=0.01)
    o4 = st.number_input(f"Slot 4: {team_b} Floor Line", value=float(odds_s4), step=0.01)
st.markdown('</div>', unsafe_allow_html=True)

# 4. ROBUST QUANT RECOVERY ENGINE MATH FORMULAS
recovery_target_value = bankroll_allocation * protection_target

# Accurate inverse market distribution hedge mapping
stake3 = round(recovery_target_value / o3, 2)
stake4 = round(recovery_target_value / o4, 2)
leftover_capital = bankroll_allocation - stake3 - stake4

if leftover_capital > 0:
    # 40% / 60% high-yield asset loading splits
    stake1 = round(leftover_capital * 0.40, 2)
    stake2 = round(leftover_capital * 0.60, 2)
else:
    stake1, stake2 = 0.0, 0.0
    st.error("Hedge target configuration bounds exceed absolute bankroll base. Lower protection floor slider.")

# 5. REAL-TIME LIVE DATA RULE TRACKER TICKER STATE SHEET
st.subheader("📊 Real-Time Rule Execution Ticker")

is_live_match = live_state in ["In Progress", "First Half", "Second Half", "Halftime"]
live_label_tag = "LIVE INCIDENT ENGINE MONITORING" if is_live_match else f"STATUS STATE: {live_state.upper()}"

st.markdown(f"""
    <div class="live-status-bar">
        <div><span class="pulse-dot"></span><span style="font-size:0.8rem; font-weight:700; color:#ff4444;">{live_label_tag}</span></div>
        <div style="font-family:'Space Grotesk'; font-weight:700; font-size:1.1rem;">{team_a} {score_a} - {score_b} {team_b}</div>
    </div>
""", unsafe_allow_html=True)

calculated_goals = score_a + score_b
condition_draw_active = (score_a == score_b)
condition_under_active = (calculated_goals < 2.5)

# Render Checkbox Badges dynamically using clean custom CSS wrappers
c_badge1, c_badge2 = st.columns(2)
with c_badge1:
    badge_html = '<div class="badge-pass">🟢 DRAW ENVIRONMENT: SECURED</div>' if condition_draw_active else '<div class="badge-fail">🔴 DRAW ENVIRONMENT: BROKEN</div>'
    st.markdown(badge_html, unsafe_allow_html=True)
with c_badge2:
    badge_html = '<div class="badge-pass">🟢 TOTAL GOALS UNDER 2.5: SECURED</div>' if condition_under_active else '<div class="badge-fail">🔴 TOTAL GOALS UNDER 2.5: BROKEN</div>'
    st.markdown(badge_html, unsafe_allow_html=True)

# 6. PORTFOLIO ALLOCATION WAGER EXECUTION SLIPS
st.subheader("📋 Executable Optimization Slips")

def generate_slip_card(label, odd_val, final_wager):
    st.markdown(f"""
        <div class="slip-wrapper">
            <div class="slip-top">
                <span class="slip-tag">{label}</span>
                <span class="slip-odds">@{odd_val:.2f}</span>
            </div>
            <div class="slip-amt">${final_wager:.2f}</div>
        </div>
    """, unsafe_allow_html=True)

generate_slip_card("Slot 1 Core: Full-Time 1X2 Match Draw", o1, stake1)
generate_slip_card("Slot 2 Core: Asian Total Goals Under 2.5", o2, stake2)
generate_slip_card(f"Slot 3 Floor: {team_a} Outright Advance Risk Hedge", o3, stake3)
generate_slip_card(f"Slot 4 Floor: {team_b} Outright Advance Risk Hedge", o4, stake4)

# 7. HIGH-YIELD SCENARIO BALANCES RETURNS PREJECTIONS MATRIX
st.subheader("🎯 Realized Scenario Profit Projections Matrix")

net_target_win = round((stake1 * o1) + (stake2 * o2) - bankroll_allocation, 2)
net_defensive_safety = round((stake2 * o2) + (stake3 * o3) - bankroll_allocation, 2)
net_blowout_safety = round((stake4 * o4) - bankroll_allocation, 2)

def print_matrix_metric_row(scenario_name, value_net):
    row_class = "yield-green" if value_net >= 0 else "yield-red"
    prefix_sign = "+" if value_net >= 0 else ""
    st.markdown(f"""
        <div class="matrix-row">
            <span style="font-size:0.85rem; font-weight:600; color:#cbd5e1;">{scenario_name}</span>
            <span class="{row_class}">{prefix_sign}${value_net:.2f}</span>
        </div>
    """, unsafe_allow_html=True)

print_matrix_metric_row("🎯 Primary Target Achieved (Cagey Tactical Draw 0-0, 1-1)", net_target_win)
print_matrix_metric_row(f"🛡️ Defensive Protection Clear ({team_a} Edge Win 1-0, 2-0)", net_defensive_safety)
print_matrix_metric_row(f"⚠️ Outlier Disruption Floor Activated ({team_b} Heavy Blowout Outright)", net_blowout_safety)
