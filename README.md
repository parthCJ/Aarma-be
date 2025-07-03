# 🌐 IoT Sensor Data API

A FastAPI-based backend to collect, manage, and store sensor data from IoT devices using MongoDB. Built for projects involving voltage, current, temperature sensors, and optional MQTT integration with AWS IoT Core.

---

## ⚙️ Tech Stack

- **Backend:** FastAPI (Python)
- **Database:** MongoDB
- **Protocol:** REST API (with Swagger UI)
- **MQTT (Optional):** AWS IoT Core via `paho-mqtt`

---

## 📦 Features

- 📥 Insert sensor data via POST request  
- 📤 Retrieve all or device-specific data  
- ✏️ Update sensor data  
- ❌ Delete device data  
- 📊 Auto-generated Swagger docs  
- 🌩️ Optional MQTT publish to AWS IoT  

---

## 🚀 Quick Start

1. **Clone Repo & Install**
   ```bash
   git clone https://github.com/your-username/Aarma-be.git
   cd Aarma-be
   pip install fastapi uvicorn pymongo paho-mqtt
