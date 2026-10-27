
import pandas as pd

from src.fuel_analysis import (
    calculate_fuel_metrics,
    detect_statistical_anomalies,
    detect_isolation_forest_anomalies,
)


def sample_data():
    return pd.DataFrame({
        "trip_id": ["T1", "T2", "T3", "T4", "T5"],
        "distance_km": [100, 200, 150, 100, 0],
        "fuel_L": [10, 30, 15, 100, 20],
    })


def test_fuel_consumption_calculation():
    result = calculate_fuel_metrics(sample_data())

    assert result.loc[0, "fuel_L_per_100km"] == 10
    assert result.loc[1, "fuel_L_per_100km"] == 15
    assert pd.isna(result.loc[4, "fuel_L_per_100km"])


def test_statistical_anomaly_column_exists():
    result = detect_statistical_anomalies(sample_data())

    assert "statistical_anomaly" in result.columns
    assert result["statistical_anomaly"].dtype == bool


def test_isolation_forest_runs():
    data = pd.DataFrame({
        "distance_km": [100] * 20,
        "fuel_L": [10] * 19 + [100],
    })

    result = detect_isolation_forest_anomalies(data)

    assert "isolation_forest_anomaly" in result.columns
    assert set(result["isolation_forest_anomaly"]).issubset(
        {"Flagged", "Normal", "Not evaluated"}
    )
