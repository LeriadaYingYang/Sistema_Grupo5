from basedatos_json import leer_json, guardar_json, generar_id

RUTA_CARRERAS = "datos/carreras.json"
RUTA_PLANTILLAS = "datos/plantillas_academicas.json"

def buscar_por_id(lista, campo_id, valor_id):  #busca un registro activo por su id
    for item in lista:
        if item[campo_id] == valor_id and item["estado"] == "Activo":
            return item
    return None

def crear_plantilla():  #crea una nueva plantilla académica para una carrera
    print("\n--- CREAR PLANTILLA ACADÉMICA ---")
    carreras = leer_json(RUTA_CARRERAS)  #carga las carreras registradas
    plantillas = leer_json(RUTA_PLANTILLAS)  #carga las plantillas registradas
    if len(carreras) == 0:  #valida si existen carreras registradas
        print("Primero debe registrar carreras.")
        return
    print("\n--- CARRERAS DISPONIBLES ---")
    for carrera in carreras:  #recorre la lista de carreras
        if carrera["estado"] == "Activo":  #muestra solo carreras activas
            print(f"ID: {carrera['id_carrera']} | {carrera['nombre']}")
    try:
        id_carrera = int(input("\nIngrese ID de la carrera: "))  #solicita el id de la carrera
    except ValueError:
        print("Debe ingresar un número.")
        return
    carrera = buscar_por_id(carreras, "id_carrera", id_carrera)  #busca la carrera ingresada
    if carrera is None:  # valida si la carrera existe
        print("Carrera no encontrada.")
        return
    nombre = input("Nombre de la plantilla: ")  #solicita el nombre de la plantilla
    descripcion = input("Descripción: ")  #solicita la descripción de la plantilla
    nueva_plantilla = {  #crea el diccionario con los datos de la nueva plantilla
        "id_plantilla": generar_id(plantillas, "id_plantilla"),
        "id_carrera": carrera["id_carrera"],
        "nombre_carrera": carrera["nombre"],
        "nombre_plantilla": nombre,
        "descripcion": descripcion,
        "estado": "Activo"}
    plantillas.append(nueva_plantilla)  #agrega la nueva plantilla a la lista
    guardar_json(RUTA_PLANTILLAS, plantillas)  #guarda la lista actualizada en el archivo json
    print("\nPlantilla creada correctamente.")
    print(f"ID generado: {nueva_plantilla['id_plantilla']}")

def ver_plantillas():  #muestra las plantillas académicas registradas
    print("\n--- LISTA DE PLANTILLAS ---")
    plantillas = leer_json(RUTA_PLANTILLAS)  #carga las plantillas registradas
    if len(plantillas) == 0:  #valida si no existen plantillas registradas
        print("No hay plantillas registradas.")
        return
    for p in plantillas:  #recorre la lista de plantillas
        if p["estado"] == "Activo":  #muestra solo plantillas activas
            print("\n-----------------------------")
            print(f"ID: {p['id_plantilla']}")
            print(f"Carrera: {p['nombre_carrera']}")
            print(f"Plantilla: {p['nombre_plantilla']}")
            print(f"Descripción: {p['descripcion']}")
    input()  #pausa la pantalla antes de volver al menú