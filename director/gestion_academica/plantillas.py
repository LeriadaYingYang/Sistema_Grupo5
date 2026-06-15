from basedatos_json import leer_json, guardar_json, generar_id
from director.utilidades import imprimir_titulo

RUTA_CARRERAS = "datos/carreras.json"
RUTA_PLANTILLAS = "datos/plantillas_academicas.json"


def buscar_por_id(lista, campo_id, valor_id):  #busca un registro activo por su id
    for item in lista:
        if item[campo_id] == valor_id and item["estado"] == "Activo":
            return item
    return None

def crear_plantilla():  #crea una nueva plantilla académica para una carrera
    imprimir_titulo("CREAR PLANTILLA ACADÉMICA")

    carreras = leer_json(RUTA_CARRERAS)  #carga las carreras registradas
    plantillas = leer_json(RUTA_PLANTILLAS)  #carga las plantillas registradas

    if len(carreras) == 0:
        print("Primero debe registrar carreras.")
        input()
        return

    mostrar_carreras()

    try:
        id_carrera = int(input("\nIngrese ID de la carrera: "))
    except ValueError:
        print("Debe ingresar un número.")
        input()
        return

    carrera = buscar_por_id(carreras, "id_carrera", id_carrera)

    if carrera is None:
        print("Carrera no encontrada.")
        input()
        return

    nombre = input("Nombre de la plantilla: ")
    descripcion = input("Descripción: ")

    nueva_plantilla = {
        "id_plantilla": generar_id(plantillas, "id_plantilla"),
        "id_carrera": carrera["id_carrera"],
        "nombre_carrera": carrera["nombre"],
        "nombre_plantilla": nombre,
        "descripcion": descripcion,
        "estado": "Activo"}

    plantillas.append(nueva_plantilla)
    guardar_json(RUTA_PLANTILLAS, plantillas)

    print("\nPlantilla creada correctamente.")
    print(f"ID generado: {nueva_plantilla['id_plantilla']}")
    input()

def editar_plantilla():  #edita una plantilla académica
    imprimir_titulo("EDITAR PLANTILLA ACADÉMICA")

    plantillas = leer_json(RUTA_PLANTILLAS)

    if len(plantillas) == 0:
        print("No hay plantillas registradas.")
        input()
        return

    mostrar_plantillas()

    try:
        id_plantilla = int(input("\nIngrese ID de la plantilla: "))
    except ValueError:
        print("Debe ingresar un número.")
        input()
        return

    for plantilla in plantillas:
        if plantilla["id_plantilla"] == id_plantilla and plantilla["estado"] == "Activo":
            nuevo_nombre = input(f"Nombre ({plantilla['nombre_plantilla']}): ").strip()
            nueva_descripcion = input(f"Descripción ({plantilla['descripcion']}): ").strip()

            if nuevo_nombre:
                plantilla["nombre_plantilla"] = nuevo_nombre

            if nueva_descripcion:
                plantilla["descripcion"] = nueva_descripcion

            guardar_json(RUTA_PLANTILLAS, plantillas)

            print("\nPlantilla actualizada correctamente.")
            input()
            return

    print("Plantilla no encontrada.")
    input()

def asignar_carrera_plantilla():  #asigna o cambia la carrera de una plantilla
    imprimir_titulo("ASIGNAR CARRERA A PLANTILLA")

    carreras = leer_json(RUTA_CARRERAS)
    plantillas = leer_json(RUTA_PLANTILLAS)

    if len(carreras) == 0:
        print("No hay carreras registradas.")
        input()
        return

    if len(plantillas) == 0:
        print("No hay plantillas registradas.")
        input()
        return

    mostrar_plantillas()

    try:
        id_plantilla = int(input("\nIngrese ID de la plantilla: "))
    except ValueError:
        print("Debe ingresar un número.")
        input()
        return

    plantilla = buscar_por_id(plantillas, "id_plantilla", id_plantilla)

    if plantilla is None:
        print("Plantilla no encontrada.")
        input()
        return

    mostrar_carreras()

    try:
        id_carrera = int(input("\nIngrese ID de la nueva carrera: "))
    except ValueError:
        print("Debe ingresar un número.")
        input()
        return

    carrera = buscar_por_id(carreras, "id_carrera", id_carrera)

    if carrera is None:
        print("Carrera no encontrada.")
        input()
        return

    plantilla["id_carrera"] = carrera["id_carrera"]
    plantilla["nombre_carrera"] = carrera["nombre"]

    guardar_json(RUTA_PLANTILLAS, plantillas)

    print("\nCarrera asignada correctamente a la plantilla.")
    input()

def ver_plantillas():  #muestra las plantillas académicas registradas
    imprimir_titulo("LISTA DE PLANTILLAS")

    plantillas = leer_json(RUTA_PLANTILLAS)

    if len(plantillas) == 0:
        print("No hay plantillas registradas.")
        input()
        return

    for p in plantillas:
        if p["estado"] == "Activo":
            print("\n-----------------------------")
            print(f"ID: {p['id_plantilla']}")
            print(f"Carrera: {p['nombre_carrera']}")
            print(f"Plantilla: {p['nombre_plantilla']}")
            print(f"Descripción: {p['descripcion']}")

    input()

def desactivar_plantilla():  #desactiva una plantilla académica
    imprimir_titulo("DESACTIVAR PLANTILLA")

    plantillas = leer_json(RUTA_PLANTILLAS)

    if len(plantillas) == 0:
        print("No hay plantillas registradas.")
        input()
        return

    mostrar_plantillas()

    try:
        id_plantilla = int(input("\nIngrese ID de la plantilla: "))
    except ValueError:
        print("Debe ingresar un número.")
        input()
        return

    for plantilla in plantillas:
        if plantilla["id_plantilla"] == id_plantilla and plantilla["estado"] == "Activo":
            plantilla["estado"] = "Inactivo"

            guardar_json(RUTA_PLANTILLAS, plantillas)

            print("\nPlantilla desactivada correctamente.")
            input()
            return

    print("Plantilla no encontrada.")
    input()

def mostrar_carreras():  #muestra las carreras activas para seleccionar
    carreras = leer_json(RUTA_CARRERAS)

    imprimir_titulo("CARRERAS DISPONIBLES")

    for carrera in carreras:
        if carrera["estado"] == "Activo":
            print(f"ID: {carrera['id_carrera']} | {carrera['nombre']}")

def mostrar_plantillas():  #muestra las plantillas activas para seleccionar
    plantillas = leer_json(RUTA_PLANTILLAS)

    imprimir_titulo("PLANTILLAS DISPONIBLES")

    for plantilla in plantillas:
        if plantilla["estado"] == "Activo":
            print(
                f"ID: {plantilla['id_plantilla']} | "
                f"Plantilla: {plantilla['nombre_plantilla']} | "
                f"Carrera: {plantilla['nombre_carrera']}")