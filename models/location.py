from datetime import datetime

class Address:
    def __init__(self, address_line, city, state, country, zip_code):
        self.address_line = address_line
        self.city = city
        self.state = state
        self.country = country
        self.zip_code = zip_code

    def __repr__(self):
        return (f"Address({self.address_line}, {self.city}, "
                f"{self.state}, {self.country}, {self.zip_code})")


class Location:
    def __init__(self, location_id, address, user_id, created_at, name=None, coordinates=None, description=None):
        """
        Represents a physical location where devices/sensors are installed.

        Args:
            location_id (str): Unique ID for the location.
            address (Address): Address object containing location details.
            user_id (str): The user who owns this location.
            created_at (datetime): Timestamp when the location was created.
            name (str, optional): Friendly name like "Warehouse #1".
            coordinates (tuple, optional): GPS coordinates (lat, lon).
            description (str, optional): Optional description of the location.
        """
        self.location_id = location_id
        self.address = address
        self.user_id = user_id
        self.created_at = created_at
        self.name = name
        self.coordinates = coordinates  # e.g., (26.9124, 75.7873)
        self.description = description

    def __repr__(self):
        return (
            f"Location(location_id={self.location_id}, user_id={self.user_id}, "
            f"address={self.address}, created_at={self.created_at.isoformat()}, "
            f"name={self.name}, coordinates={self.coordinates}, description={self.description})"
        )
