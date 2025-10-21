import json
import os


class Serializador:
    def guardar_json(self, ruta, datos):
        directorio = os.path.dirname(ruta)
        if directorio and not os.path.exists(directorio):
            os.makedirs(directorio)

        with open(ruta, "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, indent=2, ensure_ascii=False)

    def cargar_json(self, ruta):
        if not os.path.exists(ruta):
            return None

        with open(ruta, "r", encoding="utf-8") as archivo:
            return json.load(archivo)

    def objeto_a_dict(self, objeto):
        if hasattr(objeto, "to_dict"):
            return objeto.to_dict()
        return objeto

    def lista_objetos_a_dicts(self, objetos):
        return [self.objeto_a_dict(obj) for obj in objetos]
