class Booking:
    def __init__(self, space_id, booked_by, date, status, id=None):
        self.id = id
        self.space_id = space_id
        self.booked_by = booked_by
        self.date = date 
        self.status = status

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
    
    def __repr__(self):
        return f"Booking({self.space_id}, {self.booked_by}, {self.date}, {self.status}, {self.id})"