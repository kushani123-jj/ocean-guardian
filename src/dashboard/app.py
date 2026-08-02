import sys
import os
# Add project root to sys.path (go up 3 levels from this file)
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

import streamlit as st
import pandas as pd
import plotly.express as px
from src.utils.helpers import generate_vessel_data
from src.models.iuu_detector import train_and_detect

st.set_page_config(layout="wide", page_title="Ocean Guardian - Live Demo")
st.title("🌊 Ocean Guardian System")
st.caption("AI-Driven Maritime Intelligence & Ecological Monitoring (Live Simulation)")

if 'vessel_data' not in st.session_state:
    st.session_state.vessel_data = generate_vessel_data(num_vessels=50, hours=12)

st.sidebar.header("⚙️ Controls")
if st.sidebar.button("🔄 Refresh Data & Run Detection"):
    st.session_state.vessel_data = generate_vessel_data(num_vessels=50, hours=12)

st.sidebar.markdown("---")
st.sidebar.info("**Simulation Mode**: Data is generated locally.")

df = st.session_state.vessel_data
anomalies, model = train_and_detect(df)

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("🗺️ Vessel Traffic Map")
    anomaly_ids = anomalies['vessel_id'].unique()
    df['color_label'] = df['vessel_id'].apply(lambda x: 'Suspicious' if x in anomaly_ids else 'Normal')
    fig = px.scatter_mapbox(
        df,
        lat="lat",
        lon="lon",
        color="color_label",
        color_discrete_map={'Normal': '#1f77b4', 'Suspicious': '#d62728'},
        hover_data=['vessel_id', 'speed', 'distance_to_mpa'],
        zoom=8,
        height=600,
        mapbox_style="carto-positron"
    )
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("🚨 Real-Time Alerts")
    if len(anomalies) > 0:
        st.error(f"⚠️ {len(anomaly_ids)} Suspicious Vessels Detected!")
        alert_data = anomalies.groupby('vessel_id').agg({
            'speed': 'mean',
            'distance_to_mpa': 'mean',
            'anomaly_score': 'mean'
        }).reset_index().round(2)
        st.dataframe(alert_data.style.highlight_min('distance_to_mpa', color='red'))
        mock_dhw = 2.5 + (len(anomaly_ids) / 5)
        if mock_dhw > 4.5: mock_dhw = 4.5
        st.subheader("🌡️ Ecological Risk")
        st.metric("Degree Heating Weeks (DHW)", f"{mock_dhw:.2f}")
        if mock_dhw > 4.0:
            st.warning("🔥 High Coral Bleaching Risk!")
        elif mock_dhw > 2.0:
            st.info("⚠️ Moderate Risk - Monitor closely")
        else:
            st.success("✅ Low Risk")
    else:
        st.success("✅ No suspicious activity detected.")
        st.info("ℹ️ All vessels appear to be operating normally.")

st.divider()
st.caption("DataOdyssey 2026 | KDU Team | Humanity × AI")
