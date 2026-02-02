import streamlit as st
import pandas as pd
from analysis.metrics import sharpe_significance, drawdown
from analysis.plots import plot_correlation

# Title
st.title("vj_Quantitative Risk Dashboard")

# Load data
df = pd.read_csv("data/strategies.csv")
df["Date"] = pd.to_datetime(df["Date"])
df.set_index("Date", inplace=True)

# ---------------- Date Range Filter ----------------
st.sidebar.subheader("Date Filter")

start_date, end_date = st.sidebar.date_input(
    "Select Date Range",
    value=[df.index.min(), df.index.max()],
    min_value=df.index.min(),
    max_value=df.index.max()
)

date_filtered_df = df.loc[start_date:end_date]

# ---------------- Strategy Filter ----------------
st.sidebar.subheader("Strategy Selection")

selected_strategies = st.sidebar.multiselect(
    "Choose Strategies",
    options=date_filtered_df.columns.tolist(),
    default=date_filtered_df.columns.tolist()
)

filtered_df = date_filtered_df[selected_strategies]


# ---------------- Sidebar Controls ----------------
# st.sidebar.header("Dashboard Controls")

# selected_strategies = st.sidebar.multiselect(
#     "Select Strategies",
#     options=df.columns.tolist(),
#     default=df.columns.tolist()
# )

# filtered_df = df[selected_strategies]


# Show data
st.subheader("Strategy Returns")
st.dataframe(filtered_df)

# ---------------- KPI Metrics ----------------
st.subheader("Key Performance Indicators")

c1, c2, c3 = st.columns(3)

c1.metric("Total Strategies", len(filtered_df.columns))
c2.metric("Start Date", str(filtered_df.index.min().date()))
c3.metric("End Date", str(filtered_df.index.max().date()))

# ---------------- Performance Summary ----------------
st.subheader("Performance Summary")

mean_returns = filtered_df.mean()

best_strategy = mean_returns.idxmax()
worst_strategy = mean_returns.idxmin()

st.success(f"📈 Best Strategy: {best_strategy}")
st.error(f"📉 Worst Strategy: {worst_strategy}")


# Sharpe ratio + significance
st.subheader("Sharpe Ratio & Significance")
for col in filtered_df.columns:
    sharpe, p = sharpe_significance(filtered_df[col])
    st.write(f"{col}: Sharpe = {sharpe:.2f}, p-value = {p:.4f}")

# ---------------- Enhanced Automated Insights ----------------
# st.subheader("Enhanced Risk Insights")

# for col in filtered_df.columns:
#     sharpe, p = sharpe_significance(filtered_df[col])
#     max_dd = drawdown(filtered_df[col]).min()


# ---------------- Auto Risk Insights ----------------
st.subheader("Automated Risk Insights")

for col in filtered_df.columns:
    sharpe, p = sharpe_significance(filtered_df[col])
    max_dd = drawdown(filtered_df[col]).min()

    if sharpe > 1 and p < 0.05 and max_dd > -0.2:
        st.success(f"✅ {col}: Strong & stable performance")
    elif max_dd < -0.3:
        st.warning(f"⚠️ {col}: High drawdown risk detected")
    elif p > 0.05:
        st.error(f"🚨 {col}: Returns not statistically significant")
    else:
        st.info(f"ℹ️ {col}: Moderate performance, monitor closely")


# Correlation heatmap  ✅ THIS IS THE PART YOU ASKED ABOUT
st.subheader("Strategy Correlation")
fig = plot_correlation(filtered_df)
st.pyplot(fig)

# Drawdown
st.subheader("Drawdown Analysis")
strategy = st.selectbox("Select Strategy", filtered_df.columns)
dd = drawdown(filtered_df[strategy])
st.line_chart(dd)
