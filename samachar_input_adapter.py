import pandas as pd


def load_data():
    try:
        weather = pd.read_csv("clean_weather.csv")
        aqi = pd.read_csv("clean_aqi.csv")

        print("✅ Data Loaded Successfully")
        return weather, aqi

    except Exception as e:
        print("❌ Error loading data:", e)
        return None, None


def convert_to_signals(weather, aqi):

    if weather is None or aqi is None:
        print("❌ Data not loaded")
        return []

    signals = []

    # Weather
    for i, row in weather.iterrows():

        temp = row.get("temperature") or row.get("temp") or row.get("Temperature")

        if pd.isna(temp):
            continue

        signals.append({
            "signal_id": f"W_{i}",
            "timestamp": str(row.get("date", "")),
            "latitude": float(row.get("latitude", 0.0)),
            "longitude": float(row.get("longitude", 0.0)),
            "feature_type": "temperature",
            "value": float(temp),
            "dataset_id": "DS_WEATHER"
        })

    # AQI
    for i, row in aqi.iterrows():

        aqi_val = row.get("aqi") or row.get("AQI")

        if pd.isna(aqi_val):
            continue

        signals.append({
            "signal_id": f"A_{i}",
            "timestamp": str(row.get("date", "")),
            "latitude": float(row.get("latitude", 0.0)),
            "longitude": float(row.get("longitude", 0.0)),
            "feature_type": "aqi",
            "value": float(aqi_val),
            "dataset_id": "DS_AQI"
        })

    print(f"✅ Total Signals Created: {len(signals)}")

    return signals
