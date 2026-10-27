
import pandas as pd

from src.delivery_analysis import (
    delivery_kpis,
    delivery_status_summary,
    route_summary,
    vehicle_trip_counts,
)


def sample_data():
    return pd.DataFrame({
        "trip_id": ["T1", "T2", "T3", "T4"],
        "vehicle_id": ["V1", "V1", "V2", "V2"],
        "origin": ["Delhi", "Delhi", "Mumbai", "Delhi"],
        "destination": ["Pune", "Pune", "Delhi", "Pune"],
        "distance_km": [200, 220, 500, 180],
        "fuel_L": [20, 22, 50, 18],
        "delivery_status": [
            "on_time", "delayed", "failed", "on_time"
        ],
    })


def test_delivery_kpis():
    result = delivery_kpis(sample_data())

    assert result["total_trips"] == 4
    assert result["on_time_trips"] == 2
    assert result["delayed_trips"] == 1
    assert result["failed_trips"] == 1
    assert result["completion_rate"] == 75


def test_route_summary():
    result = route_summary(sample_data())

    delhi_pune = result[
        result["route"] == "Delhi → Pune"
    ].iloc[0]

    assert delhi_pune["trip_count"] == 3


def test_vehicle_trip_counts():
    result = vehicle_trip_counts(sample_data())

    assert result["trip_count"].sum() == 4


def test_status_summary_counts_all_records():
    result = delivery_status_summary(sample_data())

    assert result["trip_count"].sum() == 4
