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

---

##  Clone repo & install dependencies

git clone https://github.com/<your-username>/healthstack.git
cd healthstack
python -m venv .venv
source .venv/bin/activate   # (Windows: .venv\Scripts\activate)
pip install -r requirements.txt

---

##   Start services

- **Backend API**
python manage.py runserver

- **Celery worker**
celery -A healthstack.celery:app worker -l info

- **Celery beat (scheduler)**
celery -A healthstack.celery:app beat -l info

---

##   📊 Dashboard and 🛠 Tech Stack

Doctors log in at: http://<server-ip>:8000/dashboard/

Select athlete from dropdown

View live Heart Rate, SpO₂, Temperature trends

Alerts show in Recent Alerts panel

Hardware: Raspberry Pi Zero 2W, MAX30102, DS18B20, TP4056, MT3608

Backend: Django, Django REST Framework

Async: Celery, Redis

Messaging: MQTT (paho-mqtt, Mosquitto broker)

Frontend: Django Templates + Chart.js

System Services: systemd for Gunicorn, Celery, MQTT consumer

---

##  🔧 Deployment (Production)

sudo cp scripts/*.service /etc/systemd/system/

- **Reload systemd**
sudo systemctl daemon-reload

- **Enable and start**
sudo systemctl enable gunicorn celery-worker celery-beat run_mqtt_consumer
sudo systemctl start gunicorn celery-worker celery-beat run_mqtt_consumer

---

##   👨‍💻 Author

Developed by Shehu Yusuf.
For research & educational use in telemedicine and athlete monitoring.
