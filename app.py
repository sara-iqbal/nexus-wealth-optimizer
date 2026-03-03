import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# 1. Page Configuration & Professional Theme
st.set_page_config(page_title="Global Wealth Management", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    div[data-testid="stMetricValue"] { color: #00457C; font-size: 32px; }
    </style>
    """, unsafe_allow_html=True)

# 2. Institutional Data Setup
@st.cache_data
def get_banking_data():
    return pd.DataFrame({
        'Product': ['Mortgages', 'Lombard Loans', 'Investment Finance', 'Structured Notes', 'Unsecured Credit'],
        'Allocation_BN': [450, 300, 250, 150, 50],
        'Risk_Weight': [0.35, 0.20, 0.75, 1.00, 1.50],
        'Revenue_Margin': [0.012, 0.008, 0.022, 0.035, 0.055]
    })

df = get_banking_data()
df['RWA'] = df['Allocation_BN'] * df['Risk_Weight']
df['Net_Income'] = df['Allocation_BN'] * df['Revenue_Margin']
df['RoRWA'] = (df['Net_Income'] / df['RWA']) * 100

# 3. Header Section
st.title("🏦 Nexus Wealth Analytics")
st.subheader("Capital Optimization & Strategic Returns Dashboard")

# 4. Top KPIs (The "Executive View")
m1, m2, m3, m4 = st.columns(4)
m1.metric("Total Assets", f"${df['Allocation_BN'].sum()}B", "+2.4%")
m2.metric("Total RWA", f"${df['RWA'].sum():.1f}B", "-1.1%")
m3.metric("Avg RoRWA", f"{df['RoRWA'].mean():.2f}%", "Outperforming")
m4.metric("LCR Ratio", "122%", "Compliant")

st.divider()

# 5. The "Integrated Return Tool" (Sidebar)
st.sidebar.header("🕹️ Deal Pricing Calculator")
deal_size = st.sidebar.number_input("New Deal Size ($M)", value=100)
selected_product = st.sidebar.selectbox("Product Category", df['Product'].unique())

# Logic for dynamic calculation
p_row = df[df['Product'] == selected_product].iloc[0]
new_rwa = deal_size * p_row['Risk_Weight']
new_rev = deal_size * p_row['Revenue_Margin']
new_rorwa = (new_rev / new_rwa) * 100

st.sidebar.markdown(f"**Results for {selected_product}:**")
st.sidebar.write(f"Consumed Capital (RWA): **${new_rwa:.2f}M**")
st.sidebar.write(f"Projected RoRWA: **{new_rorwa:.2f}%**")

if new_rorwa >= 12.0:
    st.sidebar.success("✅ Above Capital Hurdle")
else:
    st.sidebar.warning("⚠️ Below Capital Hurdle (12%)")

# 6. Analytics Visuals
col_left, col_right = st.columns([3, 2])

with col_left:
    st.markdown("### The Risk-Return Frontier")
    # A sophisticated plot showing risk vs return
    fig_scatter = px.scatter(df, x="Risk_Weight", y="RoRWA", 
                             size="Allocation_BN", color="Product",
                             hover_name="Product", text="Product",
                             title="Efficiency Map: High Yield vs. Capital Intensity")
    fig_scatter.update_traces(textposition='top center')
    st.plotly_chart(fig_scatter, use_container_width=True)

with col_right:
    st.markdown("### Capital Concentration")
    fig_pie = px.pie(df, values='RWA', names='Product', hole=0.4,
                     title="Total RWA Breakdown",
                     color_discrete_sequence=px.colors.sequential.RdBu)
    st.plotly_chart(fig_pie, use_container_width=True)

st.info(" **Note :** This dashboard automates the calculation of RWA based on Basel III standards, allowing the business to prioritize 'Lombard Loans' (low risk-weight) during liquidity-constrained periods.")
