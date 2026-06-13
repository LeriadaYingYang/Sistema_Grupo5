import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


def resolver_ruta(ruta_archivo):
    ruta = Path(ruta_archivo)
    if ruta.is_absolute():
        return ruta
    return BASE_DIR / ruta


def leer_json(ruta_archivo):#si el archivo no existe devuelve lista vacia

    ruta = resolver_ruta(ruta_archivo)
    if not ruta.exists():
        return []

    with open(ruta, "r", encoding="utf-8") as archivo:
        return json.load(archivo)


def guardar_json(ruta_archivo, datos):#guarda datos dentro de un archivo JSON.

    ruta = resolver_ruta(ruta_archivo)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    with open(ruta, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, indent=4, ensure_ascii=False)


def generar_id(lista, nombre_id):#genera un ID automático según el último registro guardado.

    if len(lista) == 0:
        return 1

    return lista[-1][nombre_id] + 1