import os
import shutil
from datetime import datetime
from modelos import ArchivoFAT, BloqueDatos
from utilidades import Serializador


class GestorArchivos:
    TAMAÑO_BLOQUE = 20  # Carácteres por bloque

    def __init__(self, ruta_tabla_fat="tabla_fat.json", carpeta_datos="datos"):
        self.ruta_tabla_fat = ruta_tabla_fat
        self.carpeta_datos = carpeta_datos
        self.serializador = Serializador()

        # Crear carpeta de datos si no existe
        if not os.path.exists(self.carpeta_datos):
            os.makedirs(self.carpeta_datos)

    def cargar_tabla_fat(self):
        datos = self.serializador.cargar_json(self.ruta_tabla_fat)
        if datos is None:
            return []
        return [ArchivoFAT.from_dict(d) for d in datos]

    def guardar_tabla_fat(self, archivos):
        datos = self.serializador.lista_objetos_a_dicts(archivos)
        self.serializador.guardar_json(self.ruta_tabla_fat, datos)

    def crear_archivo(self, nombre_archivo, contenido, propietario):
        # Verificar que el archivo no exista
        archivos = self.cargar_tabla_fat()
        if any(
            a.nombre_archivo == nombre_archivo and not a.en_papelera for a in archivos
        ):
            return False, "Ya existe un archivo con ese nombre."

        # Crear carpeta para el archivo
        carpeta_archivo = os.path.join(self.carpeta_datos, nombre_archivo)
        if not os.path.exists(carpeta_archivo):
            os.makedirs(carpeta_archivo)

        # Dividir contenido en bloques de 20 caracteres
        bloques = []
        for i in range(0, len(contenido), self.TAMAÑO_BLOQUE):
            bloque_datos = contenido[i : i + self.TAMAÑO_BLOQUE]
            bloques.append(bloque_datos)

        # Si no hay contenido, crear al menos un bloque vacío
        if len(bloques) == 0:
            bloques.append("")

        # Crear archivos de bloques
        for idx, bloque_datos in enumerate(bloques):
            es_ultimo = idx == len(bloques) - 1
            siguiente_bloque = idx + 2 if not es_ultimo else None

            bloque = BloqueDatos(
                datos=bloque_datos, siguiente_bloque=siguiente_bloque, eof=es_ultimo
            )

            ruta_bloque = os.path.join(carpeta_archivo, f"bloque_{idx + 1}.json")
            self.serializador.guardar_json(ruta_bloque, bloque.to_dict())

        # Crear entrada en tabla FAT
        ruta_inicial = os.path.join(carpeta_archivo, "bloque_1.json")
        archivo_fat = ArchivoFAT(
            nombre_archivo=nombre_archivo,
            ruta_datos_inicial=ruta_inicial,
            cantidad_caracteres=len(contenido),
            propietario=propietario,
        )

        archivos.append(archivo_fat)
        self.guardar_tabla_fat(archivos)

        return True, f"Archivo '{nombre_archivo}' creado exitosamente."

    def listar_archivos(self, incluir_papelera=False):
        archivos = self.cargar_tabla_fat()

        if incluir_papelera:
            return archivos
        else:
            return [a for a in archivos if not a.en_papelera]

    def abrir_archivo(self, nombre_archivo):
        archivos = self.cargar_tabla_fat()
        archivo_fat = None

        for a in archivos:
            if a.nombre_archivo == nombre_archivo and not a.en_papelera:
                archivo_fat = a
                break

        if archivo_fat is None:
            return None, None

        # Leer todos los bloques siguiendo la cadena
        contenido_completo = ""
        ruta_bloque_actual = archivo_fat.ruta_datos_inicial

        while ruta_bloque_actual:
            datos_bloque = self.serializador.cargar_json(ruta_bloque_actual)
            if datos_bloque is None:
                break

            bloque = BloqueDatos.from_dict(datos_bloque)
            contenido_completo += bloque.datos

            # Si es el final del archivo, terminar
            if bloque.eof:
                break

            # Obtener ruta del siguiente bloque
            if bloque.siguiente_bloque:
                carpeta_archivo = os.path.dirname(ruta_bloque_actual)
                ruta_bloque_actual = os.path.join(
                    carpeta_archivo, f"bloque_{bloque.siguiente_bloque}.json"
                )
            else:
                break

        return archivo_fat, contenido_completo

    def modificar_archivo(self, nombre_archivo, nuevo_contenido):
        archivos = self.cargar_tabla_fat()
        archivo_fat = None
        idx_archivo = -1

        for idx, a in enumerate(archivos):
            if a.nombre_archivo == nombre_archivo and not a.en_papelera:
                archivo_fat = a
                idx_archivo = idx
                break

        if archivo_fat is None:
            return False, "Archivo no encontrado."

        # Eliminar carpeta de bloques antiguos
        carpeta_archivo = os.path.dirname(archivo_fat.ruta_datos_inicial)
        if os.path.exists(carpeta_archivo):
            shutil.rmtree(carpeta_archivo)

        # Crear carpeta nuevamente
        os.makedirs(carpeta_archivo)

        # Crear nuevos bloques con el nuevo contenido
        bloques = []
        for i in range(0, len(nuevo_contenido), self.TAMAÑO_BLOQUE):
            bloque_datos = nuevo_contenido[i : i + self.TAMAÑO_BLOQUE]
            bloques.append(bloque_datos)

        if len(bloques) == 0:
            bloques.append("")

        # Guardar nuevos bloques
        for idx, bloque_datos in enumerate(bloques):
            es_ultimo = idx == len(bloques) - 1
            siguiente_bloque = idx + 2 if not es_ultimo else None

            bloque = BloqueDatos(
                datos=bloque_datos, siguiente_bloque=siguiente_bloque, eof=es_ultimo
            )

            ruta_bloque = os.path.join(carpeta_archivo, f"bloque_{idx + 1}.json")
            self.serializador.guardar_json(ruta_bloque, bloque.to_dict())

        # Actualizar metadatos en tabla FAT
        archivo_fat.cantidad_caracteres = len(nuevo_contenido)
        archivo_fat.fecha_modificacion = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

        archivos[idx_archivo] = archivo_fat
        self.guardar_tabla_fat(archivos)

        return True, f"Archivo '{nombre_archivo}' modificado exitosamente."

    def eliminar_archivo(self, nombre_archivo):
        archivos = self.cargar_tabla_fat()
        archivo_fat = None

        for a in archivos:
            if a.nombre_archivo == nombre_archivo and not a.en_papelera:
                archivo_fat = a
                break

        if archivo_fat is None:
            return False, "Archivo no encontrado."

        # Marcar como "en papelera"
        archivo_fat.en_papelera = True
        archivo_fat.fecha_eliminacion = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

        self.guardar_tabla_fat(archivos)

        return True, f"Archivo '{nombre_archivo}' movido a papelera."

    def recuperar_archivo(self, nombre_archivo):
        archivos = self.cargar_tabla_fat()
        archivo_fat = None

        for a in archivos:
            if a.nombre_archivo == nombre_archivo and a.en_papelera:
                archivo_fat = a
                break

        if archivo_fat is None:
            return False, "Archivo no encontrado en papelera."

        # Restaurar desde papelera
        archivo_fat.en_papelera = False
        archivo_fat.fecha_eliminacion = None

        self.guardar_tabla_fat(archivos)

        return True, f"Archivo '{nombre_archivo}' recuperado exitosamente."

    def eliminar_permanente(self, nombre_archivo):
        archivos = self.cargar_tabla_fat()
        archivo_fat = None
        idx_archivo = -1

        for idx, a in enumerate(archivos):
            if a.nombre_archivo == nombre_archivo and a.en_papelera:
                archivo_fat = a
                idx_archivo = idx
                break

        if archivo_fat is None:
            return False, "Archivo no encontrado en papelera."

        # Eliminar carpeta de bloques físicamente
        carpeta_archivo = os.path.dirname(archivo_fat.ruta_datos_inicial)
        if os.path.exists(carpeta_archivo):
            shutil.rmtree(carpeta_archivo)

        # Quitar entrada de tabla FAT
        archivos.pop(idx_archivo)
        self.guardar_tabla_fat(archivos)

        return True, f"Archivo '{nombre_archivo}' eliminado permanentemente."

    def obtener_archivo_por_nombre(self, nombre_archivo, incluir_papelera=False):
        archivos = self.cargar_tabla_fat()

        for a in archivos:
            if a.nombre_archivo == nombre_archivo:
                if incluir_papelera or not a.en_papelera:
                    return a

        return None
