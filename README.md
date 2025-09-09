# 🩺 HealthStack – Real-Time Athlete Health Monitoring

HealthStack is a full-stack system for **real-time physiological monitoring of athletes**.  
It integrates **embedded sensors (MAX30102, DS18B20)** with a **Raspberry Pi edge device**, a **Django backend**, and a **doctor’s dashboard UI** for live visualization.

---

## 🚀 Features

- 📡 **Sensor Integration**
  - MAX30102 → Heart Rate (bpm) + SpO₂ (%)
  - DS18B20 → Skin Temperature (°C)

- 🔢 **Signal Processing**
  - Sliding window averaging  
  - Adaptive HR peak detection  
  - SpO₂ estimation using Ratio-of-Ratios  
  - Smoothing (EMA + step clamps)

- 🖥 **Backend**
  - Django + Django REST Framework  
  - API endpoint /api/ingest/ for sensor ingestion  
  - PostgreSQL database for persistent storage

- ⚙ **Asynchronous Processing**
  - Celery (workers + beat scheduler)  
  - MQTT consumer service for ingesting Pi-published data

- 📊 **Visualization**
  - Node-RED prototype (on Pi)  
  - Django doctor’s dashboard (on web)  
  - Real-time charts: Heart Rate, SpO₂, Temperature  
  - Alerts panel for abnormal values

---

## 📂 Repository Structure

``plaintext
healthstack/
├── vitals/                 # Django app for vital readings
├── dashboard/              # Doctor’s dashboard UI
├── healthstack/            # Project core settings
├── scripts/                # systemd unit files (deployment)
│   ├── gunicorn.service
│   ├── celery-worker.service
│   ├── celery-beat.service
│   └── run_mqtt_consumer.service
├── drivers/                # Custom Python drivers (MAX30102, etc.)
├── requirements.txt
└── README.md
