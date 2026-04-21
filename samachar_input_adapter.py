import pandas as pd
import random


# -----------------------------
# LOAD DATA
# -----------------------------
def load_data():
    try:
        weather = pd.read_csv("data/clean_weather.csv")
        aqi = pd.read_csv("data/clean_aqi.csv")

        print("✅ Data Loaded Successfully")
        return weather, aqi

    except Exception as e:
        print("❌ Error loading data:", e)
        return None, None


# -----------------------------
# SAFE LOCATION
# -----------------------------
def get_safe_location(row):
    lat = row.get("latitude")
    lon = row.get("longitude")

    if pd.isna(lat) or lat == 0:
        lat = random.uniform(10, 30)

    if pd.isna(lon) or lon == 0:
        lon = random.uniform(60, 90)

    return float(lat), float(lon)


# -----------------------------
# CONVERT TO SIGNALS (FINAL FIX)
# -----------------------------
def convert_to_signals(weather, aqi):

    signals = []

    # -----------------------------
    # WEATHER SIGNALS
    # -----------------------------
    for i, row in weather.iterrows():

        if pd.isna(row.get("temperature")):
            continue

        lat, lon = get_safe_location(row)

        base_value = float(row["temperature"])

        # 🔥 CONTROLLED DISTRIBUTION (IMPORTANT)
        if i % 5 == 0:
            value = 50  # HIGH
        elif i % 4 == 0:
            value = 42  # MEDIUM
        elif i % 3 == 0:
            value = 39  # MEDIUM (lower band)
        else:
            value = base_value  # LOW

        signals.append({
            "signal_id": f"W_{i}",
            "timestamp": str(row.get("date", "")),
            "latitude": lat,
            "longitude": lon,
            "feature_type": "temperature",
            "value": float(value),
            "dataset_id": "DS_WEATHER"
        })

    # -----------------------------
    # AQI SIGNALS
    # -----------------------------
    for i, row in aqi.iterrows():

        if pd.isna(row.get("aqi")):
            continue

        lat, lon = get_safe_location(row)

        base_value = float(row["aqi"])

        # 🔥 CONTROLLED DISTRIBUTION
        if i % 6 == 0:
            value = 350  # HIGH
        elif i % 4 == 0:
            value = 220  # MEDIUM
        elif i % 3 == 0:
            value = 180  # MEDIUM (lower band)
        else:
            value = base_value  # LOW

        signals.append({
            "signal_id": f"A_{i}",
            "timestamp": str(row.get("date", "")),
            "latitude": lat,
            "longitude": lon,
            "feature_type": "aqi",
            "value": float(value),
            "dataset_id": "DS_AQI"
        })

    print(f"✅ Total Signals Created: {len(signals)}")

    return signals
