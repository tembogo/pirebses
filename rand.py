import requests
import random
import time
import json
from datetime import datetime

# === Konfigurasi Firebase ===
FIREBASE_URL = "https://cbiot-7e060-default-rtdb.asia-southeast1.firebasedatabase.app"
API_KEY = "AIzaSyBKerqpbbhdaRSDXItUGddV7MQuIs9PxRg"

# === Fungsi untuk generate data sensor acak ===
def generate_random_sensor_data():
    return {
        "temperature": round(random.uniform(20.0, 35.0), 2),
        "humidity": round(random.uniform(40.0, 80.0), 2),
        "pressure": round(random.uniform(1000.0, 1020.0), 2),
        "light": round(random.uniform(100.0, 800.0), 2),
        "co2": round(random.uniform(350.0, 1000.0), 2),
        "gas": round(random.uniform(50.0, 300.0), 2),
        "noise": round(random.uniform(30.0, 70.0), 2),
        "motion": random.choice([0.0, 1.0]),
        "vibration": round(random.uniform(0.0, 5.0), 2),
        "voltage": round(random.uniform(210.0, 230.0), 2)
    }

# === Kirim data sensor terbaru ke /sensors ===
def update_sensors(sensor_data):
    url = f"{FIREBASE_URL}/sensors.json?auth={API_KEY}"
    try:
        response = requests.put(url, json=sensor_data)
        if response.status_code == 200:
            print("[OK] Data sensor terkini berhasil dikirim ke Firebase.")
        else:
            print(f"[WARN] Gagal update sensors: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"[ERROR] Terjadi kesalahan saat update sensors: {e}")

# === Tambah data ke /sensorHistory/<tanggal> ===
def update_sensor_history(sensor_data):
    timestamp = int(time.time() * 1000)
    current_date = datetime.now().strftime("%Y-%m-%d")
    history_url = f"{FIREBASE_URL}/sensorHistory/{current_date}.json?auth={API_KEY}"

    # Hanya kirim data temperatur & kelembapan ke history
    history_data = {
        "temperature": [{"timestamp": timestamp, "value": sensor_data["temperature"]}],
        "humidity": [{"timestamp": timestamp, "value": sensor_data["humidity"]}]
    }

    try:
        response = requests.patch(history_url, json=history_data)
        if response.status_code == 200:
            print("[OK] Riwayat sensor berhasil ditambahkan.")
        else:
            print(f"[WARN] Gagal update history: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"[ERROR] Terjadi kesalahan saat update history: {e}")

# === Main loop ===
if __name__ == "__main__":
    print("=== Simulasi pengiriman data sensor ke Firebase dimulai ===\n")
    while True:
        sensor_data = generate_random_sensor_data()
        print(json.dumps(sensor_data, indent=2))

        update_sensors(sensor_data)
        update_sensor_history(sensor_data)

        print("-" * 50)
        time.sleep(1)  # kirim setiap 5 detik
