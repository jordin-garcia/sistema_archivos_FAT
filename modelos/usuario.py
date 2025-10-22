import hashlib


class Usuario:
    def __init__(self, nombre_usuario, password, es_admin=False):
        self.nombre_usuario = nombre_usuario
        self.password_hash = self._hashear_password(password)
        self.es_admin = es_admin

    def _hashear_password(self, password):
        return hashlib.sha256(password.encode("utf-8")).hexdigest()

    def verificar_password(self, password):
        return self.password_hash == self._hashear_password(password)

    def to_dict(self):
        return {
            "nombre_usuario": self.nombre_usuario,
            "password_hash": self.password_hash,
            "es_admin": self.es_admin,
        }

    @classmethod
    def from_dict(cls, data):
        usuario = cls.__new__(cls)
        usuario.nombre_usuario = data["nombre_usuario"]
        usuario.password_hash = data["password_hash"]
        usuario.es_admin = data["es_admin"]
        return usuario

    def __repr__(self):
        tipo = "Admin" if self.es_admin else "Usuario"
        return f"<Usuario('{self.nombre_usuario}', tipo='{tipo}')>"

    def __str__(self):
        return self.nombre_usuario
