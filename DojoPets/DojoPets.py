import Ninja, Pet

kyle = Ninja.Ninja(pet = Pet.Dog(name = "Pepper"), pet_food = ["cheese", "hamburger"])

kyle.feed(kyle.pet_food[0])
kyle.walk()
kyle.bathe()