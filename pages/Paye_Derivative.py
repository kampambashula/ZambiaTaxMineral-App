import streamlit as st
import numpy as np
import plotly.graph_objects as go

# ------------------------------------------------------------
# --- 1. PAYE SYSTEM (ZAMBIA 2025) ---------------------------
# ------------------------------------------------------------

PAYE_BANDS = [
    (61_200, 0.00),
    (85_200, 0.20),
    (110_400, 0.30),
    (float('inf'), 0.37),
]

def calculate_paye_step(income):
    tax = 0
    prev = 0
    for limit, rate in PAYE_BANDS:
        if income > limit:
            tax += (limit - prev) * rate
            prev = limit
        else:
            tax += (income - prev) * rate
            break
    return tax

# ------------------------------------------------------------
# --- 2. LIGHT SMOOTHING -------------------------------------
# ------------------------------------------------------------

def smooth_T(income, window=2000, samples=120):
    lows = income - window
    highs = income + window
    ys = np.linspace(max(1, lows), highs, samples)
    vals = np.array([calculate_paye_step(y) for y in ys])
    kernel = np.ones(10) / 10
    smoothed = np.convolve(vals, kernel, mode='same')
    return smoothed[len(smoothed)//2]

def T_smooth(y):
    if isinstance(y, np.ndarray):
        return np.array([smooth_T(v) for v in y])
    return smooth_T(y)

# ------------------------------------------------------------
# --- 3. NUMERICAL DERIVATIVE -------------------------------
# ------------------------------------------------------------

def derivative(fn, x, h=5.0):
    return (fn(x + h) - fn(x - h)) / (2 * h)

# ------------------------------------------------------------
# --- 4. ROOT FINDING FOR y*T'(y) = T(y) --------------------
# ------------------------------------------------------------

def f_cond(T_fn, y):
    return y * derivative(T_fn, y) - T_fn(y)

def find_root(T_fn, lo=50_000, hi=1_500_000, steps=3000):
    xs = np.linspace(lo, hi, steps)
    vals = np.array([f_cond(T_fn, x) for x in xs])

    for i in range(len(xs)-1):
        if vals[i] == 0 or vals[i] * vals[i+1] < 0:
            a, b = xs[i], xs[i+1]
            fa, fb = vals[i], vals[i+1]

            # Bisection refinement
            for _ in range(40):
                m = (a + b) / 2
                fm = f_cond(T_fn, m)
                if abs(fm) < 1e-6:
                    return m
                if fa * fm <= 0:
                    b, fb = m, fm
                else:
                    a, fa = m, fm
            return (a + b) / 2
    return None

# ------------------------------------------------------------
# --- STREAMLIT APP -----------------------------------------
# ------------------------------------------------------------

st.set_page_config(page_title="Zambia PAYE Analysis", layout="wide")

st.title("PAYE Analysis – Zambia 2025")
st.write("Effective tax rate, derivative curve, and visibly marked marginal point.")

# Full-range income array
incomes = np.linspace(1, 500_000, 2000)
Tvals = T_smooth(incomes)
eff = Tvals / incomes
deriv_eff = np.gradient(eff, incomes)

# Find marginal point using root finding
root = find_root(T_smooth)

# ---------------------------
# Plot: Effective Rate with PAYE Bands
# ---------------------------
fig = go.Figure()

# Add shaded bands
prev_limit = 0
colors = ["rgba(200,200,255,0.2)", "rgba(200,255,200,0.2)", "rgba(255,200,200,0.2)", "rgba(255,255,200,0.2)"]
for i, (limit, rate) in enumerate(PAYE_BANDS):
    band_end = min(limit, 500_000)
    fig.add_shape(
        type="rect",
        x0=prev_limit, x1=band_end,
        y0=0, y1=1,
        xref="x", yref="paper",
        fillcolor=colors[i % len(colors)],
        opacity=0.3,
        line_width=0,
    )
    prev_limit = band_end

# Plot effective rate
fig.add_trace(go.Scatter(
    x=incomes, y=eff,
    mode="lines",
    name="Effective PAYE rate (smoothed)",
    line=dict(color="blue", width=2)
))

# Add marginal point marker
if root:
    fig.add_trace(go.Scatter(
        x=[root],
        y=[T_smooth(root)/root],
        mode="markers+text",
        marker=dict(size=14, color='red', symbol="x"),
        text=[f"Marginal point\nZMW {root:,.0f}"],
        textposition="top center",
        name="Marginal point"
    ))
    fig.add_vline(
        x=root,
        line_color="red",
        line_dash="dash",
        annotation_text="slope=0",
        annotation_position="top"
    )

fig.update_layout(
    title="Effective PAYE Rate vs Income (with PAYE bands)",
    xaxis_title="Income (ZMW)",
    yaxis_title="Effective Tax Rate",
    height=600
)

st.subheader("Effective Rate vs Income with PAYE Bands")
st.plotly_chart(fig, use_container_width=True)

# ---------------------------
# Plot 2: Effective Tax vs Income
# ---------------------------
fig_tax = go.Figure()
fig_tax.add_trace(go.Scatter(
    x=incomes, y=Tvals,
    mode="lines",
    name="Effective Tax (ZMW)",
    line=dict(color="green", width=2)
))

if root:
    fig_tax.add_trace(go.Scatter(
        x=[root],
        y=[T_smooth(root)],
        mode="markers+text",
        marker=dict(size=14, color='red', symbol="x"),
        text=[f"Marginal point\nZMW {root:,.0f}"],
        textposition="top center",
        name="Marginal point"
    ))
    fig_tax.add_vline(
        x=root,
        line_color="red",
        line_dash="dash",
        annotation_text="slope=0",
        annotation_position="top"
    )

fig_tax.update_layout(
    title="Effective Tax vs Income",
    xaxis_title="Income (ZMW)",
    yaxis_title="Effective Tax (ZMW)",
    height=600
)

st.subheader("Effective Tax vs Income")
st.plotly_chart(fig_tax, use_container_width=True)

# ---------------------------
# Plot 3: Derivative of Effective Rate
# ---------------------------
fig_deriv = go.Figure()
fig_deriv.add_trace(go.Scatter(
    x=incomes,
    y=deriv_eff,
    mode="lines",
    name="Derivative of effective tax",
    line=dict(color="orange", width=2)
))

if root:
    fig_deriv.add_vline(
        x=root,
        line_color="red",
        line_dash="dash",
        annotation_text="slope=0",
        annotation_position="top"
    )

fig_deriv.update_layout(
    title="Derivative of Effective Tax Rate (E′(y))",
    xaxis_title="Income (ZMW)",
    yaxis_title="Derivative",
    height=500
)

st.subheader("Derivative of Effective Rate")
st.plotly_chart(fig_deriv, use_container_width=True)

# Display marginal point
st.write(f"True marginal point occurs at income: **{root:,.0f} ZMW**")
