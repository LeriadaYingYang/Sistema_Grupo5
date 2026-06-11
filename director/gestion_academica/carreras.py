from basedatos_json import leer_json, guardar_json, generar_id
from director.utilidades import imprimir_titulo
RUTA_CARRERAS = "datos/carreras.json"

def registrar_carrera():  #registra una nueva carrera académica
    imprimir_titulo("REGISTRAR CARRERA")
    carreras = leer_json(RUTA_CARRERAS)  #carga la lista de carreras
    nombre = input("Nombre de la carrera: ")
    descripcion = input("Descripción: ")
    while True:  #valida la duración
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

def editar_carrera():  #edita una carrera existente
    imprimir_titulo("EDITAR CARRERA")

    carreras = leer_json(RUTA_CARRERAS)

    if len(carreras) == 0:
        print("No hay carreras registradas.")
        input()
        return

    ver_carreras_sin_pausa()

    try:
        id_carrera = int(input("\nIngrese ID de la carrera: "))
    except ValueError:
        print("ID inválido.")
        input()
        return

    for carrera in carreras:
        if carrera["id_carrera"] == id_carrera and carrera["estado"] == "Activo":

            nuevo_nombre = input(
                f"Nombre ({carrera['nombre']}): ").strip()
            nueva_descripcion = input(
                f"Descripción ({carrera['descripcion']}): ").strip()
            nueva_duracion = input(
                f"Duración ({carrera['duracion_meses']}): ").strip()
            if nuevo_nombre:
                carrera["nombre"] = nuevo_nombre
            if nueva_descripcion:
                carrera["descripcion"] = nueva_descripcion
            if nueva_duracion:
                try:
                    carrera["duracion_meses"] = int(nueva_duracion)
                except ValueError:
                    print("Duración inválida.")

            guardar_json(RUTA_CARRERAS, carreras)
            print("\nCarrera actualizada correctamente.")
            input()
            return
    print("Carrera no encontrada.")
    input()

def buscar_carrera():  #busca una carrera por nombre
    imprimir_titulo("BUSCAR CARRERA")
    carreras = leer_json(RUTA_CARRERAS)
    if len(carreras) == 0:
        print("No hay carreras registradas.")
        input()
        return
    texto = input("Ingrese nombre de la carrera: ").lower()
    encontrados = 0
    for carrera in carreras:
        if (carrera["estado"] == "Activo"
                and texto in carrera["nombre"].lower()):
            encontrados += 1
            print("\n-----------------------------")
            print(f"ID: {carrera['id_carrera']}")
            print(f"Nombre: {carrera['nombre']}")
            print(f"Descripción: {carrera['descripcion']}")
            print(f"Duración: {carrera['duracion_meses']} meses")
    if encontrados == 0:
        print("No se encontraron resultados.")
    input()

def ver_carreras():  #muestra las carreras registradas
    imprimir_titulo("LISTA DE CARRERAS")

    carreras = leer_json(RUTA_CARRERAS)

    if len(carreras) == 0:
        print("No hay carreras registradas.")
        input()
        return

    for carrera in carreras:
        if carrera["estado"] == "Activo":
            print("\n-----------------------------")
            print(f"ID: {carrera['id_carrera']}")
            print(f"Nombre: {carrera['nombre']}")
            print(f"Descripción: {carrera['descripcion']}")
            print(f"Duración: {carrera['duracion_meses']} meses")
    input()

def desactivar_carrera():  #desactiva una carrera
    imprimir_titulo("DESACTIVAR CARRERA")

    carreras = leer_json(RUTA_CARRERAS)

    if len(carreras) == 0:
        print("No hay carreras registradas.")
        input()
        return

    ver_carreras_sin_pausa()

    try:
        id_carrera = int(input("\nIngrese ID de la carrera: "))
    except ValueError:
        print("ID inválido.")
        input()
        return

    for carrera in carreras:
        if carrera["id_carrera"] == id_carrera:
            carrera["estado"] = "Inactivo"

            guardar_json(RUTA_CARRERAS, carreras)

            print("\nCarrera desactivada correctamente.")
            input()
            return
    print("Carrera no encontrada.")
    input()

def ver_carreras_sin_pausa():  #muestra carreras para selección
    carreras = leer_json(RUTA_CARRERAS)
    for carrera in carreras:
        if carrera["estado"] == "Activo":
            print(
                f"ID: {carrera['id_carrera']} | "
                f"{carrera['nombre']}")