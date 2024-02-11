import bcrypt
from streamlit import session_state
class Autenticador:
    def __init__(self):
        if 'auth_state' in session_state:
            self.autenticado = session_state.auth_state
        else:
            self.autenticado = False

    def validate_password(self, password, hashed_password):
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

    def __call__(self):
        return self.autenticado
