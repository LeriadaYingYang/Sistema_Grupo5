from basedatos_json import leer_json, guardar_json, generar_id
from director.utilidades import imprimir_titulo

RUTA_CARRERAS = "datos/carreras.json"
RUTA_SALONES = "datos/salones.json"

def buscar_por_id(lista, campo_id, valor_id):  #busca un registro activo por su id
    for item in lista:
        if item[campo_id] == valor_id and item["estado"] == "Activo":
            return item
    return None

def registrar_salon():  #registra un nuevo salón relacionado a una carrera
    imprimir_titulo("REGISTRAR SALON")
    carreras = leer_json(RUTA_CARRERAS)  #carga las carreras registradas
    salones = leer_json(RUTA_SALONES)  #carga los salones registrados
    if len(carreras) == 0:  #valida si existen carreras registradas
        print("Primero debe registrar carreras.")
        return

    imprimir_titulo("CARRERAS DISPONIBLES")
    for carrera in carreras:  #recorre la lista de carreras
        if carrera["estado"] == "Activo":  #muestra solo carreras activas
            print(f"ID: {carrera['id_carrera']} | {carrera['nombre']}")
    try:
        id_carrera = int(input("\nIngrese ID de carrera: "))  #solicita el id de la carrera
    except ValueError:
        print("Ingrese un número válido.")
        return

    carrera = buscar_por_id(carreras, "id_carrera", id_carrera)  #busca la carrera ingresada
    if carrera is None:  # valida si la carrera existe
        print("Carrera no encontrada.")
        return

    nombre_salon = input("Nombre del salón: ")  #solicita el nombre del salón
    turno = input("Turno: ")  #solicita el turno del salón
    nuevo_salon = {  #crea el diccionario con los datos del nuevo salón
        "id_salon": generar_id(salones, "id_salon"),
        "nombre_salon": nombre_salon,
        "turno": turno,
        "id_carrera": carrera["id_carrera"],
        "nombre_carrera": carrera["nombre"],
        "estado": "Activo"}
    salones.append(nuevo_salon)  #agrega el nuevo salón a la lista
    guardar_json(RUTA_SALONES, salones)  #guarda la lista actualizada en el archivo json
    print("\nSalón registrado correctamente.")

def ver_salones():  #muestra los salones registrados
    imprimir_titulo("LISTA DE SALONES")
    salones = leer_json(RUTA_SALONES)  #carga los salones registrados
    if len(salones) == 0:  #valida si no existen salones registrados
        print("No hay salones registrados.")
        return
    for salon in salones:  #recorre la lista de salones
        if salon["estado"] == "Activo":  #muestra solo salones activos
            print("\n-----------------------------")
            print(f"ID: {salon['id_salon']}")
            print(f"Salón: {salon['nombre_salon']}")
            print(f"Turno: {salon['turno']}")
            print(f"Carrera: {salon['nombre_carrera']}")
    input()  #pausa la pantalla antes de volver al menú