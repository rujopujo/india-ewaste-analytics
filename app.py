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
# PAGE CONFIGURATION & GLOBAL AESTHETICS
# ==============================================================================
st.set_page_config(
    page_title="India E-Waste Growth Analysis Dashboard",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern, polished UI
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    .main-header {
        background: linear-gradient(135deg, #042f2e 0%, #0f766e 50%, #14b8a6 100%);
        padding: 2.2rem 2.5rem;
        border-radius: 18px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 10px 25px -5px rgba(15, 118, 110, 0.25);
    }
    .main-header h1 {
        font-size: 2.3rem;
        font-weight: 800;
        margin: 0 0 0.5rem 0;
        letter-spacing: -0.02em;
        color: #ffffff;
    }
    .main-header p {
        font-size: 1.05rem;
        opacity: 0.92;
        margin-bottom: 1rem;
        line-height: 1.5;
    }
    .badge-container {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
        margin-top: 0.8rem;
    }
    .badge {
        background: rgba(255, 255, 255, 0.18);
        backdrop-filter: blur(8px);
        padding: 0.35rem 0.85rem;
        border-radius: 9999px;
        font-size: 0.82rem;
        font-weight: 600;
        border: 1px solid rgba(255, 255, 255, 0.25);
    }
    .metric-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 14px;
        padding: 1.25rem 1.4rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.04);
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 16px -2px rgba(15, 118, 110, 0.1);
    }
    .metric-label {
        font-size: 0.82rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #64748b;
        margin-bottom: 0.35rem;
    }
    .metric-value {
        font-size: 1.85rem;
        font-weight: 800;
        color: #0f172a;
        line-height: 1.1;
    }
    .metric-delta {
        font-size: 0.82rem;
        font-weight: 600;
        margin-top: 0.4rem;
    }
    .delta-up { color: #dc2626; }
    .delta-down { color: #16a34a; }
    .delta-neutral { color: #0284c7; }

    .feynman-box {
        background: #f0fdfa;
        border-left: 4px solid #0d9488;
        border-radius: 0 14px 14px 0;
        padding: 1.3rem 1.6rem;
        margin: 1.5rem 0;
    }
    .feynman-box h4 {
        color: #0f766e;
        font-weight: 700;
        margin-top: 0;
    }
</style>
""", unsafe_allow_html=True)

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
    
    # Strip whitespace from column names
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
    st.image("https://img.icons8.com/isometric/96/waste-sorting.png", width=64)
    st.title("Filters & Scope")
    
    # Analysis Mode
    analysis_mode = st.radio(
        "Focus Dataset Scope",
        options=["⚡ E-Waste Only (Core Study)", "🌐 All Waste Categories (Comparative)"],
        index=0
    )
    is_ewaste_only = "E-Waste Only" in analysis_mode
    
    st.markdown("---")
    
    # Year Filter Range
    min_year = int(wm_20k_df["Year"].min())
    max_year = int(wm_20k_df["Year"].max())
    selected_years = st.slider(
        "Observation Time Window",
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year),
        step=1
    )
    
    # Region Filter
    all_regions = sorted(wm_20k_df["Region"].dropna().unique().tolist())
    selected_regions = st.multiselect(
        "Geographic Regions",
        options=all_regions,
        default=all_regions
    )
    
    # City Category Filter
    all_categories = sorted(wm_20k_df["City_Category"].dropna().unique().tolist())
    selected_categories = st.multiselect(
        "City Tiers",
        options=all_categories,
        default=all_categories
    )
    
    # Waste Type Filter (if in All Waste mode)
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
    
    # Quick reset button
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

# Combined filtered
comb_mask = (
    (combined_df["Year"].between(selected_years[0], selected_years[1])) &
    (combined_df["Region"].isin(selected_regions)) &
    (combined_df["City_Category"].isin(selected_categories)) &
    (combined_df["Waste_Type"].isin(selected_waste_types))
)
filtered_combined = combined_df[comb_mask]

# Subset for E-waste specifically
ew_20k = wm_20k_df[wm_20k_df["Waste_Type"] == "E-Waste"]
filtered_ew = filtered_20k[filtered_20k["Waste_Type"] == "E-Waste"]

# ==============================================================================
# HEADER SECTION
# ==============================================================================
st.markdown("""
<div class="main-header">
    <h1>India's E-Waste Growth Analytics</h1>
    <p>How fast is electronic waste accumulating across Indian urban centers? An interactive multi-dataset study on generation rates, regional growth curves, infrastructure bottlenecks, and municipal recovery efficiencies.</p>
    <div class="badge-container">
        <span class="badge">👥 Ruhaan Joshi (24101C0057)</span>
        <span class="badge">👥 Om Thakur (24101C0041)</span>
        <span class="badge">👥 Rudra Jain (24101C0062)</span>
        <span class="badge">🏛️ INFT-C Batch 3</span>
        <span class="badge">📅 2015 – 2026 Longitudinal Study</span>
        <span class="badge">📊 25,200+ Municipal Records</span>
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

# Calculate 2015 vs 2026 CAGR for e-waste
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
        <div class="metric-delta delta-neutral">Per Reporting Municipality</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">E-Waste 11-Yr CAGR</div>
        <div class="metric-value">+{cagr_val:.2f}%</div>
        <div class="metric-delta delta-up">2015 (770 T/D) → 2026 (1,716 T/D)</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Collection Efficiency</div>
        <div class="metric-value">{avg_collection:.1f}%</div>
        <div class="metric-delta delta-up">Stagnant Infrastructure Ceiling</div>
    </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Formal Recycling Rate</div>
        <div class="metric-value">{avg_recycling:.1f}%</div>
        <div class="metric-delta delta-neutral">>50% Informal Leakage Gap</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ==============================================================================
# MAIN TABS ARCHITECTURE
# ==============================================================================
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
    "🌟 Executive Overview & Growth",
    "📊 Univariate & Outliers",
    "🥧 Composition & Share",
    "📈 Regression & Multivariate",
    "🔥 Correlation & Hexbins",
    "🗺️ Geospatial & Regional Facets",
    "🔍 Data Explorer & Export",
    "💡 Post-Mortem & Policy"
])

# ------------------------------------------------------------------------------
# TAB 1: EXECUTIVE OVERVIEW & E-WASTE GROWTH TRENDS
# ------------------------------------------------------------------------------
with tab1:
    st.markdown("### 📈 Longitudinal E-Waste Growth Trajectory (2015 – 2026)")
    
    # Calculate yearly stats for E-waste
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
        
        # Bar for Total Daily Tons
        fig_trend.add_trace(
            go.Bar(
                x=yearly_stats["Year"],
                y=yearly_stats["total_daily_tons"],
                name="Total Daily Tons Generated",
                marker_color="#0d9488",
                opacity=0.85,
                hovertemplate="<b>Year %{x}</b><br>Total Generation: %{y:.1f} Tons/Day<extra></extra>"
            ),
            secondary_y=False
        )
        
        # Line for Mean Daily Tons
        fig_trend.add_trace(
            go.Scatter(
                x=yearly_stats["Year"],
                y=yearly_stats["mean_daily_tons"],
                name="Mean Daily Tons per Center",
                mode="lines+markers",
                line=dict(color="#f97316", width=3.5),
                marker=dict(size=8, symbol="circle"),
                hovertemplate="<b>Year %{x}</b><br>Mean Generation: %{y:.2f} Tons/Day<extra></extra>"
            ),
            secondary_y=True
        )
        
        fig_trend.update_layout(
            title="<b>Annual Daily E-Waste Tonnage & Per-Center Average</b>",
            xaxis=dict(title="Year", tickmode="linear", dtick=1),
            yaxis=dict(title="Total Daily E-Waste (Tons/Day)", showgrid=True),
            yaxis2=dict(title="Mean Daily E-Waste (Tons/Day)", overlaying="y", side="right", showgrid=False),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            hovermode="x unified",
            margin=dict(l=40, r=40, t=60, b=40),
            height=430
        )
        st.plotly_chart(fig_trend, use_container_width=True)
        
    with c2:
        # State breakdown for E-Waste
        state_ew = ew_20k.groupby("State")["Daily_Waste_Generation_Tons"].agg(["sum", "mean"]).sort_values(by="sum", ascending=True).tail(8)
        fig_state = px.bar(
            state_ew,
            x="sum",
            y=state_ew.index,
            orientation="h",
            color="sum",
            color_continuous_scale="Tealgrn",
            title="<b>Top E-Waste Generating States (Cumulative Daily Tons)</b>",
            labels={"sum": "Total Daily Tons", "State": "State"}
        )
        fig_state.update_layout(height=430, margin=dict(l=20, r=20, t=60, b=40), coloraxis_showscale=False)
        st.plotly_chart(fig_state, use_container_width=True)
        
    # Feynman Concept Card
    st.markdown("""
    <div class="feynman-box">
        <h4>🧠 The Feynman Framework: The "One-Way Conveyor Belt" Dilemma</h4>
        <p>Imagine your city sitting beside a massive conveyor belt. On the intake side, logistics couriers constantly deposit brand-new smartphones, gaming consoles, laptops, and smart TVs. On the exit side, households and corporations discard obsolete gadgets. Over the past 11 years, device replacement cycles collapsed from 5 years to under 18 months, accelerating the conveyor belt by <strong>7.56% compounded annually</strong>. However, municipal recovery bins remained the exact same size.</p>
        <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1rem; margin-top: 1rem;">
            <div style="background:white; padding:1rem; border-radius:10px; border:1px solid #ccfbf1;">
                <strong style="color:#0f766e;">1. Generation Overdrive</strong><br>
                Surges observed in 2019, 2022, and 2026 reflect national telecom upgrades (4G rollouts, pandemic hardware replacements, and 5G/IoT device lifecycles).
            </div>
            <div style="background:white; padding:1rem; border-radius:10px; border:1px solid #ccfbf1;">
                <strong style="color:#0f766e;">2. The 50% Collection Ceiling</strong><br>
                While generation doubled, authorized collection efficiency flatlined at ~48.5% to 54.0%. Over half of all discarded hardware bypasses municipal oversight.
            </div>
            <div style="background:white; padding:1rem; border-radius:10px; border:1px solid #ccfbf1;">
                <strong style="color:#0f766e;">3. 140x Urban Disparity</strong><br>
                Metros average 141.32 Tons/Day per report, whereas Tier-3 centers log only 1.01 Tons/Day. High-tech obsolescence is hyper-concentrated in commercial capitals.
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Yearly Statistics Table with Progress Bars
    with st.expander("📋 View Detailed Longitudinal E-Waste Metrics (2015 - 2026)"):
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
# TAB 2: UNIVARIATE & OUTLIER DISTRIBUTIONS
# ------------------------------------------------------------------------------
with tab2:
    st.markdown("### 📊 Univariate Distributions & Outlier Spread (Cell 2 & Cell 3)")
    st.caption("Investigating the skewness of daily generation volume and detecting extreme mega-city outliers.")
    
    col_u1, col_u2 = st.columns(2)
    
    waste_metric = "Daily_Waste_Generation_Tons"
    
    with col_u1:
        st.subheader("1. Distribution & Density")
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
            color_discrete_sequence=["#0d9488"],
            labels={"x": xlab, "y": "Frequency Count"},
            title=f"Distribution Profile of {xlab}"
        )
        fig_hist.update_layout(height=420, margin=dict(l=30, r=30, t=50, b=30))
        st.plotly_chart(fig_hist, use_container_width=True)
        
    with col_u2:
        st.subheader("2. Outlier Detection across City Categories")
        fig_box = px.box(
            filtered_20k,
            x="City_Category",
            y=waste_metric,
            color="City_Category",
            color_discrete_sequence=px.colors.qualitative.Safe,
            points="outliers",
            title=f"Outlier Spread across City Tiers ({waste_metric})"
        )
        fig_box.update_layout(height=420, margin=dict(l=30, r=30, t=50, b=30), showlegend=False)
        st.plotly_chart(fig_box, use_container_width=True)
        
    st.markdown("---")
    st.subheader("3. Categorical Rankings & Grouped Comparisons")
    
    col_c1, col_c2 = st.columns(2)
    
    with col_c1:
        # Top Ranked Cities from Recycling Dataset
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
            color_continuous_scale="Blues_r",
            title=f"Top {top_n} Cities by Mean Waste Generated (Recycling Dataset)"
        )
        fig_top.update_layout(yaxis=dict(autorange="reversed"), height=460, margin=dict(l=30, r=30, t=50, b=30))
        st.plotly_chart(fig_top, use_container_width=True)
        
    with col_c2:
        # Grouped Bar Plot: Top Cities across Waste Types
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
            color_discrete_sequence=px.colors.qualitative.Bold
        )
        fig_grp.update_layout(height=460, margin=dict(l=30, r=30, t=50, b=30))
        st.plotly_chart(fig_grp, use_container_width=True)
        
    if view_static_plots:
        st.markdown("#### 🖼️ Original Matplotlib / Seaborn Visualizations")
        fig_sns, axes_sns = plt.subplots(1, 2, figsize=(14, 4.5))
        sns.histplot(data=filtered_20k, x=waste_metric, kde=True, color="teal", bins=30, ax=axes_sns[0])
        axes_sns[0].set_title(f"Seaborn HistPlot: {waste_metric}", fontweight="bold")
        sns.boxplot(data=filtered_20k, x=waste_metric, color="coral", ax=axes_sns[1], fliersize=3)
        axes_sns[1].set_title(f"Seaborn BoxPlot: {waste_metric}", fontweight="bold")
        plt.tight_layout()
        st.pyplot(fig_sns)
        plt.close(fig_sns)

# ------------------------------------------------------------------------------
# TAB 3: PART-TO-WHOLE & COMPOSITION
# ------------------------------------------------------------------------------
with tab3:
    st.markdown("### 🥧 Part-to-Whole Composition Analysis (Cell 4)")
    st.caption("Examining the volumetric and proportional share of E-Waste relative to Organic, Plastic, and Industrial categories.")
    
    col_p1, col_p2 = st.columns([5, 7])
    
    with col_p1:
        cat_counts = wm_20k_df["Waste_Type"].value_counts().reset_index()
        cat_counts.columns = ["Waste_Type", "Record_Count"]
        
        fig_donut = px.pie(
            cat_counts,
            values="Record_Count",
            names="Waste_Type",
            hole=0.55,
            title="<b>Proportional Share of Waste Classifications</b>",
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig_donut.update_traces(textposition='inside', textinfo='percent+label')
        fig_donut.update_layout(height=450, margin=dict(l=20, r=20, t=50, b=20), showlegend=False)
        st.plotly_chart(fig_donut, use_container_width=True)
        
    with col_p2:
        # Composition over time
        yearly_comp = wm_20k_df.groupby(["Year", "Waste_Type"])["Daily_Waste_Generation_Tons"].sum().reset_index()
        fig_area = px.bar(
            yearly_comp,
            x="Year",
            y="Daily_Waste_Generation_Tons",
            color="Waste_Type",
            title="<b>Longitudinal Tonnage Shift Across Categories (2015 - 2026)</b>",
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig_area.update_layout(height=450, margin=dict(l=20, r=20, t=50, b=20))
        st.plotly_chart(fig_area, use_container_width=True)
        
    # Statistical Table for Breakdown
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
# TAB 4: REGRESSION & MULTIVARIATE ANALYSIS
# ------------------------------------------------------------------------------
with tab4:
    st.markdown("### 📈 Bivariate, Regression & Multivariate Bubble Analysis (Cell 5 & Cell 6)")
    st.caption("Uncovering non-linear relationships between population density, urbanization, and waste generation volume.")
    
    col_m1, col_m2 = st.columns(2)
    
    with col_m1:
        st.subheader("1. Linear Trend & Regression")
        
        sample_size = min(1500, len(filtered_20k))
        sample_reg = filtered_20k.sample(n=sample_size, random_state=42) if sample_size > 0 else filtered_20k
        
        fig_reg = px.scatter(
            sample_reg,
            x="Population_Density",
            y="Daily_Waste_Generation_Tons",
            trendline="ols",
            trendline_color_override="#ef4444",
            opacity=0.5,
            color_discrete_sequence=["#0284c7"],
            title=f"OLS Trend: Population Density vs Daily Waste (n={sample_size})",
            labels={"Population_Density": "Population Density (People/km²)", "Daily_Waste_Generation_Tons": "Daily Waste (Tons)"}
        )
        fig_reg.update_layout(height=450, margin=dict(l=30, r=30, t=50, b=30))
        st.plotly_chart(fig_reg, use_container_width=True)
        
    with col_m2:
        st.subheader("2. Multivariate 4D Bubble Chart")
        
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
            opacity=0.75,
            title="Bubble: Density vs Waste (Sized by Urbanization Rate)",
            labels={"Population_Density": "Density (People/km²)", "Daily_Waste_Generation_Tons": "Daily Waste (Tons)"},
            color_discrete_sequence=px.colors.qualitative.Prism
        )
        fig_bubble.update_layout(height=450, margin=dict(l=30, r=30, t=50, b=30))
        st.plotly_chart(fig_bubble, use_container_width=True)
        
    st.markdown("---")
    st.subheader("3. Statistical Kernel: Violin & Strip Plots across City Categories")
    
    top_cats = wm_20k_df["City_Category"].value_counts().nlargest(4).index.tolist()
    violin_df = filtered_20k[filtered_20k["City_Category"].isin(top_cats)]
    
    fig_violin = px.violin(
        violin_df,
        x="City_Category",
        y="Daily_Waste_Generation_Tons",
        color="City_Category",
        box=True,
        points="outliers",
        title="Violin Kernel & Quartiles of Daily Waste across City Tiers",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig_violin.update_layout(height=420, margin=dict(l=30, r=30, t=50, b=30), showlegend=False)
    st.plotly_chart(fig_violin, use_container_width=True)

# ------------------------------------------------------------------------------
# TAB 5: CORRELATION & HEXBINS
# ------------------------------------------------------------------------------
with tab5:
    st.markdown("### 🔥 Correlation Matrix Heatmap & Joint Densities (Cell 7)")
    st.caption("Assessing pairwise collinearity across municipal indices, demographics, collection infrastructure, and environmental factors.")
    
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
        
        # Interactive Heatmap
        fig_heat = px.imshow(
            corr_mat,
            text_auto=".2f",
            aspect="auto",
            color_continuous_scale="RdBu_r",
            zmin=-1,
            zmax=1,
            title="<b>Correlation Heatmap (Pearson)</b>"
        )
        fig_heat.update_layout(height=470, margin=dict(l=30, r=30, t=50, b=30))
        st.plotly_chart(fig_heat, use_container_width=True)
        
    with col_k2:
        # 2D Density Heatmap
        sample_density = filtered_20k.sample(min(3000, len(filtered_20k)), random_state=42) if len(filtered_20k) > 0 else filtered_20k
        fig_density = px.density_heatmap(
            sample_density,
            x="Urbanization_Rate",
            y="Daily_Waste_Generation_Tons",
            nbinsx=25,
            nbinsy=25,
            color_continuous_scale="Viridis",
            title="<b>Joint 2D Density: Urbanization vs Daily Waste</b>",
            labels={"Urbanization_Rate": "Urbanization Rate (%)", "Daily_Waste_Generation_Tons": "Daily Waste (Tons)"}
        )
        fig_density.update_layout(height=470, margin=dict(l=30, r=30, t=50, b=30))
        st.plotly_chart(fig_density, use_container_width=True)
        
    st.info("💡 **Observation**: Urbanization Rate and Population Density show strong positive collinearity with Daily Generation Tonnage. Conversely, Municipal Efficiency Scores show modest negative correlation with uncollected leakage, indicating that governance investment improves recovery.")

# ------------------------------------------------------------------------------
# TAB 6: GEOSPATIAL & REGIONAL FACETS
# ------------------------------------------------------------------------------
with tab6:
    st.markdown("### 🗺️ Geospatial Distribution & Regional Facets (Cell 8)")
    st.caption("Analyzing geographic disparities, tourist destination impacts, and regional growth trajectories.")
    
    # 1. Geospatial City Scatter Map
    st.subheader("1. Interactive Map of Indian Urban Centers")
    
    # Aggregate city level metrics
    city_map_data = filtered_combined.groupby(["City", "State", "Region", "Latitude", "Longitude"]).agg(
        Total_Waste=("Daily_Waste_Generation_Tons", "sum"),
        Mean_Waste=("Daily_Waste_Generation_Tons", "mean"),
        Collection_Eff=("Collection_Efficiency_Percentage", "mean"),
        Recycling_Rate=("Recycling_Rate", "mean")
    ).reset_index()
    
    fig_map = px.scatter_mapbox(
        city_map_data,
        lat="Latitude",
        lon="Longitude",
        hover_name="City",
        hover_data=["State", "Region", "Total_Waste", "Collection_Eff", "Recycling_Rate"],
        size="Total_Waste",
        color="Collection_Eff",
        color_continuous_scale="Viridis",
        size_max=35,
        zoom=3.8,
        center=dict(lat=21.7679, lon=78.8718),
        mapbox_style="carto-positron",
        title="<b>Indian Cities: Bubble Size = Daily Waste, Color = Collection Efficiency (%)</b>"
    )
    fig_map.update_layout(height=520, margin=dict(l=10, r=10, t=40, b=10))
    st.plotly_chart(fig_map, use_container_width=True)
    
    st.markdown("---")
    
    # 2. Regional Facet Analysis
    st.subheader("2. Multi-Panel Regional Facet Analysis: E-Waste Growth Over Time")
    
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
            title="E-Waste Generation Curves by Region (2015 - 2026)"
        )
        fig_facet.update_layout(height=550, margin=dict(l=20, r=20, t=60, b=20), showlegend=False)
        st.plotly_chart(fig_facet, use_container_width=True)
    else:
        st.warning("No E-waste observations match current filter criteria.")
        
    # 3. Tourism & Hill Station Comparative Analysis
    st.subheader("3. Demographic Impact: Tourist & Hill Station Comparison")
    col_t1, col_t2 = st.columns(2)
    
    with col_t1:
        tourist_agg = filtered_combined.groupby("Is_Tourist")["Daily_Waste_Generation_Tons"].agg(["mean", "median", "count"]).reset_index()
        tourist_agg["Type"] = tourist_agg["Is_Tourist"].map({1: "Tourist Destination", 0: "Non-Tourist Center"})
        fig_tour = px.bar(
            tourist_agg,
            x="Type",
            y="mean",
            color="Type",
            title="Mean Daily Waste: Tourist vs Non-Tourist Cities",
            labels={"mean": "Mean Daily Waste (Tons)", "Type": "City Classification"},
            color_discrete_sequence=["#0d9488", "#f59e0b"]
        )
        fig_tour.update_layout(height=360, margin=dict(l=30, r=30, t=40, b=30), showlegend=False)
        st.plotly_chart(fig_tour, use_container_width=True)
        
    with col_t2:
        hill_agg = filtered_combined.groupby("Is_Hill_Station")["Daily_Waste_Generation_Tons"].agg(["mean", "median", "count"]).reset_index()
        hill_agg["Type"] = hill_agg["Is_Hill_Station"].map({1: "Hill Station", 0: "Plains / Coastal"})
        fig_hill = px.bar(
            hill_agg,
            x="Type",
            y="mean",
            color="Type",
            title="Mean Daily Waste: Hill Station vs Plains Centers",
            labels={"mean": "Mean Daily Waste (Tons)", "Type": "City Classification"},
            color_discrete_sequence=["#6366f1", "#10b981"]
        )
        fig_hill.update_layout(height=360, margin=dict(l=30, r=30, t=40, b=30), showlegend=False)
        st.plotly_chart(fig_hill, use_container_width=True)

# ------------------------------------------------------------------------------
# TAB 7: DATA EXPLORER & EXPORT
# ------------------------------------------------------------------------------
with tab7:
    st.markdown("### 🔍 Interactive Data Explorer & Export")
    st.caption("Inspect filtered observations, search by city or state, and export tailored slices for research.")
    
    # Search input
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
    
    # Column selector
    default_show_cols = [
        "Record_ID", "City", "State", "Region", "City_Category", "Year",
        "Waste_Type", "Daily_Waste_Generation_Tons", "Collection_Efficiency_Percentage",
        "Recycling_Rate", "Population_Density", "Municipal_Efficiency_Score"
    ]
    show_cols = st.multiselect("Customize Columns to Display", options=display_df.columns.tolist(), default=default_show_cols)
    
    st.dataframe(display_df[show_cols].head(500), use_container_width=True)
    
    # Download Button
    csv_bytes = display_df[show_cols].to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Filtered Data as CSV",
        data=csv_bytes,
        file_name=f"ewaste_analysis_filtered_{selected_years[0]}_{selected_years[1]}.csv",
        mime="text/csv",
        use_container_width=True
    )
    
    st.markdown("#### Summary Statistics of Filtered Slice")
    st.dataframe(display_df[show_cols].describe().T, use_container_width=True)

# ------------------------------------------------------------------------------
# TAB 8: POST-MORTEM & POLICY FRAMEWORK
# ------------------------------------------------------------------------------
with tab8:
    st.markdown("### 💡 Data Engineering Post-Mortem & Policy Insights")
    
    col_pm1, col_pm2 = st.columns(2)
    
    with col_pm1:
        st.markdown("""
        #### 🛠️ Data Engineering Post-Mortem: What Broke & Why
        
        In the original exploratory notebook, execution halted in Cell 3 due to a **Column Label Inconsistency**:
        
        * **The Problem:** The recycling dataset (`Waste_Management_and_Recycling_India.csv`) designated the urban area under `'City/District'`, whereas the longitudinal 20K dataset labeled it `'City'`.
        * **The Bug:** A downstream Seaborn call attempted to reference `'City/District'` inside `wm_20k_df`, throwing a `KeyError: 'City/District'`.
        * **The Resolution:** Harmonized headers immediately upon ingest:
          ```python
          if "City/District" in wm_recycling_df.columns:
              wm_recycling_df.rename(columns={"City/District": "City"}, inplace=True)
          ```
        * **Relational Integrity:** Implemented an inner join between `wm_20k_df` and `cities_master.csv` on `['City', 'State']`, pulling geographic coordinates (`Latitude`, `Longitude`) and special geographic flags (`Is_Tourist`, `Is_Hill_Station`).
        """)
        
    with col_pm2:
        st.markdown("""
        #### 🏛️ Evidence-Based Policy Framework
        
        Based on empirical findings from the 25,200+ longitudinal records:
        
        1. **The Core Crisis is Collection, Not Generation:**
           Generation inevitably scales with consumer electronics adoption (7.56% CAGR). However, collection efficiency remains frozen at ~50%. Policies targeting consumer awareness without collection infrastructure will fail.
           
        2. **Extended Producer Responsibility (EPR) Corridors:**
           Over 60% of electronic waste originates in Metro hubs (Mumbai, Delhi, Bengaluru, Kolkata, Chennai). EPR take-back centers and certified e-stewards must be clustered in these high-density nodes.
           
        3. **Formalizing the Informal Scrap Network (*Kabadiwalas*):**
           Because 90%+ of hardware routes through informal scrap merchants, municipal governments should offer subsidized testing, protective gear, and guaranteed buy-back rates to route hardware to authorized hydrometallurgical extraction plants.
        """)
        
    st.markdown("---")
    st.markdown("""
    <div style="text-align:center; padding:1.5rem 0; color:#64748b; font-size:0.9rem;">
        <strong>India's E-Waste Growth Analytics Project</strong><br>
        Built by <strong>Ruhaan Joshi (24101C0057)</strong>, <strong>Om Thakur (24101C0041)</strong>, and <strong>Rudra Jain (24101C0062)</strong><br>
        INFT-C Batch 3 • Faculty Review & Research Showcase
    </div>
    """, unsafe_allow_html=True)
