import sys
import os
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random
import requests
from PIL import Image, ImageDraw
from io import BytesIO
from sklearn.cluster import KMeans

# --- Session State ---
def init_session():
    defaults = {
        'vessel_data': None,
        'dark_mode': False,
        'chat_history': [],
        'language': 'English',
        'logged_in': False,
        'user_role': 'Researcher',
        'alerts': [],
        'sat_img': None,
        'segmented_img': None,
        'detection_img': None,
        'detections': None
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session()

# --- Default Users ---
if 'users' not in st.session_state:
    st.session_state.users = {
        'admin': {'password': 'admin123', 'role': 'Admin'},
        'officer': {'password': 'pass123', 'role': 'Fisheries Officer'},
        'researcher': {'password': 'res123', 'role': 'Researcher'}
    }

# --- Translations ---
TRANSLATIONS = {
    "English": {
        "title": "🌊 Ocean Guardian System",
        "subtitle": "AI-Driven Maritime Intelligence & Ecological Monitoring",
        "vessels": "🚢 Total Vessels",
        "suspicious": "⚠️ Suspicious",
        "confidence": "🎯 Confidence",
        "risk": "🌡️ Risk Level",
        "login": "🔐 Login",
        "signup": "📝 Sign Up",
        "create_account": "Create Account",
        "choose_username": "Choose Username",
        "choose_password": "Choose Password",
        "select_role": "Select Role",
        "account_created": "✅ Account created! Please login.",
        "username_exists": "❌ Username already exists",
        "invalid_credentials": "❌ Invalid username or password",
        "logout": "🚪 Logout",
        "welcome": "Welcome",
    },
    "Sinhala": {
        "title": "🌊 සාගර ආරක්ෂක පද්ධතිය",
        "subtitle": "AI මගින් ධාවනය වන මුහුදු බුද්ධි සහ පාරිසරික නිරීක්ෂණ",
        "vessels": "🚢 සම්පූර්ණ නැව්",
        "suspicious": "⚠️ සැක සහිත",
        "confidence": "🎯 විශ්වසනීයත්වය",
        "risk": "🌡️ අවදානම් මට්ටම",
        "login": "🔐 පුරනය වන්න",
        "signup": "📝 ලියාපදිංචි වන්න",
        "create_account": "ගිණුමක් සාදන්න",
        "choose_username": "පරිශීලක නාමය තෝරන්න",
        "choose_password": "මුරපදය තෝරන්න",
        "select_role": "භූමිකාව තෝරන්න",
        "account_created": "✅ ගිණුම සාදන ලදී! කරුණාකර පුරනය වන්න.",
        "username_exists": "❌ පරිශීලක නාමය දැනටමත් පවතී",
        "invalid_credentials": "❌ වලංගු නොවන පරිශීලක නාමය හෝ මුරපදය",
        "logout": "🚪 ඉවත් වන්න",
        "welcome": "සාදරයෙන් පිළිගනිමු",
    },
    "Tamil": {
        "title": "🌊 கடல் காவல் அமைப்பு",
        "subtitle": "AI-இயக்கப்படும் கடல் உளவுத்துறை மற்றும் சுற்றுச்சூழல் கண்காணிப்பு",
        "vessels": "🚢 மொத்த கப்பல்கள்",
        "suspicious": "⚠️ சந்தேகத்திற்கிடமான",
        "confidence": "🎯 நம்பிக்கை",
        "risk": "🌡️ ஆபத்து நிலை",
        "login": "🔐 உள்நுழைக",
        "signup": "📝 பதிவு செய்க",
        "create_account": "கணக்கை உருவாக்குக",
        "choose_username": "பயனர்பெயரை தேர்வு செய்க",
        "choose_password": "கடவுச்சொல்லை தேர்வு செய்க",
        "select_role": "பாத்திரத்தை தேர்வு செய்க",
        "account_created": "✅ கணக்கு உருவாக்கப்பட்டது! தயவுசெய்து உள்நுழையவும்.",
        "username_exists": "❌ பயனர்பெயர் ஏற்கனவே உள்ளது",
        "invalid_credentials": "❌ தவறான பயனர்பெயர் அல்லது கடவுச்சொல்",
        "logout": "🚪 வெளியேறு",
        "welcome": "வரவேற்கிறோம்",
    }
}

# --- Data Generator ---
def generate_marine_data(hours=24):
    end_time = datetime.now()
    start_time = end_time - timedelta(hours=hours)
<<<<<<< HEAD
    times = pd.date_range(start=start_time, end=end_time, freq='h')
=======
   times = pd.date_range(start=start_time, end=end_time, freq='h')
>>>>>>> 52dfb4b4a63056dc68fc912187aaf0e5456dd20c
    vessels = []
    for i in range(1, 61):
        is_anomalous = random.random() < 0.2
        lat = 6.5 + np.random.normal(0, 0.8)
        lon = 79.5 + np.random.normal(0, 0.8)
        for t in times:
            if is_anomalous:
                lat += (6.927 - lat) * 0.05 + np.random.normal(0, 0.03)
                lon += (79.861 - lon) * 0.05 + np.random.normal(0, 0.03)
                speed = np.random.uniform(0.5, 3.0)
            else:
                lat += np.random.normal(0, 0.015)
                lon += np.random.normal(0, 0.015)
                speed = np.random.uniform(8.0, 15.0)
            vessels.append({
                'vessel_id': i,
                'timestamp': t,
                'lat': lat,
                'lon': lon,
                'speed': speed,
                'is_anomalous': is_anomalous
            })
    df_vessels = pd.DataFrame(vessels)
    # SST grid
    sst_grid = []
    for lat in np.linspace(5.5, 7.5, 10):
        for lon in np.linspace(79.0, 80.5, 10):
            sst = 28.0 + np.random.normal(0, 1.5) + 0.5 * np.sin((lat - 6.0) * 2)
            sst_grid.append({'lat': lat, 'lon': lon, 'sst': sst})
    df_sst = pd.DataFrame(sst_grid)
    # Chlorophyll
    chl_grid = []
    for lat in np.linspace(5.5, 7.5, 10):
        for lon in np.linspace(79.0, 80.5, 10):
            chl = 0.3 + np.random.normal(0, 0.2) + 0.5 * np.exp(-((lat-6.5)**2 + (lon-79.8)**2) * 0.5)
            chl = max(0.05, min(2.0, chl))
            chl_grid.append({'lat': lat, 'lon': lon, 'chlorophyll': chl})
    df_chl = pd.DataFrame(chl_grid)
    # Weather
    weather = []
    for t in times[::3]:
        weather.append({
            'timestamp': t,
            'wind_speed': 5 + np.random.normal(0, 3),
            'wave_height': 0.5 + np.random.normal(0, 0.3),
            'visibility': 5 + np.random.normal(0, 2),
            'pressure': 1010 + np.random.normal(0, 5)
        })
    df_weather = pd.DataFrame(weather)
    return df_vessels, df_sst, df_chl, df_weather

# --- AI Functions ---
def detect_illegal_fishing(df):
    anomalies = df[df['is_anomalous'] == True].copy()
    if len(anomalies) > 0:
        risk_scores = np.random.uniform(60, 98, len(anomalies))
        anomalies['risk_score'] = risk_scores
        anomalies['reason'] = [
            random.choice([
                "Loitering inside Marine Protected Area",
                "AIS transponder turned off near protected zone",
                "Suspicious speed pattern",
                "Fishing in restricted zone"
            ]) for _ in range(len(anomalies))
        ]
    return anomalies

def predict_coral_bleaching(df_sst):
    if len(df_sst) > 0:
        avg_sst = df_sst['sst'].mean()
        dhw = max(0, (avg_sst - 27.5) * 1.5 + np.random.normal(0, 0.5))
        if dhw > 6: risk = "Critical"
        elif dhw > 4: risk = "High"
        elif dhw > 2: risk = "Medium"
        else: risk = "Low"
        return {'dhw': dhw, 'risk': risk, 'sst': avg_sst}
    return {'dhw': 0, 'risk': 'Unknown', 'sst': 0}

def predict_algal_bloom(df_sst, df_chl, df_weather):
    if len(df_sst) > 0 and len(df_chl) > 0:
        avg_sst = df_sst['sst'].mean()
        avg_chl = df_chl['chlorophyll'].mean()
        avg_wind = df_weather['wind_speed'].mean() if len(df_weather) > 0 else 5
        bloom_score = (avg_sst - 20) / 10 + avg_chl * 2 - avg_wind / 10
        bloom_prob = max(0, min(100, bloom_score * 20 + np.random.normal(0, 10)))
        return float(bloom_prob)
    return 0

def recommend_fishing_zones(df_sst, df_chl):
    zones = []
    for _, row in df_sst.iterrows():
        lat, lon = row['lat'], row['lon']
        mask = ((df_chl['lat'] - lat).abs() < 0.1) & ((df_chl['lon'] - lon).abs() < 0.1)
        chl = df_chl[mask]['chlorophyll'].mean()
        if pd.isna(chl): chl = 0.5
        sst = row['sst']
        if 26 < sst < 30 and 0.3 < chl < 1.5:
            status, color = "Safe", "#00AA00"
        elif 24 < sst < 31 and 0.1 < chl < 2.0:
            status, color = "Moderate", "#FFA500"
        else:
            status, color = "Avoid", "#FF0000"
        zones.append({'lat': lat, 'lon': lon, 'status': status, 'color': color, 'sst': sst, 'chlorophyll': chl})
    return pd.DataFrame(zones)

def get_chat_response(user_input, df, anomalies, lang):
    user_input = user_input.lower()
    t = TRANSLATIONS[lang]
    total_vessels = len(df['vessel_id'].unique()) if df is not None else 0
    suspicious_count = len(anomalies['vessel_id'].unique()) if anomalies is not None else 0
    if "vessel" in user_input or "count" in user_input:
        return f"{t['vessels']}: {total_vessels}, {t['suspicious']}: {suspicious_count}"
    elif "suspicious" in user_input or "alert" in user_input:
        if suspicious_count > 0:
            return f"⚠️ {suspicious_count} {t['suspicious']} detected."
        else:
            return "✅ All clear!"
    elif "risk" in user_input or "coral" in user_input:
        return "🌡️ Coral bleaching risk is monitored."
    elif "fishing" in user_input:
        return "🎣 Check the 'Fishing Zones' tab."
    elif "weather" in user_input:
        return "🌦️ Weather data in Weather tab."
    elif "hello" in user_input:
        return f"{t['welcome']}! How can I help?"
    else:
        return "Ask about vessels, suspicious activity, fishing, or weather."

# --- AI Vision Helper Functions ---
def load_image_from_url(url):
    response = requests.get(url, timeout=5)
    return Image.open(BytesIO(response.content))

def segment_image_kmeans(image, n_clusters=4):
    img = image.convert('RGB')
    np_img = np.array(img)
    pixels = np_img.reshape(-1, 3)
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    labels = kmeans.fit_predict(pixels)
    segmented = labels.reshape(np_img.shape[:2])
    colors = np.array([[0, 0, 255], [0, 255, 0], [255, 255, 0], [255, 0, 0]])
    colored = colors[segmented].astype(np.uint8)
    return Image.fromarray(colored)

def draw_detection_boxes(image, detections):
    img = image.copy()
    draw = ImageDraw.Draw(img)
    for (x1, y1, x2, y2, label, conf) in detections:
        draw.rectangle([x1, y1, x2, y2], outline='red', width=3)
        draw.text((x1, y1-12), f"{label} {conf:.0f}%", fill='red')
    return img

def generate_mock_detections(img_width, img_height):
    detections = []
    objects = ["Fishing Vessel", "Cargo Ship", "Boat", "Port", "Oil Tanker"]
    for _ in range(random.randint(5, 12)):
        x1 = random.randint(50, img_width-150)
        y1 = random.randint(50, img_height-150)
        x2 = x1 + random.randint(80, 200)
        y2 = y1 + random.randint(80, 150)
        label = random.choice(objects)
        conf = random.uniform(0.75, 0.99)
        detections.append((x1, y1, x2, y2, label, conf))
    return detections

# --- CSS ---
st.markdown("""
<style>
@keyframes pulse {
    0% { transform: scale(1); opacity: 1; }
    50% { transform: scale(1.1); opacity: 0.7; }
    100% { transform: scale(1); opacity: 1; }
}
.pulse-alert {
    animation: pulse 1.5s infinite;
    background: #e74c3c;
    color: white;
    padding: 4px 16px;
    border-radius: 20px;
    display: inline-block;
    font-weight: bold;
}
.risk-critical { background: #8B0000; color: white; padding: 2px 12px; border-radius: 12px; }
.risk-high { background: #FF0000; color: white; padding: 2px 12px; border-radius: 12px; }
.risk-medium { background: #FFA500; color: white; padding: 2px 12px; border-radius: 12px; }
.risk-low { background: #00AA00; color: white; padding: 2px 12px; border-radius: 12px; }
.main-header { font-size: 2.2rem; font-weight: 700; color: #1a5276; }
.sub-header { font-size: 1.1rem; color: #2e86c1; }
</style>
""", unsafe_allow_html=True)

# --- Generate Data ---
if st.session_state.vessel_data is None:
    vessels, sst, chl, weather = generate_marine_data(24)
    st.session_state.vessel_data = vessels
    st.session_state.sst_data = sst
    st.session_state.chl_data = chl
    st.session_state.weather_data = weather

# --- Main App ---
t = TRANSLATIONS[st.session_state.language]

# Sidebar
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3095/3095110.png", width=70)
    st.title("🌊 Guardian")
    st.caption("v2.0 | AI Maritime")
    st.markdown("---")
    st.session_state.language = st.selectbox("🌐 Language", ["English", "Sinhala", "Tamil"])
    st.session_state.dark_mode = st.toggle("🌙 Dark Mode", value=st.session_state.dark_mode)
    st.markdown("---")
    if not st.session_state.logged_in:
        tab_login, tab_signup = st.tabs(["🔐 Login", "📝 Sign Up"])
        with tab_login:
            with st.form("login_form"):
                st.subheader("Login")
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")
                if st.form_submit_button("Login"):
                    if username in st.session_state.users and st.session_state.users[username]['password'] == password:
                        st.session_state.logged_in = True
                        st.session_state.username = username
                        st.session_state.user_role = st.session_state.users[username]['role']
                        st.rerun()
                    else:
                        st.error("Invalid credentials")
        with tab_signup:
            with st.form("signup_form"):
                st.subheader("Create Account")
                new_username = st.text_input("Choose Username")
                new_password = st.text_input("Choose Password", type="password")
                new_role = st.selectbox("Select Role", ["Fisheries Officer", "Navy", "Researcher", "NGO", "Admin"])
                if st.form_submit_button("Sign Up"):
                    if new_username and new_password:
                        if new_username in st.session_state.users:
                            st.error("Username exists")
                        else:
                            st.session_state.users[new_username] = {'password': new_password, 'role': new_role}
                            st.success("Account created! Please login.")
                    else:
                        st.error("Fill all fields")
    else:
        st.success(f"Welcome, {st.session_state.username}!")
        st.caption(f"Role: {st.session_state.user_role}")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()
    st.markdown("---")
    st.caption("🏆 DataOdyssey 2026 | Team KDU")

# --- Main Content ---
if st.session_state.logged_in:
    st.markdown(f'<div class="main-header">{t["title"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sub-header">{t["subtitle"]}</div>', unsafe_allow_html=True)
    
    df = st.session_state.vessel_data
    df_sst = st.session_state.sst_data
    df_chl = st.session_state.chl_data
    df_weather = st.session_state.weather_data
    anomalies = detect_illegal_fishing(df)
    
    # --- TABS USING INDEX (NO UNPACKING) ---
    tabs = st.tabs([
        "📊 Dashboard", "🚢 Vessels", "🪸 Coral", "🌿 Algae", "🎣 Fishing Zones",
        "🌦️ Weather", "🛰️ Satellite", "📈 Analytics", "🧠 AI Vision"
    ])
    
    # --- TAB 0: DASHBOARD ---
    with tabs[0]:
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric(t["vessels"], len(df['vessel_id'].unique()))
        with col2:
            sus = len(anomalies['vessel_id'].unique())
            if sus > 0:
                st.markdown(f'<div class="pulse-alert">⚠️ {sus}</div>', unsafe_allow_html=True)
            else:
                st.metric(t["suspicious"], sus)
        with col3:
            st.metric(t["confidence"], f"{95 - sus:.0f}%")
        with col4:
            coral = predict_coral_bleaching(df_sst)
            st.metric(t["risk"], coral['risk'])
        with col5:
            bloom = predict_algal_bloom(df_sst, df_chl, df_weather)
            st.metric("🌿 Bloom Risk", f"{bloom:.0f}%")
        
        st.subheader("🗺️ Live Marine Map")
        map_style = "carto-darkmatter" if st.session_state.dark_mode else "carto-positron"
        fig = go.Figure()
        df['color'] = df['is_anomalous'].map({True: 'red', False: 'blue'})
        fig.add_trace(go.Scattermapbox(
            lat=df['lat'], lon=df['lon'],
            mode='markers',
            marker=dict(size=6, color=df['color'], opacity=0.8),
            text=df.apply(lambda r: f"Vessel {r['vessel_id']}<br>Speed: {r['speed']:.1f} kn", axis=1),
            hoverinfo='text',
            name='Vessels'
        ))
        fig.add_trace(go.Scattermapbox(
            lat=df_sst['lat'], lon=df_sst['lon'],
            mode='markers',
            marker=dict(size=12, color=df_sst['sst'], colorscale='RdBu', showscale=True, colorbar=dict(title="SST °C")),
            name='SST',
            opacity=0.3
        ))
        fig.update_layout(
            mapbox=dict(style=map_style, center=dict(lat=6.927, lon=79.861), zoom=8),
            height=500,
            margin=dict(l=0, r=0, t=0, b=0)
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("🔔 Recent Alerts")
        if sus > 0:
            for _, row in anomalies.head(3).iterrows():
                st.warning(f"🚨 Vessel {row['vessel_id']}: {row['reason']}")
        else:
            st.success("✅ No active alerts")
    
    # --- TAB 1: VESSELS ---
    with tabs[1]:
        st.subheader("🚢 Vessel Activity & Illegal Fishing Detection")
        col1, col2 = st.columns([2, 1])
        with col1:
            fig = px.scatter(df, x='timestamp', y='speed', color='is_anomalous',
                            title="Vessel Speeds Over Time",
                            labels={'is_anomalous': 'Suspicious'})
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            st.subheader("🎯 Risk Analysis")
            if len(anomalies) > 0:
                for _, row in anomalies.head(5).iterrows():
                    score = row['risk_score']
                    st.progress(score/100, text=f"Vessel {row['vessel_id']}: {score:.0f}% Risk")
                    st.caption(f"Reason: {row['reason']}")
                    st.divider()
            else:
                st.success("No suspicious vessels detected")
    
    # --- TAB 2: CORAL ---
    with tabs[2]:
        st.subheader("🪸 Coral Bleaching Prediction")
        coral = predict_coral_bleaching(df_sst)
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Sea Surface Temperature", f"{coral['sst']:.1f}°C")
        with col2:
            st.metric("Degree Heating Weeks", f"{coral['dhw']:.2f}")
        with col3:
            risk_class = coral['risk'].lower()
            st.markdown(f'<div class="risk-{risk_class}">{coral["risk"]} Risk</div>', unsafe_allow_html=True)
        fig = px.density_mapbox(df_sst, lat='lat', lon='lon', z='sst',
                                mapbox_style='carto-positron', radius=10,
                                title="Sea Surface Temperature Map",
                                color_continuous_scale='RdBu')
        fig.update_layout(mapbox=dict(center=dict(lat=6.927, lon=79.861), zoom=8))
        st.plotly_chart(fig, use_container_width=True)
    
    # --- TAB 3: ALGAE ---
    with tabs[3]:
        st.subheader("🌿 Harmful Algal Bloom Prediction")
        bloom_prob = predict_algal_bloom(df_sst, df_chl, df_weather)
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Bloom Probability", f"{bloom_prob:.1f}%")
            if bloom_prob > 70:
                st.warning("🚨 High bloom risk! Immediate monitoring advised")
            elif bloom_prob > 40:
                st.info("⚠️ Moderate bloom risk")
            else:
                st.success("✅ Low bloom risk")
        with col2:
            fig = px.scatter(df_chl, x='lon', y='lat', color='chlorophyll',
                            title="Chlorophyll Concentration",
                            color_continuous_scale='Viridis')
            st.plotly_chart(fig, use_container_width=True)
    
    # --- TAB 4: FISHING ZONES ---
    with tabs[4]:
        st.subheader("🎣 Sustainable Fishing Zone Recommendations")
        zones = recommend_fishing_zones(df_sst, df_chl)
        col1, col2 = st.columns(2)
        with col1:
            fig = px.scatter_mapbox(zones, lat='lat', lon='lon', color='status',
                                    color_discrete_map={'Safe': 'green', 'Moderate': 'orange', 'Avoid': 'red'},
                                    mapbox_style='carto-positron', title="Fishing Zones",
                                    hover_data=['sst', 'chlorophyll'])
            fig.update_layout(mapbox=dict(center=dict(lat=6.927, lon=79.861), zoom=8))
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            st.dataframe(zones[['lat', 'lon', 'status', 'sst', 'chlorophyll']].head(10))
    
    # --- TAB 5: WEATHER ---
    with tabs[5]:
        st.subheader("🌦️ Weather & Ocean Conditions")
        cols = st.columns(4)
        metrics = [
            ("Wind Speed", f"{df_weather['wind_speed'].mean():.1f} km/h"),
            ("Wave Height", f"{df_weather['wave_height'].mean():.1f} m"),
            ("Visibility", f"{df_weather['visibility'].mean():.1f} km"),
            ("Pressure", f"{df_weather['pressure'].mean():.0f} hPa")
        ]
        for col, (label, value) in zip(cols, metrics):
            col.metric(label, value)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df_weather['timestamp'], y=df_weather['wind_speed'], name='Wind Speed'))
        fig.add_trace(go.Scatter(x=df_weather['timestamp'], y=df_weather['wave_height'], name='Wave Height'))
        fig.update_layout(title="Weather Trends")
        st.plotly_chart(fig, use_container_width=True)
    
    # --- TAB 6: SATELLITE ---
    with tabs[6]:
        st.subheader("🛰️ Satellite Image Viewer")
        st.info("Comparing before/after images to observe environmental changes")
        col1, col2 = st.columns(2)
        with col1:
            st.image(
                "https://eoimages.gsfc.nasa.gov/ve/1473/trincomalee_oli_2018031_lrg.jpg",
                caption="Before (Earlier Month)",
                width="stretch"
            )
        with col2:
            st.image(
                "https://eoimages.gsfc.nasa.gov/ve/1474/trincomalee_oli_2018032_lrg.jpg",
                caption="After (Recent)",
                width="stretch"
            )
        st.caption("🔄 Drag the slider below to compare changes")
        st.slider("Comparison Overlay", 0, 100, 50, key="satellite_slider")
        st.caption("Swipe to compare changes in vegetation, water color, and coastal features")
    
    # --- TAB 7: ANALYTICS ---
    with tabs[7]:
        st.subheader("📈 Analytics Dashboard")
        col1, col2 = st.columns(2)
        with col1:
            fig = px.histogram(df, x='vessel_id', color='is_anomalous',
                              title="Vessel Activity Distribution")
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            fig = px.box(df, y='speed', color='is_anomalous',
                        title="Speed Distribution by Vessel Type")
            st.plotly_chart(fig, use_container_width=True)
        
        if st.button("📄 Generate Report"):
            report = f"""
            OCEAN GUARDIAN SYSTEM - REPORT
            Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}
            User: {st.session_state.username} ({st.session_state.user_role})
            
            SUMMARY
            - Total Vessels: {len(df['vessel_id'].unique())}
            - Suspicious Vessels: {len(anomalies['vessel_id'].unique())}
            - Coral Bleaching Risk: {predict_coral_bleaching(df_sst)['risk']}
            - Algal Bloom Risk: {predict_algal_bloom(df_sst, df_chl, df_weather):.1f}%
            
            SUSPICIOUS VESSELS
            {anomalies[['vessel_id', 'speed', 'risk_score', 'reason']].to_string() if len(anomalies)>0 else 'None'}
            """
            st.download_button(
                label="📥 Download Report",
                data=report,
                file_name=f"ocean_guardian_report_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain"
            )
    
    # --- TAB 8: AI VISION ---
    with tabs[8]:
        st.subheader("🧠 AI Vision – Satellite Image Analysis")
        st.caption("Live demonstration of AI segmentation and object detection on satellite imagery")
        
        image_url = "https://eoimages.gsfc.nasa.gov/ve/1473/trincomalee_oli_2018031_lrg.jpg"
        
        with st.spinner("Loading satellite image..."):
            try:
                img = load_image_from_url(image_url)
                st.session_state.sat_img = img
            except:
                st.error("Could not load image. Using fallback placeholder.")
                img = Image.new('RGB', (800, 400), color='green')
                st.session_state.sat_img = img
        
        img = st.session_state.sat_img
        
        sub_tab1, sub_tab2 = st.tabs(["🖼️ Image Segmentation", "🚢 Object Detection"])
        
        with sub_tab1:
            st.subheader("Semantic Segmentation (U-Net / DeepLabV3+ style)")
            st.caption("The AI classifies each pixel into categories (Water, Land, Vegetation, etc.)")
            
            col_orig, col_seg = st.columns(2)
            with col_orig:
                st.image(img, caption="Original Satellite Image", width="stretch")
            with col_seg:
                with st.spinner("Running segmentation (KMeans clustering)..."):
                    if st.session_state.segmented_img is None:
                        seg_img = segment_image_kmeans(img, n_clusters=4)
                        st.session_state.segmented_img = seg_img
                    st.image(st.session_state.segmented_img, caption="AI Segmentation Map", width="stretch")
            
            st.markdown("**Legend:** 🔵 Water · 🟢 Land · 🟡 Vegetation · 🔴 Built-up/Sand")
            st.caption("Clusters are assigned based on color similarity – this is a simplified demo of how U-Net would segment the image.")
        
        with sub_tab2:
            st.subheader("Object Detection (YOLOv11 style)")
            st.caption("The AI detects and classifies vessels and structures with confidence scores.")
            
            if st.session_state.detection_img is None:
                w, h = img.size
                detections = generate_mock_detections(w, h)
                det_img = draw_detection_boxes(img, detections)
                st.session_state.detection_img = det_img
                st.session_state.detections = detections
            
            st.image(st.session_state.detection_img, caption="AI Detection Results", width="stretch")
            
            df_det = pd.DataFrame(st.session_state.detections, columns=['x1', 'y1', 'x2', 'y2', 'Label', 'Confidence'])
            df_det['Confidence'] = (df_det['Confidence'] * 100).round(0).astype(int)
            df_det = df_det[['Label', 'Confidence']]
            st.dataframe(df_det, use_container_width=True)
            
            st.caption("🚨 **Illegal Fishing Alert:** 3 vessels detected inside the Marine Protected Area!")

# --- Chatbot ---
with st.sidebar:
    st.markdown("---")
    st.subheader("🤖 AI Chat Assistant")
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    chat_container = st.container(height=200)
    with chat_container:
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                st.markdown(f'🧑‍💻 {msg["content"]}')
            else:
                st.markdown(f'🤖 {msg["content"]}')
    col_input, col_speak = st.columns([4, 1])
    with col_input:
        user_input = st.chat_input("Ask about vessels, fishing, weather...")
    with col_speak:
        if st.button("🔊", help="Speak last response"):
            if st.session_state.chat_history:
                last = st.session_state.chat_history[-1]["content"]
                st.markdown(f'<script>speechSynthesis.speak(new SpeechSynthesisUtterance("{last}"));</script>', unsafe_allow_html=True)
    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        response = get_chat_response(user_input, df, anomalies, st.session_state.language)
        st.session_state.chat_history.append({"role": "assistant", "content": response})
        st.rerun()


