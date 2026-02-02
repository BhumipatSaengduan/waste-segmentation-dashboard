import plotly.express as px
from ..core.config import CLASS_COLORS

def create_time_series_chart(df_long, selected_class, chart_title):
    """Create time series line chart"""
    if selected_class == "All":
        fig = px.line(
            df_long,
            x="datetime" if "datetime" in df_long.columns else "date" if "date" in df_long.columns else "week",
            y="Percentage",
            color="Class",
            markers=True,
            title=chart_title,
            color_discrete_map=CLASS_COLORS
        )
    else:
        x_col = "datetime" if "datetime" in df_long.columns else "date" if "date" in df_long.columns else "week"
        fig = px.line(
            df_long[df_long["Class"] == selected_class],
            x=x_col,
            y="Percentage",
            markers=True,
            title=chart_title,
            color_discrete_sequence=[CLASS_COLORS[selected_class]]
        )

    fig.update_layout(hovermode="x unified")
    return fig

def prepare_time_series_data(df_hist, aggregation_mode):
    """Prepare dataframe for time series visualization"""
    from core.config import DB_CLASS_MAP
    
    percent_cols = [c for c in df_hist.columns if c.endswith("_percent")]

    if aggregation_mode == "Raw (Per Image)":
        # Convert to long format
        df_long = df_hist.melt(
            id_vars="datetime",
            value_vars=percent_cols,
            var_name="Class",
            value_name="Percentage"
        )
        df_long["Class"] = (
            df_long["Class"]
            .str.replace("_percent", "")
            .map(DB_CLASS_MAP)
        )
        return None, df_long

    elif aggregation_mode == "Daily Average":
        df_hist["date"] = df_hist["datetime"].dt.date
        df_daily = (
            df_hist
            .groupby("date")[percent_cols]
            .mean()
            .reset_index()
        )
        df_daily["samples"] = df_hist.groupby("date").size().values

        df_daily_long = df_daily.melt(
            id_vars=["date", "samples"],
            value_vars=percent_cols,
            var_name="Class",
            value_name="Percentage"
        )
        df_daily_long["Class"] = (
            df_daily_long["Class"]
            .str.replace("_percent", "")
            .map(DB_CLASS_MAP)
        )
        return df_daily, df_daily_long

    elif aggregation_mode == "Weekly Average":
        df_hist["week"] = df_hist["datetime"].dt.to_period("W-MON").apply(lambda r: r.start_time)
        df_weekly = (
            df_hist
            .groupby("week")[percent_cols]
            .mean()
            .reset_index()
        )
        df_weekly["samples"] = df_hist.groupby("week").size().values

        df_weekly_long = df_weekly.melt(
            id_vars=["week", "samples"],
            value_vars=percent_cols,
            var_name="Class",
            value_name="Percentage"
        )
        df_weekly_long["Class"] = (
            df_weekly_long["Class"]
            .str.replace("_percent", "")
            .map(DB_CLASS_MAP)
        )
        return df_weekly, df_weekly_long

    return None, None
