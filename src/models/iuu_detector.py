import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
import joblib
import os

def train_and_detect(data: pd.DataFrame):
    """
    Trains an Isolation Forest on the fly and returns flagged anomalies.
    """
    # Features we use to detect anomalies
    features = data[['speed', 'course_change', 'distance_to_mpa']].copy()
    
    # Handle any missing values
    features = features.fillna(features.mean())
    
    # Train Isolation Forest
    model = IsolationForest(contamination=0.15, random_state=42)
    model.fit(features)
    
    # Predict (-1 = anomaly, 1 = normal)
    data['prediction'] = model.predict(features)
    data['anomaly_score'] = model.decision_function(features)
    
    # Flag anomalies
    anomalies = data[data['prediction'] == -1].copy()
    return anomalies, model
