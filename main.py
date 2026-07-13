import streamlit as st
import pandas as pd
import requests

# 1. Premium Mobile Design Engine
st.set_page_config(
    page_title="TALOX | Quantitative Engine",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom dark-theme styling blocks matching your dashboard layouts
st.markdown("""
    <style>
    .reportview-container { background: #0b0e14; }
    .stApp { background-color: #0b0e14; color: #e2e8f0; }
    div[data-testid="stMetricValue"] { color: #f59e0b !important; font-family: monospace; }
    .portfolio-card {
        background-color: #111827;
        border: 1px solid #1f2937;
        border-radius: 8px;
        padding: 16px;
        margin-bottom: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .card-header { font-size: 0.85rem; color: #9ca3af; text-transform: uppercase; letter-spacing: 0.05em; }
    .card-odds { font-size: 1.4rem; font-weight: bold; color: #38bdf8; float: right; }
    .card-stake { font-size: 1.2rem; font-weight: bold; color: #10b981; }
    </style>
""", unsafe_allow_html=True)

# 2. Base API Connectivity Function
@st.cache_data(ttl=120)  # Caches matches for 2 mins so your phone doesn't spam the endpoint on every slider change
def fetch_espn_live_fixtures(sport, league):
    url = f"https://site.api.espn.com/apis/site/v2/sports/{sport}/{league}/scoreboard"
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15"
    }
    try:
        response = requests.get(url, headers=headers, timeout=8)
        if response.status_code == 200:
            events = response.json().get("events", [])
            cleaned_fixtures = []
            for event in events:
                match_id = event.get("id")
                match_name = event.get("name")
                status = event.get("status", {}).get("type", {}).get("description")
                
                # Safely extract competing team display profiles
                competitions = event.get("competitions", [{}])
                competitors = competitions[0].get("competitors", [])
                
                # Handle baseline sorting labels safely
                team_a = "Team A"
                team_b = "Team B"
                if len(competitors) >= 2:
                    team_a = competitors[1].get("team", {}).get("displayName", "Team A")
                    team_b = competitors[0].get("team", {}).get("displayName", "Team B")
                
                cleaned_fixtures.append({
                    "id": match_id,
                    "display_name": f"⏱️ [{status}] {match_name}",
                    "team_a": team_a,
                    "team_b": team_b
                })
            return cleaned_fixtures
    except Exception:
        return []
    return []

# 3. System App Header Setup
st.title("🎛️ TALOX Risk Management Engine")
st.caption("Live Automated Data Pipeline Enabled | v2.5")

# 4. Multi-Sport Environment Map
SPORT_PROFILES = {
    "⚽ Soccer: Tournament Knockout": {
        "sport": "soccer", "league": "fifa.world",
        "slot1": "1X2 Match Draw", "slot2": "Asian Total Under 2.5",
        "slot3": "to Qualify", "slot4": "to Qualify"
    },
    "⚽ Soccer: English Premier League": {
        "sport": "soccer", "league": "eng.1",
        "slot1": "1X2 Match Draw", "slot2": "Both Teams to Score: No",
        "slot3": "Win to Nil", "slot4": "Win to Nil"
    },
    "🏀 Basketball: NBA Fixtures": {
        "sport": "basketball", "league": "nba",
        "slot1": "Spread Corridor (1-4 Pts)", "slot2": "Alternative Match Under",
        "slot3": "Moneyline", "slot4": "Moneyline"
    }
}

# 5. Core Configurations
st.subheader("⚙️ Portfolio Parameterization")
selected_profile = st.selectbox("Target Archetype Matrix", list(SPORT_PROFILES.keys()))
active_config = SPORT_PROFILES[selected_profile]

# Fetching Data live via ESPN network call
live_games = fetch_espn_live_fixtures(active_config["sport"], active_config["league"])

# Setup match selection component parameters
team_a_name = "Team A"
team_b_name = "Team B"

if live_games:
    selected_game = st.selectbox(
        "Select Active ESPN Event Feed", 
        options=live_games, 
        format_func=lambda x: x["display_name"]
    )
    team_a_name = selected_game["team_a"]
    team_b_name = selected_game["team_b"]
    st.success(f"🎯 Connected to Live Stream: **{team_a_name}** vs **{team_b_name}**")
else:
    st.warning("⚠️ No active games found on ESPN endpoint. Defaulting to manual entries.")
    manual_input = st.text_input("Manual Match Title", value="England vs Argentina")
    if "vs" in manual_input:
        splits = manual_input.split("vs")
        team_a_name = splits[0].strip()
        team_b_name = splits[1].strip()

# Base Allocation Parameters
col_bankroll, col_floor = st.columns(2)
with col_bankroll:
    total_bankroll = st.number_input("Total Portfolio Capital ($)", min_value=1.0, value=30.0, step=5.0)
with col_floor:
    protection_floor = st.slider("Hedge Floor Protection (%)", min_value=10, max_value=50, value=35) / 100.0

# Dynamic Slot Title Generation based on current parameters
slot3_title = f"{team_a_name} {active_config['slot3']}"
slot4_title = f"{team_b_name} {active_config['slot4']}"

# 6. Odds Feeds Entry Blocks
st.subheader("📈 Real-Time Odds Entry")
c1, c2 = st.columns(2)
with c1:
    o1 = st.number_input(f"Odds: {active_config['slot1']}", min_value=1.01, value=3.00, step=0.05)
    o3 = st.number_input(f"Odds: {slot3_title}", min_value=1.01, value=1.75, step=0.05)
with c2:
    o2 = st.number_input(f"Odds: {active_config['slot2']}", min_value=1.01, value=1.59, step=0.05)
    o4 = st.number_input(f"Odds: {slot4_title}", min_value=1.01, value=2.04, step=0.05)

# 7. Portfolio Mathematical Distribution Calculations
stake3 = round((total_bankroll * protection_floor) / o3, 2)
stake4 = round((total_bankroll * protection_floor) / o4, 2)
remaining_capital = total_bankroll - stake3 - stake4

if remaining_capital > 0:
    stake1 = round(remaining_capital * 0.40, 2)
    stake2 = round(remaining_capital * 0.60, 2)
else:
    stake1, stake2 = 0.0, 0.0
    st.error("Hedge configurations exceed available portfolio capital limit.")

# 8. Render Mobile Visual Slips
st.subheader("📋 Executable Portfolio Slips")

def render_card(title, odds, stake):
    st.markdown(f"""
        <div class="portfolio-card">
            <span class="card-odds">@{odds:.2f}</span>
            <div class="card-header">{title}</div>
            <div style="margin-top: 8px;">Allocated Stake: <span class="card-stake">${stake:.2f}</span></div>
        </div>
    """, unsafe_allow_html=True)

render_card(active_config["slot1"], o1, stake1)
render_card(active_config["slot2"], o2, stake2)
render_card(slot3_title, o3, stake3)
render_card(slot4_title, o4, stake4)

# 9. Yield Risk Assessment Projection Matrix Output
st.markdown("---")
st.subheader("🎯 Scenario Matrix Returns")

p_target_hit = round((stake1 * o1) + (stake2 * o2) - total_bankroll, 2)
p_defensive = round((stake2 * o2) + (stake3 * o3) - total_bankroll, 2)
p_blowout = round((stake4 * o4) - total_bankroll, 2)

metrics_df = pd.DataFrame({
    "Tactical Match Scenario Script": [
        "Strategic Target Met (Core Matrix Wins)", 
        "Defensive Game Flow (Baseline + Floor A)", 
        "Outlier Script Deviation (Floor B Triggers)"
    ],
    "Net Simulation P&L": [f"${p_target_hit:+.2f}", f"${p_defensive:+.2f}", f"${p_blowout:+.2f}"],
    "Expected Yield Profile": ["🚀 Maximum Target Met", "🛡️ Capital Preserved", "⚠️ Risk Mitigation Active"]
})

st.table(metrics_df)
