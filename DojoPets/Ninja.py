class Ninja:
    def __init__(self, first_name = "", last_name = "", treats = [], pet_food = [], pet = ""):
        self.first_name = first_name
        self.last_name = last_name
        self.treats = treats
        self.pet_food = pet_food
        self.pet = pet

    def walk(self):
        self.pet.play()
        self.pet.noise()
        return self
    
    def feed(self, food):
        self.pet.eat(food)
        return self
    
    def bathe(self):
        self.pet.noise()
        return self