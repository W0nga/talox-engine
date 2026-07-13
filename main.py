import streamlit as st
import pandas as pd
import requests
import re

# 1. PREMIUM NEON-DARK SYSTEM DESIGN (TALOX CONFIGURATION)
st.set_page_config(
    page_title="TALOX | Quantitative Dashboard",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom premium styling framework to completely mask standard Streamlit blocks
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=JetBrains+Mono:wght@500;700&display=swap');
    
    /* Global Overrides */
    .stApp { background-color: #0d1117; color: #c9d1d9; font-family: 'Inter', sans-serif; }
    h1, h2, h3 { color: #f0f6fc !important; font-weight: 700 !important; letter-spacing: -0.02em; }
    
    /* Metric Card Styling */
    .talox-metric-box {
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0,0,0,0.2);
    }
    .metric-val-green { color: #238636; font-size: 2rem; font-family: 'JetBrains Mono', monospace; font-weight: 700; }
    
    /* Betting Slip Cards */
    .slip-container {
        background: #161b22;
        border-left: 4px solid #1f6feb;
        border-top: 1px solid #30363d;
        border-right: 1px solid #30363d;
        border-bottom: 1px solid #30363d;
        border-radius: 0px 12px 12px 0px;
        padding: 16px;
        margin-bottom: 14px;
    }
    .slip-header { font-size: 0.85rem; color: #8b949e; text-transform: uppercase; font-weight: 600; letter-spacing: 0.05em; }
    .slip-odds { float: right; background: #388bfd26; color: #58a6ff; padding: 2px 8px; border-radius: 6px; font-family: 'JetBrains Mono', monospace; font-weight: bold; }
    .slip-stake { font-size: 1.3rem; color: #56d364; font-family: 'JetBrains Mono', monospace; font-weight: 700; margin-top: 6px; }
    
    /* Live Status Badges */
    .badge-live { background: #da363326; color: #f85149; border: 1px solid #f85149; padding: 2px 8px; border-radius: 20px; font-size: 0.75rem; font-weight: bold; }
    .badge-ft { background: #21262d; color: #8b949e; border: 1px solid #30363d; padding: 2px 8px; border-radius: 20px; font-size: 0.75rem; font-weight: bold; }
    .badge-condition { background: #23863626; color: #56d364; border: 1px solid #238636; padding: 4px 10px; border-radius: 6px; font-size: 0.85rem; font-weight: 600; display: inline-block; margin: 4px 2px; }
    .badge-broken { background: #da363326; color: #f85149; border: 1px solid #da3633; padding: 4px 10px; border-radius: 6px; font-size: 0.85rem; font-weight: 600; display: inline-block; margin: 4px 2px; }
    
    /* Matrix Table */
    .matrix-row { display: flex; justify-content: space-between; padding: 12px; border-bottom: 1px solid #21262d; align-items: center; }
    .matrix-win { color: #56d364; font-family: 'JetBrains Mono', monospace; font-weight: 700; }
    .matrix-loss { color: #f85149; font-family: 'JetBrains Mono', monospace; font-weight: 700; }
    </style>
""", unsafe_allow_html=True)

# 2. DYNAMIC BROAD ENDPOINT AGGREGATOR (Resolves Missing Games Issue)
@st.cache_data(ttl=60)
def aggregate_global_fixtures():
    # Queries multiple major football endpoints simultaneously to catch all primary matches
    leagues = ["eng.1", "fifa.world", "uefa.euro", "global", "esp.1", "ita.1"]
    aggregated_games = []
    seen_ids = set()
    
    headers = {"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15"}
    
    for lg in leagues:
        try:
            url = f"https://site.api.espn.com/apis/site/v2/sports/soccer/{lg}/scoreboard"
            res = requests.get(url, headers=headers, timeout=5)
            if res.status_code == 200:
                events = res.json().get("events", [])
                for e in events:
                    match_id = e.get("id")
                    if match_id in seen_ids:
                        continue
                    
                    match_name = e.get("name")
                    status_node = e.get("status", {})
                    status_desc = status_node.get("type", {}).get("description", "")
                    period = status_node.get("period", 0)
                    display_clock = status_node.get("displayClock", "")
                    
                    # Score Processing Nodes
                    competitions = e.get("competitions", [{}])
                    competitors = competitions[0].get("competitors", [])
                    
                    t1_name, t2_name = "Team A", "Team B"
                    t1_score, t2_score = 0, 0
                    
                    if len(competitors) >= 2:
                        # ESPN ordered listing mapping (Away Team usually index 0, Home index 1)
                        t1_name = competitors[1].get("team", {}).get("displayName", "Team A")
                        t2_name = competitors[0].get("team", {}).get("displayName", "Team B")
                        t1_score = int(competitors[1].get("score", 0))
                        t2_score = int(competitors[0].get("score", 0))
                    
                    # Create clean display string for mobile dropdown menu
                    time_label = f"({display_clock})" if period > 0 and status_desc != "Final" else f"[{status_desc}]"
                    display_line = f"{time_label} {t1_name} {t1_score} - {t2_score} {t2_name}"
                    
                    aggregated_games.append({
                        "id": match_id,
                        "display": display_line,
                        "team_a": t1_name,
                        "team_b": t2_name,
                        "score_a": t1_score,
                        "score_b": t2_score,
                        "status": status_desc
                    })
                    seen_ids.add(match_id)
        except Exception:
            continue
            
    return aggregated_games

# 3. HELPER FUNCTION: STAKE TEXT CLIPBOARD PARSER
def parse_stake_clipboard(text):
    """ Parses out raw odds arrays when pasting blocks direct from Stake.com """
    odds_found = re.findall(r"\b\d+\.\d{2}\b", text)
    extracted = [float(o) for o in odds_found]
    return extracted

# --- RENDER MAIN INTERFACE ---
st.title("⚡ TALOX QUANT ENGINE")
st.caption("Active Production Matrix Framework | Real-Time Liquidity Systems")

# STAKE CLIPBOARD PARSER CONTAINER
with st.expander("📋 Fast Import: Paste Data from Stake.com", expanded=False):
    paste_data = st.text_area("Paste text copied from Stake match page here:")
    parsed_odds = []
    if paste_data:
        parsed_odds = parse_stake_clipboard(paste_data)
        if len(parsed_odds) >= 4:
            st.success(f"Found active matrix odds in text: {parsed_odds[:4]}")
        else:
            st.info(f"Scanning text... Detected values: {parsed_odds}")

# FETCH DATA PIPELINE
live_pool = aggregate_global_fixtures()

st.subheader("🏁 Live Match Environment")
if live_pool:
    selected_obj = st.selectbox("Select Active Match Target Feed", options=live_pool, format_func=lambda x: x["display"])
    team_a = selected_obj["team_a"]
    team_b = selected_obj["team_b"]
    score_a = selected_obj["score_a"]
    score_b = selected_obj["score_b"]
    match_status = selected_obj["status"]
else:
    st.warning("No active league fixtures fetched. Utilizing default testing workspace.")
    team_a, team_b = "England", "Argentina"
    score_a, score_b = 0, 0
    match_status = "Scheduled"

# PORTFOLIO CAPITAL ASSIGNMENTS
col_b, col_f = st.columns(2)
with col_b:
    bankroll = st.number_input("Portfolio Allocation Base ($)", min_value=5.0, value=30.0, step=1.0)
with col_f:
    risk_floor = st.slider("Downside Floor Protection Target (%)", min_value=50, max_value=100, value=90) / 100.0

# ASSIGN INITIAL INPUT VALS FROM PARSER OR FALLBACK DEFAULTS
def_o1 = parsed_odds[1] if len(parsed_odds) > 1 else 3.00 # Draw
def_o2 = parsed_odds[6] if len(parsed_odds) > 6 else 1.59 # Under 2.5
def_o3 = parsed_odds[2] if len(parsed_odds) > 2 else 1.75 # Qualify A
def_o4 = parsed_odds[3] if len(parsed_odds) > 3 else 2.04 # Qualify B

st.subheader("📈 Adjusted Market Variables")
c1, c2 = st.columns(2)
with c1:
    o1 = st.number_input("Slot 1: 1X2 Match Draw Odds", value=float(def_o1), step=0.01)
    o3 = st.number_input(f"Slot 3: {team_a} To Qualify Odds", value=float(def_o3), step=0.01)
with c2:
    o2 = st.number_input("Slot 2: Asian Total Under 2.5 Odds", value=float(def_o2), step=0.01)
    o4 = st.number_input(f"Slot 4: {team_b} To Qualify Odds", value=float(def_o4), step=0.01)

# 4. MATHEMATICAL OPTIMIZATION MATRIX ENGINE (Corrected Hedging Logic)
# Target recovery amounts based on protection configuration setting
target_recovery = bankroll * risk_floor

# Correct hedge allocation calculation to secure target recovery payouts
stake3 = round(target_recovery / o3, 2)
stake4 = round(target_recovery / o4, 2)

remaining = bankroll - stake3 - stake4

if remaining > 0:
    # 40/60 distribution across primary scoring constraint blocks
    stake1 = round(remaining * 0.40, 2)
    stake2 = round(remaining * 0.60, 2)
else:
    stake1, stake2 = 0.0, 0.0
    st.error("Error: Protection configurations exceed available portfolio capital. Lower your downside protection target slider.")

# 5. LIVE TICKER TRACKING & RULES STATE ENGINE
st.markdown("---")
st.subheader("⏱️ Live Game Resolution Tracker")

status_badge = f'<span class="badge-live">LIVE - {match_status}</span>' if match_status in ["In Progress", "First Half", "Second Half", "Halftime"] else f'<span class="badge-ft">{match_status}</span>'
st.markdown(f"### Current Standing: {team_a} **{score_a} - {score_b}** {team_b} {status_badge}", unsafe_allow_html=True)

total_goals = score_a + score_b
is_draw = (score_a == score_b)
is_under = (total_goals < 2.5)

# Render state rule trackers dynamically based on active game updates
c_d, c_u = st.columns(2)
with c_d:
    if is_draw:
        st.markdown('<div class="badge-condition">🟢 Draw Condition: ACTIVE</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="badge-broken">🔴 Draw Condition: BROKEN</div>', unsafe_allow_html=True)
with c_u:
    if is_under:
        st.markdown('<div class="badge-condition">🟢 Under 2.5 Condition: ACTIVE</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="badge-broken">🔴 Under 2.5 Condition: BROKEN</div>', unsafe_allow_html=True)

# 6. EXECUTABLE PORTFOLIO OPTIMIZATION SLIPS (Premium UI Layout)
st.subheader("📋 Executable Optimization Slips")

def draw_card(title, odds, stake):
    st.markdown(f"""
        <div class="slip-container">
            <span class="slip-odds">@{odds:.2f}</span>
            <div class="slip-header">{title}</div>
            <div class="slip-stake">${stake:.2f}</div>
        </div>
    """, unsafe_allow_html=True)

draw_card("Slot 1: Full-Time Match Draw", o1, stake1)
draw_card("Slot 2: Asian Total Under 2.5", o2, stake2)
draw_card(f"Slot 3: {team_a} To Qualify (Hedge Floor)", o3, stake3)
draw_card(f"Slot 4: {team_b} To Qualify (Hedge Floor)", o4, stake4)

# 7. HIGH-YIELD SCENARIO MATRIX PROJECTIONS
st.subheader("🎯 Realized Scenario Matrix Returns")

# Mathematical profit projections factoring in the corrected hedging model formulas
r_cagey = round((stake1 * o1) + (stake2 * o2) - bankroll, 2)
r_defensive = round((stake2 * o2) + (stake3 * o3) - bankroll, 2)
r_blowout = round((stake4 * o4) - bankroll, 2)

def render_matrix_row(scenario, profit):
    style_class = "matrix-win" if profit >= 0 else "matrix-loss"
    sign = "+" if profit >= 0 else ""
    st.markdown(f"""
        <div class="matrix-row">
            <span style="font-size:0.95rem; font-weight:600;">{scenario}</span>
            <span class="{style_class}">{sign}${profit:.2f}</span>
        </div>
    """, unsafe_allow_html=True)

render_matrix_row("🎯 Strategic Target Met (Cagey Draw 0-0, 1-1)", r_cagey)
render_matrix_row("🛡️ Defensive Script Met (Team A wins 1-0, 2-0)", r_defensive)
render_matrix_row("⚠️ Outlier Script Deviation (Team B Blowout 0-3)", r_blowout)
