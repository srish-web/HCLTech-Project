
import pandas as pd


def delivery_status_summary(df):
    """Summarize trips by delivery status."""
    return (
        df["delivery_status"]
        .fillna("unknown")
        .str.strip()
        .str.lower()
        .value_counts()
        .rename_axis("delivery_status")
        .reset_index(name="trip_count")
    )


def delivery_kpis(df):
    """Calculate delivery outcome metrics."""
    total = len(df)

    statuses = (
        df["delivery_status"]
        .fillna("unknown")
        .str.strip()
        .str.lower()
    )

    on_time = int(statuses.eq("on_time").sum())
    delayed = int(statuses.eq("delayed").sum())
    failed = int(statuses.eq("failed").sum())

    return {
        "total_trips": total,
        "on_time_trips": on_time,
        "delayed_trips": delayed,
        "failed_trips": failed,
        "on_time_rate": on_time / total * 100 if total else 0,
        "completion_rate": (
            (total - failed) / total * 100 if total else 0
        ),
    }


def route_summary(df):
    """Summarize trips for each origin-destination pair."""
    result = df.copy()

    result["route"] = (
        result["origin"].astype(str)
        + " → "
        + result["destination"].astype(str)
    )

    return (
        result.groupby("route", as_index=False)
        .agg(
            trip_count=("trip_id", "count"),
            average_distance_km=("distance_km", "mean"),
            average_fuel_L=("fuel_L", "mean"),
        )
        .sort_values("trip_count", ascending=False)
    )


def vehicle_trip_counts(df):
    """Count trips assigned to each vehicle."""
    return (
        df.groupby("vehicle_id")
        .size()
        .reset_index(name="trip_count")
        .sort_values("trip_count", ascending=False)
    )
