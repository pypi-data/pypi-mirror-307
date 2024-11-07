class UserManager:
    def __init__(self):
        self.user_data = {}


    def add_user(self, user_id, user_data):
            self.user_data[user_id] = user_data
            print(f'Client with {user_id} has been added')



    def remove_user(self, user_id):
        if user_id in self.user_data:
            self.user_data.pop(user_id)
            print(f'User {user_id} is deleted')
        else:
            print(f'User {user_id} was not found')

    def update_user(self, user_id, user_data):
        if user_id in self.user_data:
            self.user_data[user_id].update(user_data)
            print(f'Client with {user_id} has been updated')
        else:
            print(f'User {user_id} has not been found')

    def find_user(self, user_id):
        if user_id in self.user_data:
            return self.user_data[user_id]
        else:
            print(f'User {user_id} is not found')