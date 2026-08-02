# src/dashboard/app.py
import streamlit as st
import pandas as pd
import plotly.express as px
from src.utils.helpers import generate_vessel_data
from src.models.iuu_detector import train_and_detect

# Page config
st.set_page_config(layout="wide", page_title="Ocean Guardian - Live Demo")
st.title("🌊 Ocean Guardian System")
st.caption("AI-Driven Maritime Intelligence & Ecological Monitoring (Live Simulation)")

# --- Initialize Data in Session State (so it persists across interactions) ---
if 'vessel_data' not in st.session_state:
    st.session_state.vessel_data = generate_vessel_data(num_vessels=50, hours=12)

# --- Sidebar Controls ---
st.sidebar.header("⚙️ Controls")

# Button to regenerate data
if st.sidebar.button("🔄 Refresh Data & Run Detection"):
    st.session_state.vessel_data = generate_vessel_data(num_vessels=50, hours=12)
    # Rerun is automatically triggered by Streamlit when state changes

st.sidebar.markdown("---")
st.sidebar.info("**Simulation Mode**: Data is generated locally. In production, this connects to Global Fishing Watch APIs.")

# --- Load Data from Session State ---
df = st.session_state.vessel_data

# --- Run Detection ---
anomalies, model = train_and_detect(df)

# --- Layout: 2 Columns ---
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("🗺️ Vessel Traffic Map")
    
    # Color mapping for visualization
    anomaly_vessel_ids = anomalies['vessel_id'].unique()
    df['color_label'] = df['vessel_id'].apply(
        lambda x: 'Suspicious' if x in anomaly_vessel_ids else 'Normal'
    )
    
    # Plotly Map
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
        st.error(f"⚠️ {len(anomaly_vessel_ids)} Suspicious Vessels Detected!")
        
        # Show top suspicious vessels (aggregated)
        alert_data = anomalies.groupby('vessel_id').agg({
            'speed': 'mean',
            'distance_to_mpa': 'mean',
            'anomaly_score': 'mean'
        }).reset_index().round(2)
        
        st.dataframe(alert_data.style.highlight_min('distance_to_mpa', color='red'))
        
        # Bleaching forecast (mock calculation for demo)
        st.subheader("🌡️ Ecological Risk")
        # Higher risk if more IUU
        mock_dhw = 2.5 + (len(anomaly_vessel_ids) / 5)
        if mock_dhw > 4.5:
            mock_dhw = 4.5  # cap for realism
        
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

# --- Footer ---
st.divider()
st.caption("DataOdyssey 2026 | KDU Team | Humanity × AI")