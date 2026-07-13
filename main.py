import streamlit as st
import pandas as pd

# 1. Premium Visual Configuration
st.set_page_config(
    page_title="TALOX | Quantitative Engine",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Injecting Custom CSS to re-create the dark UI card profiles from your dashboard mockups
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

# 2. System Headers
st.title("🎛️ TALOX Risk Management Engine")
st.caption("Core Portfolio Controller v2.1 | Simulation Mode Active")

# 3. Dynamic Sport Archetype Matrix Dictionary
SPORT_PROFILES = {
    "⚽ Soccer: Tournament Knockout": {
        "slot1": "1X2 Match Draw",
        "slot2": "Asian Total Under 2.5",
        "slot3": "Team A to Qualify",
        "slot4": "Team B to Qualify"
    },
    "⚽ Soccer: Regular Season League": {
        "slot1": "1X2 Match Draw",
        "slot2": "Both Teams to Score: No",
        "slot3": "Team A Win to Nil",
        "slot4": "Team B Win to Nil"
    },
    "🏀 Basketball: NBA Slate": {
        "slot1": "Alternative Spread Corridor (1-4 Pts)",
        "slot2": "Alternative Match Under",
        "slot3": "Team A Moneyline",
        "slot4": "Team B Moneyline"
    }
}

# 4. User Configuration Controls
st.subheader("⚙️ Portfolio Parameterization")
selected_profile = st.selectbox("Select Target Market Archetype", list(SPORT_PROFILES.keys()))
active_slots = SPORT_PROFILES[selected_profile]

col_bankroll, col_floor = st.columns(2)
with col_bankroll:
    total_bankroll = st.number_input("Total Portfolio Capital ($)", min_value=1.0, value=30.0, step=5.0)
with col_floor:
    protection_floor = st.slider("Hedge Floor Protection (%)", min_value=10, max_value=50, value=35) / 100.0

# 5. Dynamic Market Odds Ingestion Slots
st.subheader("📈 Live Market Odds Feed")
c1, c2 = st.columns(2)
with c1:
    o1 = st.number_input(f"Odds: {active_slots['slot1']}", min_value=1.01, value=3.00, step=0.05)
    o3 = st.number_input(f"Odds: {active_slots['slot3']}", min_value=1.01, value=1.75, step=0.05)
with c2:
    o2 = st.number_input(f"Odds: {active_slots['slot2']}", min_value=1.01, value=1.59, step=0.05)
    o4 = st.number_input(f"Odds: {active_slots['slot4']}", min_value=1.01, value=2.04, step=0.05)

# 6. Quantitative Optimization Engine Math
# Calculate safe capital floors for protection hedges
stake3 = round((total_bankroll * protection_floor) / o3, 2)
stake4 = round((total_bankroll * protection_floor) / o4, 2)

# Distribute remaining resource allocation across primary strategic engines
remaining_capital = total_bankroll - stake3 - stake4

if remaining_capital > 0:
    # 60/40 structural split prioritizing the direct score environment constraint
    stake1 = round(remaining_capital * 0.40, 2)
    stake2 = round(remaining_capital * 0.60, 2)
else:
    stake1, stake2 = 0.0, 0.0
    st.error("Hedge floor protection configurations exceed total available portfolio capital. Lower the protection slider.")

# 7. Rendering Dynamic Visual Cards
st.subheader("📋 Executable Optimization Slips")

def render_card(title, odds, stake):
    st.markdown(f"""
        <div class="portfolio-card">
            <span class="card-odds">@{odds:.2f}</span>
            <div class="card-header">{title}</div>
            <div style="margin-top: 8px;">Allocated Stake: <span class="card-stake">${stake:.2f}</span></div>
        </div>
    """, unsafe_allow_html=True)

render_card(active_slots["slot1"], o1, stake1)
render_card(active_slots["slot2"], o2, stake2)
render_card(active_slots["slot3"], o3, stake3)
render_card(active_slots["slot4"], o4, stake4)

# 8. Scenario Matrix Projections
st.markdown("---")
st.subheader("🎯 Scenario Performance Matrix")

# Calculate mathematical performance vectors based on game scripts
p_draw_cagey = round((stake1 * o1) + (stake2 * o2) - total_bankroll, 2)
p_defensive_win = round((stake2 * o2) + (stake3 * o3) - total_bankroll, 2)
p_outlier_blowout = round((stake4 * o4) - total_bankroll, 2)

metrics_df = pd.DataFrame({
    "Tactical Match Scenario Script": [
        "Strategic Target Met (Both Core Slots Hit)", 
        "Defensive Game Flow (Baseline + Floor A)", 
        "Outlier Script Deviation (Floor B Only)"
    ],
    "Net Simulation P&L": [f"${p_draw_cagey:+.2f}", f"${p_defensive_win:+.2f}", f"${p_outlier_blowout:+.2f}"],
    "Expected Yield Profile": [
        "🚀 Maximum Target Met", 
        "🛡️ Capital Preserved", 
        "⚠️ Risk Mitigation Triggered"
    ]
})

st.table(metrics_df)
