import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Fleet Management Platform",
    layout="wide"
)

st.title("Comprehensive Logistics and Fleet Management")

df = pd.read_csv("data/dataset.csv")

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