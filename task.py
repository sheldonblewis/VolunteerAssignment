class Task:
    id: int
    name: str
    description: str
    required_volunteers: int

    def __init__(self, id: int, name: str, description: str, required_volunteers: int = 1):
        self.id = id
        self.name = name
        self.description = description
        self.required_volunteers = required_volunteers

    def __str__(self):
        return f"Task #{self.id}: {self.name}"

    def __repr__(self):
        return f"Task({self.__dict__})"
