
import base64

class Usuario:
    def __init__(self, record):
        self.nombre = record['nombre_completo']
        self.correo = record['correo']
        self.key = record['id']
        self.usuario = record['username']
        self.rol = record['rol']
        self.verificado = record['verificado']
        self.avatar = f'data:image/jpeg;base64,{base64.b64encode(open("rsc/Logos/LOGO_CAPPA.jpg", "rb").read()).decode()}'
        self.score =  record['score']
        self.rank = record['rango']


        if 'avatar' in record:
            self.avatar = record['avatar']['url']

        if 'feed' in record:
            self.feed = record['feed']

        if 'sociaLinks' in record:
            self.sociaLinks = record['sociaLinks']

    def is_admin(self):
        return self.rol == 'Administrador'

    def is_teacher(self):
        return self.rol == 'Profesor'

    def is_moderator(self):
        return self.rol == 'Moderador'

    def is_student(self):
        return self.rol == 'Estudiante'

    def is_verified(self):
        return self.verificado

    def __repr__(self):
        return self.__dict__

