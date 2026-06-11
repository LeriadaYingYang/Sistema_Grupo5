import json
import os


def leer_json(ruta_archivo): # Lee un archivo JSON y devuelve su contenido como una lista de diccionarios
    try:
        if not os.path.exists(ruta_archivo):
            return []
        with open(ruta_archivo,"r",encoding="utf-8") as archivo:
            return json.load(archivo)
    except json.JSONDecodeError:
        print(
            f"Error: el archivo "
            f"{ruta_archivo} está dañado.")
        return []
    except Exception as error:
        print(
            f"Error al leer "
            f"{ruta_archivo}: {error}")
        return []


def guardar_json(ruta_archivo, datos): # Guarda una lista de diccionarios en un archivo JSON
    try:
        with open(ruta_archivo,"w",encoding="utf-8") as archivo:
            json.dump(datos,archivo,indent=4,ensure_ascii=False)
    except Exception as error:
        print(
            f"Error al guardar "
            f"{ruta_archivo}: {error}")

def generar_id(lista, nombre_id): # Genera un nuevo ID único basado en el campo especificado en la lista de diccionarios
    ids = [item[nombre_id] for item in lista
        if nombre_id in item]
    if not ids:
        return 1
    return max(ids) + 1