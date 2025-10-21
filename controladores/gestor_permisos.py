from modelos import ArchivoFAT, Usuario


class GestorPermisos:
    def tiene_permiso_lectura(self, archivo_fat, usuario):
        # El propietario siempre tiene acceso completo
        if archivo_fat.propietario == usuario.nombre_usuario:
            return True

        # Los administradores tienen acceso completo
        if usuario.es_admin:
            return True

        # Verificar permisos específicos del usuario
        if usuario.nombre_usuario in archivo_fat.permisos:
            return archivo_fat.permisos[usuario.nombre_usuario].get("lectura", False)

        return False

    def tiene_permiso_escritura(self, archivo_fat, usuario):
        # El propietario siempre tiene acceso completo
        if archivo_fat.propietario == usuario.nombre_usuario:
            return True

        # Los administradores tienen acceso completo
        if usuario.es_admin:
            return True

        # Verificar permisos específicos del usuario
        if usuario.nombre_usuario in archivo_fat.permisos:
            return archivo_fat.permisos[usuario.nombre_usuario].get("escritura", False)

        return False

    def asignar_permiso(
        self, archivo_fat, usuario_destino, lectura, escritura, usuario_actual
    ):
        # Validar que el usuario actual sea propietario o admin
        if (
            archivo_fat.propietario != usuario_actual.nombre_usuario
            and not usuario_actual.es_admin
        ):
            return False, "Solo el propietario o administrador pueden asignar permisos"

        # No permitir asignar permisos al mismo propietario
        if usuario_destino == archivo_fat.propietario:
            return False, "El propietario ya tiene todos los permisos"

        # Asignar permisos
        archivo_fat.permisos[usuario_destino] = {
            "lectura": lectura,
            "escritura": escritura,
        }

        return True, f"Permisos asignados a {usuario_destino}"

    def revocar_permiso(self, archivo_fat, usuario_destino, usuario_actual):
        # Validar que el usuario actual sea propietario o admin
        if (
            archivo_fat.propietario != usuario_actual.nombre_usuario
            and not usuario_actual.es_admin
        ):
            return False, "Solo el propietario o administrador pueden revocar permisos"

        # No permitir revocar permisos al mismo propietario
        if usuario_destino == archivo_fat.propietario:
            return False, "No se pueden revocar permisos del propietario"

        # Verificar si el usuario tiene permisos asignados
        if usuario_destino not in archivo_fat.permisos:
            return False, f"{usuario_destino} no tiene permisos asignados"

        # Revocar permisos
        del archivo_fat.permisos[usuario_destino]

        return True, f"Permisos revocados a {usuario_destino}"

    def obtener_permisos_usuarios(self, archivo_fat, nombre_usuario):
        if nombre_usuario == archivo_fat.propietario:
            return {"lectura": True, "escritura": True}

        return archivo_fat.permisos.get(nombre_usuario, None)

    def listar_usuarios_con_permisos(self, archivo_fat):
        resultado = []

        # Agregar propietario
        resultado.append(
            (
                archivo_fat.propietario,
                {"lectura": True, "escritura": True, "propietario": True},
            )
        )

        # Agregar usuarios con permisos asignados
        for usuario, permisos in archivo_fat.permisos.items():
            resultado.append((usuario, permisos))

        return resultado
