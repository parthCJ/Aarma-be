from fastapi import APIRouter, HTTPException, status  # type: ignore
from pydantic import BaseModel, EmailStr, Field  # type: ignore
from typing import List, Optional
from datetime import datetime, timezone
from database.connection import get_database

router = APIRouter()
db = get_database()
users_collection = db["users"]
history_collection = db["user_update_history"]

# --------------------
# Pydantic User Schemas
# --------------------
class UserCreate(BaseModel):
    user_id: str = Field(..., example="USER001")
    email: EmailStr
    number: str = Field(..., example="9649722470")
    location_ids: List[str] = Field(default=[])

class UserResponse(UserCreate):
    created_at: datetime
    is_deleted: bool

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    number: Optional[str] = None
    location_ids: Optional[List[str]] = None

# -------------------------
# Create a new user
# -------------------------
@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate):
    existing = users_collection.find_one({
        "$or": [{"email": user.email}, {"number": user.number}]
    })
    if existing:
        raise HTTPException(status_code=400, detail="User with this email or number already exists")

    user_data = user.dict()
    user_data["created_at"] = datetime.now(timezone.utc)  # timezone-aware datetime
    user_data["is_deleted"] = False  # Soft delete flag by default
    users_collection.insert_one(user_data)
    return user_data

# -------------------------
# Get all users (excluding deleted)
# -------------------------
@router.get("/", response_model=List[UserResponse])
def get_all_users():
    users = list(users_collection.find({"is_deleted": {"$ne": True}}, {"_id": 0}))
    return users

# -------------------------
# Get user by ID (excluding deleted)
# -------------------------
@router.get("/{user_id}", response_model=UserResponse)
def get_user_by_id(user_id: str):
    user = users_collection.find_one(
        {"user_id": user_id, "is_deleted": {"$ne": True}}, {"_id": 0}
    )
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/")
def get_user_by_query(user_id: str = None):
    if not user_id:
        raise HTTPException(status_code=400, detail="user_id is required")
    
    user = users_collection.find_one({"user_id": user_id, "is_deleted": {"$ne": True}}, {"_id": 0})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# -------------------------
# Update user (with history)
# -------------------------
@router.patch("/{user_id}", response_model=UserResponse)
def update_user(user_id: str, user_update: UserUpdate):
    existing_user = users_collection.find_one(
        {"user_id": user_id, "is_deleted": {"$ne": True}}
    )
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")

    update_data = {k: v for k, v in user_update.dict().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No data provided for update")

    # Save current data to history
    history_data = existing_user.copy()
    history_data["_original_id"] = history_data.pop("_id")
    history_data["modified_at"] = datetime.now(timezone.utc)
    history_collection.insert_one(history_data)

    # Update user
    users_collection.update_one(
        {"user_id": user_id},
        {"$set": update_data}
    )

    updated_user = users_collection.find_one({"user_id": user_id}, {"_id": 0})
    return updated_user

# -------------------------
# Soft delete user
# -------------------------
@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: str):
    result = users_collection.update_one(
        {"user_id": user_id},
        {"$set": {"is_deleted": True}}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="User not found or already deleted")
    return

# -------------------------
# Get update history for a user
# -------------------------
@router.get("/{user_id}/history")
def get_user_update_history(user_id: str):
    history = list(history_collection.find(
        {"user_id": user_id},
        {"_id": 0}
    ))
    if not history:
        raise HTTPException(status_code=404, detail="No update history found for this user")
    return history
