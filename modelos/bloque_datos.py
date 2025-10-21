class BloqueDatos:
    def __init__(self, datos="", siguiente_archivo=None, eof=False):
        self.datos = datos
        self.siguiente_archivo = siguiente_archivo
        self.eof = eof

    def to_dict(self):
        return {
            "datos": self.datos,
            "siguiente_bloque": self.siguiente_bloque,
            "eof": self.eof,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            datos=data.get("datos", ""),
            siguiente_bloque=data.get("siguiente_bloque"),
            eof=data.get("efo", False),
        )

    def __repr__(self):
        preview = self.datos[:20] + "..." if len(self.datos) > 20 else self.datos
        return f"<BloqueDatos(datos='{preview}', siguiente={self.siguiente_bloque}, eof={self.eof})>"
