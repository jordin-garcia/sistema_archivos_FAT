from modelos import Usuario
from utilidades import Serializador


class GestorUsuarios:
    def __init__(self, ruta_usuarios="usuarios.json"):
        self.ruta_usuarios = ruta_usuarios
        self.serializador = Serializador()

    def cargar_usuarios(self):
        datos = self.serializador.cargar_json(self.ruta_usuaios)
        if datos is None:
            return []
        return [Usuario.from_dict(d) for d in datos]

    def guardar_usuarios(self, usuarios):
        datos = self.serializador.lista_objetos_a_dicts(usuarios)
        self.serializador.guardar_json(self.ruta_usuarios, datos)

    def registrar_usuario(self, nombre_usuario, password, es_admin=False):
        usuarios = self.cargar_usuarios()

        if any(u.nombre_usuario == nombre_usuario for u in usuarios):
            return False, "El usuario ya existe"

        # Crear y agregar el nuevo usuario
        nuevo_usuario = Usuario(nombre_usuario, password, es_admin)
        usuarios.append(nuevo_usuario)
        self.guardar_usuarios(usuarios)

        return True, "Usuario registrado exitosamente."

    def autenticar(self, nombre_usuario, password):
        usuarios = self.cargar_usuarios()

        for usuario in usuarios:
            if usuario.nombre_usuario == nombre_usuario:
                if usuario.verificar_password(password):
                    return usuario
                else:
                    return None, "Contraseña incorrecta"

        return None, "Usuario no encontrado"

    def obtener_todos_usuarios(self):
        usuarios = self.cargar_usuarios()
        return [u.nombre_usuario for u in usuarios]

    def obtener_usuario_por_nombre(self, nombre_usuario):
        usuarios = self.cargar_usuarios()

        for usuario in usuarios:
            if usuario.nombre_usuario == nombre_usuario:
                return usuario

        return None

    def inicializar_usuarios(self):
        usuarios = self.cargar_usuarios()

        if len(usuarios) == 0:
            # Crear usuario administrador por defecto
            admin = Usuario("admin", "admin", es_admin=True)
            self.guardar_usuarios([admin])
            return True

        return False
