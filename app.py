import streamlit as st
import pandas as pd

from analysis.metrics import sharpe_significance, drawdown
from analysis.plots import plot_correlation

# ---------------- Page Config ----------------
st.set_page_config(
    page_title="Quantitative Risk Dashboard",
    layout="wide"
)
# ---------------- Background Styling ----------------
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(
            135deg,
            #0f2027,
            #203a43,
            #2c5364
        );
        color: white;
    }

    section[data-testid="stSidebar"] {
        background-color: #1e293b;
    }

    div[data-testid="metric-container"] {
        background-color: rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 15px;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------- App Title ----------------
st.title("📊 vj_Quantitative Risk Dashboard")

# ---------------- Load Data ----------------
df = pd.read_csv("data/strategies.csv")
df["Date"] = pd.to_datetime(df["Date"])
df.set_index("Date", inplace=True)

# ---------------- Sidebar Filters ----------------
st.sidebar.header("Filters")

# Date range filter
start_date, end_date = st.sidebar.date_input(
    "Select Date Range",
    value=[df.index.min(), df.index.max()],
    min_value=df.index.min(),
    max_value=df.index.max()
)

date_filtered_df = df.loc[start_date:end_date]

# Strategy filter
selected_strategies = st.sidebar.multiselect(
    "Select Strategies",
    options=date_filtered_df.columns.tolist(),
    default=date_filtered_df.columns.tolist()
)

filtered_df = date_filtered_df[selected_strategies]

# Safety check
if filtered_df.empty:
    st.warning("⚠ Please select at least one strategy and a valid date range.")
    st.stop()

# ---------------- Tabs ----------------
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Overview",
    "📈 Risk Analysis",
    "🧠 Insights",
    "📉 Drawdown"
])

# ---------------- TAB 1: Overview ----------------
with tab1:
    st.subheader("Strategy Returns")
    st.dataframe(filtered_df)

    st.subheader("Key Performance Indicators")
    c1, c2, c3 = st.columns(3)

    c1.metric("Total Strategies", len(filtered_df.columns))
    c2.metric("Start Date", str(filtered_df.index.min().date()))
    c3.metric("End Date", str(filtered_df.index.max().date()))

    mean_returns = filtered_df.mean()
    st.subheader("Performance Summary")
    st.success(f"📈 Best Strategy: {mean_returns.idxmax()}")
    st.error(f"📉 Worst Strategy: {mean_returns.idxmin()}")

# ---------------- TAB 2: Risk Analysis ----------------
with tab2:
    st.subheader("Sharpe Ratio & Significance")

    for col in filtered_df.columns:
        sharpe, p = sharpe_significance(filtered_df[col])
        st.write(f"**{col}** → Sharpe: `{sharpe:.2f}`, p-value: `{p:.4f}`")

    st.subheader("Strategy Correlation")
    fig = plot_correlation(filtered_df)
    st.pyplot(fig)

# ---------------- TAB 3: Automated Insights ----------------
with tab3:
    st.subheader("Automated Risk Insights")

    for col in filtered_df.columns:
        sharpe, p = sharpe_significance(filtered_df[col])
        max_dd = drawdown(filtered_df[col]).min()

        if sharpe > 1 and p < 0.05 and max_dd > -0.2:
            st.success(f"✅ {col}: Strong and stable performance")
        elif max_dd < -0.3:
            st.warning(f"⚠ {col}: High drawdown risk detected")
        elif p > 0.05:
            st.error(f"🚨 {col}: Returns not statistically significant")
        else:
            st.info(f"ℹ {col}: Moderate performance, monitor closely")

# ---------------- TAB 4: Drawdown ----------------
with tab4:
    st.subheader("Drawdown Analysis")

    strategy = st.selectbox(
        "Select Strategy",
        filtered_df.columns
    )

    dd = drawdown(filtered_df[strategy])
    st.line_chart(dd)

# ---------------- Download ----------------
st.download_button(
    "⬇ Download Filtered Data",
    data=filtered_df.to_csv(),
    file_name="filtered_strategy_data.csv",
    mime="text/csv"
)
