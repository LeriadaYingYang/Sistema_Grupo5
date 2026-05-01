from basedatos_json import leer_json, guardar_json, generar_id

RUTA_PLANTILLAS = "datos/plantillas_academicas.json"
RUTA_UNIDADES = "datos/unidades.json"


def mostrar_plantillas(plantillas):#Muestra las plantillas académicas activas.

    print("\n=== PLANTILLAS ACADÉMICAS DISPONIBLES ===")

    for plantilla in plantillas:
        if plantilla["estado"] == "Activo":
            print(
                f"ID: {plantilla['id_plantilla']} | "
                f"Carrera: {plantilla['nombre_carrera']} | "
                f"Plantilla: {plantilla['nombre_plantilla']}"
            )


def buscar_plantilla_por_id(plantillas, id_plantilla):#Busca una plantilla académica activa por su ID.

    for plantilla in plantillas:
        if plantilla["id_plantilla"] == id_plantilla and plantilla["estado"] == "Activo":
            return plantilla

    return None


def registrar_unidad():#Registra una unidad o módulo dentro de una plantilla académica.

    print("\n====================================")
    print("   REGISTRAR MÓDULO O UNIDAD")
    print("====================================")

    plantillas = leer_json(RUTA_PLANTILLAS)

    if len(plantillas) == 0:
        print("Primero debe crear una plantilla académica.")
        return

    mostrar_plantillas(plantillas)

    try:
        id_plantilla = int(input("\nIngrese el ID de la plantilla académica: "))
    except ValueError:
        print("Error: debe ingresar un número.")
        return

    plantilla = buscar_plantilla_por_id(plantillas, id_plantilla)

    if plantilla is None:
        print("No existe una plantilla activa con ese ID.")
        return

    unidades = leer_json(RUTA_UNIDADES)

    nombre_unidad = input("Nombre de la unidad o módulo: ")
    descripcion = input("Descripción: ")

    while True:
        try:
            orden = int(input("Orden de la unidad/módulo: "))
            break
        except ValueError:
            print("Error: ingrese un número válido.")

    nueva_unidad = {
        "id_unidad": generar_id(unidades, "id_unidad"),
        "id_plantilla": plantilla["id_plantilla"],
        "id_carrera": plantilla["id_carrera"],
        "nombre_carrera": plantilla["nombre_carrera"],
        "nombre_plantilla": plantilla["nombre_plantilla"],
        "nombre_unidad": nombre_unidad,
        "descripcion": descripcion,
        "orden": orden,
        "estado": "Activo"
    }

    unidades.append(nueva_unidad)
    guardar_json(RUTA_UNIDADES, unidades)

    print("\nUnidad o módulo registrado correctamente.")
    print(f"ID unidad generado: {nueva_unidad['id_unidad']}")
    print(f"Carrera: {nueva_unidad['nombre_carrera']}")
    print(f"Plantilla: {nueva_unidad['nombre_plantilla']}")