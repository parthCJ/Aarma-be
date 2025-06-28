# models/device.py

class Sensor:
    def __init__(self, sensor_id, sensor_name, sensor_specification, location_id):
        self.sensor_id = sensor_id
        self.sensor_name = sensor_name
        self.sensor_specification = sensor_specification
        self.location_id = location_id

    def __repr__(self):
        return (
            f"Sensor(sensor_id={self.sensor_id}, name={self.sensor_name}, "
            f"spec={self.sensor_specification}, location_id={self.location_id})"
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

    def remove_sensor(self, sensor_id):
        """Removes a sensor by ID from the list."""
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