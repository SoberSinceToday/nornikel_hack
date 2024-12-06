class MemoryStore:
    def __init__(self):
        self.data = {}

    def add_user_data(self, user_id, data):
        self.data[user_id] = data

    def get_user_data(self, user_id):
        return self.data.get(user_id)

    def update_user_data(self, user_id, key, value):
        if user_id in self.data and key in self.data[user_id]:
            self.data[user_id][key] = value
            return True
        return False

    def clear_user_data(self, user_id):
        if user_id in self.data:
            del self.data[user_id]


store = MemoryStore()
