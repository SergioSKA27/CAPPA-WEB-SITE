import bcrypt
from streamlit import session_state
import extra_streamlit_components as stx
from st_xatadb_connection import XataConnection
from .Usuario import Usuario
import datetime

class Autenticador:
    def __init__(self,xatacon: XataConnection,manager:stx.CookieManager):
        if 'auth_state' in session_state:
            self.autenticado = session_state.auth_state
        else:
            self.autenticado = False

        self.xatacon = xatacon
        self.manager = manager

    def validate_password(self, password, hashed_password):
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

    def _get_manager(self):
        return stx.CookieManager(key='auth',)

    def set_valid_cookie(self, username,days_to_expire=1):
        manager = self.manager
        if days_to_expire > 1:
            manager.set('Validado', username,expires_at=datetime.datetime.now() + datetime.timedelta(days=days_to_expire))
        else:
            manager.set('Validado', username)

    def delete_valid_cookie(self):
        manager = self.manager
        if manager.get('Validado') is not None:
            manager.delete('Validado')

    def validate_cookie(self):
        manager = self.manager
        if manager.get_all('valid').get('Validado') is not None:
            if 'auth_state' not in session_state:
                session_state.auth_state = True
            else:
                session_state.auth_state = True

            if 'username' not in session_state:
                session_state.username = manager.get('Validado')
            else:
                session_state.username = manager.get('Validado')

            if 'userinfo' not in session_state:
                try:
                    session_state.userinfo = self.xatacon.get('Usuario',session_state.username)
                except Exception as e:
                    print(e)
            else:
                try:
                    session_state.userinfo = self.xatacon.get('Usuario',session_state.username)
                except Exception as e:
                    print(e)

            if 'user' not in session_state:
                session_state.user = Usuario(session_state.userinfo)
            else:
                session_state.user = Usuario(session_state.userinfo)




    def __call__(self):
        return self.autenticado
