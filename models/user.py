class User:
    def __init__(self, user_id, name, email, number, location_ids, created_at):
        """
        Represents a user in the IoT system.

        Args:
            user_id (str): Unique user identifier (must be provided).
            name (str): Full name of the user.
            email (str): Email address of the user.
            number (str): Contact number.
            location_ids (list[str]): List of location IDs owned by this user.
            created_at (datetime): The datetime when the user account was created.
        """
        self.user_id = user_id
        self.name = name
        self.email = email
        self.number = number
        self.location_ids = location_ids
        self.created_at = created_at

    def add_location(self, location_id):
        """Adds a location to the user's list if not already present."""
        if location_id not in self.location_ids:
            self.location_ids.append(location_id)

    def remove_location(self, location_id):
        """Removes a location from the user's list if it exists."""
        if location_id in self.location_ids:
            self.location_ids.remove(location_id)

    def __repr__(self):
        return (f"User(user_id={self.user_id}, name={self.name}, email={self.email}, "
                f"number={self.number}, locations={self.location_ids}, created_at={self.created_at.isoformat()})")
