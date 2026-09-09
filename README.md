# India E-Waste Growth Analytics

An interactive data analytics dashboard analyzing electronic waste generation, regional growth trends, municipal collection bottlenecks, and recycling efficiencies across urban centers in India (2015–2026).

**Authors:**
- Ruhaan Joshi (`24101C0057`)
- Om Thakur (`24101C0041`)
- Rudra Jain (`24101C0062`)
- Department of Information Technology, Batch INFT-C

---

## Overview

Electronic waste is among the fastest growing municipal waste streams in India. Using an 11-year longitudinal dataset of over 25,000 municipal records across major Indian cities, this project investigates how quickly e-waste generation is accelerating, where the volume is concentrated, and why municipal infrastructure struggles to keep pace.

### Key Empirical Findings

- **Generation Growth (7.56% CAGR):** Daily municipal e-waste generation recorded across reporting cities grew from 770.16 tons/day in 2015 to 1,716.08 tons/day in 2026 (7.56% compounded annually), with notable surges during 2019, 2022, and 2025–2026.
- **Urban Disparity:** E-waste is heavily skewed toward metropolitan hubs. Metros average 141.32 tons/day per reporting station, whereas Tier-3 centers log approximately 1.01 tons/day (a ~140x disparity).
- **Collection Bottleneck:** While hardware turnover has accelerated, authorized municipal collection efficiency has remained largely flat between 48.5% and 54.0%, leaving nearly half of discarded electronic hardware to informal scrap channels.
- **Top Contributing States:** Maharashtra (1,694.8 tons/day), Delhi NCT (1,627.7 tons/day), West Bengal (1,166.3 tons/day), Uttar Pradesh (1,083.3 tons/day), and Karnataka (892.9 tons/day).

---

## Conceptual Framework: The One-Way Conveyor Belt

To explain the systemic challenge behind India's e-waste growth, the analysis models urban flows as a conveyor belt:

1. **Input Acceleration:** Device turnover has quickened significantly as replacement cycles shortened from approximately five years to under eighteen months due to rapid consumer electronics adoption, telecom transitions, and hardware obsolescence.
2. **Infrastructure Inelasticity:** Municipal formal sorting, aggregation, and certified dismantling infrastructure have not scaled at the same rate, capping authorized recovery at ~50%.
3. **Informal Sector Leakage:** The remaining volume is absorbed by unorganized scrap handlers (kabadiwalas), where informal extraction methods pose significant environmental and health risks.

---

## Dashboard Structure

The application (`app.py`) is structured into eight modules:

1. **Executive Overview & Growth:** Longitudinal trends, annual daily tonnage comparisons, state rankings, and core metrics.
2. **Univariate & Outlier Analysis:** Distribution shapes, kernel density estimates, and boxplots across city tiers.
3. **Composition Analysis:** Proportional breakdowns comparing e-waste against organic, plastic, and industrial waste.
4. **Regression & Multivariate Trends:** OLS regression (population density vs. daily generation), multi-variable bubble plots, and violin distribution plots.
5. **Correlation Analysis:** Collinearity heatmaps and joint density distributions comparing demographics and municipal scores.
6. **Geospatial & Regional Facets:** Multi-panel regional time-series plots (North, South, West, East, Central, Northeast) and geographical distribution across cities.
7. **Data Explorer:** Searchable interface with dynamic column filters and CSV export capability.
8. **Policy & Engineering Notes:** Technical notes on data schema alignment and policy recommendations for Extended Producer Responsibility (EPR).

---

## Repository Structure

```text
india-ewaste-analytics/
├── .streamlit/
│   └── config.toml          # Streamlit UI configuration
├── data/
│   ├── Waste_Management_India_20K.csv           # 25,200+ municipal records (2015-2026)
│   ├── Waste_Management_and_Recycling_India.csv # City-level recycling metrics
│   └── cities_master.csv                        # Geographic coordinates and city classifications
├── notebooks/
│   └── ewem-dataanalysis.ipynb                  # Exploratory data analysis notebook
├── app.py                   # Streamlit web application
├── requirements.txt         # Python package dependencies
├── .gitignore
└── README.md
```

---

## Getting Started

### Prerequisites
- Python 3.10 or higher
- pip

### Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/rujopujo/india-ewaste-analytics.git
   cd india-ewaste-analytics
   ```

2. Create and activate a virtual environment:
   ```bash
   # Windows
   python -m venv .venv
   .venv\Scripts\activate

   # macOS/Linux
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

The app will open automatically in your browser at `http://localhost:8501`.

---

## Cloud Deployment (Streamlit Community Cloud)

To deploy this dashboard online:
1. Fork or push this repository to GitHub.
2. Sign in to [share.streamlit.io](https://share.streamlit.io) with your GitHub account.
3. Select repository `rujopujo/india-ewaste-analytics`, branch `main`, and main file path `app.py`.
4. Click **Deploy**.

---

## Tech Stack
- Python
- Streamlit
- Plotly
- Pandas / NumPy
- Seaborn / Matplotlib
- Scipy / Statsmodels

## License
MIT License
