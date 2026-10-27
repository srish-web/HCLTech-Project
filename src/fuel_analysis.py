import pandas as pd


def calculate_fuel_metrics(df):
    result = df.copy()

    result["fuel_L_per_100km"] = float("nan")

    valid = (
        result["distance_km"].gt(0)
        & result["fuel_L"].ge(0)
    )

    result.loc[valid, "fuel_L_per_100km"] = (
        result.loc[valid, "fuel_L"]
        / result.loc[valid, "distance_km"]
        * 100
    )

    return result


from sklearn.ensemble import IsolationForest

df = pd.read_csv("../data/dataset.csv")
features = df[["distance_km", "fuel_L"]].copy()

valid = (
    features["distance_km"].gt(0)
    & features["fuel_L"].ge(0)
    & features.notna().all(axis=1)
)

model = IsolationForest(
    n_estimators=100,
    contamination=0.05,
    random_state=42
)

df["fuel_anomaly"] = "Not evaluated"

df.loc[valid, "fuel_anomaly"] = (
    model.fit_predict(features.loc[valid])
)

df["fuel_anomaly"] = df["fuel_anomaly"].map(
    {-1: "Flagged", 1: "Normal"}
).fillna(df["fuel_anomaly"])
