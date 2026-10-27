# Comprehensive Logistics and Fleet Management Platform

## Project Overview
This project was developed as part of the HCLTech Career Shaper Programme. It analyzes logistics and fleet trip data to provide insights into fuel efficiency, delivery performance, vehicle utilization, driver scores, historical route patterns, and potential fuel-consumption anomalies.

## Technologies Used
- Python
- Pandas
- scikit-learn
- Streamlit
- Plotly

## Features
- Fleet performance KPIs
- Fuel consumption analysis in L/100 km
- Statistical and Isolation Forest anomaly detection
- Delivery status and performance analytics
- Driver score summaries
- Historical route comparisons
- Dataset validation and interactive filtering

## How to Run
1. Install Python.
2. Download or clone the repository.
3. Create and activate a virtual environment.
4. Install the dependencies:
   `pip install -r requirements.txt`
5. Ensure the authorized project dataset is available at `data/dataset.csv`.
6. Start the dashboard:
   `streamlit run app.py`

## Dataset
The dataset was provided by HCLTech for the project.
The dataset.csv must be added to the data folder.

## Project Status
The platform provides historical data analysis and dashboard-based insights. It does not currently implement live GPS tracking or live-traffic route optimization.
