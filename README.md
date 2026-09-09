# ⚡ India's E-Waste Growth: Interactive Analytics & Deployment Dashboard

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-teal.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

An interactive, production-grade **Streamlit Data Analytics Dashboard** analyzing the accumulation, regional growth trajectories, municipal infrastructure bottlenecks, and recovery efficiencies of electronic waste (E-Waste) across Indian urban centers.

This platform translates the empirical findings of an 11-year longitudinal dataset (2015–2026) across 25,200+ municipal records into dynamic, multi-dimensional visualizations powered by **Plotly** and **Streamlit**.

---

## 👥 Authors & Academic Attribution
* **Ruhaan Joshi** — `24101C0057`
* **Om Thakur** — `24101C0041`
* **Rudra Jain** — `24101C0062`
* **Department & Batch**: INFT-C Batch 3

---

## 📌 Executive Summary & Key Findings

1. **Growth Trajectory (7.56% CAGR):**
   Daily logged e-waste generation increased from **770.16 tons/day (2015)** to **1,716.08 tons/day (2026)**, representing an overall Compound Annual Growth Rate (CAGR) of **7.56%**, with massive surges in 2019, 2022, and 2025–2026 corresponding to consumer hardware upgrade cycles.
2. **140x Urban Disparity:**
   E-waste generation is hyper-concentrated in commercial metros. **Metros average 141.32 tons/day** per observation, while **Tier-3 centers log only 1.01 tons/day**—an urban disparity ratio of over 140x.
3. **The 50% Collection Bottleneck:**
   While device turnover doubled, authorized collection efficiency flatlined between **48.5% and 54.0%**, and recycling rates hovered at **39.5% to 46.7%**. Nearly half of all municipal e-waste escapes authorized recovery channels.
4. **Top 5 Contributing States:**
   **Maharashtra** (1,695 T/D), **Delhi NCT** (1,628 T/D), **West Bengal** (1,166 T/D), **Uttar Pradesh** (1,083 T/D), and **Karnataka** (893 T/D).

---

## 🧠 The Feynman Concept: The "One-Way Conveyor Belt"
*Imagine your city sitting beside a giant conveyor belt:*
- **Intake:** Brand new smartphones, laptops, smart TVs, and IoT appliances arrive continuously at digital speeds.
- **Exit:** Household obsolescence cycles dropped from 5 years to 18 months, speeding up the conveyor belt by 7.56% annually.
- **The Chokepoint:** Municipal recycling capacity remained stagnant, spilling toxic heavy metals (lead, mercury, cadmium) into informal scrap yards (*kabadiwalas*) and open landfills.

---

## 🖥️ Dashboard Architecture & Interactive Modules

The Streamlit app is organized into **8 specialized modules**:

| Tab | Feature Area | Description |
|---|---|---|
| **1. 🌟 Executive Overview & Growth** | Longitudinal Trends & KPIs | Dual-axis charts of daily tonnage and per-center averages (2015–2026), state leaderboards, and the Feynman conceptual model. |
| **2. 📊 Univariate & Outliers** | Distribution & Extreme Values | Interactive KDE & histograms with log-scaling, boxplots across city categories, and ranked city bar charts. |
| **3. 🥧 Composition & Share** | Part-to-Whole Breakdown | Donut charts and longitudinal stacked bars illustrating the proportional share of E-Waste vs Organic, Plastic, and Industrial categories. |
| **4. 📈 Regression & Multivariate** | Bivariate & 4D Relationships | OLS regression trends (Density vs Generation), multivariate bubble chart (sized by urbanization, colored by city tier), and violin quartile distributions. |
| **5. 🔥 Correlation & Hexbins** | Multicollinearity & Density | Pearson correlation matrix across demographics, efficiency, and environmental metrics, alongside joint 2D density distributions. |
| **6. 🗺️ Geospatial & Regional Facets** | Spatial & Demographic Mapping | Interactive map of India with generation/efficiency bubbles, regional time-series facet grids, and tourism/hill station comparative analysis. |
| **7. 🔍 Data Explorer & Export** | Filtered Table & Slicing | Instant keyword search, customized column views, descriptive statistical tables, and one-click filtered CSV export. |
| **8. 💡 Post-Mortem & Policy** | Engineering & Governance | Post-mortem of notebook schema reconciliation (`City/District` vs `City`), and actionable policy framework (EPR clusters, formalizing scrap networks). |

---

## 🚀 Local Installation & Execution

### 1. Clone or Open the Repository
```bash
git clone https://github.com/<your-username>/<your-repo-name>.git
cd <your-repo-name>
```

### 2. Create and Activate a Virtual Environment
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Launch the Streamlit App
```bash
streamlit run app.py
```
Open your browser and navigate to `http://localhost:8501`.

---

## 🌐 Deploying to GitHub & Streamlit Community Cloud (Free)

Follow these exact steps to publish your code to GitHub and deploy a public live web app:

### Step A: Push to GitHub

1. **Open your terminal** in this project folder (`ewem-dataanalysis`).
2. **Stage and commit all project files**:
   ```bash
   git add .
   git commit -m "feat: complete interactive e-waste analysis streamlit web app"
   ```
3. **Create a new repository on GitHub**:
   - Go to [github.com/new](https://github.com/new).
   - Name your repository (e.g. `india-ewaste-growth-dashboard`).
   - Leave it **Public**.
   - Do **NOT** check "Add a README", ".gitignore", or license (we already have them).
   - Click **Create repository**.
4. **Link and push your local repo to GitHub**:
   ```bash
   git branch -M main
   git remote add origin https://github.com/<YOUR-GITHUB-USERNAME>/<YOUR-REPO-NAME>.git
   git push -u origin main
   ```

---

### Step B: Deploy on Streamlit Community Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io) and log in with your **GitHub account**.
2. Click **Create app** (or **New app** in the top-right corner).
3. Under **Repository**, select your newly pushed repo: `<YOUR-GITHUB-USERNAME>/<YOUR-REPO-NAME>`.
4. Under **Branch**, select `main`.
5. Under **Main file path**, enter `app.py`.
6. Click **Deploy!**
7. Streamlit Cloud will install `requirements.txt`, load the datasets, and spin up your dashboard in ~2 minutes with a live public URL (e.g. `https://<your-app-name>.streamlit.app`).

---

## 📂 Repository File Structure

```text
ewem-dataanalysis/
├── app.py                                  # Main Streamlit dashboard application
├── requirements.txt                        # Production Python dependencies
├── .gitignore                              # Clean git tracking rules
├── README.md                               # Project documentation & deployment guide
├── .streamlit/
│   └── config.toml                         # Custom emerald/teal theme and server settings
├── cities_master.csv                       # Master Indian city metadata (coordinates, regions)
├── Waste_Management_and_Recycling_India.csv# Municipal recycling dataset
├── Waste_Management_India_20K.csv          # 25,200+ longitudinal records (2015-2026)
└── ewem-dataanalysis.ipynb                 # Reference research Jupyter Notebook
```

---

## 📦 Dependencies

* `streamlit` — Modern interactive web dashboard framework
* `plotly` — Interactive vector plotting library (zoom, pan, hover)
* `pandas` & `numpy` — High-performance tabular data processing
* `seaborn` & `matplotlib` — Scientific distribution plotting
* `scipy` & `statsmodels` — OLS trendlines and kernel density estimations

---

## 📜 License
This project is open-source under the MIT License.
