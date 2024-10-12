class User:
    def __init__(self, id, password):
        self.id = id
        self.password = password
        self.is_authenticated = False
        self.is_active = True
        self.is_anonymous = False

    def get_id(self):
        return self.id

    def validatePassword(self, p):
        self.is_authenticated = User.hash(p) == self.password
        return self.is_authenticated

    # TODO: Add hashing
    def hash(p):
        return p
