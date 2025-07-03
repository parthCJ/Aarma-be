from datetime import datetime
from typing import Dict, Any


class LocationHistory:
    def __init__(self, history_id: str, location_id: str, timestamp: datetime, old_data: Dict[str, Any], updated_fields: Dict[str, Any]):
        """
        Represents a history record of updates made to a location.

        Args:
            history_id (str): Unique ID for this history record.
            location_id (str): ID of the location being updated.
            timestamp (datetime): When the update occurred.
            old_data (dict): The original values before the update.
            updated_fields (dict): The new values that were updated.
        """
        self.history_id = history_id
        self.location_id = location_id
        self.timestamp = timestamp
        self.old_data = old_data
        self.updated_fields = updated_fields

    def __repr__(self):
        return (
            f"LocationHistory(history_id={self.history_id}, location_id={self.location_id}, "
            f"timestamp={self.timestamp.isoformat()}, old_data={self.old_data}, updated_fields={self.updated_fields})"
        )
