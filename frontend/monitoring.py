import streamlit as st
import pandas as pd
import os
from datetime import datetime
from streamlit_autorefresh import st_autorefresh


# ----------------- Page Configuration -----------------
st.set_page_config(page_title="CSAT Monitoring", page_icon="📊", layout="wide")

# ----------------- Title and Description -----------------
st.markdown("""
#  CSAT Score Monitoring Dashboard
Track and visualize predictions made by the CSAT Score Predictor system in real time.
""")

# ----------------- Constants -----------------
LOG_FILE = "storage/predictions.csv"

# ----------------- Load Logs -----------------
@st.cache_data(ttl=30)
def load_logs(file_path):
    df = pd.read_csv(file_path, parse_dates=["timestamp"])
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df

# ----------------- Check File Existence -----------------
if not os.path.exists(LOG_FILE):
    st.warning("🚫 No prediction logs found. Start making predictions to populate this dashboard.")
    st.stop()

try:
    df_logs = load_logs(LOG_FILE)
except Exception as e:
    st.error(f"❌ Error loading logs: {e}")
    st.stop()

# ----------------- Sidebar Filters -----------------
with st.sidebar:
    st.header("🔍 Filters")

    # Date filter
    min_date = df_logs["timestamp"].min().date()
    max_date = df_logs["timestamp"].max().date()

    date_range = st.date_input(" Date Range", [min_date, max_date], min_value=min_date, max_value=max_date)

    # Category filter
    if "category" in df_logs.columns:
        categories = df_logs["category"].dropna().unique().tolist()
        selected_categories = st.multiselect("📦 Category", categories, default=categories)
        df_logs = df_logs[df_logs["category"].isin(selected_categories)]

    # Date filter application
    df_logs = df_logs[
        (df_logs["timestamp"].dt.date >= date_range[0]) &
        (df_logs["timestamp"].dt.date <= date_range[1])
    ]

    st.markdown("---")
    st.info(f"📈 Showing **{len(df_logs)}** filtered predictions")
    
# ----------------- Auto Refresh -----------------
if st.sidebar.toggle("🔄 Auto-refresh every 15s"):
    st_autorefresh(interval=15000, limit=None, key="refresh")

# ----------------- Dashboard Metrics -----------------
st.markdown("## 📌 Overview Metrics")

colA, colB, colC = st.columns(3)
with colA:
    st.metric("Total Predictions", len(df_logs))

with colB:
    satisfied = df_logs[df_logs["prediction"] >= 4]
    st.metric("Satisfied (4-5)", len(satisfied))

with colC:
    unsatisfied = df_logs[df_logs["prediction"] <= 2]
    st.metric("Unsatisfied (1-2)", len(unsatisfied))

# ----------------- Time-Series & Mood Charts -----------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("📅 Daily Prediction Trends")
    time_series = (
        df_logs.groupby(df_logs["timestamp"].dt.date)["prediction"]
        .value_counts().unstack().fillna(0)
    )
    st.line_chart(time_series)

with col2:
    st.subheader("😊 Mood Distribution")
    if "mood" in df_logs.columns:
        mood_counts = df_logs["mood"].value_counts()
        st.bar_chart(mood_counts)
    else:
        st.info("No 'mood' column found in the logs.")

# ----------------- Category-wise Analysis -----------------
st.markdown("## Category & Agent Insights")
col3, col4 = st.columns(2)

with col3:
    if "Agent Shift" in df_logs.columns:
        st.subheader("👨‍💼 Agent Shift Distribution")
        shift_counts = df_logs["Agent Shift"].value_counts()
        st.bar_chart(shift_counts)

with col4:
    if "Product_category" in df_logs.columns:
        st.subheader(" Product Category Distribution")
        prod_counts = df_logs["Product_category"].value_counts()
        st.bar_chart(prod_counts)

# ----------------- Recent Logs Table -----------------
st.markdown("## 📝 Recent 50 Predictions")
st.dataframe(df_logs.sort_values("timestamp", ascending=False).head(50), use_container_width=True)

# ----------------- Footer -----------------
st.markdown("---")
st.caption("📌 This dashboard auto-refreshes every 15 seconds when enabled. Built with ❤️ using Streamlit.")
