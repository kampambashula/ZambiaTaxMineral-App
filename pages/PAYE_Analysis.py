import streamlit as st
import numpy as np
import plotly.graph_objects as go
from utils import effective_rate_paye, calculate_marginal_point

st.title("PAYE Analysis")

# Income array from zero to 500,000
income = np.linspace(0, 500_000, 5000)

# Compute effective rate using your PAYE function
effective_rate = np.array([effective_rate_paye(i) for i in income])
effective_tax = income * effective_rate

# Compute marginal point
marginal_income, marginal_rate = calculate_marginal_point(income, effective_rate)

# ------------------------------
# 1. Full-range Effective Rate vs Income
# ------------------------------
fig_full = go.Figure()
fig_full.add_trace(go.Scatter(x=income, y=effective_rate, mode='lines', name='Effective Rate'))
fig_full.add_trace(go.Scatter(x=[marginal_income], y=[marginal_rate],
                              mode='markers+text',
                              text=['True Marginal Point'],
                              textposition='top center',
                              marker=dict(color='red', size=10),
                              name='Marginal Point'))
fig_full.update_layout(title="Effective Rate vs Income (0 – 500,000 ZMW)",
                       xaxis_title="Income (ZMW)",
                       yaxis_title="Effective Rate")

# ------------------------------
# 2. Effective Tax vs Income
# ------------------------------
fig_tax = go.Figure()
fig_tax.add_trace(go.Scatter(x=income, y=effective_tax, mode='lines', name='Effective Tax'))
fig_tax.add_trace(go.Scatter(x=[marginal_income], y=[marginal_income*marginal_rate],
                             mode='markers+text',
                             text=['True Marginal Point'],
                             textposition='top center',
                             marker=dict(color='red', size=10),
                             name='Marginal Point'))
fig_tax.update_layout(title="Effective Tax vs Income",
                      xaxis_title="Income (ZMW)",
                      yaxis_title="Effective Tax (ZMW)")

# ------------------------------
# 3. Optional zoomed-in plot around exemption band (0 – 85,200)
# ------------------------------
fig_zoom = go.Figure()
mask_zoom = income <= 85_200
fig_zoom.add_trace(go.Scatter(x=income[mask_zoom], y=effective_rate[mask_zoom], mode='lines', name='Effective Rate'))
fig_zoom.update_layout(title="Effective Rate vs Income (0 – 85,200 ZMW)",
                       xaxis_title="Income (ZMW)",
                       yaxis_title="Effective Rate")

# ------------------------------
# Display plots
# ------------------------------
st.subheader("Full-range Effective Rate vs Income")
st.plotly_chart(fig_full)

st.subheader("Effective Tax vs Income")
st.plotly_chart(fig_tax)

st.subheader("Zoomed-in view around exemption band")
st.plotly_chart(fig_zoom)

# ------------------------------
# Display marginal point info
# ------------------------------
st.write(f"True marginal point occurs at income: **{marginal_income:.0f} ZMW** with effective rate **{marginal_rate*100:.2f}%**")
