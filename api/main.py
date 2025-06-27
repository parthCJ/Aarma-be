from fastapi import FastAPI, Request
from api.routes.user_routes import router as user_router
from api.routes.location_routes import router as location_router
from api.routes.device_routes import router as device_router
from api.routes.sensor_routes import router as sensor_router

app = FastAPI(
    title="IoT Device Management API",
    description="APIs to manage users, locations, devices, sensors, and data",
    version="1.0.0"
)

# Fixed route prefix to match service_layer.py (which sends to /api/sensor-data)
app.include_router(user_router, prefix="/api", tags=["Users"])
app.include_router(location_router, prefix="/api", tags=["Locations"])
app.include_router(device_router, prefix="/api", tags=["Devices"])
app.include_router(sensor_router, prefix="/sensors", tags=["Sensors"])


@app.get("/")
def root():
    return {"message": "Welcome to the IoT Device Management API!"}
