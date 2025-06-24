from fastapi import FastAPI
from api.routes.user_routes import router as user_router
from api.routes.location_routes import router as location_router
from api.routes.device_routes import router as device_router
from api.routes.sensor_routes import router as sensor_router

app = FastAPI(
    title="IoT Device Management API",
    description="APIs to manage users, locations, devices, sensors, and data",
    version="1.0.0"
)

app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(location_router, prefix="/locations", tags=["Locations"])
app.include_router(device_router, prefix="/devices", tags=["Devices"])
app.include_router(sensor_router, prefix="/sensors", tags=["Sensors"])

@app.get("/")
def root():
    return {"message": "Welcome to the IoT Device Management API!"}
