from basedatos_json import leer_json, guardar_json, generar_id

RUTA_CARRERAS = "datos/carreras.json"
RUTA_PLANTILLAS = "datos/plantillas_academicas.json"


def mostrar_carreras(carreras):#Muestra las carreras activas disponibles.

    print("\n=== CARRERAS DISPONIBLES ===")

    for carrera in carreras:
        if carrera["estado"] == "Activo":
            print(f"ID: {carrera['id_carrera']} | Carrera: {carrera['nombre']}")


def buscar_carrera_por_id(carreras, id_carrera):#Busca una carrera activa por su ID.

    for carrera in carreras:
        if carrera["id_carrera"] == id_carrera and carrera["estado"] == "Activo":
            return carrera

    return None


def crear_plantilla():#Crea una plantilla académica y la relaciona con una carrera.

    print("\n====================================")
    print("   CREAR PLANTILLA ACADÉMICA")
    print("====================================")

    carreras = leer_json(RUTA_CARRERAS)

    if len(carreras) == 0:
        print("Primero debe registrar una carrera.")
        return

    mostrar_carreras(carreras)

    try:
        id_carrera = int(input("\nIngrese el ID de la carrera: "))
    except ValueError:
        print("Error: debe ingresar un número.")
        return

    carrera = buscar_carrera_por_id(carreras, id_carrera)

    if carrera is None:
        print("No existe una carrera activa con ese ID.")
        return

    plantillas = leer_json(RUTA_PLANTILLAS)

    nombre_plantilla = input("Nombre de la plantilla académica: ")
    descripcion = input("Descripción de la plantilla: ")

    nueva_plantilla = {
        "id_plantilla": generar_id(plantillas, "id_plantilla"),
        "id_carrera": carrera["id_carrera"],
        "nombre_carrera": carrera["nombre"],
        "nombre_plantilla": nombre_plantilla,
        "descripcion": descripcion,
        "estado": "Activo"
    }

    plantillas.append(nueva_plantilla)
    guardar_json(RUTA_PLANTILLAS, plantillas)

    print("\nPlantilla académica creada correctamente.")
    print(f"ID plantilla generado: {nueva_plantilla['id_plantilla']}")
    print(f"Carrera asignada: {nueva_plantilla['nombre_carrera']}")