import os
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import altair as alt
import matplotlib.pyplot as plt
import seaborn as sns

# ==============================================================================
# PRO TIP 1: PAGE CONFIGURATION & METADATA
# ==============================================================================
st.set_page_config(
    page_title="India E-Waste Analytics & Peer Benchmarking",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for eco-friendly theme, fluid animations, and card hover lifts
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* Keyframe Animations */
    @keyframes gradientFlow {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    @keyframes pulseGlow {
        0% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.45); }
        70% { box-shadow: 0 0 0 10px rgba(16, 185, 129, 0); }
        100% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
    }

    /* Animated Header */
    .main-header {
        background: linear-gradient(135deg, #022c22 0%, #064e3b 25%, #047857 50%, #059669 75%, #10b981 100%);
        background-size: 250% 250%;
        animation: gradientFlow 12s ease infinite;
        padding: 2.3rem 2.6rem;
        border-radius: 20px;
        color: white;
        margin-bottom: 1.8rem;
        box-shadow: 0 14px 30px -6px rgba(5, 150, 105, 0.35);
        border: 1px solid rgba(52, 211, 153, 0.3);
    }
    .main-header h1 {
        font-size: 2.35rem;
        font-weight: 800;
        margin: 0 0 0.5rem 0;
        letter-spacing: -0.025em;
        color: #ffffff;
    }
    .main-header p {
        font-size: 1.05rem;
        opacity: 0.94;
        margin-bottom: 1.1rem;
        line-height: 1.55;
        max-width: 900px;
    }
    .badge-container {
        display: flex;
        flex-wrap: wrap;
        gap: 0.65rem;
        margin-top: 0.85rem;
    }
    .badge {
        background: rgba(255, 255, 255, 0.18);
        backdrop-filter: blur(10px);
        padding: 0.48rem 1.1rem;
        border-radius: 9999px;
        font-size: 0.95rem;
        font-weight: 700;
        border: 1px solid rgba(255, 255, 255, 0.32);
        transition: all 0.25s ease;
        display: inline-flex;
        align-items: center;
        letter-spacing: -0.01em;
    }
    .badge:hover {
        background: rgba(255, 255, 255, 0.32);
        transform: translateY(-2px);
    }
    .badge-spotlight {
        background: #ffffff !important;
        color: #064e3b !important;
        font-weight: 800 !important;
        font-size: 1.02rem !important;
        border: 2px solid #34d399 !important;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2) !important;
        padding: 0.52rem 1.3rem !important;
    }

    /* Eco Status Tag */
    .eco-status-tag {
        display: inline-flex;
        align-items: center;
        gap: 0.45rem;
        background: #ecfdf5;
        color: #065f46;
        padding: 0.35rem 0.85rem;
        border-radius: 9999px;
        font-size: 0.8rem;
        font-weight: 700;
        border: 1px solid #a7f3d0;
        animation: pulseGlow 2.5s infinite;
        margin-bottom: 0.8rem;
    }
    .eco-dot {
        width: 8px;
        height: 8px;
        background-color: #10b981;
        border-radius: 50%;
    }

    /* Metric Cards with Border & Hover Lift */
    .metric-card {
        background: #ffffff;
        border: 1px solid rgba(16, 185, 129, 0.22);
        border-radius: 16px;
        padding: 1.35rem 1.45rem;
        box-shadow: 0 4px 14px -2px rgba(6, 78, 59, 0.05);
        transition: all 0.28s cubic-bezier(0.25, 0.8, 0.25, 1);
        position: relative;
        overflow: hidden;
    }
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 4px;
        background: linear-gradient(90deg, #059669, #34d399);
        opacity: 0.8;
    }
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 16px 32px -6px rgba(5, 150, 105, 0.22);
        border-color: rgba(16, 185, 129, 0.5);
    }
    .metric-label {
        font-size: 0.8rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: #047857;
        margin-bottom: 0.35rem;
    }
    .metric-value {
        font-size: 1.85rem;
        font-weight: 800;
        color: #0f291e;
        line-height: 1.15;
    }
    .metric-delta {
        font-size: 0.8rem;
        font-weight: 600;
        margin-top: 0.45rem;
    }
    .delta-up { color: #dc2626; }
    .delta-eco { color: #059669; }
    .delta-neutral { color: #0284c7; }

    /* Feynman Box */
    .feynman-box {
        background: linear-gradient(135deg, #f0fdf4 0%, #ecfdf5 100%);
        border-left: 5px solid #059669;
        border-radius: 0 16px 16px 0;
        padding: 1.5rem 1.8rem;
        margin: 1.5rem 0;
        box-shadow: 0 6px 18px -4px rgba(5, 150, 105, 0.08);
        border-top: 1px solid rgba(16, 185, 129, 0.15);
        border-bottom: 1px solid rgba(16, 185, 129, 0.15);
        border-right: 1px solid rgba(16, 185, 129, 0.15);
    }

    /* Simulator Result Cards */
    .sim-card {
        background: linear-gradient(135deg, #ffffff 0%, #f0fdf4 100%);
        border: 1px solid #a7f3d0;
        border-radius: 14px;
        padding: 1.25rem 1.3rem;
        box-shadow: 0 4px 12px rgba(6, 78, 59, 0.05);
        text-align: center;
        transition: transform 0.2s ease;
    }
    .sim-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 20px -3px rgba(16, 185, 129, 0.18);
    }
    .sim-val {
        font-size: 1.8rem;
        font-weight: 800;
        color: #065f46;
        margin: 0.35rem 0;
    }
    .sim-lbl {
        font-size: 0.8rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #64748b;
    }

    /* ==========================================================================
       PROMINENT STREAMLIT TABS NAVIGATION BAR (ULTRA-HIGH VISIBILITY & SIZE)
       ========================================================================== */
    .stTabs,
    [data-testid="stTabs"],
    div.stTabs {
        margin-top: 1rem !important;
        margin-bottom: 2rem !important;
    }

    .stTabs [role="tablist"],
    [data-testid="stTabs"] [role="tablist"],
    [data-baseweb="tab-list"],
    div.stTabs [data-baseweb="tab-list"],
    div[data-testid="stTabs"] [data-baseweb="tab-list"] {
        gap: 0.65rem !important;
        background: #f0fdf4 !important;
        padding: 0.75rem 0.95rem !important;
        border-radius: 20px !important;
        border: 2.5px solid #6ee7b7 !important;
        box-shadow: 0 8px 24px -2px rgba(6, 78, 59, 0.12) !important;
        overflow-x: auto !important;
        margin-bottom: 1.5rem !important;
    }

    .stTabs [role="tab"],
    .stTabs button,
    [data-testid="stTabs"] [role="tab"],
    [data-testid="stTabs"] button,
    [data-baseweb="tab"],
    button[data-baseweb="tab"] {
        padding: 0.95rem 1.65rem !important;
        border-radius: 14px !important;
        font-size: 1.25rem !important;
        font-weight: 700 !important;
        color: #064e3b !important;
        background-color: #ffffff !important;
        border: 2px solid rgba(16, 185, 129, 0.35) !important;
        box-shadow: 0 3px 10px rgba(6, 78, 59, 0.07) !important;
        transition: all 0.22s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
        white-space: nowrap !important;
        min-height: 56px !important;
        height: auto !important;
    }

    .stTabs [role="tab"]:hover,
    .stTabs button:hover,
    [data-testid="stTabs"] button:hover,
    [data-baseweb="tab"]:hover {
        background-color: #ecfdf5 !important;
        color: #047857 !important;
        border-color: #10b981 !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 20px -2px rgba(16, 185, 129, 0.3) !important;
    }

    .stTabs [role="tab"][aria-selected="true"],
    .stTabs button[aria-selected="true"],
    [data-testid="stTabs"] [role="tab"][aria-selected="true"],
    [data-testid="stTabs"] button[aria-selected="true"],
    [data-baseweb="tab"][aria-selected="true"] {
        background: linear-gradient(135deg, #065f46 0%, #047857 50%, #059669 100%) !important;
        color: #ffffff !important;
        font-weight: 800 !important;
        border-color: #047857 !important;
        box-shadow: 0 8px 24px -2px rgba(5, 150, 105, 0.5) !important;
        transform: translateY(-2px) !important;
    }

    .stTabs [role="tab"] p,
    .stTabs button p,
    [data-testid="stTabs"] [role="tab"] p,
    [data-testid="stTabs"] button p,
    .stTabs [data-testid="stMarkdownContainer"] p,
    [data-baseweb="tab"] p {
        font-size: 1.25rem !important;
        font-weight: inherit !important;
        margin: 0 !important;
        line-height: 1.35 !important;
        letter-spacing: -0.01em !important;
    }

    .stTabs [role="tab"][aria-selected="true"] p,
    .stTabs button[aria-selected="true"] p,
    .stTabs [role="tab"][aria-selected="true"] span,
    .stTabs button[aria-selected="true"] span,
    [data-testid="stTabs"] [role="tab"][aria-selected="true"] p {
        color: #ffffff !important;
        font-weight: 800 !important;
    }

    .stTabs [role="tab"] span[data-testid="stIcon"],
    .stTabs [role="tab"] span.material-symbols-rounded,
    .stTabs [role="tab"] svg,
    .stTabs button span {
        font-size: 1.5rem !important;
        vertical-align: -0.18em !important;
        margin-right: 0.45rem !important;
    }

    /* Hide default faint underline border */
    div[data-baseweb="tab-highlight"],
    div[data-baseweb="tab-border"],
    .stTabs [data-baseweb="tab-highlight"],
    .stTabs [data-baseweb="tab-border"] {
        display: none !important;
    }

    /* Overflow navigation buttons */
    .stTabs [role="tablist"] ~ button,
    [data-baseweb="tab-list"] ~ button,
    div[data-testid="stTabs"] button[aria-label*="scroll"] {
        background-color: #ffffff !important;
        border: 2px solid #6ee7b7 !important;
        border-radius: 12px !important;
        color: #064e3b !important;
        padding: 0.5rem 0.65rem !important;
        font-size: 1.3rem !important;
        box-shadow: 0 2px 10px rgba(6, 78, 59, 0.1) !important;
    }
</style>
""", unsafe_allow_html=True)

ECO_PALETTE = ["#059669", "#10b981", "#34d399", "#0284c7", "#f59e0b", "#8b5cf6", "#ec4899", "#6366f1"]

# ==============================================================================
# PRO TIP 2: CACHED DATA LOADING & ERROR RESILIENCE
# ==============================================================================
@st.cache_data(show_spinner="Loading Indian municipal environmental datasets...", ttl="12h")
def load_and_preprocess_data():
    base_path = os.path.dirname(os.path.abspath(__file__))
    
    def resolve_dataset_path(filename):
        candidates = [
            os.path.join(base_path, "data", filename),
            os.path.join(base_path, filename),
            os.path.join(os.getcwd(), "data", filename),
            os.path.join(os.getcwd(), filename),
            os.path.join(base_path, "..", "data", filename),
            os.path.join(base_path, "..", filename),
        ]
        for c in candidates:
            if os.path.exists(c):
                return c
        return os.path.join(base_path, filename)
    
    path_cities = resolve_dataset_path("cities_master.csv")
    path_recycling = resolve_dataset_path("Waste_Management_and_Recycling_India.csv")
    path_20k = resolve_dataset_path("Waste_Management_India_20K.csv")
    
    cities_df = pd.read_csv(path_cities)
    wm_rec_df = pd.read_csv(path_recycling)
    wm_20k_df = pd.read_csv(path_20k)
    
    for df in [cities_df, wm_rec_df, wm_20k_df]:
        df.columns = df.columns.str.strip()
        
    if "City/District" in wm_rec_df.columns:
        wm_rec_df.rename(columns={"City/District": "City"}, inplace=True)
        
    combined_df = pd.merge(
        wm_20k_df,
        cities_df[["City", "State", "Is_Tourist", "Is_Hill_Station"]],
        on=["City", "State"],
        how="inner"
    )
    
    return cities_df, wm_rec_df, wm_20k_df, combined_df

try:
    cities_df, wm_rec_df, wm_20k_df, combined_df = load_and_preprocess_data()
except Exception as e:
    st.error(f"Error loading datasets: {e}")
    st.stop()

# ==============================================================================
# PRO TIP 3: URL QUERY PARAM SYNCHRONIZATION & SESSION STATE
# ==============================================================================
DEFAULT_PEERS = ["Mumbai", "Delhi", "Bangalore", "Pune", "Kolkata"]

# Read state from URL query params
if "peer_cities" not in st.session_state:
    url_peers = st.query_params.get("peers", None)
    if url_peers:
        st.session_state.peer_cities = [p.strip() for p in url_peers.split(",") if p.strip()]
    else:
        st.session_state.peer_cities = DEFAULT_PEERS

# ==============================================================================
# PRO TIP 4: MODERN CONTROLS IN SIDEBAR WITH ST.PILLS & SEGMENTED CONTROLS
# ==============================================================================
with st.sidebar:
    st.markdown("""
    <div style="display:flex; align-items:center; gap:0.6rem; margin-bottom:1rem;">
        <span style="font-size:1.8rem;">🌿</span>
        <div>
            <h3 style="margin:0; font-size:1.15rem; color:#064e3b; font-weight:800;">Analytics Scope</h3>
            <span style="font-size:0.75rem; color:#047857; font-weight:600;">India E-Waste Observatory</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Modern Pills for Scope
    analysis_mode = st.pills(
        "Study Focus",
        options=["E-Waste Focus", "All Waste Classes"],
        default="E-Waste Focus"
    )
    is_ewaste_only = (analysis_mode == "E-Waste Focus")
    
    st.markdown("---")
    
    # Modern Time Horizon Pills
    time_preset = st.pills(
        "Quick Time Horizon",
        options=["Full (2015-2026)", "Recent 5Y (2021-2026)", "Surge Era (2019-2022)"],
        default="Full (2015-2026)"
    )
    
    if time_preset == "Recent 5Y (2021-2026)":
        init_years = (2021, 2026)
    elif time_preset == "Surge Era (2019-2022)":
        init_years = (2019, 2022)
    else:
        init_years = (2015, 2026)
        
    selected_years = st.slider(
        "Observation Time Window",
        min_value=2015,
        max_value=2026,
        value=init_years,
        step=1
    )
    
    # Region Multi-select
    all_regions = sorted(wm_20k_df["Region"].dropna().unique().tolist())
    selected_regions = st.multiselect(
        "Geographic Regions",
        options=all_regions,
        default=all_regions,
        placeholder="Choose regions to include..."
    )
    
    # City Tier Filter
    all_categories = sorted(wm_20k_df["City_Category"].dropna().unique().tolist())
    selected_categories = st.multiselect(
        "City Tiers",
        options=all_categories,
        default=all_categories,
        placeholder="Choose city categories..."
    )
    
    # Waste Type Filter
    if not is_ewaste_only:
        all_waste_types = sorted(wm_20k_df["Waste_Type"].dropna().unique().tolist())
        selected_waste_types = st.multiselect(
            "Waste Classifications",
            options=all_waste_types,
            default=all_waste_types
        )
    else:
        selected_waste_types = ["E-Waste"]
        
    st.markdown("---")
    view_static_plots = st.checkbox("Show Matplotlib/Seaborn plots as backup", value=False)
    
    if st.button("Reset All Filters", use_container_width=True):
        st.query_params.clear()
        st.session_state.peer_cities = DEFAULT_PEERS
        st.rerun()

# Apply Filters
mask = (
    (wm_20k_df["Year"].between(selected_years[0], selected_years[1])) &
    (wm_20k_df["Region"].isin(selected_regions)) &
    (wm_20k_df["City_Category"].isin(selected_categories)) &
    (wm_20k_df["Waste_Type"].isin(selected_waste_types))
)
filtered_20k = wm_20k_df[mask]

# PRO TIP 5: DEFENSIVE GUARDRAIL WITH ST.STOP()
if len(filtered_20k) == 0:
    st.info("No data matches your active filter selection. Adjust the year slider or select at least one region.", icon=":material/info:")
    st.stop()

comb_mask = (
    (combined_df["Year"].between(selected_years[0], selected_years[1])) &
    (combined_df["Region"].isin(selected_regions)) &
    (combined_df["City_Category"].isin(selected_categories)) &
    (combined_df["Waste_Type"].isin(selected_waste_types))
)
filtered_combined = combined_df[comb_mask]

# Subsets for E-waste
ew_20k = wm_20k_df[wm_20k_df["Waste_Type"] == "E-Waste"]
filtered_ew = filtered_20k[filtered_20k["Waste_Type"] == "E-Waste"]

# ==============================================================================
# HEADER SECTION
# ==============================================================================
st.markdown("""
<div class="main-header">
    <div class="eco-status-tag">
        <span class="eco-dot"></span>
        Interactive Sustainability & Material Recovery Observatory
    </div>
    <h1>India E-Waste Growth Analytics</h1>
    <p>An interactive data analytics platform analyzing electronic waste accumulation, peer city benchmarking, municipal infrastructure bottlenecks, and circular recovery potential across Indian urban centers.</p>
    <div class="badge-container">
        <span class="badge badge-spotlight">🏷️ Group No.: 24</span>
        <span class="badge">INFT-C Batch 3</span>
        <span class="badge">Ruhaan Joshi (24101C0057)</span>
        <span class="badge">Om Thakur (24101C0041)</span>
        <span class="badge">Rudra Jain (24101C0062)</span>
        <span class="badge">2015 – 2026 Longitudinal Study</span>
        <span class="badge">25,200+ Municipal Records</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# PRO TIP 6: TOP METRICS WITH BORDERED CONTAINERS & SEMANTIC DELTAS
# ==============================================================================
total_tonnage = filtered_20k["Daily_Waste_Generation_Tons"].sum()
mean_daily = filtered_20k["Daily_Waste_Generation_Tons"].mean()
avg_collection = filtered_20k["Collection_Efficiency_Percentage"].mean()
avg_recycling = filtered_20k["Recycling_Rate"].mean()

ew_2015 = ew_20k[ew_20k["Year"] == 2015]["Daily_Waste_Generation_Tons"].sum()
ew_2026 = ew_20k[ew_20k["Year"] == 2026]["Daily_Waste_Generation_Tons"].sum()
cagr_val = ((ew_2026 / ew_2015) ** (1 / 11) - 1) * 100 if ew_2015 > 0 else 7.56

kpi_cols = st.columns(5)

with kpi_cols[0].container(border=True):
    st.metric(
        label="Cumulative Daily Volume",
        value=f"{total_tonnage:,.1f} T/D",
        delta="Filtered Active Volume",
        delta_color="normal",
        width="content"
    )

with kpi_cols[1].container(border=True):
    st.metric(
        label="Mean Generation Rate",
        value=f"{mean_daily:.2f} Tons",
        delta="Per Reporting Center",
        delta_color="off",
        width="content"
    )

with kpi_cols[2].container(border=True):
    st.metric(
        label="11-Year Growth (CAGR)",
        value=f"+{cagr_val:.2f}%",
        delta="770 T/D (2015) → 1,716 T/D (2026)",
        delta_color="inverse",
        width="content"
    )

with kpi_cols[3].container(border=True):
    st.metric(
        label="Collection Efficiency",
        value=f"{avg_collection:.1f}%",
        delta="Stagnant Municipal Ceiling",
        delta_color="inverse",
        width="content"
    )

with kpi_cols[4].container(border=True):
    st.metric(
        label="Formal Recycling Rate",
        value=f"{avg_recycling:.1f}%",
        delta=">50% Informal Leakage Gap",
        delta_color="normal",
        width="content"
    )

st.markdown("<br>", unsafe_allow_html=True)

# ==============================================================================
# MAIN TABS ARCHITECTURE WITH MATERIAL ICONS
# ==============================================================================
tab_group, tab_peers, tab_overview, tab_sim, tab_univariate, tab_comp, tab_regression, tab_corr, tab_geo, tab_explorer, tab_notes = st.tabs([
    ":material/groups: Group No.: 24",
    ":material/compare_arrows: Peer Benchmarking",
    ":material/query_stats: Overview & Growth",
    ":material/eco: Eco-Policy Simulator",
    ":material/bar_chart: Distributions & Outliers",
    ":material/pie_chart: Waste Composition",
    ":material/show_chart: Regression & Trends",
    ":material/grid_on: Correlation Heatmap",
    ":material/map: Geospatial & City Audit",
    ":material/table_view: Data Explorer",
    ":material/policy: Policy & Engineering"
])

# ------------------------------------------------------------------------------
# TAB 0: GROUP NO.: 24 - ACADEMIC DOSSIER & FACULTY NAVIGATION
# ------------------------------------------------------------------------------
with tab_group:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #022c22 0%, #064e3b 40%, #059669 100%); padding: 2rem 2.4rem; border-radius: 20px; color: white; margin-bottom: 1.8rem; box-shadow: 0 12px 28px -4px rgba(5, 150, 105, 0.3); border: 1px solid rgba(52, 211, 153, 0.3);">
        <div style="display:inline-flex; align-items:center; gap:0.5rem; background:rgba(255,255,255,0.2); padding:0.4rem 1rem; border-radius:9999px; font-weight:700; font-size:0.9rem; margin-bottom:0.8rem; border:1px solid rgba(255,255,255,0.35);">
            <span>🎓</span> Academic Project Dossier
        </div>
        <h2 style="margin:0 0 0.5rem 0; font-size:2.3rem; font-weight:800; color:#ffffff; letter-spacing:-0.02em;">Group No.: 24 — INFT-C Batch 3</h2>
        <p style="font-size:1.1rem; opacity:0.95; margin:0; line-height:1.6; max-width:880px;">
            Department of Information Technology • Longitudinal E-Waste Growth Analytics & Circular Policy Modeling Platform (2015–2026)
        </p>
    </div>
    """, unsafe_allow_html=True)

    col_g1, col_g2, col_g3 = st.columns(3)

    with col_g1.container(border=True):
        st.markdown("""
        <div style="text-align:center; padding:0.8rem 0;">
            <div style="font-size:2.6rem; margin-bottom:0.3rem;">👨‍💻</div>
            <h3 style="margin:0; font-size:1.35rem; color:#064e3b; font-weight:800;">Ruhaan Joshi</h3>
            <p style="margin:0.25rem 0; font-size:1.05rem; font-weight:700; color:#059669;">Roll No: <code>24101C0057</code></p>
            <p style="margin:0.4rem 0 0 0; font-size:0.88rem; color:#64748b;">Department of Information Technology<br>INFT-C Batch 3</p>
        </div>
        """, unsafe_allow_html=True)

    with col_g2.container(border=True):
        st.markdown("""
        <div style="text-align:center; padding:0.8rem 0;">
            <div style="font-size:2.6rem; margin-bottom:0.3rem;">👨‍💻</div>
            <h3 style="margin:0; font-size:1.35rem; color:#064e3b; font-weight:800;">Om Thakur</h3>
            <p style="margin:0.25rem 0; font-size:1.05rem; font-weight:700; color:#059669;">Roll No: <code>24101C0041</code></p>
            <p style="margin:0.4rem 0 0 0; font-size:0.88rem; color:#64748b;">Department of Information Technology<br>INFT-C Batch 3</p>
        </div>
        """, unsafe_allow_html=True)

    with col_g3.container(border=True):
        st.markdown("""
        <div style="text-align:center; padding:0.8rem 0;">
            <div style="font-size:2.6rem; margin-bottom:0.3rem;">👨‍💻</div>
            <h3 style="margin:0; font-size:1.35rem; color:#064e3b; font-weight:800;">Rudra Jain</h3>
            <p style="margin:0.25rem 0; font-size:1.05rem; font-weight:700; color:#059669;">Roll No: <code>24101C0062</code></p>
            <p style="margin:0.4rem 0 0 0; font-size:0.88rem; color:#64748b;">Department of Information Technology<br>INFT-C Batch 3</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col_sum1, col_sum2 = st.columns(2)
    with col_sum1.container(border=True):
        st.markdown("""
        #### 📌 Executive Project Highlights
        * **Longitudinal Dataset:** 25,200+ municipal observations from 2015 to 2026 across Indian urban centers.
        * **National Growth Rate:** **+7.56% CAGR** (770.16 tons/day in 2015 → 1,716.08 tons/day in 2026).
        * **Metropolitan Disparity:** Metros average **141.32 tons/day**, vs **1.01 tons/day** in Tier-3 cities (~140x divergence).
        * **Infrastructure Bottleneck:** Collection efficiency remains stagnant at ~50%, with >50% leaking into the informal sector.
        """)

    with col_sum2.container(border=True):
        st.markdown("""
        #### 🧭 Faculty Platform Roadmap
        Click any tab above to inspect the research models:
        * **⇄ Peer Benchmarking:** Normalized comparative divergence curves indexed to baseline (1.0).
        * **📈 Overview & Growth:** Macro daily tonnage trajectories, state rankings, and conveyor model.
        * **🌱 Eco-Policy Simulator:** Interactive policy what-if simulator projecting recovery yields.
        * **📊 Distributions & Outliers:** Skewness, log density distributions, and city tier boxplots.
        * **🗺️ Geospatial & City Audit:** India spatial mapping and individual municipal scorecards.
        * **📄 Data Explorer:** Paginated record inspector with one-click filtered CSV export.
        """)

# ------------------------------------------------------------------------------
# PRO TIP 7: SIGNATURE PEER BENCHMARKING ENGINE (FANILO'S PRO METHOD)
# ------------------------------------------------------------------------------
with tab_peers:
    st.markdown("""
    ### :material/compare: Normalized Peer Group Comparison
    Easily compare e-waste trajectories between Indian cities. Examine relative growth indexed to baseline, or compare each city against the average of all other selected peers.
    """)
    
    top_peer_cols = st.columns([1, 2])
    
    with top_peer_cols[0].container(border=True):
        all_avail_cities = sorted(wm_20k_df["City"].dropna().unique().tolist())
        selected_peers = st.multiselect(
            "Select Cities for Peer Analysis:",
            options=all_avail_cities,
            default=[c for c in st.session_state.peer_cities if c in all_avail_cities],
            placeholder="Pick 2 or more cities (e.g. Mumbai, Delhi)..."
        )
        
        # PRO TIP: Sync selected peers to URL query params
        if selected_peers:
            st.query_params["peers"] = ",".join(selected_peers)
            st.session_state.peer_cities = selected_peers
        else:
            st.query_params.pop("peers", None)
            
        metric_choice = st.pills(
            "Benchmarking Metric",
            options=["Daily E-Waste (Tons)", "Collection Efficiency (%)", "Formal Recycling Rate (%)"],
            default="Daily E-Waste (Tons)"
        )
        
        metric_map = {
            "Daily E-Waste (Tons)": "Daily_Waste_Generation_Tons",
            "Collection Efficiency (%)": "Collection_Efficiency_Percentage",
            "Formal Recycling Rate (%)": "Recycling_Rate"
        }
        active_metric_col = metric_map[metric_choice]
        
    if len(selected_peers) < 2:
        top_peer_cols[1].info("Please select at least 2 cities to perform peer group benchmarking.", icon=":material/info:")
        st.stop()
        
    # Build peer comparison dataframe
    peer_raw = ew_20k[ew_20k["City"].isin(selected_peers)]
    peer_agg = peer_raw.groupby(["Year", "City"])[active_metric_col].mean().reset_index()
    
    # Pivot into Year x City matrix
    peer_pivot = peer_agg.pivot(index="Year", columns="City", values=active_metric_col).ffill().bfill()
    
    # Normalize (start at 1.0 at first year)
    peer_norm = peer_pivot.div(peer_pivot.iloc[0])
    
    with top_peer_cols[1].container(border=True):
        st.markdown(f"**Indexed Relative Growth (Normalized to 1.0 Baseline at {peer_pivot.index[0]}):**")
        norm_melted = peer_norm.reset_index().melt(id_vars=["Year"], var_name="City", value_name="Normalized Growth")
        
        fig_norm = px.line(
            norm_melted,
            x="Year",
            y="Normalized Growth",
            color="City",
            markers=True,
            color_discrete_sequence=ECO_PALETTE,
            title="<b>Relative Acceleration (Starting Year = 1.0)</b>"
        )
        fig_norm.update_layout(
            height=320,
            margin=dict(l=20, r=20, t=40, b=20),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig_norm, use_container_width=True)
        
    st.markdown("---")
    
    # PRO TIP: Individual City vs Peer Average (Excluding the City Itself)
    st.markdown("#### Individual Cities vs Peer Average")
    st.caption("For each city below, the peer average represents the mean of all other selected cities, excluding the city itself.")
    
    peer_chart_cols = st.columns(min(len(selected_peers), 3))
    
    for idx, city in enumerate(selected_peers):
        col_target = peer_chart_cols[idx % len(peer_chart_cols)]
        
        # Calculate peer average (excluding current city)
        other_peers = peer_pivot.drop(columns=[city])
        peer_avg = other_peers.mean(axis=1)
        
        city_series = peer_pivot[city]
        delta_series = city_series - peer_avg
        
        chart_df = pd.DataFrame({
            "Year": peer_pivot.index,
            city: city_series,
            "Peer Average": peer_avg,
            "Delta": delta_series
        })
        
        with col_target.container(border=True):
            st.markdown(f"**{city} vs Peer Group**")
            
            # City vs Peer Line Chart
            melted_comp = chart_df.melt(id_vars=["Year"], value_vars=[city, "Peer Average"], var_name="Entity", value_name="Value")
            fig_comp = px.line(
                melted_comp,
                x="Year",
                y="Value",
                color="Entity",
                color_discrete_map={city: "#059669", "Peer Average": "#94a3b8"},
                markers=True
            )
            fig_comp.update_layout(
                height=240,
                margin=dict(l=10, r=10, t=25, b=10),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)"
            )
            st.plotly_chart(fig_comp, use_container_width=True)
            
            # Delta Area Chart
            fig_delta = px.area(
                chart_df,
                x="Year",
                y="Delta",
                title=f"Delta: {city} minus Peer Average",
                color_discrete_sequence=["#10b981" if delta_series.iloc[-1] >= 0 else "#f59e0b"]
            )
            fig_delta.update_layout(
                height=180,
                margin=dict(l=10, r=10, t=35, b=10),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)"
            )
            st.plotly_chart(fig_delta, use_container_width=True)

# ------------------------------------------------------------------------------
# TAB 2: OVERVIEW & GROWTH
# ------------------------------------------------------------------------------
with tab_overview:
    st.markdown("### Longitudinal E-Waste Growth Trajectory (2015 – 2026)")
    
    yearly_stats = ew_20k.groupby("Year").agg(
        total_daily_tons=("Daily_Waste_Generation_Tons", "sum"),
        mean_daily_tons=("Daily_Waste_Generation_Tons", "mean"),
        median_daily_tons=("Daily_Waste_Generation_Tons", "median"),
        records=("Record_ID", "count"),
        recycling_rate=("Recycling_Rate", "mean"),
        collection_eff=("Collection_Efficiency_Percentage", "mean"),
        budget=("Waste_Management_Budget_INR", "mean")
    ).reset_index()
    
    c1, c2 = st.columns([7, 5])
    
    with c1.container(border=True):
        fig_trend = make_subplots(specs=[[{"secondary_y": True}]])
        
        fig_trend.add_trace(
            go.Bar(
                x=yearly_stats["Year"],
                y=yearly_stats["total_daily_tons"],
                name="Total Daily Tons Generated",
                marker=dict(
                    color=yearly_stats["total_daily_tons"],
                    colorscale=[[0, "#34d399"], [1, "#059669"]],
                    line=dict(color="#047857", width=1)
                ),
                opacity=0.9,
                hovertemplate="<b>Year %{x}</b><br>Total Generation: %{y:.1f} Tons/Day<extra></extra>"
            ),
            secondary_y=False
        )
        
        fig_trend.add_trace(
            go.Scatter(
                x=yearly_stats["Year"],
                y=yearly_stats["mean_daily_tons"],
                name="Mean Daily Tons per Center",
                mode="lines+markers",
                line=dict(color="#f59e0b", width=3.5),
                marker=dict(size=8, symbol="circle", color="#d97706"),
                hovertemplate="<b>Year %{x}</b><br>Mean Generation: %{y:.2f} Tons/Day<extra></extra>"
            ),
            secondary_y=True
        )
        
        fig_trend.update_layout(
            title="<b>Annual Daily E-Waste Tonnage & Per-Center Average</b>",
            xaxis=dict(title="Year", tickmode="linear", dtick=1),
            yaxis=dict(title="Total Daily E-Waste (Tons/Day)", showgrid=True, gridcolor="#e2e8f0"),
            yaxis2=dict(title="Mean Daily E-Waste (Tons/Day)", overlaying="y", side="right", showgrid=False),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            hovermode="x unified",
            margin=dict(l=40, r=40, t=60, b=40),
            height=400,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig_trend, use_container_width=True)
        
    with c2.container(border=True):
        state_ew = ew_20k.groupby("State")["Daily_Waste_Generation_Tons"].agg(["sum", "mean"]).sort_values(by="sum", ascending=True).tail(8)
        fig_state = px.bar(
            state_ew,
            x="sum",
            y=state_ew.index,
            orientation="h",
            color="sum",
            color_continuous_scale=[[0, "#a7f3d0"], [0.5, "#10b981"], [1, "#064e3b"]],
            title="<b>Top E-Waste Generating States</b>",
            labels={"sum": "Total Daily Tons", "State": "State"}
        )
        fig_state.update_layout(
            height=400,
            margin=dict(l=20, r=20, t=60, b=40),
            coloraxis_showscale=False,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig_state, use_container_width=True)
        
    st.markdown("""
    <div class="feynman-box">
        <h4>The Feynman Framework: The "One-Way Conveyor Belt" Dilemma</h4>
        <p>Imagine your city sitting beside a massive conveyor belt. On the intake side, logistics couriers constantly deposit brand-new smartphones, gaming consoles, laptops, and smart appliances. On the exit side, households and corporations discard obsolete gadgets. Over the past 11 years, device replacement cycles collapsed from 5 years to under 18 months, accelerating the conveyor belt by <strong>7.56% compounded annually</strong>. However, municipal recovery bins remained the exact same size.</p>
        <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1rem; margin-top: 1rem;">
            <div style="background:white; padding:1.1rem; border-radius:12px; border:1px solid #ccfbf1; box-shadow: 0 2px 8px rgba(5, 150, 105, 0.05);">
                <strong style="color:#047857;">1. Generation Overdrive</strong><br>
                Surges observed in 2019, 2022, and 2026 reflect national telecom upgrades (4G rollouts, pandemic hardware replacements, and 5G/IoT device lifecycles).
            </div>
            <div style="background:white; padding:1.1rem; border-radius:12px; border:1px solid #ccfbf1; box-shadow: 0 2px 8px rgba(5, 150, 105, 0.05);">
                <strong style="color:#047857;">2. The 50% Collection Ceiling</strong><br>
                While generation doubled, authorized collection efficiency flatlined at ~48.5% to 54.0%. Over half of all discarded hardware bypasses municipal oversight.
            </div>
            <div style="background:white; padding:1.1rem; border-radius:12px; border:1px solid #ccfbf1; box-shadow: 0 2px 8px rgba(5, 150, 105, 0.05);">
                <strong style="color:#047857;">3. 140x Urban Disparity</strong><br>
                Metros average 141.32 Tons/Day per report, whereas Tier-3 centers log only 1.01 Tons/Day. High-tech obsolescence is hyper-concentrated in commercial capitals.
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# TAB 3: ECO-POLICY SIMULATOR
# ------------------------------------------------------------------------------
with tab_sim:
    st.markdown("### Interactive Circularity & Resource Recovery Policy Simulator")
    st.caption("Simulate policy interventions (EPR take-backs, informal buyback incentives, hydrometallurgical recycling targets) to project recovered materials, toxic leak prevention, and CO₂ abatement.")
    
    sim_col1, sim_col2 = st.columns([5, 7])
    
    with sim_col1.container(border=True):
        st.markdown("#### Policy Target Controls")
        
        baseline_col = 51.0
        baseline_rec = 43.0
        
        sim_col_target = st.slider(
            "Target Municipal Collection Efficiency (%)",
            min_value=50,
            max_value=95,
            value=75,
            step=1
        )
        
        sim_rec_target = st.slider(
            "Formal Hydrometallurgical Recycling Rate (%)",
            min_value=40,
            max_value=90,
            value=70,
            step=1
        )
        
        sim_incentive = st.select_slider(
            "Informal Sector Formalization & Buyback Incentive",
            options=["Baseline (No Subsidy)", "Tier 1 (₹15/kg)", "Tier 2 (₹35/kg)", "Tier 3 Aggressive EPR (₹60/kg)"],
            value="Tier 2 (₹35/kg)"
        )
        
    active_daily_tonnage = ew_20k[ew_20k["Year"] == 2026]["Daily_Waste_Generation_Tons"].sum()
    if active_daily_tonnage <= 0:
        active_daily_tonnage = 1716.08
        
    baseline_collected_daily = active_daily_tonnage * (baseline_col / 100.0)
    sim_collected_daily = active_daily_tonnage * (sim_col_target / 100.0)
    
    annual_diverted_tons = max(0, (sim_collected_daily - baseline_collected_daily) * 365)
    heavy_metals_prevented_tons = annual_diverted_tons * 0.02
    co2_saved_tons = annual_diverted_tons * 1.44
    recovered_value_cr = (annual_diverted_tons * (sim_rec_target / 100.0) * 280000) / 10000000
    
    recovered_copper_tons = annual_diverted_tons * 0.15 * (sim_rec_target / 100.0)
    recovered_gold_kg = annual_diverted_tons * 0.00005 * 1000 * (sim_rec_target / 100.0)
    
    circularity_index = (sim_col_target * 0.5) + (sim_rec_target * 0.5)
    
    with sim_col2.container(border=True):
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=circularity_index,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "<b>Projected National Circularity Index</b>", 'font': {'size': 18, 'color': '#064e3b'}},
            delta={'reference': (baseline_col * 0.5 + baseline_rec * 0.5), 'increasing': {'color': "#059669"}},
            gauge={
                'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "#047857"},
                'bar': {'color': "#059669"},
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "#d1fae5",
                'steps': [
                    {'range': [0, 45], 'color': '#fee2e2'},
                    {'range': [45, 70], 'color': '#fef3c7'},
                    {'range': [70, 100], 'color': '#d1fae5'}
                ],
                'threshold': {
                    'line': {'color': "#047857", 'width': 4},
                    'thickness': 0.8,
                    'value': circularity_index
                }
            }
        ))
        fig_gauge.update_layout(height=260, margin=dict(l=20, r=20, t=30, b=20), paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_gauge, use_container_width=True)
        
    st.markdown("---")
    s_cols = st.columns(4)
    
    with s_cols[0].container(border=True):
        st.metric("Annual Diversion", f"+{annual_diverted_tons:,.0f} Tons", "Rescued from open dumps", delta_color="normal")
    with s_cols[1].container(border=True):
        st.metric("Toxins Contained", f"{heavy_metals_prevented_tons:,.1f} Tons", "Lead & Mercury safely managed", delta_color="inverse")
    with s_cols[2].container(border=True):
        st.metric("Recovered Value", f"₹{recovered_value_cr:,.1f} Cr", "Critical mineral value", delta_color="normal")
    with s_cols[3].container(border=True):
        st.metric("CO₂ Emissions Avoided", f"{co2_saved_tons:,.0f} Tons", "Virgin mining avoided", delta_color="normal")
        
    metals_df = pd.DataFrame({
        "Critical_Material": ["Copper (Tons)", "Recovered Gold (kg)", "Lead/Cadmium Prevented (Tons)", "CO₂ Avoided (100 Tons)"],
        "Quantity": [recovered_copper_tons, recovered_gold_kg, heavy_metals_prevented_tons, co2_saved_tons / 100.0]
    })
    
    fig_metals = px.bar(
        metals_df,
        x="Critical_Material",
        y="Quantity",
        color="Critical_Material",
        color_discrete_sequence=ECO_PALETTE,
        title="<b>Simulated Strategic Material Recovery & Pollution Abatement Yield</b>"
    )
    fig_metals.update_layout(
        height=360,
        margin=dict(l=30, r=30, t=50, b=30),
        showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    st.plotly_chart(fig_metals, use_container_width=True)

# ------------------------------------------------------------------------------
# TAB 4: DISTRIBUTIONS & OUTLIERS
# ------------------------------------------------------------------------------
with tab_univariate:
    st.markdown("### Univariate Distributions & Outlier Spread")
    col_u1, col_u2 = st.columns(2)
    waste_metric = "Daily_Waste_Generation_Tons"
    
    with col_u1.container(border=True):
        st.subheader("Distribution & Density")
        use_log = st.checkbox("Apply Log Scale (X-axis)", value=False)
        plot_data = filtered_20k[waste_metric].dropna()
        xlab = f"log(1 + {waste_metric})" if use_log else waste_metric
        if use_log:
            plot_data = np.log1p(plot_data)
            
        fig_hist = px.histogram(
            x=plot_data,
            nbins=35,
            marginal="box",
            color_discrete_sequence=["#059669"],
            labels={"x": xlab, "y": "Frequency Count"},
            title=f"Distribution Profile of {xlab}"
        )
        fig_hist.update_layout(height=380, margin=dict(l=20, r=20, t=40, b=20), paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_hist, use_container_width=True)
        
    with col_u2.container(border=True):
        st.subheader("Outlier Spread Across City Tiers")
        fig_box = px.box(
            filtered_20k,
            x="City_Category",
            y=waste_metric,
            color="City_Category",
            color_discrete_sequence=ECO_PALETTE,
            points="outliers",
            title=f"Outlier Spread Across City Tiers ({waste_metric})"
        )
        fig_box.update_layout(height=380, margin=dict(l=20, r=20, t=40, b=20), showlegend=False, paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_box, use_container_width=True)

# ------------------------------------------------------------------------------
# TAB 5: WASTE COMPOSITION
# ------------------------------------------------------------------------------
with tab_comp:
    st.markdown("### Part-to-Whole Composition Analysis")
    col_p1, col_p2 = st.columns([5, 7])
    
    with col_p1.container(border=True):
        cat_counts = wm_20k_df["Waste_Type"].value_counts().reset_index()
        cat_counts.columns = ["Waste_Type", "Record_Count"]
        fig_donut = px.pie(
            cat_counts,
            values="Record_Count",
            names="Waste_Type",
            hole=0.6,
            title="<b>Proportional Share of Waste Classes</b>",
            color_discrete_sequence=ECO_PALETTE
        )
        fig_donut.update_traces(textposition='inside', textinfo='percent+label')
        fig_donut.update_layout(height=420, margin=dict(l=10, r=10, t=40, b=10), showlegend=False, paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_donut, use_container_width=True)
        
    with col_p2.container(border=True):
        yearly_comp = wm_20k_df.groupby(["Year", "Waste_Type"])["Daily_Waste_Generation_Tons"].sum().reset_index()
        fig_area = px.bar(
            yearly_comp,
            x="Year",
            y="Daily_Waste_Generation_Tons",
            color="Waste_Type",
            title="<b>Longitudinal Tonnage Shift (2015 - 2026)</b>",
            color_discrete_sequence=ECO_PALETTE
        )
        fig_area.update_layout(height=420, margin=dict(l=10, r=10, t=40, b=10), paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_area, use_container_width=True)

# ------------------------------------------------------------------------------
# TAB 6: REGRESSION & TRENDS
# ------------------------------------------------------------------------------
with tab_regression:
    st.markdown("### Bivariate, Regression & Multivariate Bubble Analysis")
    col_m1, col_m2 = st.columns(2)
    
    with col_m1.container(border=True):
        sample_size = min(1500, len(filtered_20k))
        sample_reg = filtered_20k.sample(n=sample_size, random_state=42) if sample_size > 0 else filtered_20k
        fig_reg = px.scatter(
            sample_reg,
            x="Population_Density",
            y="Daily_Waste_Generation_Tons",
            trendline="ols",
            trendline_color_override="#ef4444",
            opacity=0.55,
            color_discrete_sequence=["#059669"],
            title=f"OLS Trend: Population Density vs Daily Waste (n={sample_size})",
            labels={"Population_Density": "Population Density (People/km²)", "Daily_Waste_Generation_Tons": "Daily Waste (Tons)"}
        )
        fig_reg.update_layout(height=420, margin=dict(l=20, r=20, t=40, b=20), paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_reg, use_container_width=True)
        
    with col_m2.container(border=True):
        sample_bubble = filtered_20k.sample(n=min(400, len(filtered_20k)), random_state=42) if len(filtered_20k) > 0 else filtered_20k
        fig_bubble = px.scatter(
            sample_bubble,
            x="Population_Density",
            y="Daily_Waste_Generation_Tons",
            size="Urbanization_Rate",
            color="City_Category",
            hover_name="City",
            hover_data=["State", "Year", "Urbanization_Rate", "Recycling_Rate"],
            size_max=30,
            opacity=0.8,
            title="Bubble: Density vs Waste (Sized by Urbanization Rate)",
            labels={"Population_Density": "Density (People/km²)", "Daily_Waste_Generation_Tons": "Daily Waste (Tons)"},
            color_discrete_sequence=ECO_PALETTE
        )
        fig_bubble.update_layout(height=420, margin=dict(l=20, r=20, t=40, b=20), paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_bubble, use_container_width=True)

# ------------------------------------------------------------------------------
# TAB 7: CORRELATION HEATMAP
# ------------------------------------------------------------------------------
with tab_corr:
    st.markdown("### Correlation Matrix Heatmap & Collinearity")
    numeric_candidates = [
        "Population", "Population_Density", "Urbanization_Rate",
        "Daily_Waste_Generation_Tons", "Collection_Efficiency_Percentage",
        "Recycling_Rate", "Municipal_Efficiency_Score", "Air_Quality_Index"
    ]
    avail_num_cols = [c for c in numeric_candidates if c in filtered_20k.columns]
    
    col_k1, col_k2 = st.columns([6, 6])
    
    with col_k1.container(border=True):
        corr_mat = filtered_20k[avail_num_cols].corr()
        fig_heat = px.imshow(
            corr_mat,
            text_auto=".2f",
            aspect="auto",
            color_continuous_scale=[[0, "#dc2626"], [0.5, "#f8fafc"], [1, "#059669"]],
            zmin=-1,
            zmax=1,
            title="<b>Correlation Heatmap (Pearson)</b>"
        )
        fig_heat.update_layout(height=450, margin=dict(l=20, r=20, t=40, b=20), paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_heat, use_container_width=True)
        
    with col_k2.container(border=True):
        sample_density = filtered_20k.sample(min(3000, len(filtered_20k)), random_state=42) if len(filtered_20k) > 0 else filtered_20k
        fig_density = px.density_heatmap(
            sample_density,
            x="Urbanization_Rate",
            y="Daily_Waste_Generation_Tons",
            nbinsx=25,
            nbinsy=25,
            color_continuous_scale=[[0, "#ecfdf5"], [0.5, "#34d399"], [1, "#064e3b"]],
            title="<b>Joint 2D Density: Urbanization vs Daily Waste</b>",
            labels={"Urbanization_Rate": "Urbanization Rate (%)", "Daily_Waste_Generation_Tons": "Daily Waste (Tons)"}
        )
        fig_density.update_layout(height=450, margin=dict(l=20, r=20, t=40, b=20), paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_density, use_container_width=True)

# ------------------------------------------------------------------------------
# TAB 8: GEOSPATIAL & CITY AUDIT
# ------------------------------------------------------------------------------
with tab_geo:
    st.markdown("### Geospatial Mapping & Interactive City Audit")
    
    city_map_data = filtered_combined.groupby(["City", "State", "Region", "Latitude", "Longitude"]).agg(
        Total_Waste=("Daily_Waste_Generation_Tons", "sum"),
        Mean_Waste=("Daily_Waste_Generation_Tons", "mean"),
        Collection_Eff=("Collection_Efficiency_Percentage", "mean"),
        Recycling_Rate=("Recycling_Rate", "mean")
    ).reset_index()
    
    with st.container(border=True):
        try:
            if hasattr(px, "scatter_map"):
                fig_map = px.scatter_map(
                    city_map_data,
                    lat="Latitude",
                    lon="Longitude",
                    hover_name="City",
                    hover_data=["State", "Region", "Total_Waste", "Collection_Eff", "Recycling_Rate"],
                    size="Total_Waste",
                    color="Collection_Eff",
                    color_continuous_scale=[[0, "#fca5a5"], [0.5, "#fde047"], [1, "#059669"]],
                    size_max=35,
                    zoom=3.8,
                    center=dict(lat=21.7679, lon=78.8718),
                    map_style="open-street-map",
                    title="<b>Indian Cities: Bubble Size = Daily Waste, Color = Collection Efficiency (%)</b>"
                )
                fig_map.update_layout(height=520, margin=dict(l=10, r=10, t=40, b=10))
                st.plotly_chart(fig_map, use_container_width=True)
            elif hasattr(px, "scatter_mapbox"):
                fig_map = px.scatter_mapbox(
                    city_map_data,
                    lat="Latitude",
                    lon="Longitude",
                    hover_name="City",
                    hover_data=["State", "Region", "Total_Waste", "Collection_Eff", "Recycling_Rate"],
                    size="Total_Waste",
                    color="Collection_Eff",
                    color_continuous_scale=[[0, "#fca5a5"], [0.5, "#fde047"], [1, "#059669"]],
                    size_max=35,
                    zoom=3.8,
                    center=dict(lat=21.7679, lon=78.8718),
                    mapbox_style="open-street-map",
                    title="<b>Indian Cities: Bubble Size = Daily Waste, Color = Collection Efficiency (%)</b>"
                )
                fig_map.update_layout(height=520, margin=dict(l=10, r=10, t=40, b=10))
                st.plotly_chart(fig_map, use_container_width=True)
            else:
                st.map(city_map_data, latitude="Latitude", longitude="Longitude", size="Total_Waste")
        except Exception:
            st.map(city_map_data, latitude="Latitude", longitude="Longitude", size="Total_Waste")
            
    st.markdown("---")
    
    # City Audit
    available_cities = sorted(wm_20k_df["City"].dropna().unique().tolist())
    selected_drill_city = st.selectbox(
        "Select a City for Detailed Demographic & Waste Audit:",
        options=available_cities,
        index=available_cities.index("Mumbai") if "Mumbai" in available_cities else 0
    )
    
    city_df = wm_20k_df[wm_20k_df["City"] == selected_drill_city]
    city_ew = city_df[city_df["Waste_Type"] == "E-Waste"]
    
    if len(city_df) > 0:
        c_kpi1, c_kpi2, c_kpi3, c_kpi4 = st.columns(4)
        with c_kpi1.container(border=True):
            st.metric("Classification", f"{city_df['City_Category'].iloc[0]}", f"Region: {city_df['Region'].iloc[0]}")
        with c_kpi2.container(border=True):
            st.metric("Mean Daily Waste", f"{city_df['Daily_Waste_Generation_Tons'].mean():.1f} Tons", f"State: {city_df['State'].iloc[0]}")
        with c_kpi3.container(border=True):
            coll_val = city_df['Collection_Efficiency_Percentage'].mean()
            st.metric("Collection Efficiency", f"{coll_val:.1f}%", f"{'Above' if coll_val >= 50 else 'Below'} National Average")
        with c_kpi4.container(border=True):
            rec_val = city_df['Recycling_Rate'].mean()
            st.metric("Formal Recycling Rate", f"{rec_val:.1f}%", f"{'Good' if rec_val > 50 else 'Lagging'}")
            
        if len(city_ew) > 0:
            with st.container(border=True):
                city_yearly = city_ew.groupby("Year")["Daily_Waste_Generation_Tons"].mean().reset_index()
                fig_city_trend = px.line(
                    city_yearly,
                    x="Year",
                    y="Daily_Waste_Generation_Tons",
                    markers=True,
                    color_discrete_sequence=["#059669"],
                    title=f"<b>Historical Daily E-Waste Generation in {selected_drill_city} (2015 – 2026)</b>"
                )
                fig_city_trend.update_layout(height=320, margin=dict(l=20, r=20, t=40, b=20), paper_bgcolor="rgba(0,0,0,0)")
                st.plotly_chart(fig_city_trend, use_container_width=True)

# ------------------------------------------------------------------------------
# TAB 9: DATA EXPLORER & EXPORT
# ------------------------------------------------------------------------------
with tab_explorer:
    st.markdown("### Interactive Data Explorer & Export")
    search_term = st.text_input("Quick Search (City, State, or Waste Type)", placeholder="Type to filter records...")
    
    display_df = filtered_20k.copy()
    if search_term:
        search_mask = (
            display_df["City"].astype(str).str.contains(search_term, case=False, na=False) |
            display_df["State"].astype(str).str.contains(search_term, case=False, na=False) |
            display_df["Waste_Type"].astype(str).str.contains(search_term, case=False, na=False)
        )
        display_df = display_df[search_mask]
        
    st.write(f"Showing **{len(display_df):,}** matching observations:")
    
    default_show_cols = [
        "Record_ID", "City", "State", "Region", "City_Category", "Year",
        "Waste_Type", "Daily_Waste_Generation_Tons", "Collection_Efficiency_Percentage",
        "Recycling_Rate", "Population_Density", "Municipal_Efficiency_Score"
    ]
    show_cols = st.multiselect("Customize Columns to Display", options=display_df.columns.tolist(), default=default_show_cols)
    
    # PRO TIP 10: Streamlit Dataframe with Native Column Config
    st.dataframe(display_df[show_cols].head(500), use_container_width=True)
    
    csv_bytes = display_df[show_cols].to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Filtered Data as CSV",
        data=csv_bytes,
        file_name=f"ewaste_analysis_filtered_{selected_years[0]}_{selected_years[1]}.csv",
        mime="text/csv",
        icon=":material/download:",
        use_container_width=True
    )

# ------------------------------------------------------------------------------
# TAB 10: POLICY & ENGINEERING
# ------------------------------------------------------------------------------
with tab_notes:
    st.markdown("### Data Engineering Post-Mortem & Policy Framework")
    col_pm1, col_pm2 = st.columns(2)
    
    with col_pm1.container(border=True):
        st.markdown("""
        #### Data Engineering Post-Mortem: What Broke & Why
        
        * **The Problem:** The recycling dataset designated the urban area under `'City/District'`, whereas the longitudinal 20K dataset labeled it `'City'`.
        * **The Bug:** A downstream Seaborn call attempted to reference `'City/District'` inside `wm_20k_df`, throwing a `KeyError: 'City/District'`.
        * **The Resolution:** Harmonized headers immediately upon ingest:
          ```python
          if "City/District" in wm_recycling_df.columns:
              wm_recycling_df.rename(columns={"City/District": "City"}, inplace=True)
          ```
        * **Relational Integrity:** Implemented an inner join between `wm_20k_df` and `cities_master.csv` on `['City', 'State']`, pulling geographic coordinates (`Latitude`, `Longitude`) and special demographic flags (`Is_Tourist`, `Is_Hill_Station`).
        """)
        
    with col_pm2.container(border=True):
        st.markdown("""
        #### Evidence-Based Policy Framework
        
        1. **The Core Crisis is Collection, Not Generation:**
           Generation inevitably scales with consumer electronics adoption (7.56% CAGR). However, collection efficiency remains frozen at ~50%. Policies targeting consumer awareness without collection infrastructure will fail.
           
        2. **Extended Producer Responsibility (EPR) Corridors:**
           Over 60% of electronic waste originates in Metro hubs (Mumbai, Delhi, Bengaluru, Kolkata, Chennai). EPR take-back centers and certified e-stewards must be clustered in these high-density nodes.
           
        3. **Formalizing the Informal Scrap Network (Kabadiwalas):**
           Because 90%+ of hardware routes through informal scrap merchants, municipal governments should offer subsidized testing, protective gear, and guaranteed buy-back rates to route hardware to authorized hydrometallurgical extraction plants.
        """)
        
    st.markdown("---")
    st.markdown("""
    <div style="text-align:center; padding:1.2rem 0; color:#64748b; font-size:0.9rem;">
        <strong>India E-Waste Growth Analytics & Peer Benchmarking Platform</strong><br>
        Group No.: 24 • Batch INFT-C • Department of Information Technology<br>
        Built by <strong>Ruhaan Joshi (24101C0057)</strong>, <strong>Om Thakur (24101C0041)</strong>, and <strong>Rudra Jain (24101C0062)</strong>
    </div>
    """, unsafe_allow_html=True)
