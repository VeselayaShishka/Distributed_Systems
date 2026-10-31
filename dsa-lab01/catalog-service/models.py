from itertools import count

class Book:

    _id = count(1)

    def __init__(self, name, status, category):
        self.id = next(Book._id)
        self.name = name
        self.status = status
        self.category = category

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "status": self.status,
            "category": self.category
        }