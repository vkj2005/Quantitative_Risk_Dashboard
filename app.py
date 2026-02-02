import streamlit as st
import pandas as pd
from analysis.metrics import sharpe_significance, drawdown
from analysis.plots import plot_correlation

# Title
st.title("Quantitative Risk Dashboard")

# Load data
df = pd.read_csv("data/strategies.csv")
df["Date"] = pd.to_datetime(df["Date"])
df.set_index("Date", inplace=True)

# Show data
st.subheader("Strategy Returns")
st.dataframe(df)

# Sharpe ratio + significance
st.subheader("Sharpe Ratio & Significance")
for col in df.columns:
    sharpe, p = sharpe_significance(df[col])
    st.write(f"{col}: Sharpe = {sharpe:.2f}, p-value = {p:.4f}")

# Correlation heatmap  ✅ THIS IS THE PART YOU ASKED ABOUT
st.subheader("Strategy Correlation")
fig = plot_correlation(df)
st.pyplot(fig)

# Drawdown
st.subheader("Drawdown Analysis")
strategy = st.selectbox("Select Strategy", df.columns)
dd = drawdown(df[strategy])
st.line_chart(dd)
