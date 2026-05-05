from basedatos_json import leer_json, guardar_json, generar_id

RUTA_CARRERAS = "datos/carreras.json"
RUTA_PLANTILLAS = "datos/plantillas_academicas.json"


def buscar_por_id(lista, campo_id, valor_id):
    for item in lista:
        if item[campo_id] == valor_id and item["estado"] == "Activo":
            return item
    return None

def crear_plantilla():
    print("\n=== CREAR PLANTILLA ACADÉMICA ===")

    carreras = leer_json(RUTA_CARRERAS)
    plantillas = leer_json(RUTA_PLANTILLAS)

    if len(carreras) == 0:
        print("Primero debe registrar carreras.")
        return

    print("\n=== CARRERAS DISPONIBLES ===")
    for carrera in carreras:
        if carrera["estado"] == "Activo":
            print(f"ID: {carrera['id_carrera']} | {carrera['nombre']}")

    try:
        id_carrera = int(input("\nIngrese ID de la carrera: "))
    except ValueError:
        print("Debe ingresar un número.")
        return

    carrera = buscar_por_id(carreras, "id_carrera", id_carrera)

    if carrera is None:
        print("Carrera no encontrada.")
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

def ver_plantillas():
    print("\n=== LISTA DE PLANTILLAS ===")

    plantillas = leer_json(RUTA_PLANTILLAS)

    if len(plantillas) == 0:
        print("No hay plantillas registradas.")
        return

    for p in plantillas:
        if p["estado"] == "Activo":
            print("\n-----------------------------")
            print(f"ID: {p['id_plantilla']}")
            print(f"Carrera: {p['nombre_carrera']}")
            print(f"Plantilla: {p['nombre_plantilla']}")
            print(f"Descripción: {p['descripcion']}")