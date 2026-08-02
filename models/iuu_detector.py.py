import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib

def train_isolation_forest(data: pd.DataFrame):
    model = IsolationForest(contamination=0.05, random_state=42)
    model.fit(data[['speed', 'course_change', 'distance_to_mpa']])
    joblib.dump(model, 'models/iuu_model.pkl')
    return model

def detect_anomalies(data: pd.DataFrame):
    model = joblib.load('models/iuu_model.pkl')
    preds = model.predict(data[['speed', 'course_change', 'distance_to_mpa']])
    data['anomaly'] = preds == -1
    return data[data['anomaly']]