from firebase_admin import auth
from flask_login import logout_user
from bullytracker import firestoredb


# User class for flask_login. This class takes a firebase idtoken ans
# verifies it and sets the attributes according to the result
class User:
    def __init__(self, id_token):
        try:
            # _auth_user_data stores user info related to authentication...
            self._auth_user_data = auth.verify_id_token(id_token, check_revoked=True)

            self.id_token = id_token
            self.user_id = self._auth_user_data["uid"]
            self.is_authenticated = True
            self.is_active = True

        except Exception as e:
            self.is_authenticated = False
            self.is_active = False
            # is this needed or are the attributes enough?
            print("User authentication failed: ")
            print(e)
            logout_user()
            return  # No need to fetch data if the user is bad...

        # User firestored data
        self.user_data = firestoredb.get_user(self.user_id).to_dict()

    def get_id(self):
        return self.id_token


# Docs say check_revoked flag is very expensive, so if it proves
# too slow, check: https://firebase.google.com/docs/auth/admin/manage-sessions#detect_id_token_revocation
