from basedatos_json import leer_json, guardar_json, generar_id
from director.utilidades import imprimir_titulo
RUTA_CARRERAS = "datos/carreras.json"

def registrar_carrera():  #registra una nueva carrera académica
    print("\n--- REGISTRAR CARRERA ---")
    carreras = leer_json(RUTA_CARRERAS)  #carga la lista de carreras desde el archivo json
    nombre = input("Nombre de la carrera: ")  #solicita el nombre de la carrera
    descripcion = input("Descripción: ")  #solicita la descripción de la carrera
    while True:  #valida que la duración sea un número entero
        try:
            duracion = int(input("Duración en meses: "))
            break
        except ValueError:
            print("Ingrese un número válido.")
    nueva_carrera = {  #crea el diccionario con los datos de la nueva carrera
        "id_carrera": generar_id(carreras, "id_carrera"),
        "nombre": nombre,
        "descripcion": descripcion,
        "duracion_meses": duracion,
        "estado": "Activo"}
    carreras.append(nueva_carrera)  #agrega la nueva carrera a la lista
    guardar_json(RUTA_CARRERAS, carreras)  #guarda la lista actualizada en el archivo json
    print("\nCarrera registrada correctamente.")
    print(f"ID generado: {nueva_carrera['id_carrera']}")
    input()  #pausa la pantalla antes de volver al menú

def ver_carreras():  #muestra las carreras registradas
    print("\n--- LISTA DE CARRERAS ---")
    carreras = leer_json(RUTA_CARRERAS)  #carga la lista de carreras desde el archivo json
    if len(carreras) == 0:  #valida si no existen carreras registradas
        print("No hay carreras registradas.")
        input()
        return
    for carrera in carreras:  #recorre la lista de carreras
        if carrera["estado"] == "Activo":  #muestra solo carreras activas
            print("\n-----------------------------")
            print(f"ID: {carrera['id_carrera']}")
            print(f"Nombre: {carrera['nombre']}")
            print(f"Descripción: {carrera['descripcion']}")
            print(f"Duración: {carrera['duracion_meses']} meses")
    input()  #pausa la pantalla antes de volver al menú