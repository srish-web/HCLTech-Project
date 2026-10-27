
import pandas as pd

from src.validation import validate_dataset


def test_validation_detects_duplicate_trip_id():
    df = pd.DataFrame({
        "trip_id": ["T1", "T1"],
        "vehicle_id": ["V1", "V1"],
        "driver_id": ["D1", "D1"],
        "origin": ["Delhi", "Delhi"],
        "destination": ["Pune", "Pune"],
        "distance_km": [100, 120],
        "fuel_L": [10, 12],
        "delivery_status": ["on_time", "delayed"],
        "driver_score": [80, 85],
    })

    result = validate_dataset(df)

    assert result["duplicate_trip_ids"] == 1
    assert result["invalid_distances"] == 0
    assert result["negative_fuel_values"] == 0


def test_validation_detects_missing_column():
    df = pd.DataFrame({"trip_id": ["T1"]})

    result = validate_dataset(df)

    assert "distance_km" in result["missing_columns"]
