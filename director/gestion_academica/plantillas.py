from basedatos_json import leer_json, guardar_json, generar_id
from director.utilidades import imprimir_titulo

RUTA_CARRERAS = "datos/carreras.json"
RUTA_PLANTILLAS = "datos/plantillas_academicas.json"


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

def buscar_por_id(lista, campo_id, valor_id):  #busca un registro activo por su id
    for item in lista:
        if item[campo_id] == valor_id and item["estado"] == "Activo":
            return item
    return None

def buscar_oculto_por_id(lista, campo_id, valor_id):  #busca un registro oculto por su id
    for item in lista:
        if item[campo_id] == valor_id and item["estado"] == "Oculto":
            return item
    return None

def existe_plantilla(plantillas, nombre, id_carrera):  #valida si ya existe una plantilla activa en una carrera
    for plantilla in plantillas:
        if (plantilla["estado"] == "Activo"
                and plantilla["nombre_plantilla"].lower() == nombre.lower()
                and plantilla["id_carrera"] == id_carrera):
            return True
    return False

def crear_plantilla():  #crea una nueva plantilla académica para una carrera
    imprimir_titulo("CREAR PLANTILLA ACADÉMICA")

    carreras = leer_json(RUTA_CARRERAS)  #carga las carreras registradas
    plantillas = leer_json(RUTA_PLANTILLAS)  #carga las plantillas registradas

    if len(carreras) == 0:
        print("Primero debe registrar carreras.")
        input()
        return

    if mostrar_carreras() == 0:
        print("No hay carreras activas.")
        input()
        return

    id_carrera = leer_entero("\nIngrese ID de la carrera: ")
    carrera = buscar_por_id(carreras, "id_carrera", id_carrera)

    if carrera is None:
        print("Carrera no encontrada.")
        input()
        return

    nombre = leer_texto("Nombre de la plantilla: ")

    if existe_plantilla(plantillas, nombre, id_carrera):
        print("Ya existe una plantilla activa con ese nombre para esta carrera.")
        input()
        return

    descripcion = leer_texto("Descripción: ")

    nueva_plantilla = {
        "id_plantilla": generar_id(plantillas, "id_plantilla"),
        "id_carrera": carrera["id_carrera"],
        "nombre_carrera": carrera["nombre"],
        "nombre_plantilla": nombre,
        "descripcion": descripcion,
        "estado": "Activo"}

    plantillas.append(nueva_plantilla)
    guardar_json(RUTA_PLANTILLAS, plantillas)

    print("\nPlantilla creada correctamente.")
    print(f"ID generado: {nueva_plantilla['id_plantilla']}")
    input()

def editar_plantilla():  #edita una plantilla académica por opciones
    imprimir_titulo("EDITAR PLANTILLA ACADÉMICA")

    plantillas = leer_json(RUTA_PLANTILLAS)

    if len(plantillas) == 0:
        print("No hay plantillas registradas.")
        input()
        return

    if mostrar_plantillas() == 0:
        print("No hay plantillas activas para editar.")
        input()
        return

    id_plantilla = leer_entero("\nIngrese ID de la plantilla: ")
    plantilla = buscar_por_id(plantillas, "id_plantilla", id_plantilla)

    if plantilla is None:
        print("Plantilla no encontrada.")
        input()
        return

    while True:
        imprimir_titulo("DATOS DE LA PLANTILLA")
        print(f"ID: {plantilla['id_plantilla']}")
        print(f"Carrera: {plantilla['nombre_carrera']}")
        print(f"Plantilla: {plantilla['nombre_plantilla']}")
        print(f"Descripción: {plantilla['descripcion']}")

        print("\n¿Qué desea editar?")
        print("1. Nombre")
        print("2. Descripción")
        print("3. Guardar y volver")

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            nuevo_nombre = leer_texto("Nuevo nombre de la plantilla: ")

            if existe_plantilla(plantillas, nuevo_nombre, plantilla["id_carrera"]) and nuevo_nombre.lower() != plantilla["nombre_plantilla"].lower():
                print("Ya existe otra plantilla activa con ese nombre para esta carrera.")
            else:
                plantilla["nombre_plantilla"] = nuevo_nombre
                print("Nombre actualizado correctamente.")

        elif opcion == "2":
            plantilla["descripcion"] = leer_texto("Nueva descripción: ")
            print("Descripción actualizada correctamente.")

        elif opcion == "3":
            guardar_json(RUTA_PLANTILLAS, plantillas)
            print("\nPlantilla actualizada correctamente.")
            input()
            break

        else:
            print("Opción inválida.")

def asignar_carrera_plantilla():  #asigna o cambia la carrera de una plantilla
    imprimir_titulo("ASIGNAR CARRERA A PLANTILLA")

    carreras = leer_json(RUTA_CARRERAS)
    plantillas = leer_json(RUTA_PLANTILLAS)

    if len(carreras) == 0:
        print("No hay carreras registradas.")
        input()
        return
    if len(plantillas) == 0:
        print("No hay plantillas registradas.")
        input()
        return
    if mostrar_plantillas() == 0:
        print("No hay plantillas activas.")
        input()
        return

    id_plantilla = leer_entero("\nIngrese ID de la plantilla: ")
    plantilla = buscar_por_id(plantillas, "id_plantilla", id_plantilla)

    if plantilla is None:
        print("Plantilla no encontrada.")
        input()
        return

    if mostrar_carreras() == 0:
        print("No hay carreras activas.")
        input()
        return

    id_carrera = leer_entero("\nIngrese ID de la nueva carrera: ")
    carrera = buscar_por_id(carreras, "id_carrera", id_carrera)

    if carrera is None:
        print("Carrera no encontrada.")
        input()
        return

    if existe_plantilla(plantillas, plantilla["nombre_plantilla"], id_carrera):
        print("Ya existe una plantilla con ese nombre en la carrera seleccionada.")
        input()
        return

    plantilla["id_carrera"] = carrera["id_carrera"]
    plantilla["nombre_carrera"] = carrera["nombre"]

    guardar_json(RUTA_PLANTILLAS, plantillas)

    print("\nCarrera asignada correctamente a la plantilla.")
    input()

def ver_plantillas():  #muestra las plantillas académicas registradas
    imprimir_titulo("LISTA DE PLANTILLAS")
    plantillas = leer_json(RUTA_PLANTILLAS)

    if len(plantillas) == 0:
        print("No hay plantillas registradas.")
        input()
        return

    encontrados = 0

    for p in plantillas:
        if p["estado"] == "Activo":
            encontrados += 1
            print("\n-----------------------------")
            print(f"ID: {p['id_plantilla']}")
            print(f"Carrera: {p['nombre_carrera']}")
            print(f"Plantilla: {p['nombre_plantilla']}")
            print(f"Descripción: {p['descripcion']}")

    if encontrados == 0:
        print("No hay plantillas activas.")

    input()

def desactivar_plantilla():  #oculta una plantilla académica
    imprimir_titulo("OCULTAR PLANTILLA")

    plantillas = leer_json(RUTA_PLANTILLAS)

    if len(plantillas) == 0:
        print("No hay plantillas registradas.")
        input()
        return
    while True:
        if mostrar_plantillas() == 0:
            print("No hay plantillas activas para ocultar.")
            input()
            return
        print("0. Volver")
        id_plantilla = leer_entero("\nIngrese ID de la plantilla a ocultar: ")
        if id_plantilla == 0:
            break
        plantilla = buscar_por_id(plantillas, "id_plantilla", id_plantilla)
        if plantilla is None:
            print("Plantilla no encontrada.")
            continue
        confirmar = input(f"¿Desea ocultar {plantilla['nombre_plantilla']}? (s/n): ").lower()
        if confirmar == "s":
            plantilla["estado"] = "Oculto"
            guardar_json(RUTA_PLANTILLAS, plantillas)
            print("\nPlantilla ocultada correctamente.")
            input()
            break
        print("Operación cancelada.")

def activar_plantilla():  #activa una plantilla oculta
    imprimir_titulo("ACTIVAR PLANTILLA")

    plantillas = leer_json(RUTA_PLANTILLAS)
    if len(plantillas) == 0:
        print("No hay plantillas registradas.")
        input()
        return
    while True:
        if mostrar_plantillas_ocultas() == 0:
            print("No hay plantillas ocultas para activar.")
            input()
            return

        print("0. Volver")
        id_plantilla = leer_entero("\nIngrese ID de la plantilla a activar: ")
        if id_plantilla == 0:
            break
        plantilla = buscar_oculto_por_id(plantillas, "id_plantilla", id_plantilla)
        if plantilla is None:
            print("Plantilla oculta no encontrada.")
            continue
        confirmar = input(f"¿Desea activar {plantilla['nombre_plantilla']}? (s/n): ").lower()
        if confirmar == "s":
            plantilla["estado"] = "Activo"
            guardar_json(RUTA_PLANTILLAS, plantillas)
            print("\nPlantilla activada correctamente.")
            input()
            break

        print("Operación cancelada.")

def mostrar_carreras():  #muestra las carreras activas para seleccionar
    carreras = leer_json(RUTA_CARRERAS)

    imprimir_titulo("CARRERAS DISPONIBLES")
    encontrados = 0
    for carrera in carreras:
        if carrera["estado"] == "Activo":
            encontrados += 1
            print(f"ID: {carrera['id_carrera']} | {carrera['nombre']}")
    return encontrados

def mostrar_plantillas():  #muestra las plantillas activas para seleccionar
    plantillas = leer_json(RUTA_PLANTILLAS)
    imprimir_titulo("PLANTILLAS DISPONIBLES")
    encontrados = 0
    for plantilla in plantillas:
        if plantilla["estado"] == "Activo":
            encontrados += 1
            print(
                f"ID: {plantilla['id_plantilla']} | "
                f"Plantilla: {plantilla['nombre_plantilla']} | "
                f"Carrera: {plantilla['nombre_carrera']}")

    return encontrados

def mostrar_plantillas_ocultas():  #muestra las plantillas ocultas
    plantillas = leer_json(RUTA_PLANTILLAS)
    imprimir_titulo("PLANTILLAS OCULTAS")
    encontrados = 0
    for plantilla in plantillas:
        if plantilla["estado"] == "Oculto":
            encontrados += 1
            print(
                f"ID: {plantilla['id_plantilla']} | "
                f"Plantilla: {plantilla['nombre_plantilla']} | "
                f"Carrera: {plantilla['nombre_carrera']}")
    return encontrados