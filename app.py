import os
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import seaborn as sns

# ==============================================================================
# PAGE CONFIGURATION & ECO-FRIENDLY AESTHETICS
# ==============================================================================
st.set_page_config(
    page_title="India E-Waste Growth Analytics & Circularity Dashboard",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for rich eco-friendly design system, micro-animations, and glassmorphic styling
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

    @keyframes subtleFloat {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-4px); }
        100% { transform: translateY(0px); }
    }

    /* Eco-Friendly Animated Header Banner */
    .main-header {
        background: linear-gradient(135deg, #022c22 0%, #064e3b 25%, #047857 50%, #059669 75%, #10b981 100%);
        background-size: 250% 250%;
        animation: gradientFlow 12s ease infinite;
        padding: 2.3rem 2.6rem;
        border-radius: 20px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 14px 30px -6px rgba(5, 150, 105, 0.35);
        border: 1px solid rgba(52, 211, 153, 0.3);
        position: relative;
        overflow: hidden;
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
        gap: 0.55rem;
        margin-top: 0.6rem;
    }
    .badge {
        background: rgba(255, 255, 255, 0.16);
        backdrop-filter: blur(10px);
        padding: 0.38rem 0.9rem;
        border-radius: 9999px;
        font-size: 0.82rem;
        font-weight: 600;
        border: 1px solid rgba(255, 255, 255, 0.28);
        transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .badge:hover {
        background: rgba(255, 255, 255, 0.28);
        transform: translateY(-2px);
    }

    /* Live Eco-Status Tag */
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

    /* Interactive Metric Cards with Gradient Accent & Micro-Hover Lift */
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
        transition: height 0.25s ease;
    }
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 16px 32px -6px rgba(5, 150, 105, 0.22);
        border-color: rgba(16, 185, 129, 0.5);
    }
    .metric-card:hover::before {
        height: 6px;
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

    /* The Feynman Explanatory Container */
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
    .feynman-box h4 {
        color: #065f46;
        font-weight: 700;
        margin-top: 0;
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
</style>
""", unsafe_allow_html=True)

# Custom color palette for Plotly figures
ECO_PALETTE = ["#059669", "#10b981", "#34d399", "#0284c7", "#f59e0b", "#8b5cf6", "#ec4899", "#6366f1"]

# ==============================================================================
# DATA LOADING & PREPROCESSING (CACHED)
# ==============================================================================
@st.cache_data(show_spinner=True)
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
    
    # Standardize column headers
    for df in [cities_df, wm_rec_df, wm_20k_df]:
        df.columns = df.columns.str.strip()
        
    # Harmonize City identifier
    if "City/District" in wm_rec_df.columns:
        wm_rec_df.rename(columns={"City/District": "City"}, inplace=True)
        
    # Relational merge with cities_master for geospatial and regional flags
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
# SIDEBAR FILTERS & CONTROLS
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
    
    analysis_mode = st.radio(
        "Focus Dataset Scope",
        options=["E-Waste Focus (Core Longitudinal Study)", "All Waste Classifications (Comparative)"],
        index=0
    )
    is_ewaste_only = "E-Waste Focus" in analysis_mode
    
    st.markdown("---")
    
    # Year Range Slider
    min_year = int(wm_20k_df["Year"].min())
    max_year = int(wm_20k_df["Year"].max())
    selected_years = st.slider(
        "Observation Time Window",
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year),
        step=1
    )
    
    # Geographic Region Multi-select
    all_regions = sorted(wm_20k_df["Region"].dropna().unique().tolist())
    selected_regions = st.multiselect(
        "Geographic Regions",
        options=all_regions,
        default=all_regions
    )
    
    # City Tier Filter
    all_categories = sorted(wm_20k_df["City_Category"].dropna().unique().tolist())
    selected_categories = st.multiselect(
        "City Tiers",
        options=all_categories,
        default=all_categories
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
        st.rerun()

# Apply Filters
mask = (
    (wm_20k_df["Year"].between(selected_years[0], selected_years[1])) &
    (wm_20k_df["Region"].isin(selected_regions)) &
    (wm_20k_df["City_Category"].isin(selected_categories)) &
    (wm_20k_df["Waste_Type"].isin(selected_waste_types))
)
filtered_20k = wm_20k_df[mask]

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
    <p>An interactive data analytics platform analyzing electronic waste accumulation, regional growth trajectories, municipal infrastructure bottlenecks, and circular recovery potential across Indian urban centers.</p>
    <div class="badge-container">
        <span class="badge">Ruhaan Joshi (24101C0057)</span>
        <span class="badge">Om Thakur (24101C0041)</span>
        <span class="badge">Rudra Jain (24101C0062)</span>
        <span class="badge">INFT-C Batch 3</span>
        <span class="badge">2015 – 2026 Longitudinal Study</span>
        <span class="badge">25,200+ Municipal Records</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# TOP-LEVEL KPI METRICS
# ==============================================================================
col1, col2, col3, col4, col5 = st.columns(5)

total_tonnage = filtered_20k["Daily_Waste_Generation_Tons"].sum()
mean_daily = filtered_20k["Daily_Waste_Generation_Tons"].mean() if len(filtered_20k) > 0 else 0
avg_collection = filtered_20k["Collection_Efficiency_Percentage"].mean() if len(filtered_20k) > 0 else 0
avg_recycling = filtered_20k["Recycling_Rate"].mean() if len(filtered_20k) > 0 else 0

ew_2015 = ew_20k[ew_20k["Year"] == 2015]["Daily_Waste_Generation_Tons"].sum()
ew_2026 = ew_20k[ew_20k["Year"] == 2026]["Daily_Waste_Generation_Tons"].sum()
cagr_val = ((ew_2026 / ew_2015) ** (1 / 11) - 1) * 100 if ew_2015 > 0 else 7.56

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Cumulative Daily Tonnage</div>
        <div class="metric-value">{total_tonnage:,.1f}</div>
        <div class="metric-delta delta-up">Filtered Active Volume (Tons/Day)</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Mean Daily Generation</div>
        <div class="metric-value">{mean_daily:.2f} <span style="font-size:1rem;color:#64748b;">Tons</span></div>
        <div class="metric-delta delta-neutral">Per Reporting Center</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">11-Year Growth (CAGR)</div>
        <div class="metric-value">+{cagr_val:.2f}%</div>
        <div class="metric-delta delta-up">2015 (770 T/D) → 2026 (1,716 T/D)</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Collection Efficiency</div>
        <div class="metric-value">{avg_collection:.1f}%</div>
        <div class="metric-delta delta-up">Stagnant Collection Ceiling</div>
    </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Formal Recycling Rate</div>
        <div class="metric-value">{avg_recycling:.1f}%</div>
        <div class="metric-delta delta-eco">>50% Informal Sector Leakage</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ==============================================================================
# MAIN TABS ARCHITECTURE
# ==============================================================================
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs([
    "Overview & Growth",
    "Eco-Policy Simulator",
    "Distributions & Outliers",
    "Waste Composition",
    "Regression & Trends",
    "Correlation & Collinearity",
    "Geospatial & City Inspector",
    "Data Explorer & Export",
    "Policy & Engineering"
])

# ------------------------------------------------------------------------------
# TAB 1: OVERVIEW & E-WASTE GROWTH TRENDS
# ------------------------------------------------------------------------------
with tab1:
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
    
    with c1:
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
            height=430,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig_trend, use_container_width=True)
        
    with c2:
        state_ew = ew_20k.groupby("State")["Daily_Waste_Generation_Tons"].agg(["sum", "mean"]).sort_values(by="sum", ascending=True).tail(8)
        fig_state = px.bar(
            state_ew,
            x="sum",
            y=state_ew.index,
            orientation="h",
            color="sum",
            color_continuous_scale=[[0, "#a7f3d0"], [0.5, "#10b981"], [1, "#064e3b"]],
            title="<b>Top E-Waste Generating States (Cumulative Daily Tons)</b>",
            labels={"sum": "Total Daily Tons", "State": "State"}
        )
        fig_state.update_layout(
            height=430,
            margin=dict(l=20, r=20, t=60, b=40),
            coloraxis_showscale=False,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig_state, use_container_width=True)
        
    # Feynman Concept Card
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
    
    with st.expander("View Detailed Longitudinal E-Waste Metrics (2015 - 2026)"):
        display_yearly = yearly_stats.rename(columns={
            "Year": "Year",
            "records": "Observations Count",
            "total_daily_tons": "Total Daily (Tons)",
            "mean_daily_tons": "Mean Daily (Tons)",
            "median_daily_tons": "Median Daily (Tons)",
            "recycling_rate": "Recycling Rate (%)",
            "collection_eff": "Collection Eff (%)",
            "budget": "Mean Municipal Budget (INR)"
        })
        st.dataframe(
            display_yearly.style.format({
                "Total Daily (Tons)": "{:,.2f}",
                "Mean Daily (Tons)": "{:.2f}",
                "Median Daily (Tons)": "{:.2f}",
                "Recycling Rate (%)": "{:.1f}%",
                "Collection Eff (%)": "{:.1f}%",
                "Mean Municipal Budget (INR)": "₹{:,.0f}"
            }),
            use_container_width=True
        )

# ------------------------------------------------------------------------------
# TAB 2: INTERACTIVE ECO-POLICY SIMULATOR & CIRCULAR ECONOMY CALCULATOR
# ------------------------------------------------------------------------------
with tab2:
    st.markdown("### Interactive Circularity & Resource Recovery Policy Simulator")
    st.caption("Simulate policy interventions (EPR take-backs, informal buyback incentives, hydrometallurgical recycling targets) to project recovered materials, toxic leak prevention, and CO₂ abatement.")
    
    sim_col1, sim_col2 = st.columns([5, 7])
    
    with sim_col1:
        st.markdown("#### Policy Target Controls")
        
        baseline_col = 51.0
        baseline_rec = 43.0
        
        sim_col_target = st.slider(
            "Target Municipal Collection Efficiency (%)",
            min_value=50,
            max_value=95,
            value=75,
            step=1,
            help="Percentage of generated electronic waste successfully aggregated into authorized municipal channels."
        )
        
        sim_rec_target = st.slider(
            "Formal Hydrometallurgical Recycling Rate (%)",
            min_value=40,
            max_value=90,
            value=70,
            step=1,
            help="Percentage of collected e-waste dismantled via certified zero-emission recovery facilities."
        )
        
        sim_incentive = st.select_slider(
            "Informal Sector Formalization & Buyback Incentive",
            options=["Baseline (No Subsidy)", "Tier 1 (₹15/kg)", "Tier 2 (₹35/kg)", "Tier 3 Aggressive EPR (₹60/kg)"],
            value="Tier 2 (₹35/kg)"
        )
        
        st.info("💡 **Did You Know?** 1 metric ton of discarded printed circuit boards contains up to 800x more gold than 1 ton of raw mined gold ore. Capturing this urban mine cuts heavy metal poisoning and avoids virgin extraction.")
        
    # Empirical calculation model
    active_daily_tonnage = ew_20k[ew_20k["Year"] == 2026]["Daily_Waste_Generation_Tons"].sum()
    if active_daily_tonnage <= 0:
        active_daily_tonnage = 1716.08
        
    # Baseline vs Target
    baseline_collected_daily = active_daily_tonnage * (baseline_col / 100.0)
    sim_collected_daily = active_daily_tonnage * (sim_col_target / 100.0)
    
    annual_diverted_tons = (sim_collected_daily - baseline_collected_daily) * 365
    annual_diverted_tons = max(0, annual_diverted_tons)
    
    # Heavy metal prevention (~2% lead, mercury, cadmium, arsenic)
    heavy_metals_prevented_tons = annual_diverted_tons * 0.02
    
    # CO2 saved (1.44 tons CO2-eq saved per ton formally recycled)
    co2_saved_tons = annual_diverted_tons * 1.44
    
    # Economic mineral recovery value (estimate ~₹2.8 Lakhs/ton mixed e-waste via hydrometallurgy)
    recovered_value_cr = (annual_diverted_tons * (sim_rec_target / 100.0) * 280000) / 10000000
    
    # Critical metal yield
    recovered_copper_tons = annual_diverted_tons * 0.15 * (sim_rec_target / 100.0)
    recovered_gold_kg = annual_diverted_tons * 0.00005 * 1000 * (sim_rec_target / 100.0)
    
    # Circularity Index Score (0 to 100)
    circularity_index = (sim_col_target * 0.5) + (sim_rec_target * 0.5)
    
    with sim_col2:
        # Circularity Gauge Chart
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
        fig_gauge.update_layout(height=280, margin=dict(l=20, r=20, t=40, b=20), paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_gauge, use_container_width=True)
        
    st.markdown("---")
    st.markdown("#### Projected Annual Eco-Impact & Material Recovery")
    
    s_col1, s_col2, s_col3, s_col4 = st.columns(4)
    
    with s_col1:
        st.markdown(f"""
        <div class="sim-card">
            <div class="sim-lbl">Annual Landfill Diversion</div>
            <div class="sim-val">+{annual_diverted_tons:,.0f}</div>
            <span style="font-size:0.75rem; color:#059669; font-weight:700;">Metric Tons Rescued/Year</span>
        </div>
        """, unsafe_allow_html=True)
        
    with s_col2:
        st.markdown(f"""
        <div class="sim-card">
            <div class="sim-lbl">Toxic Metals Prevented</div>
            <div class="sim-val">{heavy_metals_prevented_tons:,.1f}</div>
            <span style="font-size:0.75rem; color:#dc2626; font-weight:700;">Tons Lead & Mercury Contained</span>
        </div>
        """, unsafe_allow_html=True)
        
    with s_col3:
        st.markdown(f"""
        <div class="sim-card">
            <div class="sim-lbl">Recovered Materials Value</div>
            <div class="sim-val">₹{recovered_value_cr:,.1f} Cr</div>
            <span style="font-size:0.75rem; color:#d97706; font-weight:700;">Precious & Base Metals Yield</span>
        </div>
        """, unsafe_allow_html=True)
        
    with s_col4:
        st.markdown(f"""
        <div class="sim-card">
            <div class="sim-lbl">CO₂ Abatement</div>
            <div class="sim-val">{co2_saved_tons:,.0f}</div>
            <span style="font-size:0.75rem; color:#0284c7; font-weight:700;">Tons CO₂e Virgin Mining Avoided</span>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Material Recovery Breakdown Chart
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
        height=380,
        margin=dict(l=30, r=30, t=50, b=30),
        showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    st.plotly_chart(fig_metals, use_container_width=True)

# ------------------------------------------------------------------------------
# TAB 3: UNIVARIATE & OUTLIER DISTRIBUTIONS
# ------------------------------------------------------------------------------
with tab3:
    st.markdown("### Univariate Distributions & Outlier Spread")
    st.caption("Analyzing distribution skewness, log-transformed profiles, and extreme high-tonnage metro outliers.")
    
    col_u1, col_u2 = st.columns(2)
    waste_metric = "Daily_Waste_Generation_Tons"
    
    with col_u1:
        st.subheader("Distribution & Density")
        use_log = st.checkbox("Apply Log Scale (X-axis)", value=False)
        
        plot_data = filtered_20k[waste_metric].dropna()
        if use_log:
            plot_data = np.log1p(plot_data)
            xlab = f"log(1 + {waste_metric})"
        else:
            xlab = waste_metric
            
        fig_hist = px.histogram(
            x=plot_data,
            nbins=35,
            marginal="box",
            color_discrete_sequence=["#059669"],
            labels={"x": xlab, "y": "Frequency Count"},
            title=f"Distribution Profile of {xlab}"
        )
        fig_hist.update_layout(
            height=420,
            margin=dict(l=30, r=30, t=50, b=30),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig_hist, use_container_width=True)
        
    with col_u2:
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
        fig_box.update_layout(
            height=420,
            margin=dict(l=30, r=30, t=50, b=30),
            showlegend=False,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig_box, use_container_width=True)
        
    st.markdown("---")
    st.subheader("Categorical Rankings & Grouped Comparisons")
    
    col_c1, col_c2 = st.columns(2)
    
    with col_c1:
        top_n = st.slider("Select Top N Cities to Rank", min_value=5, max_value=25, value=10)
        top_cities_rec = (
            wm_rec_df.groupby("City")["Waste Generated (Tons/Day)"]
            .mean()
            .nlargest(top_n)
            .reset_index()
        )
        fig_top = px.bar(
            top_cities_rec,
            x="Waste Generated (Tons/Day)",
            y="City",
            orientation="h",
            color="Waste Generated (Tons/Day)",
            color_continuous_scale=[[0, "#6ee7b7"], [1, "#065f46"]],
            title=f"Top {top_n} Cities by Mean Waste Generated (Recycling Dataset)"
        )
        fig_top.update_layout(
            yaxis=dict(autorange="reversed"),
            height=460,
            margin=dict(l=30, r=30, t=50, b=30),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig_top, use_container_width=True)
        
    with col_c2:
        top_5_cities = wm_20k_df["City"].value_counts().head(5).index.tolist()
        sample_city_df = wm_20k_df[wm_20k_df["City"].isin(top_5_cities)]
        grouped_agg = sample_city_df.groupby(["City", "Waste_Type"])["Daily_Waste_Generation_Tons"].mean().reset_index()
        
        fig_grp = px.bar(
            grouped_agg,
            x="City",
            y="Daily_Waste_Generation_Tons",
            color="Waste_Type",
            barmode="group",
            title="Mean Daily Waste Generation Grouped by City & Waste Type",
            color_discrete_sequence=ECO_PALETTE
        )
        fig_grp.update_layout(
            height=460,
            margin=dict(l=30, r=30, t=50, b=30),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig_grp, use_container_width=True)
        
    if view_static_plots:
        st.markdown("#### Original Matplotlib / Seaborn Visualizations")
        fig_sns, axes_sns = plt.subplots(1, 2, figsize=(14, 4.5))
        sns.histplot(data=filtered_20k, x=waste_metric, kde=True, color="teal", bins=30, ax=axes_sns[0])
        axes_sns[0].set_title(f"Seaborn HistPlot: {waste_metric}", fontweight="bold")
        sns.boxplot(data=filtered_20k, x=waste_metric, color="coral", ax=axes_sns[1], fliersize=3)
        axes_sns[1].set_title(f"Seaborn BoxPlot: {waste_metric}", fontweight="bold")
        plt.tight_layout()
        st.pyplot(fig_sns)
        plt.close(fig_sns)

# ------------------------------------------------------------------------------
# TAB 4: PART-TO-WHOLE & COMPOSITION
# ------------------------------------------------------------------------------
with tab4:
    st.markdown("### Part-to-Whole Composition Analysis")
    st.caption("Volumetric and proportional share of E-Waste relative to Organic, Plastic, and Industrial categories.")
    
    col_p1, col_p2 = st.columns([5, 7])
    
    with col_p1:
        cat_counts = wm_20k_df["Waste_Type"].value_counts().reset_index()
        cat_counts.columns = ["Waste_Type", "Record_Count"]
        
        fig_donut = px.pie(
            cat_counts,
            values="Record_Count",
            names="Waste_Type",
            hole=0.6,
            title="<b>Proportional Share of Waste Classifications</b>",
            color_discrete_sequence=ECO_PALETTE
        )
        fig_donut.update_traces(textposition='inside', textinfo='percent+label')
        fig_donut.update_layout(
            height=450,
            margin=dict(l=20, r=20, t=50, b=20),
            showlegend=False,
            paper_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig_donut, use_container_width=True)
        
    with col_p2:
        yearly_comp = wm_20k_df.groupby(["Year", "Waste_Type"])["Daily_Waste_Generation_Tons"].sum().reset_index()
        fig_area = px.bar(
            yearly_comp,
            x="Year",
            y="Daily_Waste_Generation_Tons",
            color="Waste_Type",
            title="<b>Longitudinal Tonnage Shift Across Categories (2015 - 2026)</b>",
            color_discrete_sequence=ECO_PALETTE
        )
        fig_area.update_layout(
            height=450,
            margin=dict(l=20, r=20, t=50, b=20),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig_area, use_container_width=True)
        
    st.subheader("Category Volumetric Breakdown")
    cat_summary = wm_20k_df.groupby("Waste_Type").agg(
        Total_Tons=("Daily_Waste_Generation_Tons", "sum"),
        Mean_Daily_Tons=("Daily_Waste_Generation_Tons", "mean"),
        Median_Daily_Tons=("Daily_Waste_Generation_Tons", "median"),
        Avg_Recycling_Rate=("Recycling_Rate", "mean"),
        Avg_Collection_Eff=("Collection_Efficiency_Percentage", "mean")
    ).sort_values(by="Total_Tons", ascending=False).reset_index()
    
    st.dataframe(
        cat_summary.style.format({
            "Total_Tons": "{:,.1f}",
            "Mean_Daily_Tons": "{:.2f}",
            "Median_Daily_Tons": "{:.2f}",
            "Avg_Recycling_Rate": "{:.1f}%",
            "Avg_Collection_Eff": "{:.1f}%"
        }),
        use_container_width=True
    )

# ------------------------------------------------------------------------------
# TAB 5: REGRESSION & MULTIVARIATE ANALYSIS
# ------------------------------------------------------------------------------
with tab5:
    st.markdown("### Bivariate, Regression & Multivariate Bubble Analysis")
    st.caption("Uncovering non-linear relationships between population density, urbanization, and daily waste generation.")
    
    col_m1, col_m2 = st.columns(2)
    
    with col_m1:
        st.subheader("Linear Trend & Regression")
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
        fig_reg.update_layout(
            height=450,
            margin=dict(l=30, r=30, t=50, b=30),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig_reg, use_container_width=True)
        
    with col_m2:
        st.subheader("Multivariate 4D Bubble Chart")
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
        fig_bubble.update_layout(
            height=450,
            margin=dict(l=30, r=30, t=50, b=30),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig_bubble, use_container_width=True)
        
    st.markdown("---")
    st.subheader("Statistical Kernel: Violin & Quartile Distributions Across City Tiers")
    
    top_cats = wm_20k_df["City_Category"].value_counts().nlargest(4).index.tolist()
    violin_df = filtered_20k[filtered_20k["City_Category"].isin(top_cats)]
    
    fig_violin = px.violin(
        violin_df,
        x="City_Category",
        y="Daily_Waste_Generation_Tons",
        color="City_Category",
        box=True,
        points="outliers",
        title="Violin Kernel & Quartiles of Daily Waste Across City Tiers",
        color_discrete_sequence=ECO_PALETTE
    )
    fig_violin.update_layout(
        height=420,
        margin=dict(l=30, r=30, t=50, b=30),
        showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    st.plotly_chart(fig_violin, use_container_width=True)

# ------------------------------------------------------------------------------
# TAB 6: CORRELATION & COLLINEARITY
# ------------------------------------------------------------------------------
with tab6:
    st.markdown("### Correlation Matrix Heatmap & Joint Densities")
    st.caption("Pairwise collinearity across municipal indices, demographics, collection infrastructure, and air quality.")
    
    numeric_candidates = [
        "Population",
        "Population_Density",
        "Urbanization_Rate",
        "Daily_Waste_Generation_Tons",
        "Collection_Efficiency_Percentage",
        "Recycling_Rate",
        "Municipal_Efficiency_Score",
        "Air_Quality_Index"
    ]
    avail_num_cols = [c for c in numeric_candidates if c in filtered_20k.columns]
    
    col_k1, col_k2 = st.columns([6, 6])
    
    with col_k1:
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
        fig_heat.update_layout(
            height=470,
            margin=dict(l=30, r=30, t=50, b=30),
            paper_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig_heat, use_container_width=True)
        
    with col_k2:
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
        fig_density.update_layout(
            height=470,
            margin=dict(l=30, r=30, t=50, b=30),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig_density, use_container_width=True)
        
    st.info("💡 **Key Finding**: Urbanization Rate and Population Density correlate positively with daily e-waste tonnage. Higher Municipal Efficiency Scores correlate with reduced uncollected waste, confirming the role of local governance.")

# ------------------------------------------------------------------------------
# TAB 7: GEOSPATIAL & CITY DEEP DIVE INSPECTOR
# ------------------------------------------------------------------------------
with tab7:
    st.markdown("### Geospatial Mapping & Interactive City Deep Dive")
    st.caption("Explore national spatial distributions or select any Indian city for an individual waste and infrastructure audit.")
    
    # 1. Map of India
    st.subheader("1. Interactive Map of Indian Urban Centers")
    
    city_map_data = filtered_combined.groupby(["City", "State", "Region", "Latitude", "Longitude"]).agg(
        Total_Waste=("Daily_Waste_Generation_Tons", "sum"),
        Mean_Waste=("Daily_Waste_Generation_Tons", "mean"),
        Collection_Eff=("Collection_Efficiency_Percentage", "mean"),
        Recycling_Rate=("Recycling_Rate", "mean")
    ).reset_index()
    
    if len(city_map_data) > 0:
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
                    title="<b>Indian Cities: Bubble Size = Total Daily Waste, Color = Collection Efficiency (%)</b>"
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
                    title="<b>Indian Cities: Bubble Size = Total Daily Waste, Color = Collection Efficiency (%)</b>"
                )
                fig_map.update_layout(height=520, margin=dict(l=10, r=10, t=40, b=10))
                st.plotly_chart(fig_map, use_container_width=True)
            else:
                st.map(city_map_data, latitude="Latitude", longitude="Longitude", size="Total_Waste")
        except Exception:
            st.map(city_map_data, latitude="Latitude", longitude="Longitude", size="Total_Waste")
    else:
        st.warning("No city geospatial data matches the current filters.")
        
    st.markdown("---")
    
    # 2. Interactive City-Level Drilldown Inspector
    st.subheader("2. Interactive City Audit & Infrastructure Scorecard")
    available_cities = sorted(wm_20k_df["City"].dropna().unique().tolist())
    
    selected_drill_city = st.selectbox(
        "Select a City for Deep Dive Audit:",
        options=available_cities,
        index=available_cities.index("Mumbai") if "Mumbai" in available_cities else 0
    )
    
    city_df = wm_20k_df[wm_20k_df["City"] == selected_drill_city]
    city_ew = city_df[city_df["Waste_Type"] == "E-Waste"]
    
    if len(city_df) > 0:
        city_state = city_df["State"].iloc[0]
        city_region = city_df["Region"].iloc[0]
        city_tier = city_df["City_Category"].iloc[0]
        city_avg_gen = city_df["Daily_Waste_Generation_Tons"].mean()
        city_avg_coll = city_df["Collection_Efficiency_Percentage"].mean()
        city_avg_rec = city_df["Recycling_Rate"].mean()
        
        c_kpi1, c_kpi2, c_kpi3, c_kpi4 = st.columns(4)
        with c_kpi1:
            st.metric("City Classification", f"{city_tier}", f"Region: {city_region}")
        with c_kpi2:
            st.metric("Mean Daily Waste", f"{city_avg_gen:.1f} Tons", f"State: {city_state}")
        with c_kpi3:
            st.metric("Collection Efficiency", f"{city_avg_coll:.1f}%", f"{'Above' if city_avg_coll >= 50 else 'Below'} National Baseline")
        with c_kpi4:
            st.metric("Formal Recycling Rate", f"{city_avg_rec:.1f}%", f"{'Good' if city_avg_rec > 50 else 'Lagging'}")
            
        # City Historical Trend Chart
        if len(city_ew) > 0:
            city_yearly = city_ew.groupby("Year")["Daily_Waste_Generation_Tons"].mean().reset_index()
            fig_city_trend = px.line(
                city_yearly,
                x="Year",
                y="Daily_Waste_Generation_Tons",
                markers=True,
                line_shape="spline",
                color_discrete_sequence=["#059669"],
                title=f"<b>Historical Daily E-Waste Generation in {selected_drill_city} (2015 – 2026)</b>"
            )
            fig_city_trend.update_layout(
                height=350,
                margin=dict(l=30, r=30, t=50, b=30),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)"
            )
            st.plotly_chart(fig_city_trend, use_container_width=True)
            
    st.markdown("---")
    
    # 3. Regional Facet Analysis
    st.subheader("3. Multi-Panel Regional Facet Analysis: E-Waste Growth Over Time")
    ew_comb_subset = filtered_combined[filtered_combined["Waste_Type"] == "E-Waste"]
    
    if len(ew_comb_subset) > 0:
        fig_facet = px.scatter(
            ew_comb_subset,
            x="Year",
            y="Daily_Waste_Generation_Tons",
            facet_col="Region",
            facet_col_wrap=3,
            color="Region",
            hover_name="City",
            opacity=0.75,
            trendline="lowess",
            title="E-Waste Generation Curves by Region (2015 - 2026)",
            color_discrete_sequence=ECO_PALETTE
        )
        fig_facet.update_layout(
            height=550,
            margin=dict(l=20, r=20, t=60, b=20),
            showlegend=False,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig_facet, use_container_width=True)
    else:
        st.warning("No E-waste observations match current filter criteria.")

# ------------------------------------------------------------------------------
# TAB 8: DATA EXPLORER & EXPORT
# ------------------------------------------------------------------------------
with tab8:
    st.markdown("### Interactive Data Explorer & Export")
    st.caption("Inspect filtered observations, search by city or state, and export tailored slices for research.")
    
    search_term = st.text_input("Quick Search (City, State, or Waste Type)", placeholder="e.g. Mumbai, E-Waste, Delhi...")
    
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
    
    st.dataframe(display_df[show_cols].head(500), use_container_width=True)
    
    csv_bytes = display_df[show_cols].to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Filtered Data as CSV",
        data=csv_bytes,
        file_name=f"ewaste_analysis_filtered_{selected_years[0]}_{selected_years[1]}.csv",
        mime="text/csv",
        use_container_width=True
    )
    
    st.markdown("#### Summary Statistics of Filtered Slice")
    st.dataframe(display_df[show_cols].describe().T, use_container_width=True)

# ------------------------------------------------------------------------------
# TAB 9: POST-MORTEM & POLICY FRAMEWORK
# ------------------------------------------------------------------------------
with tab9:
    st.markdown("### Data Engineering Post-Mortem & Policy Framework")
    
    col_pm1, col_pm2 = st.columns(2)
    
    with col_pm1:
        st.markdown("""
        #### Data Engineering Post-Mortem: What Broke & Why
        
        In the original exploratory notebook, execution halted in Cell 3 due to a **Column Label Inconsistency**:
        
        * **The Problem:** The recycling dataset (`Waste_Management_and_Recycling_India.csv`) designated the urban area under `'City/District'`, whereas the longitudinal 20K dataset labeled it `'City'`.
        * **The Bug:** A downstream Seaborn call attempted to reference `'City/District'` inside `wm_20k_df`, throwing a `KeyError: 'City/District'`.
        * **The Resolution:** Harmonized headers immediately upon ingest:
          ```python
          if "City/District" in wm_recycling_df.columns:
              wm_recycling_df.rename(columns={"City/District": "City"}, inplace=True)
          ```
        * **Relational Integrity:** Implemented an inner join between `wm_20k_df` and `cities_master.csv` on `['City', 'State']`, pulling geographic coordinates (`Latitude`, `Longitude`) and special demographic flags (`Is_Tourist`, `Is_Hill_Station`).
        """)
        
    with col_pm2:
        st.markdown("""
        #### Evidence-Based Policy Framework
        
        Based on empirical findings from the 25,200+ longitudinal records:
        
        1. **The Core Crisis is Collection, Not Generation:**
           Generation inevitably scales with consumer electronics adoption (7.56% CAGR). However, collection efficiency remains frozen at ~50%. Policies targeting consumer awareness without collection infrastructure will fail.
           
        2. **Extended Producer Responsibility (EPR) Corridors:**
           Over 60% of electronic waste originates in Metro hubs (Mumbai, Delhi, Bengaluru, Kolkata, Chennai). EPR take-back centers and certified e-stewards must be clustered in these high-density nodes.
           
        3. **Formalizing the Informal Scrap Network (Kabadiwalas):**
           Because 90%+ of hardware routes through informal scrap merchants, municipal governments should offer subsidized testing, protective gear, and guaranteed buy-back rates to route hardware to authorized hydrometallurgical extraction plants.
        """)
        
    st.markdown("---")
    st.markdown("""
    <div style="text-align:center; padding:1.5rem 0; color:#64748b; font-size:0.9rem;">
        <strong>India E-Waste Growth Analytics & Circularity Project</strong><br>
        Built by <strong>Ruhaan Joshi (24101C0057)</strong>, <strong>Om Thakur (24101C0041)</strong>, and <strong>Rudra Jain (24101C0062)</strong><br>
        Department of Information Technology • Batch INFT-C
    </div>
    """, unsafe_allow_html=True)
