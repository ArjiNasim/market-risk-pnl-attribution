import streamlit as st
import pandas as pd
import numpy as np
import datetime
import plotly.express as px
import plotly.graph_objects as go

# Configuration de la page
st.set_page_config(
    page_title="Market Risk & P&L Analytics Engine",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Automated Market Risk & P&L Attribution Analytics Engine")
st.caption("Real-time Risk Consumption Monitoring, P&L Attribution & Data Certification Dashboard")
st.markdown("---")

# Generation de donnees synthétiques
@st.cache_data
def load_market_data(selected_date):
    np.random.seed(42 + selected_date.day)
    desks = ['FIC_Rates', 'FIC_Credit', 'EQD_Delta', 'EQD_Vol']
    n_records = 600

    df_risk = pd.DataFrame({
        'Date': selected_date,
        'Trade_ID': [f'TRD_{i:04d}' for i in range(n_records)],
        'Desk': np.random.choice(desks, n_records),
        'Delta': np.random.normal(0, 50000, n_records),
        'Gamma': np.random.normal(0, 10000, n_records),
        'Vega': np.random.normal(1000, 20000, n_records),
        'DV01': np.random.normal(0, 5000, n_records),
        'VaR_Hist_99': np.random.uniform(10000, 150000, n_records),
        'VaR_Param_99': np.random.uniform(9000, 160000, n_records),
        'Stress_Test_Global': np.random.uniform(50000, 500000, n_records)
    })

    df_pnl = pd.DataFrame({
        'Date': selected_date,
        'Trade_ID': df_risk['Trade_ID'],
        'Desk': df_risk['Desk'],
        'PnL_Market': np.random.normal(8000, 25000, n_records),
        'PnL_Carry': np.random.normal(1500, 3000, n_records),
        'PnL_Unexplained': np.random.normal(0, 4500, n_records)
    })
    df_pnl['Daily_PnL'] = df_pnl['PnL_Market'] + df_pnl['PnL_Carry'] + df_pnl['PnL_Unexplained']

    df_limits = pd.DataFrame({
        'Desk': desks,
        'Limit_VaR_99': [1800000, 2200000, 2800000, 3500000],
        'Limit_Stress_Test': [7500000, 8500000, 11000000, 14000000],
        'Limit_DV01': [120000, 180000, 0, 0],
        'Limit_Vega': [0, 40000, 450000, 1800000]
    })

    return df_risk, df_pnl, df_limits

# Sidebar
st.sidebar.header("⚙️ Control Panel")
selected_date = st.sidebar.date_input("Trading Date", datetime.date.today())

df_risk, df_pnl, df_limits = load_market_data(selected_date)
df_risk['Asset_Class'] = df_risk['Desk'].apply(lambda x: 'FIC' if 'FIC' in x else 'EQD')
df_pnl['Asset_Class'] = df_pnl['Desk'].apply(lambda x: 'FIC' if 'FIC' in x else 'EQD')

asset_class_filter = st.sidebar.multiselect("Asset Class", options=['FIC', 'EQD'], default=['FIC', 'EQD'])
available_desks = df_risk[df_risk['Asset_Class'].isin(asset_class_filter)]['Desk'].unique()
desk_filter = st.sidebar.multiselect("Trading Desk", options=available_desks, default=available_desks)

df_risk_filtered = df_risk[df_risk['Desk'].isin(desk_filter)]
df_pnl_filtered = df_pnl[df_pnl['Desk'].isin(desk_filter)]

df_master = pd.merge(df_risk_filtered, df_pnl_filtered, on=['Date', 'Trade_ID', 'Desk', 'Asset_Class'])
metrics = ['Delta', 'Gamma', 'Vega', 'DV01', 'VaR_Hist_99', 'VaR_Param_99', 'Stress_Test_Global', 
           'PnL_Market', 'PnL_Carry', 'PnL_Unexplained', 'Daily_PnL']
df_agg = df_master.groupby(['Asset_Class', 'Desk'])[metrics].sum().reset_index()

# Monitoring & Alertes
df_monitoring = pd.merge(df_agg, df_limits, on='Desk')
alerts = []
for _, row in df_monitoring.iterrows():
    if row['VaR_Hist_99'] > row['Limit_VaR_99']:
        alerts.append({'Desk': row['Desk'], 'Metric': 'VaR 99%', 'Value': row['VaR_Hist_99'], 'Limit': row['Limit_VaR_99'], 'Severity': 'CRITICAL'})
    if row['Stress_Test_Global'] > row['Limit_Stress_Test']:
        alerts.append({'Desk': row['Desk'], 'Metric': 'Stress Test', 'Value': row['Stress_Test_Global'], 'Limit': row['Limit_Stress_Test'], 'Severity': 'HIGH'})

df_alerts = pd.DataFrame(alerts)

# KPIs
c1, c2, c3, c4 = st.columns(4)
c1.metric("Daily P&L", f"{df_agg['Daily_PnL'].sum():,.0f} €")
c2.metric("99% VaR", f"{df_agg['VaR_Hist_99'].sum():,.0f} €")
c3.metric("Stress Test Exposure", f"{df_agg['Stress_Test_Global'].sum():,.0f} €")
c4.metric("Active Breaches", f"{len(df_alerts)}")

st.markdown("---")

# Tabs
t1, t2, t3 = st.tabs(["🚨 Risk Alerts", "📊 Risk vs Limits", "💰 P&L Attribution"])

with t1:
    if not df_alerts.empty:
        st.warning("Limit Breaches Detected")
        st.dataframe(df_alerts, use_container_width=True)
    else:
        st.success("All metrics within limits.")

with t2:
    fig_var = go.Figure()
    fig_var.add_trace(go.Bar(x=df_monitoring['Desk'], y=df_monitoring['VaR_Hist_99'], name='VaR 99%'))
    fig_var.add_trace(go.Bar(x=df_monitoring['Desk'], y=df_monitoring['Limit_VaR_99'], name='Limit'))
    fig_var.update_layout(barmode='group', title='VaR 99% vs Limits (€)')
    st.plotly_chart(fig_var, use_container_width=True)

with t3:
    fig_pnl = px.bar(df_agg, x='Desk', y=['PnL_Market', 'PnL_Carry', 'PnL_Unexplained'], title='P&L Attribution Breakdown (€)')
    st.plotly_chart(fig_pnl, use_container_width=True)
