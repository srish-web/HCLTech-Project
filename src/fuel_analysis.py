
import pandas as pd
from sklearn.ensemble import IsolationForest


def calculate_fuel_metrics(df):
    """Calculate fuel consumption in litres per 100 km."""
    result = df.copy()

    result["fuel_L_per_100km"] = float("nan")

    valid = (
        result["distance_km"].gt(0)
        & result["fuel_L"].ge(0)
        & result["distance_km"].notna()
        & result["fuel_L"].notna()
    )

    result.loc[valid, "fuel_L_per_100km"] = (
        result.loc[valid, "fuel_L"]
        / result.loc[valid, "distance_km"]
        * 100
    )

    return result


def detect_statistical_anomalies(df):
    """Flag unusually high fuel consumption using the IQR rule."""
    result = calculate_fuel_metrics(df)

    values = result["fuel_L_per_100km"].dropna()

    result["statistical_anomaly"] = False

    if len(values) < 4:
        result["statistical_threshold"] = float("nan")
        return result

    q1 = values.quantile(0.25)
    q3 = values.quantile(0.75)
    iqr = q3 - q1

    upper_threshold = q3 + 1.5 * iqr

    result["statistical_threshold"] = upper_threshold

    result["statistical_anomaly"] = (
        result["fuel_L_per_100km"] > upper_threshold
    ).fillna(False)

    return result


def detect_isolation_forest_anomalies(
    df,
    contamination=0.05,
    random_state=42,
):
    """Flag unusual fuel-efficiency observations with Isolation Forest."""
    result = calculate_fuel_metrics(df)

    result["isolation_forest_anomaly"] = "Not evaluated"

    valid = (
        result["fuel_L_per_100km"].notna()
        & result["fuel_L_per_100km"].ge(0)
    )

    if valid.sum() < 10:
        return result

    features = result.loc[
        valid, ["fuel_L_per_100km"]
    ].copy()

    model = IsolationForest(
        n_estimators=100,
        contamination=contamination,
        random_state=random_state,
    )

    predictions = model.fit_predict(features)

    result.loc[valid, "isolation_forest_anomaly"] = [
        "Flagged" if prediction == -1 else "Normal"
        for prediction in predictions
    ]

    return result
