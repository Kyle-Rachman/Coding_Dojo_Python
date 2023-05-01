class User:
    def __init__(self, first_name, last_name, email, age):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.age = age
        self.is_rewards_member = False
        self.gold_card_points = 0

    def display_info(self):
        print(f"First name: {self.first_name}")
        print(f"Last name: {self.last_name}")
        print(f"Email: {self.email}")
        print(f"Age: {self.age}")
        print(f"Rewards Member: {self.is_rewards_member}")
        print(f"Gold Card Points: {self.gold_card_points}")
        return self

    def enroll(self):
        if self.is_rewards_member is not True:
            self.is_rewards_member = True
            self.gold_card_points = 200
        else:
            print("User already a member")
        return self

    def spend_points(self,amount):
        if amount < self.gold_card_points:
            self.gold_card_points -= amount
        else:
            print("You don't have enough points to do that!")
        return self

user1 = User("Kyle","Rachman","kcrachman@gmail.com",23)
user2 = User("George","Washington","none@gmail.com",67)
user3 = User("Mark", "King", "mking8@gmail.com", 22)

user1.display_info().enroll().spend_points(50).display_info().enroll()
user2.enroll().spend_points(80).display_info()
user3.display_info().spend_points(40)