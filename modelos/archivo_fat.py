from datetime import datetime


class ArchivoFAT:
    def __init__(
        self,
        nombre_archivo,
        ruta_datos_inicial,
        en_papelera=False,
        cantidad_caracteres=0,
        fecha_creacion=None,
        fecha_modificacion=None,
        fecha_eliminacion=None,
        propietario=None,
        permisos=None,
    ):
        self.nombre_archivo = nombre_archivo
        self.ruta_datos_inicial = ruta_datos_inicial
        self.en_papelera = en_papelera
        self.cantidad_caracteres = cantidad_caracteres
        self.fecha_creacion = fecha_creacion or datetime.now().isoformat()
        self.fecha_modificacion = fecha_modificacion or datetime.now().isoformat()
        self.fecha_eliminacion = fecha_eliminacion
        self.propietario = propietario
        self.permisos = permisos if permisos is not None else {}

    def to_dict(self):
        return {
            "nombre_archivo": self.nombre_archivo,
            "ruta_datos_inicial": self.ruta_datos_inicial,
            "en_papelera": self.en_papelera,
            "cantidad_caracteres": self.cantidad_caracteres,
            "fecha_creacion": self.fecha_creacion,
            "fecha_modificacion": self.fecha_modificacion,
            "fecha_eliminacion": self.fecha_eliminacion,
            "propietario": self.propietario,
            "permisos": self.permisos,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            nombre_archivo=data["nombre_archivo"],
            ruta_datos_inicial=data["ruta_datos_inicial"],
            en_papelera=data.get("en_papelera", False),
            cantidad_caracteres=data.get("cantidad_caracteres", 0),
            fecha_creacion=data.get("fecha_creacion"),
            fecha_modificacion=data.get("fecha_modificacion"),
            fecha_eliminacion=data.get("fecha_eliminacion"),
            propietario=data.get("propietario"),
            permisos=data.get("permisos", {}),
        )

    def __repr__(self):
        estado = "Papelera" if self.en_papelera else "Activo"
        return f"<ArchivoFAT('{self.nombre_archivo}', {self.cantidad_caracteres} chars, {estado})>"
