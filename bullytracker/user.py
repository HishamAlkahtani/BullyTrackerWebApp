# Some of  the properties of the User class
# are required by flask-login, and some are required
# by firebase-admin, so some properties may never
# be used, but are still needed.
# id is the username of the user.
class User:
    def __init__(self, id, password, email):
        self.id = id
        self.email = email
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

    def to_firebase_dict(self):
        dict = {}
        dict["uid"] = self.id
        dict["password"] = self.password
        dict["email"] = self.password
        return dict
