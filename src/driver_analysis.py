
import pandas as pd


def score_summary(df):
    """Describe the existing driver_score field."""
    scores = pd.to_numeric(
        df["driver_score"], errors="coerce"
    ).dropna()

    if scores.empty:
        return {
            "count": 0,
            "mean": float("nan"),
            "median": float("nan"),
            "minimum": float("nan"),
            "maximum": float("nan"),
        }

    return {
        "count": int(scores.count()),
        "mean": float(scores.mean()),
        "median": float(scores.median()),
        "minimum": float(scores.min()),
        "maximum": float(scores.max()),
    }


def driver_score_summary(df):
    """Summarize recorded scores by driver."""
    return (
        df.groupby("driver_id", as_index=False)
        .agg(
            trip_count=("trip_id", "count"),
            average_score=("driver_score", "mean"),
            median_score=("driver_score", "median"),
        )
        .sort_values("average_score", ascending=False)
    )



def compare_historical_routes(df):
    """Compare recorded distances for repeated city pairs."""
    result = df.copy()

    result = result[
        result["distance_km"].notna()
        & result["distance_km"].gt(0)
    ]

    return (
        result.groupby(
            ["origin", "destination"],
            as_index=False,
        )
        .agg(
            trip_count=("trip_id", "count"),
            average_distance_km=("distance_km", "mean"),
            minimum_observed_distance_km=("distance_km", "min"),
            maximum_observed_distance_km=("distance_km", "max"),
        )
        .sort_values("trip_count", ascending=False)
    )
