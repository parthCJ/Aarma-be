# models/sensor_history.py
from datetime import datetime

class SensorUpdateHistory:
    def __init__(self, history_id, sensor_id, timestamp, old_data, updated_fields):
        """
        Represents a change made to a sensor's data (for audit/history tracking).

        Args:
            history_id (str): Unique identifier for the history record.
            sensor_id (str): ID of the sensor that was updated.
            timestamp (datetime): When the change was made.
            old_data (dict): Dictionary of old values.
            updated_fields (dict): Dictionary of updated values.
        """
        self.history_id = history_id
        self.sensor_id = sensor_id
        self.timestamp = timestamp
        self.old_data = old_data
        self.updated_fields = updated_fields

    def __repr__(self):
        return (
            f"SensorUpdateHistory(history_id={self.history_id}, sensor_id={self.sensor_id}, "
            f"timestamp={self.timestamp.isoformat()}, old_data={self.old_data}, "
            f"updated_fields={self.updated_fields})"
        )
