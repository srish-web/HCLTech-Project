
import sys
from pathlib import Path
import time
import pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.fuel_analysis import (
    detect_statistical_anomalies,
    detect_isolation_forest_anomalies,
)
from src.delivery_analysis import (
    delivery_kpis,
    route_summary,
)
from src.validation import validate_dataset


df = pd.read_csv("data/dataset.csv")

tasks = {
    "Data validation": lambda: validate_dataset(df),
    "Statistical fuel analysis": lambda: (
        detect_statistical_anomalies(df)
    ),
    "Isolation Forest": lambda: (
        detect_isolation_forest_anomalies(df)
    ),
    "Delivery analytics": lambda: delivery_kpis(df),
    "Route analysis": lambda: route_summary(df),
}

print(f"Dataset size: {len(df)} rows")


REPEATS = 7

for name, task in tasks.items():
    # Warm-up run, excluded from the measurements
    task()

    timings = []

    for _ in range(REPEATS):
        start = time.perf_counter()
        task()
        elapsed = time.perf_counter() - start
        timings.append(elapsed)

    timings.sort()
    median_time = timings[len(timings) // 2]

    print(
        f"{name}: "
        f"median={median_time:.4f} seconds, "
        f"minimum={min(timings):.4f} seconds, "
        f"maximum={max(timings):.4f} seconds"
    )

