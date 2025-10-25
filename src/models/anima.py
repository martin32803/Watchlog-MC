


class Animal:
    def __init__(self, name: str, type: str, age: int = 0):
        self.name = name
        self.type = type
        self.age = age
    
    def __repr__(self):
        return f"<Animal name={self.name} type={self.type} age={self.age}>"
    
    def can_be_vaccinated(self) -> bool:
        return self.age < 5
    
    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "type": self.type,
            "age": self.age,
        }