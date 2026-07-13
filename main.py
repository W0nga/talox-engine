import streamlit as st
import pandas as pd
import requests
import re

# 1. ULTRALUX OLED-DARK GLOBAL VISUAL CONFIGURATION
st.set_page_config(
    page_title="TALOX | Quantum Engine",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom Style Sheet Injection to completely mask default Streamlit and build a premium native app UI
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');
    
    /* Global Workspace Layout */
    .stApp { background-color: #03070c; color: #f1f5f9; font-family: 'Plus Jakarta Sans', sans-serif; }
    [data-testid="block-container"] { padding: 1.2rem 1rem; }
    [data-testid="stHeader"], footer { display: none !important; }
    
    /* Top Brand Navigation Deck */
    .talox-nav {
        display: flex; justify-content: space-between; align-items: center;
        background: #090f1c; border: 1px solid #1e293b; border-radius: 12px;
        padding: 12px 16px; margin-bottom: 18px;
    }
    .talox-logo { font-family: 'Space Grotesk', sans-serif; font-size: 1.4rem; font-weight: 700; background: linear-gradient(90deg, #38bdf8, #34d399); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .talox-status { font-family: 'Space Grotesk', sans-serif; font-size: 0.75rem; color: #34d399; background: rgba(52, 211, 153, 0.1); padding: 4px 10px; border-radius: 20px; font-weight: bold; border: 1px solid rgba(52, 211, 153, 0.2); }
    
    /* Metric Display Blocks */
    .kpi-row { display: flex; gap: 10px; margin-bottom: 14px; }
    .kpi-card { flex: 1; background: #0b1324; border: 1px solid #1e293b; border-radius: 12px; padding: 14px; text-align: center; }
    .kpi-title { font-size: 0.7rem; color: #64748b; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; }
    .kpi-data { font-family: 'Space Grotesk', sans-serif; font-size: 1.2rem; font-weight: 700; color: #ffffff; margin-top: 4px; }
    
    /* Premium Premium UI Workspace Cards */
    .ui-panel { background: #070d1a; border: 1px solid #1a2436; border-radius: 14px; padding: 16px; margin-bottom: 14px; }
    .panel-header { font-family: 'Space Grotesk', sans-serif; font-size: 0.9rem; font-weight: 700; color: #38bdf8; text-transform: uppercase; letter-spacing: 0.03em; margin-bottom: 12px; border-bottom: 1px solid #1a2436; padding-bottom: 6px; }
    
    /* Clean Custom Verification Ticker Bar */
    .live-ticker { display: flex; justify-content: space-between; align-items: center; background: rgba(56, 189, 248, 0.04); border: 1px solid #1a2436; border-radius: 10px; padding: 10px 14px; margin-bottom: 14px; }
    .live-dot { width: 8px; height: 8px; background-color: #ef4444; border-radius: 50%; display: inline-block; margin-right: 6px; box-shadow: 0 0 8px #ef4444; }
    
    /* State Dynamic Rule Badges */
    .badge-ok { background: rgba(52, 211, 153, 0.1); color: #34d399; border: 1px solid rgba(52, 211, 153, 0.3); padding: 4px 10px; border-radius: 6px; font-size: 0.75rem; font-weight: 700; display: inline-block; }
    .badge-no { background: rgba(239, 68, 68, 0.1); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.3); padding: 4px 10px; border-radius: 6px; font-size: 0.75rem; font-weight: 700; display: inline-block; }
    
    /* Micro-engineered Interactive Execution Slips */
    .bet-slip { background: #09101f; border-left: 4px solid #38bdf8; border-top: 1px solid #1a2436; border-right: 1px solid #1a2436; border-bottom: 1px solid #1a2436; border-radius: 4px 12px 12px 4px; padding: 12px 16px; margin-bottom: 8px; display: flex; justify-content: space-between; align-items: center; }
    .bet-slip-hedge { border-left-color: #a855f7; }
    .slip-label { font-size: 0.8rem; font-weight: 600; color: #cbd5e1; }
    .slip-sub { font-size: 0.65rem; color: #64748b; text-transform: uppercase; margin-top: 2px; }
    .slip-odds { font-family: 'Space Grotesk', sans-serif; font-size: 0.85rem; font-weight: 700; color: #38bdf8; background: rgba(56, 189, 248, 0.1); padding: 2px 6px; border-radius: 4px; }
    .slip-odds-hedge { color: #c084fc; background: rgba(168, 85, 247, 0.1); }
    .slip-stake { font-family: 'Space Grotesk', sans-serif; font-size: 1.2rem; font-weight: 700; color: #34d399; }
    
    /* High Yield Yield Projection Matrix Rows */
    .matrix-container { background: #050a12; border: 1px solid #141b29; border-radius: 10px; padding: 4px; }
    .matrix-item { display: flex; justify-content: space-between; padding: 10px 12px; border-bottom: 1px solid #141b29; align-items: center; }
    .matrix-item:last-child { border-bottom: none; }
    .matrix-win { font-family: 'Space Grotesk', sans-serif; font-weight: 700; color: #34d399; font-size: 1.05rem; }
    .matrix-loss { font-family: 'Space Grotesk', sans-serif; font-weight: 700; color: #f87171; font-size: 1.05rem; }
    
    /* Streamlit Interactive Input Controls Masking Styles */
    div[data-testid="stExpander"] { background: #070d1a; border: 1px solid #1a2436; border-radius: 12px; }
    .stSelectbox div[data-baseweb="select"] { background-color: #0b1324 !important; border: 1px solid #1e293b !important; border-radius: 8px !important; color: white !important; }
    div[data-testid="stMarkdownContainer"] p { margin-bottom: 0px; }
    input { background-color: #040812 !important; color: #ffffff !important; border: 1px solid #1e293b !important; border-radius: 6px !important; }
    </style>
""", unsafe_allow_html=True)

# 2. BRAND NAVIGATION BAR DECK CONTAINER
st.markdown("""
    <div class="talox-nav">
        <div class="talox-logo">TALOX CORE v3.0</div>
        <div class="talox-status">MATRIX ONLINE</div>
    </div>
""", unsafe_allow_html=True)

# 3. ADVANCED SEPARATED FIXTURES ENGINE (Fixes Dropdown & Handles England/Marquee Future Games)
@st.cache_data(ttl=30)
def pull_live_scoreboard_pool():
    discovered = []
    seen = set()
    headers = {"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15"}
    for lg in ["eng.1", "fifa.world", "uefa.euro", "global"]:
        try:
            res = requests.get(f"https://site.api.espn.com/apis/site/v2/sports/soccer/{lg}/scoreboard", headers=headers, timeout=3)
            if res.status_code == 200:
                for ev in res.json().get("events", []):
                    i_d = ev.get("id")
                    if i_d in seen: continue
                    title = ev.get("name")
                    st_desc = ev.get("status", {}).get("type", {}).get("description", "")
                    comps = ev.get("competitions", [{}])[0]
                    teams = comps.get("competitors", [])
                    if len(teams) >= 2:
                        ta = teams[1].get("team", {}).get("displayName", "Team A")
                        tb = teams[0].get("team", {}).get("displayName", "Team B")
                        sa = int(teams[1].get("score", 0))
                        sb = int(teams[0].get("score", 0))
                        discovered.append({"id": i_d, "label": f"⏱️ [{st_desc}] {ta} {sa}-{sb} {tb}", "ta": ta, "tb": tb, "sa": sa, "sb": sb, "status": st_desc})
                        seen.add(i_d)
        except Exception: continue
    return discovered

# HARDCODED UPCOMING FUTURE EVENTS DATA DICTIONARY (Solves the Future England Game Problem)
FUTURE_MARQUEE_POOL = [
    {"id": "mq_eng_arg", "label": "🏆 [FUTURE MARQUEE] England vs Argentina (World Cup Final Setup)", "ta": "England", "tb": "Argentina", "sa": 0, "sb": 0, "status": "Scheduled"},
    {"id": "mq_fra_esp", "label": "🏆 [FUTURE MARQUEE] France vs Spain (UEFA Championship Block)", "ta": "France", "tb": "Spain", "sa": 0, "sb": 0, "status": "Scheduled"},
    {"id": "mq_bra_ger", "label": "🏆 [FUTURE MARQUEE] Brazil vs Germany (International Friendly Slate)", "ta": "Brazil", "tb": "Germany", "sa": 0, "sb": 0, "status": "Scheduled"}
]

# DISPLAY SEPARATED INTERACTIVE TABS TO SEGREGATE SPORT CONTEXTS
st.markdown('<div class="ui-panel">', unsafe_allow_html=True)
st.markdown('<div class="panel-header">🎯 Select Match Target Environment</div>', unsafe_allow_html=True)

tab_live, tab_marquee, tab_manual = st.tabs(["📡 Live Scoreboard", "🏆 Marquee Future Fixtures", "🛠️ Custom Sandbox"])

team_a, team_b, score_a, score_b, current_match_status = "England", "Argentina", 0, 0, "Scheduled"

with tab_live:
    live_pool = pull_live_scoreboard_pool()
    if live_pool:
        chosen_live = st.selectbox("Select Active Live Event Data Stream", options=live_pool, format_func=lambda x: x["label"], key="live_sel")
        team_a, team_b, score_a, score_b, current_match_status = chosen_live["ta"], chosen_live["tb"], chosen_live["sa"], chosen_live["sb"], chosen_live["status"]
    else:
        st.info("No active live events detected on scoreboard networks right now.")

with tab_marquee:
    chosen_mq = st.selectbox("Select Upcoming Elite Target Matches", options=FUTURE_MARQUEE_POOL, format_func=lambda x: x["label"], key="mq_sel")
    if chosen_mq and not st.session_state.get("live_sel"):
        team_a, team_b, score_a, score_b, current_match_status = chosen_mq["ta"], chosen_mq["tb"], chosen_mq["sa"], chosen_mq["sb"], chosen_mq["status"]
    elif chosen_mq:
        # Override if user explicitly interacts with the marquee tab dropdown
        team_a, team_b, score_a, score_b, current_match_status = chosen_mq["ta"], chosen_mq["tb"], chosen_mq["sa"], chosen_mq["sb"], chosen_mq["status"]

with tab_manual:
    m_input = st.text_input("Type Custom Match Config (Format: Team A vs Team B)", value="England vs Argentina")
    if "vs" in m_input:
        splits = m_input.split("vs")
        team_a, team_b = splits[0].strip(), splits[1].strip()

st.markdown('</div>', unsafe_allow_html=True)

# CLIPBOARD IMPORTER UTILITY CARD CONTAINER
with st.expander("📋 Stake.com Smart Paste Clipboard Parser", expanded=False):
    paste_blob = st.text_area("Paste text copied straight from your Stake event sheet:")
    extracted_odds_list = []
    if paste_blob:
        extracted_odds_list = [float(x) for x in re.findall(r"\b\d+\.\d{2}\b", paste_blob)]
        if len(extracted_odds_list) >= 4:
            st.success(f"Parsed array matching layout fields: {extracted_odds_list[:4]}")

# 4. PORTFOLIO BASE INPUT METRIC BLOCKS
st.markdown('<div class="ui-panel">', unsafe_allow_html=True)
st.markdown('<div class="panel-header">⚙️ Portfolio Liquidity Control Parameters</div>', unsafe_allow_html=True)
col_bank, col_floor_slider = st.columns(2)
with col_bank:
    bankroll = st.number_input("Total Allocation Capital ($)", min_value=5.0, value=30.0, step=5.0)
with col_floor_slider:
    # Changed slider lower limit option boundaries to reflect optimal matrix spaces
    protection_ratio = st.slider("Hedge Downside Floor Safeguard (%)", min_value=10, max_value=100, value=90) / 100.0
st.markdown('</div>', unsafe_allow_html=True)

# MAP THE ODDS ACCORDING TO STAKE VALUES FROM PDF
fallback_o1 = extracted_odds_list[1] if len(extracted_odds_list) > 1 else 3.00  # Draw Line
fallback_o2 = extracted_odds_list[6] if len(extracted_odds_list) > 6 else 1.59  # Under 2.5 Line
fallback_o3 = extracted_odds_list[2] if len(extracted_odds_list) > 2 else 1.75  # Qualify A Line
fallback_o4 = extracted_odds_list[3] if len(extracted_odds_list) > 3 else 2.04  # Qualify B Line

st.markdown('<div class="ui-panel">', unsafe_allow_html=True)
st.markdown('<div class="panel-header">📈 Live Market Matrix Odds Feed</div>', unsafe_allow_html=True)
c_lines1, c_lines2 = st.columns(2)
with c_lines1:
    o1 = st.number_input("Slot 1 Core: 90' Match Draw Line", value=float(fallback_o1), step=0.01)
    o3 = st.number_input(f"Slot 3 Floor: {team_a} To Advance", value=float(fallback_o3), step=0.01)
with c_lines2:
    o2 = st.number_input("Slot 2 Core: Asian Total Under 2.5", value=float(fallback_o2), step=0.01)
    o4 = st.number_input(f"Slot 4 Floor: {team_b} To Advance", value=float(fallback_o4), step=0.01)
st.markdown('</div>', unsafe_allow_html=True)

# 5. HIGH-YIELD REAL-TIME BALANCED MATRIX MATH CONFIGURATION ENGINE
# To prevent the hedges from absorbing 100% of capital, calculate conditional balance allocations
target_recovery = bankroll * protection_ratio

# Hedges are conditional: only ONE team can advance out of a tournament fixture! 
# Therefore, Stake 3 and 4 do not run concurrently in loss parameters. 
# They are allocated out of the available pool to cover the loss of core slots if a knockout occurs in regular time.
stake3 = round(target_recovery / o3, 2)
stake4 = round(target_recovery / o4, 2)

# Calculate true required overhead matrix limits safely
remaining_working_capital = bankroll - stake3 - stake4

if remaining_working_capital > 0:
    # 40/60 distribution profile configuration split to maximize direct draw outcomes
    stake1 = round(remaining_working_capital * 0.40, 2)
    stake2 = round(remaining_working_capital * 0.60, 2)
else:
    # Auto-balancing sub-routine if user selects an over-constrained safety parameter
    st.warning("⚠️ High Protection Floor has locked up standard asset lines. Switching to Auto-Balance Mode...")
    stake1 = round(bankroll * 0.15, 2)
    stake2 = round(bankroll * 0.25, 2)
    stake3 = round((bankroll * 0.35) / o3, 2)
    stake4 = round((bankroll * 0.25) / o4, 2)

# 6. INCIDENT LIVE STATUS TRACKER DISPLAY ENGINE
st.markdown(f"""
    <div class="live-ticker">
        <div><span class="live-dot"></span><span style="font-size:0.75rem; font-weight:700; color:#ef4444; letter-spacing:0.05em;">ENGINE MONITORING: {current_match_status.upper()}</span></div>
        <div style="font-family:'Space Grotesk'; font-weight:700; font-size:1rem; color:#ffffff;">{team_a} {score_a} - {score_b} {team_b}</div>
    </div>
""", unsafe_allow_html=True)

goals_sum = score_a + score_b
draw_active = (score_a == score_b)
under_active = (goals_sum < 2.5)

col_check1, col_check2 = st.columns(2)
with col_check1:
    html_b = '<div class="badge-ok">🟢 90M DRAW ENVIRONMENT: VALID</div>' if draw_active else '<div class="badge-no">🔴 90M DRAW ENVIRONMENT: BROKEN</div>'
    st.markdown(html_b, unsafe_allow_html=True)
with col_check2:
    html_b = '<div class="badge-ok">🟢 ASIAN TOTAL UNDER 2.5: VALID</div>' if under_active else '<div class="badge-no">🔴 ASIAN TOTAL UNDER 2.5: BROKEN</div>'
    st.markdown(html_b, unsafe_allow_html=True)

# 7. EXECUTABLE HIGH-END SLIP LAYOUT MODULES
st.subheader("📋 Executable Portfolio Allocation Slips")

def print_slip(title, odds, stake, is_hedge=False):
    h_class = "bet-slip-hedge" if is_hedge else ""
    o_class = "slip-odds-hedge" if is_hedge else ""
    sub_label = "DOWNSTREAM PROTECTION FLOOR" if is_hedge else "CORE HIGH YIELD ENGINE TARGET"
    st.markdown(f"""
        <div class="bet-slip {h_class}">
            <div>
                <div class="slip-label">{title}</div>
                <div class="slip-sub">{sub_label}</div>
            </div>
            <div style="text-align: right; display: flex; align-items: center; gap: 14px;">
                <span class="slip-odds {o_class}">@{odds:.2f}</span>
                <span class="slip-stake">${stake:.2f}</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

print_slip("Slot 1: Full-Time 1X2 Match Draw", o1, stake1)
print_slip("Slot 2: Asian Total Goals Under 2.5", o2, stake2)
print_slip(f"Slot 3: {team_a} Outright Advance Overload", o3, stake3, is_hedge=True)
print_slip(f"Slot 4: {team_b} Outright Advance Overload", o4, stake4, is_hedge=True)

# 8. THE CORRECT REAL-TIME HIGH-YIELD STACKED SCENARIO RETURN MATRIX
st.subheader("🎯 Realized Scenario Profit Projections Matrix")

# MATH BREAKDOWN FOR INTERACTIVE STACKED RETURNS:
# Scenario 1 (Cagey Draw): Slot 1 hits + Slot 2 hits + EITHER Team A or Team B must qualify eventually!
# We calculate the minimum guaranteed stacked return assuming the lower-odds team advances.
min_qualify_payout = min(stake3 * o3, stake4 * o4)
p_cagey_draw = round((stake1 * o1) + (stake2 * o2) + min_qualify_payout - bankroll, 2)

# Scenario 2 (Defensive Win): Team A wins 1-0 or 2-0. Slot 2 hits (Under) + Slot 3 hits (Team A Qualifies).
p_defensive_win = round((stake2 * o2) + (stake3 * o3) - bankroll, 2)

# Scenario 3 (Outlier Breakout Deviation): Team B blows them out 3-0. Slots 1, 2, 3 lose. Slot 4 hits (Team B Qualifies).
p_outlier_blowout = round((stake4 * o4) - bankroll, 2)

st.markdown('<div class="matrix-container">', unsafe_allow_html=True)

def print_matrix_line(name, profit):
    style = "matrix-win" if profit >= 0 else "matrix-loss"
    sign = "+" if profit >= 0 else ""
    st.markdown(f"""
        <div class="matrix-item">
            <span style="font-size:0.85rem; font-weight:600; color:#cbd5e1;">{name}</span>
            <span class="{style}">{sign}${profit:.2f}</span>
        </div>
    """, unsafe_allow_html=True)

print_matrix_line("🎯 Primary Script Target Met (Tactical Tie 0-0, 1-1 Match Stacking)", p_cagey_draw)
print_matrix_line(f"🛡️ Defensive Script Met ({team_a} Under-Win 1-0, 2-0 Combined Payout)", p_defensive_win)
print_matrix_line("⚠️ Outlier Script Deviation (Heavy One-Sided Breakout Scenario)", p_outlier_blowout)

st.markdown('</div>', unsafe_allow_html=True)
