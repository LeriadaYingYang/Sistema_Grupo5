from basedatos_json import leer_json, guardar_json, generar_id

RUTA_CARRERAS = "datos/carreras.json"
RUTA_SALONES = "datos/salones.json"

def buscar_por_id(lista, campo_id, valor_id):
    for item in lista:
        if item[campo_id] == valor_id and item["estado"] == "Activo":
            return item
    return None

def registrar_salon():
    print("\n=== REGISTRAR SALÓN ===")

    carreras = leer_json(RUTA_CARRERAS)
    salones = leer_json(RUTA_SALONES)

    if len(carreras) == 0:
        print("Primero debe registrar carreras.")
        return

    print("\n=== CARRERAS DISPONIBLES ===")
    for carrera in carreras:
        if carrera["estado"] == "Activo":
            print(f"ID: {carrera['id_carrera']} | {carrera['nombre']}")

    try:
        id_carrera = int(input("\nIngrese ID de carrera: "))
    except ValueError:
        print("Ingrese un número válido.")
        return

    carrera = buscar_por_id(carreras, "id_carrera", id_carrera)

    if carrera is None:
        print("Carrera no encontrada.")
        return

    nombre_salon = input("Nombre del salón: ")
    turno = input("Turno: ")

    nuevo_salon = {
        "id_salon": generar_id(salones, "id_salon"),
        "nombre_salon": nombre_salon,
        "turno": turno,
        "id_carrera": carrera["id_carrera"],
        "nombre_carrera": carrera["nombre"],
        "estado": "Activo"}

    salones.append(nuevo_salon)
    guardar_json(RUTA_SALONES, salones)

    print("\nSalón registrado correctamente.")

def ver_salones():
    print("\n=== LISTA DE SALONES ===")

    salones = leer_json(RUTA_SALONES)

    if len(salones) == 0:
        print("No hay salones registrados.")
        return

    for salon in salones:
        if salon["estado"] == "Activo":
            print("\n-----------------------------")
            print(f"ID: {salon['id_salon']}")
            print(f"Salón: {salon['nombre_salon']}")
            print(f"Turno: {salon['turno']}")
            print(f"Carrera: {salon['nombre_carrera']}")