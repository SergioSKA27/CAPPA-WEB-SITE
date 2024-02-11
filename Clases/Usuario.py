
import base64

class Usuario:
    def __init__(self, record):
        if record is None:
            self.empty = True
            self.usuario = 'Iniciar Sesión'
            return

        self.nombre = record['nombre_completo']
        self.correo = record['correo']
        self.key = record['id']
        self.usuario = record['username']
        self.rol = record['rol']
        self.verificado = record['verificado']
        self.avatar = f'data:image/jpeg;base64,{base64.b64encode(open("rsc/Logos/LOGO_CAPPA.jpg", "rb").read()).decode()}'
        self.score =  record['score']
        self.rank = record['rango']
        self.empty = False

        if 'avatar' in record:
            self.avatar = record['avatar']['url']

        if 'feed' in record:
            self.feed = record['feed']

        if 'sociaLinks' in record:
            self.sociaLinks = record['sociaLinks']

    def is_admin(self):
        if self.empty:
            return False
        return self.rol == 'Administrador'

    def is_teacher(self):
        if self.empty:
            return False
        return self.rol == 'Profesor'

    def is_moderator(self):
        if self.empty:
            return False
        return self.rol == 'Moderador'

    def is_student(self):
        if self.empty:
            return False
        return self.rol == 'Estudiante'

    def is_verified(self):
        if self.empty:
            return False
        return self.verificado

    def __repr__(self):
        return self.__dict__

