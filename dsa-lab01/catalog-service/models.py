from itertools import count

class Book:

    _id = count(0)

    def __init__(self, name, status, category):
        self.id = next(Book._id)
        self.name = name
        self.status = status
        self.category = category