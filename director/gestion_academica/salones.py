from basedatos_json import leer_json, guardar_json, generar_id
from director.utilidades import imprimir_titulo

RUTA_CARRERAS = "datos/carreras.json"
RUTA_SALONES = "datos/salones.json"
RUTA_PLANTILLAS = "datos/plantillas_academicas.json"

def buscar_por_id(lista, campo_id, valor_id):  #busca un registro activo por su id
    for item in lista:
        if item[campo_id] == valor_id and item["estado"] == "Activo":
            return item
    return None

def registrar_salon():  #registra un nuevo salón relacionado a una carrera
    imprimir_titulo("REGISTRAR SALON")

    carreras = leer_json(RUTA_CARRERAS)
    salones = leer_json(RUTA_SALONES)

    if len(carreras) == 0:
        print("Primero debe registrar carreras.")
        input()
        return

    mostrar_carreras()

    try:
        id_carrera = int(input("\nIngrese ID de carrera: "))
    except ValueError:
        print("Ingrese un número válido.")
        input()
        return

    carrera = buscar_por_id(carreras, "id_carrera", id_carrera)

    if carrera is None:
        print("Carrera no encontrada.")
        input()
        return

    nombre_salon = input("Nombre del salón: ")
    turno = input("Turno: ")

    nuevo_salon = {
        "id_salon": generar_id(salones, "id_salon"),
        "nombre_salon": nombre_salon,
        "turno": turno,
        "id_carrera": carrera["id_carrera"],
        "nombre_carrera": carrera["nombre"],
        "id_plantilla": None,
        "nombre_plantilla": "",
        "estado": "Activo"
    }

    salones.append(nuevo_salon)
    guardar_json(RUTA_SALONES, salones)

    print("\nSalón registrado correctamente.")
    print(f"ID generado: {nuevo_salon['id_salon']}")
    input()

def editar_salon():  #edita los datos de un salón
    imprimir_titulo("EDITAR SALON")

    salones = leer_json(RUTA_SALONES)

    if len(salones) == 0:
        print("No hay salones registrados.")
        input()
        return

    mostrar_salones()

    try:
        id_salon = int(input("\nIngrese ID del salón: "))
    except ValueError:
        print("Ingrese un número válido.")
        input()
        return

    for salon in salones:
        if salon["id_salon"] == id_salon and salon["estado"] == "Activo":
            nuevo_nombre = input(f"Nombre ({salon['nombre_salon']}): ").strip()
            nuevo_turno = input(f"Turno ({salon['turno']}): ").strip()

            if nuevo_nombre:
                salon["nombre_salon"] = nuevo_nombre

            if nuevo_turno:
                salon["turno"] = nuevo_turno

            guardar_json(RUTA_SALONES, salones)

            print("\nSalón actualizado correctamente.")
            input()
            return

    print("Salón no encontrado.")
    input()

def asignar_plantilla_salon():  #asigna una plantilla académica a un salón
    imprimir_titulo("ASIGNAR PLANTILLA AL SALON")

    salones = leer_json(RUTA_SALONES)
    plantillas = leer_json(RUTA_PLANTILLAS)

    if len(salones) == 0:
        print("No hay salones registrados.")
        input()
        return

    if len(plantillas) == 0:
        print("No hay plantillas registradas.")
        input()
        return

    mostrar_salones()

    try:
        id_salon = int(input("\nIngrese ID del salón: "))
    except ValueError:
        print("Ingrese un número válido.")
        input()
        return

    salon = buscar_por_id(salones, "id_salon", id_salon)

    if salon is None:
        print("Salón no encontrado.")
        input()
        return

    mostrar_plantillas_por_carrera(salon["id_carrera"])

    try:
        id_plantilla = int(input("\nIngrese ID de la plantilla: "))
    except ValueError:
        print("Ingrese un número válido.")
        input()
        return

    plantilla = buscar_por_id(plantillas, "id_plantilla", id_plantilla)

    if plantilla is None or plantilla["id_carrera"] != salon["id_carrera"]:
        print("Plantilla no válida para la carrera del salón.")
        input()
        return

    salon["id_plantilla"] = plantilla["id_plantilla"]
    salon["nombre_plantilla"] = plantilla["nombre_plantilla"]

    guardar_json(RUTA_SALONES, salones)

    print("\nPlantilla asignada correctamente al salón.")
    input()

def ver_salones():  #muestra los salones registrados
    imprimir_titulo("LISTA DE SALONES")

    salones = leer_json(RUTA_SALONES)

    if len(salones) == 0:
        print("No hay salones registrados.")
        input()
        return

    encontrados = 0

    for salon in salones:
        if salon["estado"] == "Activo":
            encontrados += 1

            print("\n-----------------------------")
            print(f"ID: {salon['id_salon']}")
            print(f"Salón: {salon['nombre_salon']}")
            print(f"Turno: {salon['turno']}")
            print(f"Carrera: {salon['nombre_carrera']}")
            print(f"Plantilla: {salon.get('nombre_plantilla', '')}")

    if encontrados == 0:
        print("No hay salones activos.")

    input()

def cerrar_salon():  #cierra un salón activo
    imprimir_titulo("CERRAR SALON")

    salones = leer_json(RUTA_SALONES)

    if len(salones) == 0:
        print("No hay salones registrados.")
        input()
        return

    mostrar_salones()

    try:
        id_salon = int(input("\nIngrese ID del salón: "))
    except ValueError:
        print("Ingrese un número válido.")
        input()
        return

    for salon in salones:
        if salon["id_salon"] == id_salon and salon["estado"] == "Activo":
            salon["estado"] = "Cerrado"

            guardar_json(RUTA_SALONES, salones)

            print("\nSalón cerrado correctamente.")
            input()
            return

    print("Salón no encontrado.")
    input()

def mostrar_carreras():  #muestra las carreras activas para seleccionar
    carreras = leer_json(RUTA_CARRERAS)

    imprimir_titulo("CARRERAS DISPONIBLES")

    for carrera in carreras:
        if carrera["estado"] == "Activo":
            print(f"ID: {carrera['id_carrera']} | {carrera['nombre']}")

def mostrar_salones():  #muestra los salones activos para seleccionar
    salones = leer_json(RUTA_SALONES)

    imprimir_titulo("SALONES DISPONIBLES")

    for salon in salones:
        if salon["estado"] == "Activo":
            print(
                f"ID: {salon['id_salon']} | "
                f"Salón: {salon['nombre_salon']} | "
                f"Carrera: {salon['nombre_carrera']}")

def mostrar_plantillas_por_carrera(id_carrera):  #muestra las plantillas de una carrera
    plantillas = leer_json(RUTA_PLANTILLAS)

    imprimir_titulo("PLANTILLAS DISPONIBLES")

    encontrados = 0

    for plantilla in plantillas:
        if plantilla["estado"] == "Activo" and plantilla["id_carrera"] == id_carrera:
            encontrados += 1
            print(
                f"ID: {plantilla['id_plantilla']} | "
                f"Plantilla: {plantilla['nombre_plantilla']}")

    if encontrados == 0:
        print("No hay plantillas para la carrera del salón.")