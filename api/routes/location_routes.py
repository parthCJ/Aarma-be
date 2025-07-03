from fastapi import APIRouter, HTTPException, status
from fastapi import Query
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field
from typing import Optional, List, Tuple
from datetime import datetime, timezone
from database.connection import get_database

router = APIRouter()
db = get_database()
locations_collection = db["locations"]
location_history_collection = db["location_update_history"]

# ----------------------------
# Pydantic Schemas
# ----------------------------

class Address(BaseModel):
    address_line: str
    city: str
    state: str
    country: str
    zip_code: str

class LocationCreate(BaseModel):
    location_id: str = Field(..., example="LOC001")
    user_id: str
    address: Address
    name: str  
    coordinates: Tuple[float, float] 
    description: str  

class LocationUpdate(BaseModel):
    address: Optional[Address] = None
    name: Optional[str] = None
    coordinates: Optional[Tuple[float, float]] = None
    description: Optional[str] = None

class LocationResponse(LocationCreate):
    created_at: datetime
    is_deleted: bool

# ----------------------------
# Routes
# ----------------------------

@router.post("/", response_model=LocationResponse, status_code=status.HTTP_201_CREATED)
def create_location(location: LocationCreate):
    if locations_collection.find_one({"location_id": location.location_id}):
        raise HTTPException(status_code=400, detail="Location already exists")

    location_data = location.model_dump()
    location_data["created_at"] = datetime.now(timezone.utc)
    location_data["is_deleted"] = False
    locations_collection.insert_one(location_data)
    return location_data

@router.get("/", response_model=List[LocationResponse])
def get_all_locations():
    return list(locations_collection.find({"is_deleted": {"$ne": True}}, {"_id": 0}))

@router.get("/{location_id}", response_model=LocationResponse)
def get_location(location_id: str):
    location = locations_collection.find_one({"location_id": location_id, "is_deleted": {"$ne": True}}, {"_id": 0})
    if not location:
        raise HTTPException(status_code=404, detail="Location not found")
    return location

@router.patch("/{location_id}", response_model=LocationResponse)
def update_location(location_id: str, updates: LocationUpdate):
    location = locations_collection.find_one({"location_id": location_id, "is_deleted": {"$ne": True}})
    if not location:
        raise HTTPException(status_code=404, detail="Location not found")

    update_data = {k: v for k, v in updates.model_dump(exclude_unset=True).items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields provided for update")

    # Log history before update
    history_entry = {
        "location_id": location_id,
        "timestamp": datetime.now(timezone.utc),
        "old_data": {k: location[k] for k in update_data if k in location},
        "updated_fields": update_data
    }
    location_history_collection.insert_one(history_entry)

    # Apply update
    locations_collection.update_one(
        {"location_id": location_id},
        {"$set": update_data}
    )

    updated = locations_collection.find_one({"location_id": location_id}, {"_id": 0})
    return updated

@router.delete("/{location_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_location(location_id: str):
    result = locations_collection.update_one(
        {"location_id": location_id},
        {"$set": {"is_deleted": True}}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Location not found or already deleted")
    return





@router.get("/filter", response_model=List[LocationResponse])
def filter_locations(
    user_id: Optional[str] = None,
    city: Optional[str] = None,
    state: Optional[str] = None,
    country: Optional[str] = None,
    name: Optional[str] = None,
    created_from: Optional[str] = Query(None, description="Format: YYYY-MM-DDTHH:MM:SS"),
    created_to: Optional[str] = Query(None, description="Format: YYYY-MM-DDTHH:MM:SS")
):
    query = {"is_deleted": {"$ne": True}}

    if user_id:
        query["user_id"] = user_id
    if city:
        query["address.city"] = {"$regex": city, "$options": "i"}
    if state:
        query["address.state"] = {"$regex": state, "$options": "i"}
    if country:
        query["address.country"] = {"$regex": country, "$options": "i"}
    if name:
        query["name"] = {"$regex": name, "$options": "i"}
    if created_from or created_to:
        query["created_at"] = {}
        if created_from:
            query["created_at"]["$gte"] = datetime.fromisoformat(created_from)
        if created_to:
            query["created_at"]["$lte"] = datetime.fromisoformat(created_to)

    locations = locations_collection.find(query, {"_id": 0})
    return jsonable_encoder(list(locations))
