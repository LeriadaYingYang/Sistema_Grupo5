import json
import os


def leer_json(ruta_archivo):# Si el archivo no existe devuelve lista vacía

    if not os.path.exists(ruta_archivo):
        return []

    with open(ruta_archivo, "r", encoding="utf-8") as archivo:
        return json.load(archivo)


def guardar_json(ruta_archivo, datos):#guarda datos dentro de un archivo JSON.

    with open(ruta_archivo, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, indent=4, ensure_ascii=False)


def generar_id(lista, nombre_id):#genera un ID automático según el último registro guardado.

    if len(lista) == 0:
        return 1

    return lista[-1][nombre_id] + 1