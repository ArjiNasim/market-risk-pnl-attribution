# 📈 Automated Market Risk & P&L Attribution Analytics Engine

End-to-end quantitative risk and data engineering pipeline designed to automate the processing, monitoring, and reporting of market risk metrics and P&L attribution for Fixed Income & Equities (FIC / EQD) trading desks.

## 🎯 Project Overview
In a trading floor environment, ensuring the integrity of Daily P&L and monitoring risk consumption against allocated limits is critical for the 1st and 2nd Lines of Defense (LOD1 / LOD2). This project simulates a full automated workflow: from synthetic trade data generation to interactive limit breach alerts and unexplained P&L flagging.

## ⚙️ Core Modules & Features

* **1. Synthetic Data Engine:** Generates realistic daily datasets including positions, sensitivities (Delta, Gamma, Vega, DV01), VaR (Historical & Parametric), Stress Tests, and P&L components (Market, Carry, Unexplained).
* **2. Risk Aggregation & Data Quality:** Multi-level aggregation from individual trades to asset classes (FIC/EQD). Includes data certification controls (e.g., flagging >30% divergence between Historical and Parametric VaR).
* **3. Automated Limit Monitoring:** Compares aggregated risk metrics against Risk Management limits, generating automated severity-based alerts (CRITICAL, HIGH, MEDIUM) for any limit breaches.
* **4. P&L Income Attribution:** Isolates and flags abnormal daily variations. Triggers "INVESTIGATION REQUIRED" if the Unexplained P&L exceeds predefined critical thresholds (relative ratio or absolute value).
* **5. Executive Reporting & Export:** Automatically drafts an Executive Summary for Senior Management and exports structured data in `.parquet` and `.csv` formats, optimized for seamless integration with PowerBI or Streamlit dashboards.

## 🛠️ Tech Stack
* **Language:** Python 3.10+
* **Libraries:** Pandas, NumPy, Matplotlib, Seaborn, PyArrow
* **Data Architecture:** Automated Parquet exports for BI dashboarding readiness

## 🚀 How to Run (Google Colab / Jupyter)
1. Clone the repository:
   ```bash
   git clone [https://github.com/ArjiNasim/market-risk-pnl-attribution.git](https://github.com/ArjiNasim/market-risk-pnl-attribution.git)
