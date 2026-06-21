from basedatos_json import leer_json, guardar_json, generar_id
from director.utilidades import imprimir_titulo

RUTA_MODULOS = "datos/modulos.json"
RUTA_SALONES = "datos/salones.json"
RUTA_CARRERAS = "datos/carreras.json"
RUTA_PLANTILLAS = "datos/plantillas_academicas.json"
RUTA_UNIDADES = "datos/unidades.json"

def buscar_por_id(lista, campo_id, valor_id):  #busca un registro activo por su id
    for item in lista:
        if item[campo_id] == valor_id and item["estado"] == "Activo":
            return item
    return None

def mostrar_carreras(carreras):  #muestra las carreras activas
    imprimir_titulo("CARRERAS DISPONIBLES")
    for carrera in carreras:
        if carrera["estado"] == "Activo":
            print(f"ID: {carrera['id_carrera']} | {carrera['nombre']}")

def mostrar_plantillas(plantillas, id_carrera):  #muestra las plantillas de una carrera
    imprimir_titulo("PLANTILLAS DISPONIBLES")
    for plantilla in plantillas:
        if plantilla["estado"] == "Activo" and plantilla["id_carrera"] == id_carrera:
            print(f"ID: {plantilla['id_plantilla']} | {plantilla['nombre_plantilla']}")

def mostrar_salones(salones, id_carrera):  #muestra los salones de una carrera
    imprimir_titulo("SALONES DISPONIBLES")
    for salon in salones:
        if salon["estado"] == "Activo" and salon["id_carrera"] == id_carrera:
            print(f"ID: {salon['id_salon']} | {salon['nombre_salon']} | {salon['turno']}")

def mostrar_modulos(modulos):  #muestra los módulos activos
    imprimir_titulo("MÓDULOS DISPONIBLES")
    for modulo in modulos:
        if modulo["estado"] == "Activo":
            print(
                f"ID: {modulo['id_modulo']} | "
                f"Módulo: {modulo['nombre_modulo']} | "
                f"Salón: {modulo['nombre_salon']}")

def registrar_modulo():  #registra módulos después de seleccionar carrera, plantilla y salón
    imprimir_titulo("CREAR MÓDULO")

    carreras = leer_json(RUTA_CARRERAS)
    plantillas = leer_json(RUTA_PLANTILLAS)
    salones = leer_json(RUTA_SALONES)
    modulos = leer_json(RUTA_MODULOS)

    if len(carreras) == 0:
        print("Primero debe registrar carreras.")
        input()
        return

    if len(plantillas) == 0:
        print("Primero debe crear plantillas académicas.")
        input()
        return

    if len(salones) == 0:
        print("Primero debe registrar salones.")
        input()
        return

    mostrar_carreras(carreras)

    try:
        id_carrera = int(input("\nIngrese ID de carrera: "))
    except ValueError:
        print("Debe ingresar un número.")
        input()
        return

    carrera = buscar_por_id(carreras, "id_carrera", id_carrera)

    if carrera is None:
        print("Carrera no encontrada.")
        input()
        return

    mostrar_plantillas(plantillas, id_carrera)

    try:
        id_plantilla = int(input("\nIngrese ID de plantilla: "))
    except ValueError:
        print("Debe ingresar un número.")
        input()
        return

    plantilla = buscar_por_id(plantillas, "id_plantilla", id_plantilla)

    if plantilla is None or plantilla["id_carrera"] != id_carrera:
        print("Plantilla no válida.")
        input()
        return

    mostrar_salones(salones, id_carrera)

    try:
        id_salon = int(input("\nIngrese ID de salón: "))
    except ValueError:
        print("Debe ingresar un número.")
        input()
        return

    salon = buscar_por_id(salones, "id_salon", id_salon)

    if salon is None or salon["id_carrera"] != id_carrera:
        print("Salón no válido.")
        input()
        return

    while True:
        try:
            cantidad = int(input("¿Cuántos módulos desea crear?: "))
            if cantidad > 0:
                break
            print("La cantidad debe ser mayor que 0.")
        except ValueError:
            print("Ingrese un número válido.")

    for i in range(1, cantidad + 1):
        imprimir_titulo(f"MÓDULO {i}")

        nombre = input("Nombre del módulo: ")
        descripcion = input("Descripción: ")

        nuevo_modulo = {
            "id_modulo": generar_id(modulos, "id_modulo"),
            "id_carrera": carrera["id_carrera"],
            "nombre_carrera": carrera["nombre"],
            "id_plantilla": plantilla["id_plantilla"],
            "nombre_plantilla": plantilla["nombre_plantilla"],
            "id_salon": salon["id_salon"],
            "nombre_salon": salon["nombre_salon"],
            "turno": salon["turno"],
            "id_unidad": None,
            "nombre_unidad": "",
            "nombre_modulo": nombre,
            "descripcion": descripcion,
            "orden": i,
            "estado": "Activo"}

        modulos.append(nuevo_modulo)
        print(f"Módulo agregado: {nombre}")

    guardar_json(RUTA_MODULOS, modulos)

    print("\nMódulos registrados correctamente.")
    input()

def editar_modulo():  #edita los datos de un módulo
    imprimir_titulo("EDITAR MÓDULO")

    modulos = leer_json(RUTA_MODULOS)

    if len(modulos) == 0:
        print("No hay módulos registrados.")
        input()
        return

    mostrar_modulos(modulos)

    try:
        id_modulo = int(input("\nIngrese ID del módulo: "))
    except ValueError:
        print("Debe ingresar un número.")
        input()
        return

    for modulo in modulos:
        if modulo["id_modulo"] == id_modulo and modulo["estado"] == "Activo":
            nuevo_nombre = input(f"Nombre ({modulo['nombre_modulo']}): ").strip()
            nueva_descripcion = input(f"Descripción ({modulo['descripcion']}): ").strip()

            if nuevo_nombre:
                modulo["nombre_modulo"] = nuevo_nombre

            if nueva_descripcion:
                modulo["descripcion"] = nueva_descripcion

            guardar_json(RUTA_MODULOS, modulos)

            print("\nMódulo actualizado correctamente.")
            input()
            return

    print("Módulo no encontrado.")
    input()

def asignar_modulo_unidad():  #asigna una unidad a un módulo
    imprimir_titulo("ASIGNAR MÓDULO A UNIDAD")

    modulos = leer_json(RUTA_MODULOS)
    unidades = leer_json(RUTA_UNIDADES)

    if len(modulos) == 0:
        print("No hay módulos registrados.")
        input()
        return

    if len(unidades) == 0:
        print("No hay unidades registradas.")
        input()
        return

    mostrar_modulos(modulos)

    try:
        id_modulo = int(input("\nIngrese ID del módulo: "))
    except ValueError:
        print("Debe ingresar un número.")
        input()
        return

    modulo = buscar_por_id(modulos, "id_modulo", id_modulo)

    if modulo is None:
        print("Módulo no encontrado.")
        input()
        return

    imprimir_titulo("UNIDADES DISPONIBLES")

    for unidad in unidades:
        if unidad["estado"] == "Activo":
            print(f"ID: {unidad['id_unidad']} | {unidad['nombre_unidad']}")

    try:
        id_unidad = int(input("\nIngrese ID de unidad: "))
    except ValueError:
        print("Debe ingresar un número.")
        input()
        return

    unidad = buscar_por_id(unidades, "id_unidad", id_unidad)

    if unidad is None:
        print("Unidad no encontrada.")
        input()
        return

    modulo["id_unidad"] = unidad["id_unidad"]
    modulo["nombre_unidad"] = unidad["nombre_unidad"]

    guardar_json(RUTA_MODULOS, modulos)

    print("\nUnidad asignada correctamente al módulo.")
    input()

def ver_modulos():  #muestra los módulos registrados
    imprimir_titulo("VER MÓDULOS")

    modulos = leer_json(RUTA_MODULOS)

    if len(modulos) == 0:
        print("No hay módulos registrados.")
        input()
        return

    encontrados = 0

    for modulo in modulos:
        if modulo["estado"] == "Activo":
            encontrados += 1

            print("\n-----------------------------")
            print(f"ID: {modulo['id_modulo']}")
            print(f"Carrera: {modulo['nombre_carrera']}")
            print(f"Plantilla: {modulo['nombre_plantilla']}")
            print(f"Salón: {modulo['nombre_salon']}")
            print(f"Turno: {modulo['turno']}")
            print(f"Módulo: {modulo['nombre_modulo']}")
            print(f"Unidad: {modulo['nombre_unidad']}")
            print(f"Descripción: {modulo['descripcion']}")

    if encontrados == 0:
        print("No hay módulos activos.")

    input()

def desactivar_modulo():  #desactiva un módulo
    imprimir_titulo("DESACTIVAR MÓDULO")

    modulos = leer_json(RUTA_MODULOS)

    if len(modulos) == 0:
        print("No hay módulos registrados.")
        input()
        return

    mostrar_modulos(modulos)

    try:
        id_modulo = int(input("\nIngrese ID del módulo: "))
    except ValueError:
        print("Debe ingresar un número.")
        input()
        return

    for modulo in modulos:
        if modulo["id_modulo"] == id_modulo and modulo["estado"] == "Activo":
            modulo["estado"] = "Inactivo"

            guardar_json(RUTA_MODULOS, modulos)

            print("\nMódulo desactivado correctamente.")
            input()
            return

    print("Módulo no encontrado.")
    input()