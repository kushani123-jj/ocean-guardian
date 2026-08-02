import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def generate_vessel_data(num_vessels=30, hours=24):
    """
    Generates realistic mock AIS data.
    Normal vessels move in straight lines at ~10 knots.
    Anomalous vessels (IUU) will loiter near protected zones or turn off transponders.
    """
    data = []
    end_time = datetime.now()
    start_time = end_time - timedelta(hours=hours)
    
    # Define a marine protected area (MPA) center
    mpa_lat, mpa_lon = -8.5, 115.5  # Example: near Bali, Indonesia
    
    for vessel_id in range(1, num_vessels + 1):
        # 20% chance the vessel is "suspicious" (IUU)
        is_anomalous = random.random() < 0.2
        
        # Starting position (spread across a region)
        lat = -8.0 + np.random.normal(0, 0.5)
        lon = 115.0 + np.random.normal(0, 0.5)
        
        # Generate time steps
        num_points = random.randint(10, 40)
        times = pd.date_range(start=start_time, periods=num_points, freq='H')
        
        for t in times:
            # Normal movement: drift slowly
            if is_anomalous:
                # Anomalous: loiter near MPA or zigzag aggressively
                if random.random() < 0.1:
                    lat += np.random.uniform(-0.05, 0.05)
                    lon += np.random.uniform(-0.05, 0.05)
                else:
                    # Move towards MPA
                    lat += (mpa_lat - lat) * 0.1 + np.random.normal(0, 0.02)
                    lon += (mpa_lon - lon) * 0.1 + np.random.normal(0, 0.02)
                speed = np.random.uniform(0.5, 3.0)  # Slow loitering
                course = np.random.uniform(0, 360)
            else:
                # Normal: steady course
                lat += np.random.normal(0, 0.02)
                lon += np.random.normal(0, 0.02)
                speed = np.random.uniform(8.0, 15.0)  # Normal fishing/transit speed
                course = np.random.uniform(0, 360)
            
            # Distance to MPA (feature for the model)
            dist_to_mpa = np.sqrt((lat - mpa_lat)**2 + (lon - mpa_lon)**2)
            
            data.append({
                'vessel_id': vessel_id,
                'timestamp': t,
                'lat': lat,
                'lon': lon,
                'speed': speed,
                'course': course,
                'distance_to_mpa': dist_to_mpa,
                'is_anomalous': is_anomalous  # Ground truth for testing
            })
    
    df = pd.DataFrame(data)
    # Add a 'course_change' feature (rate of change)
    df['course_change'] = df.groupby('vessel_id')['course'].diff().fillna(0).abs()
    return df
