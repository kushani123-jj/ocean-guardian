import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def generate_vessel_data(num_vessels=30, hours=24, include_trails=True):
    """
    Generates realistic mock AIS data with vessel trails and timestamps.
    """
    data = []
    end_time = datetime.now()
    start_time = end_time - timedelta(hours=hours)
    
    # Sri Lanka MPA
    mpa_lat, mpa_lon = 6.927, 79.861  # Colombo
    
    for vessel_id in range(1, num_vessels + 1):
        is_anomalous = random.random() < 0.2
        lat = 6.5 + np.random.normal(0, 0.5)
        lon = 79.5 + np.random.normal(0, 0.5)
        
        num_points = random.randint(15, 50)
        times = pd.date_range(start=start_time, periods=num_points, freq='H')
        
        for t in times:
            if is_anomalous:
                if random.random() < 0.1:
                    lat += np.random.uniform(-0.05, 0.05)
                    lon += np.random.uniform(-0.05, 0.05)
                else:
                    lat += (mpa_lat - lat) * 0.1 + np.random.normal(0, 0.02)
                    lon += (mpa_lon - lon) * 0.1 + np.random.normal(0, 0.02)
                speed = np.random.uniform(0.5, 3.0)
                course = np.random.uniform(0, 360)
            else:
                lat += np.random.normal(0, 0.02)
                lon += np.random.normal(0, 0.02)
                speed = np.random.uniform(8.0, 15.0)
                course = np.random.uniform(0, 360)
            
            dist_to_mpa = np.sqrt((lat - mpa_lat)**2 + (lon - mpa_lon)**2)
            
            data.append({
                'vessel_id': vessel_id,
                'timestamp': t,
                'lat': lat,
                'lon': lon,
                'speed': speed,
                'course': course,
                'distance_to_mpa': dist_to_mpa,
                'is_anomalous': is_anomalous
            })
    
    df = pd.DataFrame(data)
    df['course_change'] = df.groupby('vessel_id')['course'].diff().fillna(0).abs()
    return df

def get_vessel_trail(df, vessel_id):
    """Extract trail coordinates for a specific vessel."""
    vessel_data = df[df['vessel_id'] == vessel_id].sort_values('timestamp')
    return list(zip(vessel_data['lat'], vessel_data['lon']))
