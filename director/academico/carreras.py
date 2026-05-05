from basedatos_json import leer_json, guardar_json, generar_id

RUTA_CARRERAS = "datos/carreras.json"


def registrar_carrera():
    print("\n=== REGISTRAR CARRERA ===")
    carreras = leer_json(RUTA_CARRERAS)
    nombre = input("Nombre de la carrera: ")
    descripcion = input("Descripción: ")

    while True:
        try:
            duracion = int(input("Duración en meses: "))
            break
        except ValueError:
            print("Ingrese un número válido.")

    nueva_carrera = {
        "id_carrera": generar_id(carreras, "id_carrera"),
        "nombre": nombre,
        "descripcion": descripcion,
        "duracion_meses": duracion,
        "estado": "Activo"}

    carreras.append(nueva_carrera)
    guardar_json(RUTA_CARRERAS, carreras)

    print("\nCarrera registrada correctamente.")
    print(f"ID generado: {nueva_carrera['id_carrera']}")
    input()

def ver_carreras():
    print("\n=== LISTA DE CARRERAS ===")

    carreras = leer_json(RUTA_CARRERAS)

    if len(carreras) == 0:
        print("No hay carreras registradas.")
        return

    for carrera in carreras:
        if carrera["estado"] == "Activo":
            print("\n-----------------------------")
            print(f"ID: {carrera['id_carrera']}")
            print(f"Nombre: {carrera['nombre']}")
            print(f"Descripción: {carrera['descripcion']}")
            print(f"Duración: {carrera['duracion_meses']} meses")
    input()