# models/user_update_history.py

from datetime import datetime
from typing import Dict, Any

class UserUpdateHistory:
    def __init__(self, history_id: str, user_id: str, timestamp: datetime, old_data: Dict[str, Any], updated_fields: Dict[str, Any]):
        """
        Represents a historical update record for a user.

        Args:
            history_id (str): Unique history record ID.
            user_id (str): The user who was updated.
            timestamp (datetime): When the update occurred.
            old_data (Dict[str, Any]): The original values before the update.
            updated_fields (Dict[str, Any]): Only the fields that were changed, with new values.
        """
        self.history_id = history_id
        self.user_id = user_id
        self.timestamp = timestamp
        self.old_data = old_data
        self.updated_fields = updated_fields

    def to_dict(self) -> Dict[str, Any]:
        return {
            "_id": self.history_id,
            "user_id": self.user_id,
            "timestamp": self.timestamp,
            "old_data": self.old_data,
            "updated_fields": self.updated_fields
        }

    def __repr__(self) -> str:
        return (
            f"UserUpdateHistory(history_id={self.history_id}, user_id={self.user_id}, "
            f"timestamp={self.timestamp.isoformat()}, old_data={self.old_data}, "
            f"updated_fields={self.updated_fields})"
        )
