# India E-Waste Growth Analytics & Circularity Assessment

> 🌐 **Live Web Application:** [https://india-ewaste-analytics-rukaryjpzq4futpejbkf3v.streamlit.app](https://india-ewaste-analytics-rukaryjpzq4futpejbkf3v.streamlit.app)  
> [![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://india-ewaste-analytics-rukaryjpzq4futpejbkf3v.streamlit.app)

An interactive data analytics platform investigating electronic waste accumulation, regional growth trajectories, municipal infrastructure bottlenecks, and peer group benchmarking across Indian urban centers (2015–2026).

**Academic Attribution:**
* **Ruhaan Joshi** — Roll No: `24101C0057`
* **Om Thakur** — Roll No: `24101C0041`
* **Rudra Jain** — Roll No: `24101C0062`
* **Department:** Department of Information Technology
* **Batch:** INFT-C Batch 3
* **Live Deployment:** [india-ewaste-analytics-rukaryjpzq4futpejbkf3v.streamlit.app](https://india-ewaste-analytics-rukaryjpzq4futpejbkf3v.streamlit.app)
* **Repository:** [https://github.com/rujopujo/india-ewaste-analytics](https://github.com/rujopujo/india-ewaste-analytics)

---

## Abstract

Rapid digitalization, shortened device replacement cycles, and expanding consumer electronics adoption have positioned electronic waste (e-waste) among the fastest growing municipal waste streams in India. Using an 11-year longitudinal dataset of over 25,200 municipal records across Indian urban centers, this project analyzes the statistical growth rate of e-waste generation, isolates severe geographical and tier-based disparities, diagnoses municipal collection bottlenecks, and models circular resource recovery scenarios using an interactive web platform built with Streamlit, Plotly, and Altair.

---

## Research Objectives

1. **Growth Quantification:** Measure daily e-waste generation trends from 2015 to 2026 and compute the national Compound Annual Growth Rate (CAGR).
2. **Urban Disparity Assessment:** Contrast generation volumes across Metros, Tier-1, Tier-2, and Tier-3 urban centers to determine concentration ratios.
3. **Infrastructure Bottleneck Diagnosis:** Evaluate the operational gap between consumer disposal rates, municipal collection efficiencies, and authorized recycling capacities.
4. **Peer Group Benchmarking:** Provide normalized, indexed comparative analytics enabling side-by-side performance assessments of Indian municipal corporations against peer averages.
5. **Circular Economy Scenario Modeling:** Construct an interactive policy simulator projecting landfill diversion, toxic heavy metal containment, critical mineral recovery yields, and net carbon abatement.

---

## Key Empirical Findings

* **Longitudinal Growth (7.56% CAGR):** Aggregate daily logged e-waste generation rose from **770.16 tons/day in 2015** to **1,716.08 tons/day in 2026**, representing an overall Compound Annual Growth Rate of **7.56%**. Distinct acceleration spikes occurred during 2019, 2022, and 2025–2026, coinciding with national hardware refresh cycles.
* **140x Urban Generation Disparity:** E-waste is overwhelmingly concentrated in commercial metropolitan hubs. Reporting stations in **Metros average 141.32 tons/day**, compared to **1.01 tons/day in Tier-3 centers**—an urban disparity factor of approximately 140x.
* **The 50% Collection Ceiling:** Despite generation volume more than doubling over the study window, average municipal collection efficiency has remained stagnant between **48.5% and 54.0%**, while formal recycling rates plateaued between **39.5% and 46.7%**. Consequently, over half of all discarded municipal electronics escape formal regulatory channels.
* **Top Contributing States:** Five states account for the majority of recorded volume: **Maharashtra** (1,694.8 tons/day), **Delhi NCT** (1,627.7 tons/day), **West Bengal** (1,166.3 tons/day), **Uttar Pradesh** (1,083.3 tons/day), and **Karnataka** (892.9 tons/day).
* **Demographic Collinearity:** Ordinary Least Squares (OLS) regression confirms a statistically significant positive correlation between population density, urbanization rates, and daily generation tonnage, while municipal efficiency scores correlate negatively with informal leakage.

---

## Conceptual Framework: The "One-Way Conveyor Belt"

To explain the operational divergence between hardware obsolescence and municipal treatment capacity, the study applies the conveyor belt model:

1. **Input Acceleration:** Consumer electronic lifecycles collapsed from five years to under eighteen months, driven by rapid telecommunication transitions (4G to 5G), planned obsolescence, and declining device acquisition costs.
2. **Infrastructure Inelasticity:** Formal municipal recycling infrastructure in most tier-2 and tier-3 centers relies on conventional mechanical sorting rather than specialized hydrometallurgical extraction facilities, freezing authorized processing capacity.
3. **Informal Sector Leakage:** The uncollected delta (>50%) routes through unorganized scrap handlers (kabadiwalas), where primitive acid bath stripping and open incineration introduce toxic lead, mercury, and cadmium into local groundwater tables and ambient air.

---

## Application Architecture & Analytical Modules

The dashboard (`app.py`) is structured into ten distinct analytical modules:

| Module | Core Functionality | Methodological Focus |
|---|---|---|
| **1. Peer Benchmarking Engine** | Multi-City Comparative Analysis | Normalized growth curves indexed to 1.0; individual city trajectory plotted against peer group average (excluding the subject city); delta area divergence charts. |
| **2. Executive Overview & Growth** | Longitudinal Macro Trends | Dual-axis generation trends (total daily tonnage vs. per-center mean), state rankings, and conceptual framework. |
| **3. Eco-Policy Simulator** | Circular Economy Modeling | Dynamic what-if simulator adjusting collection targets, recycling rates, and buyback subsidies to project landfill diversion, toxin containment, recovered mineral value, and CO2 abatement. |
| **4. Distributions & Outliers** | Univariate Spread Analysis | Histograms and Kernel Density Estimation (KDE) with log-scale transformation options and quartile boxplots across city tiers. |
| **5. Waste Composition** | Part-to-Whole Breakdown | Interactive donut charts and longitudinal stacked area plots tracking e-waste share relative to organic, plastic, and industrial waste. |
| **6. Regression & Trends** | Multivariate Bivariate Analysis | OLS trendlines (population density vs. daily tonnage) and 4D bubble charts (sized by urbanization, colored by city tier). |
| **7. Correlation Heatmap** | Collinearity Matrix | Pearson correlation coefficient matrix across demographic indices, collection efficiency, recycling rates, and air quality index (AQI). |
| **8. Geospatial & City Audit** | Spatial Mapping & Urban Profiling | Interactive map of India plotting collection efficiency and waste volume; searchable city-by-city historical audit scorecard. |
| **9. Data Explorer & Export** | Granular Record Inspection | Searchable, paginated tabular view with dynamic column filtering and one-click filtered CSV export. |
| **10. Policy & Engineering Notes** | Technical Post-Mortem & Recommendations | Engineering documentation on schema alignment (`City/District` vs. `City`) and policy recommendations for Extended Producer Responsibility (EPR). |

---

## Software Engineering Highlights

* **State Synchronization via URL Parameters (`st.query_params`):** User filter states, selected peer cities, and active metrics automatically sync to the URL query string, making specific filtered analytical views deep-linkable and shareable.
* **High-Performance In-Memory Caching (`@st.cache_data`):** Multi-table datasets totaling 25,200+ records are preprocessed and cached in memory with a 12-hour TTL, enabling sub-second filtering and re-rendering.
* **Defensive Error Handling (`st.stop()`):** Input selections are guarded against null or empty filter states using informative callouts and clean process termination, eliminating unhandled runtime tracebacks.
* **Dual Visualization Engines:** Combines Plotly for vector charts and map rendering with Altair for comparative peer analysis.
* **Modular Clean Repository Structure:** Clear separation of data storage (`data/`), analytical notebooks (`notebooks/`), application configuration (`.streamlit/`), and core application logic (`app.py`).

---

## Repository Directory Tree

```text
india-ewaste-analytics/
├── .streamlit/
│   └── config.toml                         # Streamlit UI theme and server configuration
├── data/
│   ├── Waste_Management_India_20K.csv          # Longitudinal dataset (25,200+ records, 2015-2026)
│   ├── Waste_Management_and_Recycling_India.csv# Municipal recycling dataset
│   └── cities_master.csv                       # City coordinates, state, and geographic metadata
├── notebooks/
│   └── ewem-dataanalysis.ipynb                 # Reference exploratory data analysis notebook
├── app.py                                  # Main Streamlit web application
├── requirements.txt                        # Python package dependencies
├── .gitignore                              # Git exclusion rules
└── README.md                               # Academic project documentation
```

---

## Installation & Local Execution

### Prerequisites
* Python 3.10 or higher
* Git

### Step-by-Step Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/rujopujo/india-ewaste-analytics.git
   cd india-ewaste-analytics
   ```

2. **Create and activate a virtual environment:**
   ```bash
   # Windows
   python -m venv .venv
   .venv\Scripts\activate

   # macOS / Linux
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Launch the application:**
   ```bash
   streamlit run app.py
   ```
   The application will automatically initialize in your default web browser at `http://localhost:8501`.

---

## Cloud Deployment Guide

The application is deployed and live on **Streamlit Community Cloud**:

> 🌐 **Live Web App:** [https://india-ewaste-analytics-rukaryjpzq4futpejbkf3v.streamlit.app](https://india-ewaste-analytics-rukaryjpzq4futpejbkf3v.streamlit.app)

### Re-deploying or Hosting Your Own Instance:

1. Host the repository on GitHub under a public repository.
2. Sign in to [share.streamlit.io](https://share.streamlit.io) via GitHub authentication.
3. Select repository `rujopujo/india-ewaste-analytics`, branch `main`, and main file path `app.py`.
4. Click **Deploy**. The platform will install packages specified in `requirements.txt` and launch the application at a public URL.

---

## Technology Stack

* **Language:** Python 3.10+
* **Web Framework:** Streamlit (v1.35+)
* **Visualization:** Plotly Express, Plotly Graph Objects, Altair, Seaborn, Matplotlib
* **Data Processing:** Pandas, NumPy
* **Statistical Modeling:** SciPy, Statsmodels (OLS regression)

---

## License

This project is licensed under the MIT License. See `LICENSE` for details.
