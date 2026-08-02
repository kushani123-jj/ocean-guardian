# 🌊 Ocean Guardian System

**AI-Driven Maritime Intelligence & Ecological Monitoring Platform**

[![Python 3.8](https://img.shields.io/badge/python-3.8-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io)

## 📝 Overview

The Ocean Guardian System transitions marine conservation from reactive to predictive by integrating satellite imagery, AIS vessel telemetry, and environmental data into a unified pipeline. It detects illegal fishing in real‑time, forecasts coral bleaching and algal blooms, and maps sustainable fishing zones – all visualised on a live operational dashboard.

## 🚀 Features

- **IUU Fishing Detection** – Isolation Forest & XGBoost for suspicious vessel behaviour.
- **Ecological Risk Forecasting** – LSTM networks for Degree Heating Weeks (DHW) and algal bloom probability.
- **Habitat Suitability Mapping** – Random Forest correlating fish migrations with oceanographic features.
- **Interactive Dashboard** – Streamlit + Plotly/Mapbox for real‑time situational awareness.

## 🛠️ Tech Stack

- **Languages**: Python 3.8
- **Data Processing**: Pandas, NumPy, GeoPandas, Rasterio
- **Machine Learning**: Scikit‑learn, TensorFlow/Keras, XGBoost
- **Visualisation**: Streamlit, Plotly, Folium, Mapbox
- **APIs**: Global Fishing Watch, Google Earth Engine, Copernicus, NOAA, Open‑Meteo, OBIS

## 📦 Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/ocean-guardian.git
   cd ocean-guardian