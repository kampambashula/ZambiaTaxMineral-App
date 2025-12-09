import streamlit as st
import numpy as np
import plotly.graph_objects as go
from scipy.ndimage import gaussian_filter1d

st.title("Mineral Royalty Analysis – Copper")

# ------------------------------------------------------------
# Copper price bands and official royalty rates
# ------------------------------------------------------------
COPPER_PRICE_BANDS = [
    (0, 4500, 0.055),
    (4500, 6000, 0.065),
    (6000, 7500, 0.075),
    (7500, 9000, 0.085),
    (9000, float('inf'), 0.10),
]

def copper_royalty_rate(price):
    for low, high, rate in COPPER_PRICE_BANDS:
        if low <= price < high:
            return rate
    return COPPER_PRICE_BANDS[-1][2]

# ------------------------------------------------------------
# User input: Copper production
# ------------------------------------------------------------
production = st.slider("Select Copper Production (tonnes)", min_value=10_000, max_value=1_000_000, value=50_000, step=10_000)

# ------------------------------------------------------------
# Stepwise royalty rate for plotting
# ------------------------------------------------------------
prices = np.linspace(3000, 10_500, 1000)
royalty_step = np.array([copper_royalty_rate(p) for p in prices])

# Smoothed royalty rate for optimal schedule
royalty_smooth = gaussian_filter1d(royalty_step, sigma=20)

# ---------------------------
# Plot 1: Stepwise bands + smoothed royalty overlay
# ---------------------------
fig_step = go.Figure()

# Add shaded regions for price bands
colors = ["rgba(200,200,255,0.2)", "rgba(200,255,200,0.2)", "rgba(255,200,200,0.2)", "rgba(255,255,200,0.2)", "rgba(200,255,255,0.2)"]
for i, (low, high, rate) in enumerate(COPPER_PRICE_BANDS):
    band_end = min(high, 10_500)
    fig_step.add_shape(
        type="rect",
        x0=low, x1=band_end,
        y0=0, y1=rate,
        fillcolor=colors[i % len(colors)],
        opacity=0.2,
        line_width=0
    )

# Plot stepwise royalty
fig_step.add_trace(go.Scatter(
    x=prices,
    y=royalty_step,
    mode='lines',
    name='Stepwise Royalty Rate',
    line=dict(shape='hv', color='blue', width=3)
))

# Overlay smoothed royalty rate
fig_step.add_trace(go.Scatter(
    x=prices,
    y=royalty_smooth,
    mode='lines',
    name='Smoothed (Optimal) Royalty Rate',
    line=dict(color='red', width=3, dash='dash')
))

fig_step.update_layout(
    title="Copper Royalty: Stepwise vs Smoothed (Optimal) Rate",
    xaxis_title="Copper Price (USD/tonne)",
    yaxis_title="Royalty Rate",
    height=500
)

st.subheader("Copper Royalty: Stepwise Bands with Smoothed Optimal Overlay")
st.plotly_chart(fig_step, use_container_width=True)

# ------------------------------------------------------------
# Plot 2: Revenue comparison with peak revenue marker
# ------------------------------------------------------------
# Revenue under stepwise and smoothed rates
revenue_step = production * prices * royalty_step
revenue_smooth = production * prices * royalty_smooth

# Find peak revenue on smoothed curve
peak_idx = np.argmax(revenue_smooth)
peak_price = prices[peak_idx]
peak_revenue = revenue_smooth[peak_idx]

fig_revenue = go.Figure()
fig_revenue.add_trace(go.Scatter(
    x=prices,
    y=revenue_step,
    mode='lines',
    name='Revenue (Stepwise Rate)',
    line=dict(color='blue', width=2)
))
fig_revenue.add_trace(go.Scatter(
    x=prices,
    y=revenue_smooth,
    mode='lines',
    name='Revenue (Smoothed Rate)',
    line=dict(color='red', width=3, dash='dash')
))

# Add marker for peak revenue
fig_revenue.add_trace(go.Scatter(
    x=[peak_price],
    y=[peak_revenue],
    mode='markers+text',
    marker=dict(size=12, color='green', symbol='star'),
    text=[f"Peak Revenue\nPrice: ${peak_price:.0f}"],
    textposition='top center',
    name='Peak Revenue'
))

fig_revenue.update_layout(
    title=f"Revenue under Stepwise vs Smoothed Royalty Rate (Production: {production:,} tonnes)",
    xaxis_title="Copper Price (USD/tonne)",
    yaxis_title="Revenue (ZMW)",
    height=500
)

st.subheader("Revenue Comparison: Stepwise vs Smoothed Royalty")
st.plotly_chart(fig_revenue, use_container_width=True)

st.markdown(f"""
**Notes:**  
- The first graph shows the official stepwise copper royalty rates with shaded price bands.  
- The red dashed line represents a smoothed "optimal" royalty rate.  
- The second graph shows the revenue comparison for the selected copper production ({production:,} tonnes).  
- **Peak revenue occurs at copper price: ${peak_price:.0f}, revenue: {peak_revenue:,.0f} ZMW.**
""")
