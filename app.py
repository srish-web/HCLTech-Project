import streamlit as st
import pandas as pd
import plotly.express as px

from src.fuel_analysis import (
    calculate_fuel_metrics,
    detect_statistical_anomalies,
    detect_isolation_forest_anomalies,
)
from src.delivery_analysis import (
    delivery_status_summary,
    delivery_kpis,
    route_summary,
    vehicle_trip_counts,
)
from src.driver_analysis import (
    score_summary,
    driver_score_summary,
)
from src.delivery_analysis import compare_historical_routes

from src.validation import validate_dataset


st.set_page_config(
    page_title="Fleet Management Platform",
    layout="wide"
)

st.title("Comprehensive Logistics and Fleet Management")

df = pd.read_csv("data/dataset.csv")
fuel_df = detect_statistical_anomalies(df)
fuel_df = detect_isolation_forest_anomalies(fuel_df)

# Sidebar filters
st.sidebar.header("Filters")

vehicles = sorted(
    df["vehicle_id"].dropna().unique().tolist()
)

selected_vehicles = st.sidebar.multiselect(
    "Select vehicles",
    vehicles,
    default=vehicles
)

filtered = df[df["vehicle_id"].isin(selected_vehicles)]

# KPI calculations
total_trips = len(filtered)
total_distance = filtered["distance_km"].sum()
total_fuel = filtered["fuel_L"].sum()

c1, c2, c3 = st.columns(3)

c1.metric("Total Trips", f"{total_trips:,}")
c2.metric("Total Distance", f"{total_distance:,.1f} km")
c3.metric("Total Fuel", f"{total_fuel:,.1f} L")

# Delivery analytics
status_counts = (
    filtered["delivery_status"]
    .fillna("unknown")
    .value_counts()
    .rename_axis("Status")
    .reset_index(name="Trips")
)

st.subheader("Delivery Status")
st.plotly_chart(
    px.bar(status_counts, x="Status", y="Trips"),
    use_container_width=True
)

st.subheader("Trip Records")
st.dataframe(filtered, use_container_width=True)


# Module A: Fuel efficiency and anomaly detection
st.header("Module A — Fuel Efficiency")

fuel_filtered = fuel_df[
    fuel_df["vehicle_id"].isin(selected_vehicles)
].copy()

valid_fuel = fuel_filtered["fuel_L_per_100km"].dropna()

if not valid_fuel.empty:
    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Mean Fuel Consumption",
        f"{valid_fuel.mean():.2f} L/100 km",
    )

    c2.metric(
        "Median Fuel Consumption",
        f"{valid_fuel.median():.2f} L/100 km",
    )

    c3.metric(
        "Statistical Anomalies",
        int(fuel_filtered["statistical_anomaly"].sum()),
    )

    st.subheader("Fuel Consumption Distribution")

    st.plotly_chart(
        px.histogram(
            fuel_filtered,
            x="fuel_L_per_100km",
            nbins=30,
            title="Fuel Consumption per 100 km",
        ),
        use_container_width=True,
    )

    st.subheader("Trips with Unusually High Fuel Consumption")

    flagged = fuel_filtered[
        fuel_filtered["statistical_anomaly"]
    ]

    st.dataframe(
        flagged[
            [
                "trip_id",
                "vehicle_id",
                "distance_km",
                "fuel_L",
                "fuel_L_per_100km",
                "statistical_threshold",
                "isolation_forest_anomaly",
            ]
        ],
        use_container_width=True,
    )
else:
    st.warning("No valid fuel-consumption records are available.")




# Module B: Delivery analytics
st.header("Module B — Delivery Analytics")

delivery_filtered = df[
    df["vehicle_id"].isin(selected_vehicles)
].copy()

kpis = delivery_kpis(delivery_filtered)

c1, c2, c3, c4 = st.columns(4)

c1.metric("Total Trips", kpis["total_trips"])
c2.metric("On-Time Rate", f'{kpis["on_time_rate"]:.1f}%')
c3.metric("Completion Rate", f'{kpis["completion_rate"]:.1f}%')
c4.metric("Failed Trips", kpis["failed_trips"])

st.subheader("Delivery Status Breakdown")

status_data = delivery_status_summary(delivery_filtered)

st.plotly_chart(
    px.bar(
        status_data,
        x="delivery_status",
        y="trip_count",
        title="Trips by Delivery Status",
    ),
    use_container_width=True,
)

st.subheader("Most Frequently Used Routes")

routes = route_summary(delivery_filtered)

st.dataframe(routes.head(20), use_container_width=True)

st.subheader("Trip Counts by Vehicle")

vehicle_counts = vehicle_trip_counts(delivery_filtered)

st.plotly_chart(
    px.bar(
        vehicle_counts.head(20),
        x="vehicle_id",
        y="trip_count",
        title="Top 20 Vehicles by Number of Trips",
    ),
    use_container_width=True,
)



# Module C: Driver score exploration
st.header("Module C — Driver Score Analysis")

driver_filtered = df[
    df["vehicle_id"].isin(selected_vehicles)
].copy()

summary = score_summary(driver_filtered)

c1, c2, c3 = st.columns(3)

c1.metric("Average Recorded Score", f'{summary["mean"]:.2f}')
c2.metric("Median Recorded Score", f'{summary["median"]:.2f}')
c3.metric(
    "Observed Score Range",
    f'{summary["minimum"]:.0f}–{summary["maximum"]:.0f}',
)

st.caption(
    "The score calculation and its meaning have not been verified. "
    "These results describe the recorded field, not driver safety."
)

st.subheader("Distribution of Recorded Scores")

st.plotly_chart(
    px.histogram(
        driver_filtered,
        x="driver_score",
        nbins=20,
        title="Distribution of Driver Scores",
    ),
    use_container_width=True,
)

st.subheader("Driver-Level Score Summary")

driver_scores = driver_score_summary(driver_filtered)

st.dataframe(driver_scores, use_container_width=True)



# Module D: Historical route analysis
st.header("Module D — Route Analysis")

historical_routes = compare_historical_routes(
    delivery_filtered
)

st.write(
    "This analysis compares recorded trips. "
    "It does not identify the optimal road route or account "
    "for live traffic."
)

st.dataframe(
    historical_routes.head(20),
    use_container_width=True,
)

st.subheader("Recorded Distance by Route")

if not historical_routes.empty:
    route_labels = historical_routes.copy()

    route_labels["route"] = (
        route_labels["origin"]
        + " → "
        + route_labels["destination"]
    )

    st.plotly_chart(
        px.bar(
            route_labels.head(20),
            x="route",
            y="average_distance_km",
            title="Average Recorded Distance by Route",
        ),
        use_container_width=True,
    )
else:
    st.info("No valid route-distance records are available.")



# Data-quality validation
st.header("Data Quality Validation")

quality = validate_dataset(df)

st.write("Dataset rows:", quality["row_count"])
st.write("Missing required columns:", quality["missing_columns"])

if quality["missing_columns"]:
    st.error("Some required columns are missing.")
else:
    st.write("Missing values:", quality["missing_values"])
    st.write("Duplicate trip IDs:", quality["duplicate_trip_ids"])
    st.write("Invalid distances:", quality["invalid_distances"])
    st.write("Negative fuel values:", quality["negative_fuel_values"])
