from lib.space import Space

class SpaceRepository:

    # We initialise with a database connection
    def __init__(self, connection):
        self._connection = connection

    # Retrieve all spaces
    def all(self):
        rows = self._connection.execute('SELECT * from spaces')
        spaces = []
        for row in rows:
            item = Space(row["name"], row["description"], row["availability_start_date"], row["availability_end_date"], row["price_per_night"], row["image_url"], row["owner_id"], row["id"])
            spaces.append(item)
        return spaces

    # Find a single space by their id
    def find(self, space_id):
        rows = self._connection.execute(
            'SELECT * from spaces WHERE id = %s', [space_id])
        row = rows[0]
        return Space(row["name"], row["description"], row["availability_start_date"], row["availability_end_date"], row["price_per_night"], row["image_url"], row["owner_id"], row["id"])

    # Create a new space
    # Do you want to get its id back? Look into RETURNING id;
    def create(self, space):
        self._connection.execute('INSERT INTO spaces (name, description, availability_start_date, availability_end_date, price_per_night, image_url, owner_id) VALUES (%s, %s, %s, %s, %s, %s, %s)', [
                                space.name, space.description, space.availability_start_date, space.availability_end_date, space.price_per_night, space.image_url, space.owner_id])
        return None

    # Delete an space by their id
    def delete(self, space_id):
        self._connection.execute(
            'DELETE FROM spaces WHERE id = %s', [space_id])
        return None



    # Find spaces by their owner_id
    def find_by_owner_id(self, owner_id):
        rows = self._connection.execute(
            'SELECT id, name, description, availability_start_date, availability_end_date, price_per_night, image_url, owner_id FROM spaces WHERE owner_id = %s', [owner_id])
        user_spaces = []
        for row in rows:
            item = Space(row["name"], row["description"], row["availability_start_date"], row["availability_end_date"], row["price_per_night"], row["image_url"], row["owner_id"], row["id"])
            user_spaces.append(item)
        return user_spaces

