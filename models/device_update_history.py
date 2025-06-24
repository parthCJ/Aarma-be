# models/device_history.py
from datetime import datetime
from typing import Dict, Any

class DeviceUpdateHistory:
    def __init__(self, history_id: str, device_id: str, timestamp: datetime, old_data: Dict[str, Any], updated_fields: Dict[str, Any]):
        """
        Represents the history of updates made to a device.

        Args:
            history_id (str): Unique history record ID.
            device_id (str): ID of the device that was updated.
            timestamp (datetime): When the update happened.
            old_data (dict): Fields and values before update.
            updated_fields (dict): Fields and values after update.
        """
        self.history_id = history_id
        self.device_id = device_id
        self.timestamp = timestamp
        self.old_data = old_data
        self.updated_fields = updated_fields

    def __repr__(self):
        return (
            f"DeviceUpdateHistory(history_id={self.history_id}, device_id={self.device_id}, "
            f"timestamp={self.timestamp.isoformat()}, old_data={self.old_data}, updated_fields={self.updated_fields})"
        )
