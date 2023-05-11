class Pet:
    def __init__(self, name = "", type = "", tricks = []):
        self.name = name
        self.type = type
        self.tricks = tricks
        self.health = 100
        self.energy = 100

    def sleep(self):
        self.energy += 25
        return self
    
    def eat(self, food):
        self.energy += 5
        self.health += 10
        print(f"{self.name} has eaten {food}!")
        return self
    
    def play(self):
        self.health += 5
        return self
    
    def noise(self):
        print("Pet noises!")
        return self

class Dog(Pet):
    def __init__(self, name = "", type = "", tricks = []):
        super().__init__(name, type, tricks)
    
    def noise(self):
        print("Woof!")
        return self

class Cat(Pet):
    def __init__(self, name = "", type = "", tricks = []):
        super().__init__(name, type, tricks)
    
    def noise(self):
        print("Meow!")
        return self