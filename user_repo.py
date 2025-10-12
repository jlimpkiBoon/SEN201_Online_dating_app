class user:
    def __init__(self, username, age, gender, city):
        self.username = username
        self.age = age
        self.gender = gender
        self.city = city 

user_list = []

def creeate_user(username, age, gender, city):
    return user(username, age, gender, city)
             

def add_user(user):
    user_list.append(user)


