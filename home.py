import streamlit as st

st.set_page_config(page_title="Zambia Tax & Mineral Analysis", layout="wide")

# --- Header ---
st.markdown("<h1 style='text-align: center; color: #2E86C1;'>Zambia Tax & Mineral Analysis App</h1>", unsafe_allow_html=True)
st.markdown("---")

# --- Introduction ---
st.markdown("""
Welcome to the **Zambia Tax & Mineral Analysis App**, your interactive tool for exploring taxation and mineral royalties in Zambia.  

Use the sidebar to navigate between the different analysis pages.
""")
st.image("tax.png", caption="Zambia Tax Overview", use_container_width=True)

# --- Pages Overview ---
st.markdown("### Pages Available:")
st.markdown("""
- **PAYE Analysis**: Explore Zambia's PAYE system, effective tax rates, and marginal points.  
- **Mineral Royalty Analysis**: Examine copper mineral royalties, production effects, and revenue optimization.  
""")


# --- Footer / Call-to-action ---
st.markdown("---")
st.markdown("""
For guidance on using the app:
- Use the sidebar to switch between **PAYE Analysis** and **Mineral Royalty Analysis** pages.
- Hover over graphs to see detailed values.
- Adjust parameters interactively (e.g., copper production) to explore different scenarios.
""")
