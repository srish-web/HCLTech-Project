
import pandas as pd


REQUIRED_COLUMNS = [
    "trip_id",
    "vehicle_id",
    "driver_id",
    "origin",
    "destination",
    "distance_km",
    "fuel_L",
    "delivery_status",
    "driver_score",
]


def validate_dataset(df):
    """Return basic data-quality checks for the fleet dataset."""
    missing_columns = [
        column
        for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:
        return {
            "row_count": len(df),
            "missing_columns": missing_columns,
            "missing_values": {},
            "duplicate_trip_ids": None,
            "invalid_distances": None,
            "negative_fuel_values": None,
        }

    return {
        "row_count": len(df),
        "missing_columns": [],
        "missing_values": df[
            REQUIRED_COLUMNS
        ].isna().sum().to_dict(),
        "duplicate_trip_ids": int(
            df["trip_id"].duplicated().sum()
        ),
        "invalid_distances": int(
            (~df["distance_km"].gt(0)).sum()
        ),
        "negative_fuel_values": int(
            df["fuel_L"].lt(0).sum()
        ),
    }
