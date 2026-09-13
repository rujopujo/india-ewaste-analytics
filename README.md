# India E-Waste Growth Analytics & Circularity Assessment

<div align="center">

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://india-ewaste-analytics-rukaryjpzq4futpejbkf3v.streamlit.app)
![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35%2B-FF4B4B?logo=streamlit&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-5.18%2B-3F4F75?logo=plotly&logoColor=white)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-emerald.svg)

**An enterprise-grade, cloud-deployed environmental analytics platform investigating electronic waste accumulation, regional growth trajectories, municipal infrastructure bottlenecks, and peer group benchmarking across Indian urban centers (2015–2026).**

[Explore Live Web App ➔](https://india-ewaste-analytics-rukaryjpzq4futpejbkf3v.streamlit.app) • [View Architecture](#streamlits-cloud-deployment-architecture--engineering) • [Local Setup](#installation--local-execution) • [Methodology](#mathematical--statistical-formulations)

</div>

---

### Academic & Institutional Attribution

* **Department:** Department of Information Technology
* **Cohort / Batch:** INFT-C Batch 3
* **Project Team:**
  * **Ruhaan Joshi** — Roll No: `24101C0057`
  * **Om Thakur** — Roll No: `24101C0041`
  * **Rudra Jain** — Roll No: `24101C0062`
* **Live Deployment:** [india-ewaste-analytics-rukaryjpzq4futpejbkf3v.streamlit.app](https://india-ewaste-analytics-rukaryjpzq4futpejbkf3v.streamlit.app)
* **GitHub Repository:** [https://github.com/rujopujo/india-ewaste-analytics](https://github.com/rujopujo/india-ewaste-analytics)

---

## Executive Summary & Abstract

Rapid consumer digitization, shortening hardware lifecycles, and widespread expansion of telecommunications infrastructure (4G LTE to 5G Standalone) have positioned electronic waste (**e-waste**) among the fastest-accelerating solid waste vectors in India. Despite aggressive legislative frameworks—including the **E-Waste (Management) Rules 2022** and Extended Producer Responsibility (EPR) mandates—a critical empirical disconnect persists between national generation estimates and municipal-level operational capacities.

This research presents an interactive, web-based analytics and decision-support platform designed using **Streamlit**, **Plotly**, and **Altair**, evaluating an 11-year longitudinal corpus of **25,200+ municipal records** spanning Indian cities from **2015 through 2026**. The system models multi-decade growth curves, calculates national and regional Compound Annual Growth Rates (CAGR), diagnoses structural collection deficits, provides indexed peer group city benchmarking, and simulates circular material recovery scenarios (landfill diversion, toxic containment, critical mineral yields, and net carbon abatement).

---

## Core Research Objectives

```
   ┌────────────────────────────────────────────────────────────────────────┐
   │                       RESEARCH OBJECTIVE MATRIX                        │
   ├─────────────────────────────┬──────────────────────────────────────────┤
   │ 1. Longitudinal Growth      │ Quantify daily e-waste escalation from   │
   │    Quantification           │ 2015 to 2026; evaluate CAGR trajectories.│
   ├─────────────────────────────┼──────────────────────────────────────────┤
   │ 2. Urban Stratification     │ Measure generational disparity factors   │
   │    & Disparities            │ between Metros, Tier-1, Tier-2, & Tier-3.│
   ├─────────────────────────────┼──────────────────────────────────────────┤
   │ 3. Infrastructure Deficit   │ Diagnose the gap between gross disposal, │
   │    Diagnosis                │ formal collection, and recycling caps.   │
   ├─────────────────────────────┼──────────────────────────────────────────┤
   │ 4. Peer Group               │ Enable baseline-indexed, side-by-side    │
   │    Benchmarking             │ municipal performance comparative models.│
   ├─────────────────────────────┼──────────────────────────────────────────┤
   │ 5. Circular Economy         │ Formulate dynamic what-if simulations    │
   │    Scenario Modeling        │ for toxic isolation & mineral recovery.  │
   └─────────────────────────────┴──────────────────────────────────────────┘
```

1. **Longitudinal Growth Quantification:** Accurately measure daily municipal e-waste generation trajectories from 2015 to 2026 across Indian states, isolating structural shifts and inflection points.
2. **Urban Disparity Assessment:** Contrast generation volumes across Metro, Tier-1, Tier-2, and Tier-3 urban classifications to evaluate geographic concentration ratios and demographic collinearity.
3. **Infrastructure Bottleneck Diagnosis:** Pinpoint the structural ceiling where municipal collection efficiency and authorized formal recycling plateau, isolating the informal sector leakage volume.
4. **Peer Group Benchmarking:** Provide normalized, indexed comparative analytics enabling municipal commissioners and urban planners to benchmark individual cities against synthetic peer group medians.
5. **Circular Economy Scenario Modeling:** Construct an interactive policy simulator projecting landfill diversion, hazardous heavy metal containment (lead, mercury, cadmium), critical mineral reclamation (gold, copper, rare earths), and net greenhouse gas (GHG) abatement.

---

## Key Empirical Findings

* **Longitudinal Expansion (+7.56% CAGR):** Aggregate daily logged e-waste generation escalated from **770.16 tons/day in 2015** to **1,716.08 tons/day in 2026**, representing an annualized growth rate (CAGR) of **7.56%**. Distinct acceleration spikes occurred during 2019, 2022, and 2025–2026, coinciding with national telecommunication upgrades and consumer electronic refresh waves.
* **140x Urban Generation Disparity:** E-waste is overwhelmingly concentrated in commercial metropolitan hubs. Reporting stations in **Metros average 141.32 tons/day**, compared to **1.01 tons/day in Tier-3 centers**—an urban disparity factor of approximately **140x**.
* **The 50% Formal Collection Ceiling:** Despite generation volumes more than doubling over the study window, average municipal collection efficiency has remained stagnant between **48.5% and 54.0%**, while formal recycling rates plateaued between **39.5% and 46.7%**. Consequently, more than **50% of all discarded municipal electronics escape formal regulatory channels** into the informal dismantling sector.
* **Top Contributing States:** Five states account for the majority of recorded volume:
  1. **Maharashtra** (1,694.8 tons/day)
  2. **Delhi NCT** (1,627.7 tons/day)
  3. **West Bengal** (1,166.3 tons/day)
  4. **Uttar Pradesh** (1,083.3 tons/day)
  5. **Karnataka** (892.9 tons/day)
* **Demographic Collinearity:** Ordinary Least Squares (OLS) regression confirms a statistically significant positive correlation between population density, urbanization rates, and daily generation tonnage, while municipal efficiency scores correlate negatively with informal leakage.

---

## Conceptual Framework: The "One-Way Conveyor Belt"

```
[ Rapid Consumer Adoption ]  ──▶  [ Hardware Obsolescence ]  ──▶  [ Municipal Generation ]
  - Shorter replacement cycles      - 4G to 5G migration           - 1,716+ tons/day (2026)
  - Lower device acquisition cost   - Planned obsolescence         - 7.56% CAGR
                                                                         │
                                                                         ▼
                                                     ┌───────────────────────────────────────┐
                                                     │ 50% Municipal Infrastructure Ceiling  │
                                                     └───────────────────┬───────────────────┘
                                                                         │
                                       ┌─────────────────────────────────┴─────────────────────────────────┐
                                       ▼                                                                   ▼
                         [ Formal Channel (45%) ]                                            [ Informal Leakage (55%) ]
                         - Authorized R2 recyclers                                           - Unregulated scrap yards (kabadiwalas)
                         - Hydrometallurgical extraction                                     - Primitive open acid-bath stripping
                         - 98%+ mineral purity yields                                        - Open-air incineration & lead slag runoff
                         - Safe slag containment                                             - Soil & groundwater heavy metal contamination
```

1. **Input Acceleration:** Consumer electronic lifecycles collapsed from five years to under eighteen months, driven by telecommunication transitions, planned obsolescence, and declining device acquisition costs.
2. **Infrastructure Inelasticity:** Formal municipal recycling infrastructure in most tier-2 and tier-3 centers relies on conventional mechanical sorting rather than specialized hydrometallurgical extraction facilities, freezing authorized processing capacity.
3. **Informal Sector Leakage:** The uncollected delta (>50%) routes through unorganized scrap handlers (*kabadiwalas*), where primitive acid bath stripping and open incineration introduce toxic lead, mercury, and cadmium into local groundwater tables and ambient air.

---

## Streamlit Cloud Deployment Architecture & Engineering

The application is engineered specifically for resilient, continuous deployment on **Streamlit Community Cloud** (`share.streamlit.io`), adhering to production design patterns:

```
                            STREAMLIT APPLICATION RUNTIME PIPELINE
 ┌──────────────────────┐     ┌─────────────────────────────────────────────────────────────┐
 │  Client Web Browser  │ ──▶ │                    Streamlit Server Host                    │
 └──────────────────────┘     │                                                             │
            ▲                 │  ┌───────────────────────────────────────────────────────┐  │
            │ WebSocket       │  │               URL State Engine (st.query_params)      │  │
            │ (Bi-directional)│  │     - Deep-linkable filters (?peers=Mumbai,Delhi)     │  │
            ▼                 │  └──────────────────────────┬────────────────────────────┘  │
 ┌──────────────────────┐     │                             ▼                               │
 │   HTML5 / CSS3 DOM   │     │  ┌───────────────────────────────────────────────────────┐  │
 │  - Plus Jakarta Sans │     │  │             Cached Data Pipeline (@st.cache_data)     │  │
 │  - Keyframe CSS      │ ◀── │  │     - 12h TTL In-Memory Hash Cache                    │  │
 │  - Responsive Layout │     │  │     - Multi-path Fallback Dataset Resolver            │  │
 └──────────────────────┘     │  └──────────────────────────┬────────────────────────────┘  │
                              │                             ▼                               │
                              │  ┌───────────────────────────────────────────────────────┐  │
                              │  │                  Analytical Engine                    │  │
                              │  │     - Altair Layered Peer Benchmarking Engine         │  │
                              │  │     - Plotly 6.0+ Geospatial & Vector Renderers       │  │
                              │  │     - SciPy / Statsmodels OLS Regression Core         │  │
                              │  │     - Dynamic Eco-Policy Circularity Simulator        │  │
                              │  └───────────────────────────────────────────────────────┘  │
                              └─────────────────────────────────────────────────────────────┘
```

### 1. In-Memory Hash Caching (`@st.cache_data` with 12h TTL)
* Processing 25,200+ multi-table records on every interactive widget interaction would induce heavy latency and CPU throttling in cloud containers.
* The data pipeline uses `@st.cache_data(ttl="12h", show_spinner=...)` to load, harmonize, merge, and clean the multi-table datasets into memory once. Filter slicing operations run in memory with sub-50ms execution times.

### 2. Multi-Path Dataset Resolver
* When deploying across different container configurations (e.g., local Windows developer machines vs. Streamlit Cloud's headless Linux Debian containers), working directory paths often differ (`/mount/src/...` vs. `c:\Users\...`).
* The data ingestion layer implements an adaptive `resolve_dataset_path()` resolver that iterates through relative, absolute, parent, and subfolder path candidates to guarantee zero `FileNotFoundError` exceptions upon cloud spin-up.

### 3. URL Parameter State Persistence (`st.query_params`)
* The application synchronizes analytical state (such as active peer benchmarking cities) directly to browser URL query parameters:
  ```python
  st.query_params["peers"] = ",".join(selected_peers)
  ```
* This enables researchers, municipal officers, and educators to share exact analytical views, peer comparisons, and state profiles via direct copy-paste URLs.

### 4. Custom Design System & Micro-Interactions
* **Typography:** Integrates Google Fonts (`Plus Jakarta Sans`) across all DOM elements for clean academic legibility.
* **Dynamic Animations:** Implements custom CSS keyframe animations:
  * `@keyframes gradientFlow`: Fluid 12-second emerald-to-forest gradient shift on executive headers.
  * `@keyframes pulseGlow`: Subtle radiating glow on the live status badge.
* **Interactive Hover Lifts:** Metric cards feature subtle elevation shifts (`transform: translateY(-5px)`) and cubic-bezier border transitions for a modern, tactile feel.
* **Semantic Delta Badges:** Employs explicit color semantics—`delta_color="inverse"` for rising waste accumulation and stagnant recycling ceilings, and `delta_color="normal"` for environmental recovery achievements.

### 5. Defensive Guardrails (`st.stop()`)
* Eliminates unhandled tracebacks and red error banners on Streamlit Cloud.
* If user-applied cross-filters result in an empty dataset slice, the application catches the condition defensively, rendering an informative callout with `:material/info:` guidance and gracefully halting subsequent layout execution using `st.stop()`.

### 6. Cloud Configuration & Theme Directives (`.streamlit/config.toml`)
* Headless mode (`headless = true`) ensures instant background binding without attempting to launch local GUI processes.
* Cross-Site Request Forgery (`enableXsrfProtection = true`) is strictly enforced for cloud security.
* Telemetry collection (`gatherUsageStats = false`) is disabled to prevent latency overhead.
* Brand colors are locked to an environmental theme:
  ```toml
  [theme]
  primaryColor = "#059669"
  backgroundColor = "#f6fbf8"
  secondaryBackgroundColor = "#ffffff"
  textColor = "#0f291e"
  font = "sans serif"
  ```

---

## Interactive Analytical Modules

The web dashboard (`app.py`) is structured into **10 dedicated modules** accessed via an icon-enhanced tab navigation system:

| # | Module | Material Icon | Core Methodological Functionality | Primary Visualization |
|---|---|---|---|---|
| **1** | **Peer Benchmarking** | `:material/compare_arrows:` | **Normalized Multi-City Growth Divergence:** Indexes generation curves to baseline (1.0). Computes each city's trajectory against the composite average of all *other* selected peer cities. | Layered Altair Line & Area Charts with interactive tooltips |
| **2** | **Overview & Growth** | `:material/query_stats:` | **Macro Longitudinal Trajectories:** Analyzes aggregate daily tonnage alongside per-center averages from 2015 to 2026. Computes 11-year CAGR and state rankings. | Dual-axis Plotly line plots & horizontal sorted bar charts |
| **3** | **Eco-Policy Simulator** | `:material/eco:` | **Circular Economy Scenario Modeling:** Interactive what-if policy playground. Adjusts collection targets (%), recycling rates (%), and buyback subsidies (₹/device) to simulate material and financial yields. | Dynamic KPI metric cards with recovery yield indicators |
| **4** | **Distributions & Outliers** | `:material/bar_chart:` | **Univariate Spread Analysis:** Evaluates skewness, log-transformed density distributions, and interquartile range (IQR) boxplots across Metro, Tier-1, Tier-2, and Tier-3 categories. | Plotly KDE density histograms & boxplots |
| **5** | **Waste Composition** | `:material/pie_chart:` | **Part-to-Whole Evolution:** Compares e-waste generation proportions against plastic, organic, and industrial waste streams over the 11-year longitudinal window. | Interactive Plotly Donut Charts & 100% Stacked Area Plots |
| **6** | **Regression & Trends** | `:material/show_chart:` | **Multivariate Collinearity:** Fits Ordinary Least Squares (OLS) models exploring the relationship between demographic variables (population density, urbanization) and daily tonnage. | 4D Bubble Scatter Plots (x: density, y: tons, size: urban%, color: tier) |
| **7** | **Correlation Heatmap** | `:material/grid_on:` | **Feature Collinearity Matrix:** Pearson correlation matrix across demographic indices, collection efficiency, recycling rates, and environmental air quality (AQI). | Diverging Heatmap with annotated correlation coefficients |
| **8** | **Geospatial & City Audit** | `:material/map:` | **Spatial Disparity & Historical Audit:** Plots national municipal performance on an interactive map. Features a deep-dive scorecard for individual city historical audits. | Plotly 6.0+ Vector Map (`scatter_map` / `scatter_geo`) |
| **9** | **Data Explorer & Export** | `:material/table_view:` | **Granular Record Inspection:** Paginated, multi-column searchable tabular data viewer with one-click filtered CSV export capabilities (`st.download_button`). | Streamlit Dataframe with column filters & download utility |
| **10** | **Policy & Engineering** | `:material/policy:` | **Technical Documentation & Policy Roadmaps:** Details schema harmonization, Extended Producer Responsibility (EPR) mandates, and formalization strategies for informal recyclers. | Structured Feynman-style alert callouts & reference guides |

---

## Mathematical & Statistical Formulations

### 1. Compound Annual Growth Rate (CAGR)
The annualized expansion of aggregate electronic waste over the 11-year observational timeframe is modeled as:

$$\text{CAGR} = \left( \frac{V_{2026}}{V_{2015}} \right)^{\frac{1}{n}} - 1$$

Where:
* $V_{2015} = 770.16 \text{ tons/day}$ (Baseline volume)
* $V_{2026} = 1,716.08 \text{ tons/day}$ (Terminal volume)
* $n = 11 \text{ years}$ ($2026 - 2015$)
* Resulting in a national growth rate of **$\approx 7.56\%$ per annum**.

### 2. Peer Group Normalized Divergence Engine
To eliminate scale distortions when comparing mega-metros (e.g., Mumbai, Delhi) against emerging tech hubs (e.g., Pune, Hyderabad), the platform computes a **Normalized Base Index ($I_{i,t}$)**:

$$I_{i,t} = \frac{G_{i,t}}{G_{i, t_0}}$$

Where $G_{i,t}$ is the daily waste generation of city $i$ in year $t$, and $t_0 = 2015$.

To benchmark city $i$ without self-bias, the synthetic **Peer Benchmark Index ($P_{i,t}$)** calculates the unweighted mean of all selected peers $S$ excluding city $i$:

$$P_{i,t} = \frac{1}{|S| - 1} \sum_{j \in S, \, j \neq i} I_{j,t}$$

The **Divergence Factor ($\Delta_{i,t}$)** is evaluated as:

$$\Delta_{i,t} = I_{i,t} - P_{i,t}$$

* $\Delta_{i,t} > 0$: City is accumulating e-waste at an accelerated velocity relative to its peer group.
* $\Delta_{i,t} < 0$: City demonstrates relative mitigation or slower growth than its peer group.

### 3. Circular Economy Scenario Equations
The Eco-Policy Simulator models four environmental and economic recovery dimensions:

1. **Net Landfill Diversion ($\mathcal{D}$):**
   $$\mathcal{D} = G_{\text{annual}} \times \left( \frac{\eta_{\text{target}} - \eta_{\text{base}}}{100} \right) \times \left( \frac{\rho_{\text{recycle}}}{100} \right)$$

2. **Heavy Metal Containment ($\mathcal{H}_{\text{toxic}}$):**
   $$\mathcal{H}_{\text{toxic}} = \mathcal{D} \times \left( \beta_{\text{lead}} + \beta_{\text{mercury}} + \beta_{\text{cadmium}} \right)$$
   *(where $\beta$ represents empirical metal composition constants per ton of mixed e-waste).*

3. **Critical Mineral Reclamation Value ($\mathcal{V}_{\text{mineral}}$):**
   $$\mathcal{V}_{\text{mineral}} = \sum_{k \in \{\text{Au, Cu, Pd, REE}\}} \left( \mathcal{D} \times \gamma_k \times \mathcal{P}_k \times \epsilon_{\text{recovery}} \right)$$
   *(where $\gamma_k$ is metal yield/ton, $\mathcal{P}_k$ is market price, and $\epsilon$ is hydrometallurgical extraction efficiency).*

4. **Net Carbon Abatement ($\mathcal{C}_{\text{GHG}}$):**
   $$\mathcal{C}_{\text{GHG}} = \mathcal{D} \times \left( \phi_{\text{virgin extraction}} - \phi_{\text{secondary recycling}} \right) \text{ MT } \text{CO}_2\text{e}$$

---

## Dataset Architecture & Schema Reference

The platform synthesizes data across three structured sources located in `data/`:

```
   data/
   ├── Waste_Management_India_20K.csv            (25,200+ records, 2015-2026)
   ├── Waste_Management_and_Recycling_India.csv  (Municipal infrastructure & recycling data)
   └── cities_master.csv                         (City geospatial coordinates & classifications)
```

### 1. Longitudinal Master Dataset (`Waste_Management_India_20K.csv`)
* **Scope:** 25,200+ municipal observation rows covering 2015 through 2026.
* **Fields:**
  * `Year` (Integer: 2015–2026)
  * `City` (Categorical: Indian municipal corporations)
  * `State` (Categorical: State / Union Territory)
  * `Region` (North, South, East, West, Central, North-East)
  * `City_Category` (Metro, Tier-1, Tier-2, Tier-3)
  * `Population` (Numeric: Census and projected municipal population)
  * `Population_Density_per_sq_km` (Numeric: Inhabitants per km²)
  * `Urbanization_Rate` (Float: Urban sprawl and density index)
  * `Waste_Type` (E-Waste, Plastic, Organic, Industrial)
  * `Daily_Waste_Generation_Tons` (Float: Measured generation in metric tons/day)
  * `Collection_Efficiency_Percentage` (Float: Formal municipal collection rate, 0–100%)
  * `Recycling_Rate` (Float: Formal authorized processing rate, 0–100%)
  * `Air_Quality_Index` (Numeric: Local AQI metric)

### 2. Recycling Infrastructure Dataset (`Waste_Management_and_Recycling_India.csv`)
* **Scope:** Municipal treatment capacity, mechanical vs. hydrometallurgical recycling, informal scrap leakage.
* **Schema Harmonization:** The raw column `City/District` is programmatically sanitized and renamed to `City` to ensure relational joins across datasets.

### 3. Geospatial Reference Master (`cities_master.csv`)
* **Scope:** Master spatial coordinates for GIS mapping.
* **Fields:** `City`, `State`, `Latitude`, `Longitude`, `Is_Tourist`, `Is_Hill_Station`.

---

## Repository Directory Tree

```text
india-ewaste-analytics/
├── .streamlit/
│   └── config.toml                           # Streamlit UI theme, headless server & XSRF settings
├── data/
│   ├── Waste_Management_India_20K.csv        # Longitudinal records (25,200+ rows, 2015-2026)
│   ├── Waste_Management_and_Recycling_India.csv # Municipal recycling & facility benchmarks
│   └── cities_master.csv                     # City GIS coordinates, states, and geographic metadata
├── notebooks/
│   └── ewem-dataanalysis.ipynb               # Reference exploratory data analysis & validation
├── app.py                                    # Enterprise Streamlit application (1,170+ lines)
├── requirements.txt                          # Pinned Python package dependencies for cloud builds
├── .gitignore                                # Version control exclusion rules
└── README.md                                 # Comprehensive project documentation
```

---

## Installation & Local Execution

### Prerequisites
* **Python:** Version `3.10`, `3.11`, or `3.12`
* **Git:** Version `2.30+`
* **RAM:** Minimum 2 GB recommended

### Step-by-Step Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/rujopujo/india-ewaste-analytics.git
   cd india-ewaste-analytics
   ```

2. **Initialize a virtual environment:**
   ```bash
   # Windows (PowerShell)
   python -m venv .venv
   .venv\Scripts\Activate.ps1

   # macOS / Linux (bash/zsh)
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Run the Streamlit application:**
   ```bash
   streamlit run app.py
   ```
   The application will automatically bind to `http://localhost:8501` and launch your default browser.

---

## Streamlit Cloud Deployment Guide

The application is deployed live on **Streamlit Community Cloud**:

> 🌐 **Production URL:** [https://india-ewaste-analytics-rukaryjpzq4futpejbkf3v.streamlit.app](https://india-ewaste-analytics-rukaryjpzq4futpejbkf3v.streamlit.app)

### Re-Deploying or Forking to Your Own Streamlit Cloud Instance:

1. **Fork or Push:** Ensure your repository is pushed to GitHub with `app.py`, `requirements.txt`, `.streamlit/config.toml`, and the `data/` directory.
2. **Access Streamlit Cloud:** Navigate to [share.streamlit.io](https://share.streamlit.io) and authenticate with your GitHub account.
3. **Configure New App:**
   * **Repository:** `your-username/india-ewaste-analytics`
   * **Branch:** `main`
   * **Main file path:** `app.py`
   * **App URL:** Customize your desired subdomain.
4. **Deploy:** Click **Deploy!** Streamlit Cloud will create a container, install packages from `requirements.txt`, and initialize the app.

### Deployment Best Practices & Troubleshooting

* **Headless Display & Visualization Fallback:** Plotly vector maps automatically detect cloud container limitations. If WebGL context is restricted, maps gracefully fall back to standard projection renderers or `st.map()`.
* **Container Memory Limits:** Streamlit Community Cloud enforces a ~1 GB RAM limit. The combination of `@st.cache_data` and memory-efficient categorical dtype downcasting prevents container Out-Of-Memory (OOM) termination.
* **Relative File Path Integrity:** The custom `resolve_dataset_path()` utility in `app.py` prevents path resolution crashes when running in Streamlit Cloud's `/mount/src/` environment.

---

## Technology Stack

| Domain | Technology / Library | Minimum Version | Purpose |
|---|---|---|---|
| **Web Runtime** | `streamlit` | `1.35.0+` | Reactive web dashboard, session state, URL sync, UI layout |
| **Data Manipulation** | `pandas` | `2.0.0+` | Vectorized dataset ingestion, schema merging, aggregation |
| **Numerical Processing** | `numpy` | `1.24.0+` | Array operations, log transformations, CAGR modeling |
| **Interactive Plotting** | `plotly` | `5.18.0+` | Vector charts, bubble plots, donut charts, scatter maps |
| **Peer Benchmarking** | `altair` | `5.0.0+` | Layered multi-series normalized line & area divergence plots |
| **Statistical Analysis** | `scipy` | `1.10.0+` | Kernel density estimations (KDE), variance statistics |
| **Econometric Modeling**| `statsmodels`| `0.14.0+` | Ordinary Least Squares (OLS) bivariate & multivariate regressions|
| **Static Visualization**| `seaborn`, `matplotlib` | `0.12.0+`, `3.7.0+` | Fallback exploratory statistical plots |

---

## Policy Implications & Recommendations

1. **Formalizing the Informal Sector:** Rather than criminalizing unorganized scrap dealers (*kabadiwalas*), municipalities must establish **Authorized Aggregation Hubs** where informal collectors receive fair-market buyback prices for intact electronics, preventing open-air acid leaching.
2. **Extended Producer Responsibility (EPR) Auditability:** Current EPR credit systems rely heavily on paper certificates. Integrating state-level IoT weighing bridges at authorized recycling facilities can eliminate double-counting of recycled tonnage.
3. **Decentralized Hydrometallurgical Hubs:** Tier-2 and Tier-3 urban clusters require regional hydrometallurgical recycling facilities subsidized through public-private partnerships (PPP), reducing high inter-state shipping overheads that incentivize illegal local dumping.

---

## License

Distributed under the **MIT License**. See `LICENSE` for details.
