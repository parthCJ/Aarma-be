# models/device.py
from datetime import datetime

class SensorReading:
    def __init__(self, sensor_name, status, reading, unit, note="", sensor_health=None, sensor_specification=None):
        self.sensor_name = sensor_name
        self.status = status  # e.g. "OK", "Error", "Offline"
        self.reading = reading  # e.g. 23.5
        self.unit = unit  # e.g. "°C", "%", "ppm"
        self.note = note
        self.sensor_health = sensor_health  # Optional extra data
        self.sensor_specification = sensor_specification

    def __repr__(self):
        return (
            f"SensorReading(sensor_name={self.sensor_name}, status={self.status}, "
            f"reading={self.reading}{self.unit}, note={self.note}, "
            f"health={self.sensor_health}, spec={self.sensor_specification})"
        )


class SensorData:
    def __init__(self, device_id, sensor_id, readings):
        self.device_id = device_id
        self.sensor_id = sensor_id
        self.created_at = datetime.now()
        self.readings = readings  # List of SensorReading

    def __repr__(self):
        return (
            f"SensorData(device_id={self.device_id}, sensor_id={self.sensor_id}, "
            f"created_at={self.created_at}, readings={self.readings})"
        )


class Sensor:
    def __init__(self, sensor_id):
        self.sensor_id = sensor_id
        self.sensor_data_log = []  # List of SensorData
        self.devices = []  # List of device IDs using this sensor

    def add_sensor_data(self, data):
        if isinstance(data, SensorData):
            self.sensor_data_log.append(data)

    def add_device(self, device_id):
        if device_id not in self.devices:
            self.devices.append(device_id)

    def remove_device(self, device_id):
        if device_id in self.devices:
            self.devices.remove(device_id)
            print(f"Device {device_id} removed from sensor {self.sensor_id}.")
        else:
            print(f"Device {device_id} not found in sensor {self.sensor_id}.")

    def __repr__(self):
        return (
            f"Sensor(sensor_id={self.sensor_id}, devices={self.devices}, "
            f"sensor_data_log={self.sensor_data_log})"
        )


class Device:
    def __init__(self, device_id, location_id, location_mark, device_name, sensors):
        """
        Represents a device that contains a list of sensors.

        Args:
            device_id (str): Unique ID for the device.
            location_id (str): ID of the location where the device is installed.
            location_mark (str): Specific area/spot in the location.
            device_name (str): Name or label of the device.
            sensors (list[Sensor]): List of Sensor objects.
        """
        self.device_id = device_id
        self.location_id = location_id
        self.location_mark = location_mark
        self.device_name = device_name
        self.sensors = sensors

    def add_sensor(self, sensor):
        """Adds a sensor if it's not already in the list."""
        if isinstance(sensor, Sensor) and sensor.sensor_id not in [s.sensor_id for s in self.sensors]:
            self.sensors.append(sensor)
            sensor.add_device(self.device_id)

    def remove_sensor(self, sensor_id):
        """Removes a sensor by ID from the list."""
        for sensor in self.sensors:
            if sensor.sensor_id == sensor_id:
                sensor.remove_device(self.device_id)
        original_count = len(self.sensors)
        self.sensors = [s for s in self.sensors if s.sensor_id != sensor_id]
        if len(self.sensors) < original_count:
            print(f"Sensor {sensor_id} removed.")
        else:
            print(f"Sensor {sensor_id} not found.")

    def __repr__(self):
        return (
            f"Device(device_id={self.device_id}, name={self.device_name}, location_id={self.location_id}, "
            f"location_mark={self.location_mark}, sensors={self.sensors})"
        )
