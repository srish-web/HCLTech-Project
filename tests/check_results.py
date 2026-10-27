
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import pandas as pd

from src.fuel_analysis import (
    calculate_fuel_metrics,
    detect_statistical_anomalies,
)
from src.delivery_analysis import delivery_kpis
from src.validation import validate_dataset


df = pd.read_csv("data/dataset.csv")

# Independently verify fuel calculations
fuel_df = calculate_fuel_metrics(df)

valid = (
    df["distance_km"].gt(0)
    & df["fuel_L"].ge(0)
    & df["distance_km"].notna()
    & df["fuel_L"].notna()
)

expected = (
    df.loc[valid, "fuel_L"]
    / df.loc[valid, "distance_km"]
    * 100
)

actual = fuel_df.loc[valid, "fuel_L_per_100km"]

assert (
    (expected - actual).abs() < 1e-9
).all(), "Fuel calculation mismatch"

print("PASS: Fuel calculations match independent results")

# Independently verify delivery counts
kpis = delivery_kpis(df)

statuses = df["delivery_status"].str.strip().str.lower()

assert kpis["total_trips"] == len(df)
assert kpis["on_time_trips"] == int((statuses == "on_time").sum())
assert kpis["delayed_trips"] == int((statuses == "delayed").sum())
assert kpis["failed_trips"] == int((statuses == "failed").sum())

print("PASS: Delivery counts match independent results")

# Check data quality
quality = validate_dataset(df)

assert quality["missing_columns"] == []
assert quality["duplicate_trip_ids"] == 0

print("PASS: Required columns and trip IDs validated")

# Check statistical anomaly output
anomalies = detect_statistical_anomalies(df)

assert "statistical_anomaly" in anomalies.columns
assert anomalies["statistical_anomaly"].notna().all()

print("PASS: Statistical anomaly output validated")
