class Space:
    def __init__(self, name, description, availability_start_date, availability_end_date, price_per_night, image_url, owner_id, id = None):
        self.id = id
        self.name = name
        self.description = description
        self.availability_start_date = availability_start_date 
        self.availability_end_date = availability_end_date 
        self.price_per_night = price_per_night
        self.image_url = image_url
        self.owner_id = owner_id
        
    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __repr__(self):
        return f"Space({self.name}, {self.description}, {self.availability_start_date}, {self.availability_end_date}, {self.price_per_night}, {self.image_url}, {self.owner_id}, {self.id})"
