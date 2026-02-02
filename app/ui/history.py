import streamlit as st
import pandas as pd
from datetime import datetime, date

from ..core.logger import get_logger
from ..db.database import load_history
from ..core.config import DB_CLASS_MAP

PAGE_SIZE = 20

# =========================
# LOGGER
# =========================
logger = get_logger("ui.history")

def render_history_section():
    """
    Render the historical records section in Streamlit with filters, pagination, and export.

    Features:
        - Filter records by waste class and date range.
        - Paginate results (default 20 records per page).
        - Display selected columns and percentages for visible classes.
        - Export filtered records as CSV.
    
    Uses:
        - st.session_state.history_page for pagination.
        - DB_CLASS_MAP for class display mapping.
    """
    st.divider()
    st.subheader("📂 Historical Records")

    logger.info("History section opened")

    df_hist = load_history()

    if df_hist.empty:
        logger.info("History is empty")
        st.info("No historical records available.")
        return

    df_hist["datetime"] = pd.to_datetime(df_hist["datetime"])
    logger.info(f"Loaded history records | total={len(df_hist)}")

    # =========================
    # CLASS FILTER
    # =========================
    all_classes = list(DB_CLASS_MAP.values())
    class_filter = st.multiselect(
        "Select Waste Classes",
        options=all_classes,
        default=all_classes
    )

    st.markdown("### 🔎 Filters")

    # =========================
    # DATE FILTER
    # =========================
    min_date = df_hist["datetime"].min().date()
    max_date = df_hist["datetime"].max().date()

    date_range = st.date_input(
        "Select Date Range",
        value=(min_date, max_date)
    )
    st.caption("Select a single date or a date range")

    # Normalize date input
    if isinstance(date_range, tuple):
        if len(date_range) == 2:
            start_date, end_date = date_range
        elif len(date_range) == 1:
            start_date = end_date = date_range[0]
        else:
            start_date = min_date
            end_date = max_date
    elif isinstance(date_range, date):
        start_date = end_date = date_range
    else:
        start_date = min_date
        end_date = max_date

    if start_date > end_date:
        start_date, end_date = end_date, start_date

    logger.info(
        f"History filter applied | date={start_date} → {end_date} | classes={class_filter}"
    )

    # =========================
    # APPLY FILTERS
    # =========================
    filtered_df = df_hist[
        (df_hist["datetime"].dt.date >= start_date) &
        (df_hist["datetime"].dt.date <= end_date)
    ].copy()

    percent_cols = [f"{c}_percent" for c in DB_CLASS_MAP.keys()]
    class_cols_to_keep = [
        col for col in percent_cols
        if DB_CLASS_MAP[col.replace("_percent", "")] in class_filter
    ]

    base_cols = [
        "id",
        "datetime",
        "image",
        "model_version",
        "source",
        "confidence"
    ]

    filtered_df = filtered_df[base_cols + class_cols_to_keep]

    if filtered_df.empty:
        logger.info("No records after applying filters")
        st.info("No records match the selected filters.")
        return

    # =========================
    # PAGINATION
    # =========================
    total_pages = (len(filtered_df) + PAGE_SIZE - 1) // PAGE_SIZE

    if "history_page" not in st.session_state:
        st.session_state.history_page = 1

    page = st.session_state.history_page
    start_idx = (page - 1) * PAGE_SIZE
    end_idx = start_idx + PAGE_SIZE

    logger.info(
        f"Render history page | page={page}/{total_pages} | rows={len(filtered_df)}"
    )

    display_df = filtered_df.iloc[start_idx:end_idx]

    display_df = display_df.drop(columns=["id"])

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )


    st.caption(f"Page {page} of {total_pages}")

    col1, col2, col3 = st.columns([6, 1, 1])

    with col1:
        st.write(" ")

    with col2:
        if st.button("⬅️ Previous") and page > 1:
            st.session_state.history_page -= 1
            logger.info(
                f"History pagination | previous → page {st.session_state.history_page}"
            )

    with col3:
        if st.button("Next ➡️") and page < total_pages:
            st.session_state.history_page += 1
            logger.info(
                f"History pagination | next → page {st.session_state.history_page}"
            )

    # =========================
    # EXPORT CSV
    # =========================
    filename = f"filtered_waste_history_{datetime.now().strftime('%Y%m%d')}.csv"

    st.download_button(
        "⬇️ Export Records (CSV)",
        filtered_df.to_csv(index=False).encode("utf-8"),
        filename,
        use_container_width=True
    )

    logger.info(
        f"History export triggered | rows={len(filtered_df)} | file={filename}"
    )

    st.caption("Export historical records currently shown above.")
