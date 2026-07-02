from database.basedatos import leer_json, guardar_json, generar_id
from director.utilidades import imprimir_titulo

RUTA_CARRERAS = "datos/carreras.json"

def leer_texto(mensaje):  #valida que el texto no esté vacío
    while True:
        texto = input(mensaje).strip()
        if texto != "":
            return texto
        print("Este campo no puede estar vacío.")

def leer_entero(mensaje):  #valida que el dato ingresado sea numérico
    while True:
        try:
            return int(input(mensaje))
        except ValueError:
            print("Debe ingresar un número.")

def leer_entero_positivo(mensaje):  #valida que el número sea mayor que cero
    while True:
        numero = leer_entero(mensaje)
        if numero > 0:
            return numero
        print("El número debe ser mayor que 0.")

def buscar_carrera_por_id(carreras, id_carrera):  #busca una carrera activa por id
    for carrera in carreras:
        if carrera["id_carrera"] == id_carrera and carrera["estado"] == "Activo":
            return carrera
    return None

def buscar_carrera_oculta_por_id(carreras, id_carrera):  #busca una carrera oculta por id
    for carrera in carreras:
        if carrera["id_carrera"] == id_carrera and carrera["estado"] == "Oculto":
            return carrera
    return None

def existe_carrera(carreras, nombre):  #verifica si existe una carrera activa con el mismo nombre
    for carrera in carreras:
        if carrera["estado"] == "Activo" and carrera["nombre"].lower() == nombre.lower():
            return True
    return False

def registrar_carrera():  #registra una nueva carrera académica
    imprimir_titulo("REGISTRAR CARRERA")
    carreras = leer_json(RUTA_CARRERAS)

    nombre = leer_texto("Nombre de la carrera: ")

    if existe_carrera(carreras, nombre):
        print("Ya existe una carrera activa con ese nombre.")
        input()
        return
    descripcion = leer_texto("Descripción: ")
    duracion = leer_entero_positivo("Duración en meses: ")

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

def editar_carrera():  #edita una carrera existente por opciones
    imprimir_titulo("EDITAR CARRERA")
    carreras = leer_json(RUTA_CARRERAS)

    if len(carreras) == 0:
        print("No hay carreras registradas.")
        input()
        return

    if ver_carreras_sin_pausa() == 0:
        print("No hay carreras activas para editar.")
        input()
        return

    id_carrera = leer_entero_positivo("\nIngrese ID de la carrera: ")
    carrera = buscar_carrera_por_id(carreras, id_carrera)
    if carrera is None:
        print("Carrera no encontrada.")
        input()
        return
    while True:
        imprimir_titulo("DATOS DE LA CARRERA")
        print(f"ID: {carrera['id_carrera']}")
        print(f"Nombre: {carrera['nombre']}")
        print(f"Descripción: {carrera['descripcion']}")
        print(f"Duración: {carrera['duracion_meses']} meses")

        print("\n¿Qué desea editar?")
        print("1. Nombre")
        print("2. Descripción")
        print("3. Duración")
        print("4. Guardar y volver")

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            nuevo_nombre = leer_texto("Nuevo nombre de la carrera: ")
            if existe_carrera(carreras, nuevo_nombre) and nuevo_nombre.lower() != carrera["nombre"].lower():
                print("Ya existe otra carrera activa con ese nombre.")
            else:
                carrera["nombre"] = nuevo_nombre
                print("Nombre actualizado correctamente.")
        elif opcion == "2":
            carrera["descripcion"] = leer_texto("Nueva descripción: ")
            print("Descripción actualizada correctamente.")
        elif opcion == "3":
            carrera["duracion_meses"] = leer_entero_positivo("Nueva duración en meses: ")
            print("Duración actualizada correctamente.")
        elif opcion == "4":
            guardar_json(RUTA_CARRERAS, carreras)
            print("\nCarrera actualizada correctamente.")
            input()
            break

        else:
            print("Opción inválida.")

def buscar_carrera():  #busca una carrera por nombre
    imprimir_titulo("BUSCAR CARRERA")
    carreras = leer_json(RUTA_CARRERAS)
    if len(carreras) == 0:
        print("No hay carreras registradas.")
        input()
        return
    texto = leer_texto("Ingrese nombre de la carrera: ").lower()
    encontrados = 0
    for carrera in carreras:
        if carrera["estado"] == "Activo" and texto in carrera["nombre"].lower():
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

    encontrados = 0

    for carrera in carreras:
        if carrera["estado"] == "Activo":
            encontrados += 1
            print("\n-----------------------------")
            print(f"ID: {carrera['id_carrera']}")
            print(f"Nombre: {carrera['nombre']}")
            print(f"Descripción: {carrera['descripcion']}")
            print(f"Duración: {carrera['duracion_meses']} meses")

    if encontrados == 0:
        print("No hay carreras activas.")

    input()

def desactivar_carrera():  #oculta una carrera activa
    imprimir_titulo("OCULTAR CARRERA")
    carreras = leer_json(RUTA_CARRERAS)

    if len(carreras) == 0:
        print("No hay carreras registradas.")
        input()
        return

    while True:
        if ver_carreras_sin_pausa() == 0:
            print("No hay carreras activas para ocultar.")
            input()
            return

        print("0. Volver")
        id_carrera = leer_entero("\nIngrese ID de la carrera a ocultar: ")

        if id_carrera == 0:
            break

        carrera = buscar_carrera_por_id(carreras, id_carrera)

        if carrera is None:
            print("Carrera no encontrada.")
            continue

        confirmar = input(f"¿Desea ocultar {carrera['nombre']}? (s/n): ").lower()
        if confirmar == "s":
            carrera["estado"] = "Oculto"
            guardar_json(RUTA_CARRERAS, carreras)
            print("\nCarrera ocultada correctamente.")
            input()
            break
        print("Operación cancelada.")

def activar_carrera():  #activa una carrera oculta
    imprimir_titulo("ACTIVAR CARRERA")
    carreras = leer_json(RUTA_CARRERAS)

    if len(carreras) == 0:
        print("No hay carreras registradas.")
        input()
        return

    while True:
        if ver_carreras_ocultas_sin_pausa() == 0:
            print("No hay carreras ocultas para activar.")
            input()
            return
        print("0. Volver")
        id_carrera = leer_entero("\nIngrese ID de la carrera a activar: ")

        if id_carrera == 0:
            break

        carrera = buscar_carrera_oculta_por_id(carreras, id_carrera)

        if carrera is None:
            print("Carrera oculta no encontrada.")
            continue

        confirmar = input(f"¿Desea activar {carrera['nombre']}? (s/n): ").lower()

        if confirmar == "s":
            carrera["estado"] = "Activo"
            guardar_json(RUTA_CARRERAS, carreras)
            print("\nCarrera activada correctamente.")
            input()
            break

        print("Operación cancelada.")

def ver_carreras_sin_pausa():  #muestra carreras activas para selección
    carreras = leer_json(RUTA_CARRERAS)
    encontrados = 0

    imprimir_titulo("CARRERAS ACTIVAS")

    for carrera in carreras:
        if carrera["estado"] == "Activo":
            encontrados += 1
            print(f"ID: {carrera['id_carrera']} | {carrera['nombre']}")

    return encontrados

def ver_carreras_ocultas_sin_pausa():  #muestra carreras ocultas para selección
    carreras = leer_json(RUTA_CARRERAS)
    encontrados = 0

    imprimir_titulo("CARRERAS OCULTAS")
    for carrera in carreras:
        if carrera["estado"] == "Oculto":
            encontrados += 1
            print(f"ID: {carrera['id_carrera']} | {carrera['nombre']}")
    return encontrados