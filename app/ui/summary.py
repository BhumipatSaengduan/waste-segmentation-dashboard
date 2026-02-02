import streamlit as st
import pandas as pd

from ..db.database import load_history
from ..core.config import DB_CLASS_MAP

def render_data_summary():
    """Render the data summary section with key metrics."""
    st.divider()
    st.subheader("📊 Data Summary")

    df_hist_summary = load_history()

    if df_hist_summary.empty:
        st.info("No data available for summary.")
        return

    total_images = len(df_hist_summary)
    df_hist_summary["datetime"] = pd.to_datetime(df_hist_summary["datetime"])
    latest_datetime = df_hist_summary["datetime"].max()

    percent_cols = [c for c in df_hist_summary.columns if c.endswith("_percent")]
    total_by_class = (
        df_hist_summary[percent_cols]
        .sum()
        .rename(lambda x: x.replace("_percent", ""))
    )
    most_common_class = total_by_class.rename(DB_CLASS_MAP).idxmax()

    s1, s2, s3 = st.columns(3)
    s1.metric(label="🖼️ Total Images Analyzed", value=total_images)
    s2.metric(
        label="⏱️ Latest Analysis",
        value=latest_datetime.strftime("%Y-%m-%d"),
        delta=latest_datetime.strftime("%H:%M")
    )
    s3.metric(label="♻️ Most Frequent Waste Class", value=most_common_class)
