import streamlit as st
import pandas as pd
from datetime import datetime

from ..core.logger import get_logger
from ..db.database import load_history
from ..core.config import CLASS_NAMES
from ..visualization.timeseries import (
    prepare_time_series_data,
    create_time_series_chart
)

PAGE_SIZE = 10

# =========================
# LOGGER
# =========================
logger = get_logger("ui.timeseries")

def render_time_series_section():
    """Render the temporal trends section with time series visualization."""
    st.divider()
    st.subheader("📈 Temporal Trends")

    logger.info("Time series section opened")

    aggregation_mode = st.radio(
        "Time Series Aggregation",
        ["Raw (Per Image)", "Daily Average", "Weekly Average"],
        horizontal=True
    )

    logger.info(f"Aggregation mode selected | mode={aggregation_mode}")

    df_hist = load_history()

    if df_hist.empty:
        logger.info("Time series skipped | history is empty")
        st.info("Not enough data to display time series.")
        return

    df_hist["datetime"] = pd.to_datetime(df_hist["datetime"])
    logger.info(f"History loaded for time series | rows={len(df_hist)}")

    df_agg, df_long = prepare_time_series_data(df_hist, aggregation_mode)

    if df_long is None:
        logger.warning("Time series preparation failed | df_long is None")
        st.info("Unable to prepare time series data.")
        return

    # =========================
    # WASTE CLASS SELECTION
    # =========================
    options = ["All"] + CLASS_NAMES
    key = aggregation_mode.replace(" ", "_").lower()

    selected = st.selectbox(
        "Select Waste Class",
        options,
        index=0,
        key=key
    )

    logger.info(
        f"Time series class selected | mode={aggregation_mode} | class={selected}"
    )

    # =========================
    # PLOT CHART
    # =========================
    title = f"Waste Proportion Over Time ({aggregation_mode})"
    fig = create_time_series_chart(df_long, selected, title)

    st.plotly_chart(fig, use_container_width=True)

    logger.info("Time series chart rendered")

    if aggregation_mode == "Raw (Per Image)":
        st.caption("Each point represents the result from a single image.")

    # =========================
    # TABLE + PAGINATION
    # =========================
    if df_agg is not None and not df_agg.empty:
        page_key = f"time_series_page_{aggregation_mode}"

        if page_key not in st.session_state:
            st.session_state[page_key] = 1

        page = st.session_state[page_key]
        total_pages = (len(df_agg) + PAGE_SIZE - 1) // PAGE_SIZE
        start_idx = (page - 1) * PAGE_SIZE
        end_idx = start_idx + PAGE_SIZE

        logger.info(
            f"Render time series table | mode={aggregation_mode} | page={page}/{total_pages}"
        )

        display_df = df_agg.iloc[start_idx:end_idx]

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )

        st.caption(f"Page {page} of {total_pages}")

        col_1, col_2, col_3 = st.columns([6, 1, 1])

        with col_1:
             st.write(" ")
                
        with col_2:
            if st.button("⬅️ Previous", key=f"prev_{page_key}") and page > 1:
                st.session_state[page_key] -= 1
                logger.info(
                    f"Time series pagination | previous → page {page - 1} | mode={aggregation_mode}"
                )
           
        with col_3:
            if st.button("Next ➡️", key=f"next_{page_key}") and page < total_pages:
                st.session_state[page_key] += 1
                logger.info(
                    f"Time series pagination | next → page {page + 1} | mode={aggregation_mode}"
                )

        # =========================
        # EXPORT CSV
        # =========================
        filename = (
            f"{aggregation_mode.split()[0].lower()}_summary_"
            f"{datetime.now().strftime('%Y%m%d')}.csv"
        )

        st.download_button(
            f"⬇️ Export {aggregation_mode} Summary (CSV)",
            df_agg.to_csv(index=False).encode("utf-8"),
            filename,
            use_container_width=True
        )

        logger.info(
            f"Time series export triggered | mode={aggregation_mode} | rows={len(df_agg)} | file={filename}"
        )
