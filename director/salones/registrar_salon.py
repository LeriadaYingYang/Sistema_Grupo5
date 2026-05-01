from basedatos_json import leer_json, guardar_json, generar_id

RUTA_CARRERAS = "datos/carreras.json"
RUTA_SALONES = "datos/salones.json"


def mostrar_carreras(carreras):#Muestra solo las carreras activas disponibles.

    print("\n=== CARRERAS DISPONIBLES ===")

    if len(carreras) == 0:
        print("No hay carreras registradas.")
        input()
        return

    for carrera in carreras:
        if carrera["estado"] == "Activo":
            print(f"ID: {carrera['id_carrera']} | Carrera: {carrera['nombre']}")


def buscar_carrera_por_id(carreras, id_carrera):#Busca una carrera por su ID.

    for carrera in carreras:
        if carrera["id_carrera"] == id_carrera and carrera["estado"] == "Activo":
            return carrera

    return None


def registrar_salon():# Registra un salón y lo asigna a una carrera existente.

    print("\n====================================")
    print("   REGISTRAR SALÓN Y ASIGNAR CARRERA")
    print("====================================")

    carreras = leer_json(RUTA_CARRERAS)

    if len(carreras) == 0:
        print("Primero debe registrar una carrera.")
        input()
        return

    mostrar_carreras(carreras)

    try:
        id_carrera = int(input("\nIngrese el ID de la carrera: "))
    except ValueError:
        print("Error: debe ingresar un número.")
        input()
        return

    carrera_encontrada = buscar_carrera_por_id(carreras, id_carrera)

    if carrera_encontrada is None:
        print("No existe una carrera activa con ese ID.")
        input()
        return

    salones = leer_json(RUTA_SALONES)

    nombre_salon = input("Nombre del salón: ")
    turno = input("Turno del salón: ")

    nuevo_salon = {
        "id_salon": generar_id(salones, "id_salon"),
        "nombre_salon": nombre_salon,
        "turno": turno,
        "id_carrera": carrera_encontrada["id_carrera"],
        "nombre_carrera": carrera_encontrada["nombre"],
        "estado": "Activo"
    }

    salones.append(nuevo_salon)
    guardar_json(RUTA_SALONES, salones)

    print("\nSalón registrado correctamente.")
    print(f"ID salón generado: {nuevo_salon['id_salon']}")
    print(f"Carrera asignada: {nuevo_salon['nombre_carrera']}")
    input()