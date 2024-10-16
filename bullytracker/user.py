from firebase_admin import auth
from flask_login import logout_user


# User class for flask_login. This class takes a firebase idtoken ans
# verifies it and sets the attributes according to the result
class User:
    def __init__(self, idtoken):
        try:
            self._userData = auth.verify_id_token(idtoken, check_revoked=True)
            self.id = idtoken
            self.is_authenticated = True
            self.is_active = True
        except:
            self.is_authenticated = False
            self.is_active = False
            # is this needed or are the attributes enough?
            logout_user()

    def get_id(self):
        return self.id


# Docs say check_revoked flag is very expensive, so if it proves
# too slow, check: https://firebase.google.com/docs/auth/admin/manage-sessions#detect_id_token_revocation
