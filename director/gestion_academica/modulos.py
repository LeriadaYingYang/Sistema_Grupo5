from database.basedatos import leer_json, guardar_json, generar_id
from director.utilidades import imprimir_titulo

RUTA_MODULOS = "datos/modulos.json"
RUTA_SALONES = "datos/salones.json"
RUTA_CARRERAS = "datos/carreras.json"
RUTA_PLANTILLAS = "datos/plantillas_academicas.json"
RUTA_UNIDADES = "datos/unidades.json"

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

def buscar_por_id(lista, campo_id, valor_id):  #busca un registro activo por su id
    for item in lista:
        if item[campo_id] == valor_id and item["estado"] == "Activo":
            return item
    return None

def existe_modulo(modulos, nombre, id_salon, id_plantilla):  #valida si ya existe el módulo activo
    for modulo in modulos:
        if (modulo["estado"] == "Activo"
                and modulo["nombre_modulo"].lower() == nombre.lower()
                and modulo["id_salon"] == id_salon
                and modulo["id_plantilla"] == id_plantilla):
            return True
    return False

def mostrar_carreras(carreras):  #muestra las carreras activas
    imprimir_titulo("CARRERAS DISPONIBLES")
    encontrados = 0

    for carrera in carreras:
        if carrera["estado"] == "Activo":
            encontrados += 1
            print(f"ID: {carrera['id_carrera']} | {carrera['nombre']}")

    return encontrados

def mostrar_plantillas(plantillas, id_carrera):  #muestra las plantillas de una carrera
    imprimir_titulo("PLANTILLAS DISPONIBLES")
    encontrados = 0

    for plantilla in plantillas:
        if plantilla["estado"] == "Activo" and plantilla["id_carrera"] == id_carrera:
            encontrados += 1
            print(f"ID: {plantilla['id_plantilla']} | {plantilla['nombre_plantilla']}")

    return encontrados

def mostrar_salones(salones, id_carrera):  #muestra los salones de una carrera
    imprimir_titulo("SALONES DISPONIBLES")
    encontrados = 0

    for salon in salones:
        if salon["estado"] == "Activo" and salon["id_carrera"] == id_carrera:
            encontrados += 1
            print(f"ID: {salon['id_salon']} | {salon['nombre_salon']} | {salon['turno']}")

    return encontrados

def mostrar_modulos(modulos):  #muestra los módulos activos
    imprimir_titulo("MÓDULOS DISPONIBLES")
    encontrados = 0

    for modulo in modulos:
        if modulo["estado"] == "Activo":
            encontrados += 1
            print(
                f"ID: {modulo['id_modulo']} | "
                f"Módulo: {modulo['nombre_modulo']} | "
                f"Salón: {modulo['nombre_salon']}")

    return encontrados

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

    if mostrar_carreras(carreras) == 0:
        print("No hay carreras activas.")
        input()
        return

    id_carrera = leer_entero_positivo("\nIngrese ID de carrera: ")
    carrera = buscar_por_id(carreras, "id_carrera", id_carrera)

    if carrera is None:
        print("Carrera no encontrada.")
        input()
        return

    if len(plantillas) == 0:
        print("Primero debe crear plantillas académicas.")
        input()
        return

    if mostrar_plantillas(plantillas, id_carrera) == 0:
        print("No hay plantillas activas para esta carrera.")
        input()
        return

    id_plantilla = leer_entero_positivo("\nIngrese ID de plantilla: ")
    plantilla = buscar_por_id(plantillas, "id_plantilla", id_plantilla)

    if plantilla is None or plantilla["id_carrera"] != id_carrera:
        print("Plantilla no válida.")
        input()
        return

    if len(salones) == 0:
        print("Primero debe registrar salones.")
        input()
        return

    if mostrar_salones(salones, id_carrera) == 0:
        print("No hay salones activos para esta carrera.")
        input()
        return

    id_salon = leer_entero_positivo("\nIngrese ID de salón: ")
    salon = buscar_por_id(salones, "id_salon", id_salon)

    if salon is None or salon["id_carrera"] != id_carrera:
        print("Salón no válido.")
        input()
        return

    cantidad = leer_entero_positivo("¿Cuántos módulos desea crear?: ")

    for i in range(1, cantidad + 1):
        imprimir_titulo(f"MÓDULO {i}")

        nombre = leer_texto("Nombre del módulo: ")

        if existe_modulo(modulos, nombre, id_salon, id_plantilla):
            print("Ya existe un módulo activo con ese nombre en este salón y plantilla.")
            continue

        descripcion = leer_texto("Descripción: ")

        nuevo_modulo = {
            "id_modulo": generar_id(modulos, "id_modulo"),
            "id_carrera": carrera["id_carrera"],
            "nombre_carrera": carrera["nombre"],
            "id_plantilla": plantilla["id_plantilla"],
            "nombre_plantilla": plantilla["nombre_plantilla"],
            "id_salon": salon["id_salon"],
            "nombre_salon": salon["nombre_salon"],
            "turno": salon["turno"],
            "nombre_modulo": nombre,
            "descripcion": descripcion,
            "orden": i,
            "estado": "Activo"
        }

        modulos.append(nuevo_modulo)
        print(f"Módulo agregado: {nombre}")

    guardar_json(RUTA_MODULOS, modulos)

    print("\nMódulos registrados correctamente.")
    input()

def editar_modulo():  #edita los datos de un módulo por opciones
    imprimir_titulo("EDITAR MÓDULO")

    modulos = leer_json(RUTA_MODULOS)

    if len(modulos) == 0:
        print("No hay módulos registrados.")
        input()
        return

    if mostrar_modulos(modulos) == 0:
        print("No hay módulos activos para editar.")
        input()
        return

    id_modulo = leer_entero_positivo("\nIngrese ID del módulo: ")
    modulo = buscar_por_id(modulos, "id_modulo", id_modulo)

    if modulo is None:
        print("Módulo no encontrado.")
        input()
        return

    while True:
        imprimir_titulo("DATOS DEL MÓDULO")
        print(f"ID: {modulo['id_modulo']}")
        print(f"Carrera: {modulo['nombre_carrera']}")
        print(f"Plantilla: {modulo['nombre_plantilla']}")
        print(f"Salón: {modulo['nombre_salon']}")
        print(f"Módulo: {modulo['nombre_modulo']}")
        print(f"Descripción: {modulo['descripcion']}")

        print("\n¿Qué desea editar?")
        print("1. Nombre")
        print("2. Descripción")
        print("3. Guardar y volver")

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            nuevo_nombre = leer_texto("Nuevo nombre del módulo: ")

            if existe_modulo(modulos, nuevo_nombre, modulo["id_salon"], modulo["id_plantilla"]) and nuevo_nombre.lower() != modulo["nombre_modulo"].lower():
                print("Ya existe otro módulo activo con ese nombre en este salón y plantilla.")
            else:
                modulo["nombre_modulo"] = nuevo_nombre
                print("Nombre actualizado correctamente.")

        elif opcion == "2":
            modulo["descripcion"] = leer_texto("Nueva descripción: ")
            print("Descripción actualizada correctamente.")

        elif opcion == "3":
            guardar_json(RUTA_MODULOS, modulos)
            print("\nMódulo actualizado correctamente.")
            input()
            break

        else:
            print("Opción inválida.")


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
            print(f"Descripción: {modulo['descripcion']}")

    if encontrados == 0:
        print("No hay módulos activos.")

    input()

def desactivar_modulo():  #oculta un módulo
    imprimir_titulo("OCULTAR MÓDULO")

    modulos = leer_json(RUTA_MODULOS)

    if len(modulos) == 0:
        print("No hay módulos registrados.")
        input()
        return

    while True:
        if mostrar_modulos(modulos) == 0:
            print("No hay módulos activos para ocultar.")
            input()
            return

        print("0. Volver")
        id_modulo = leer_entero("\nIngrese ID del módulo a ocultar: ")

        if id_modulo == 0:
            break
        modulo = buscar_por_id(modulos, "id_modulo", id_modulo)
        if modulo is None:
            print("Módulo no encontrado.")
            continue
        confirmar = input(f"¿Desea ocultar {modulo['nombre_modulo']}? (s/n): ").lower()
        if confirmar == "s":
            modulo["estado"] = "Oculto"
            guardar_json(RUTA_MODULOS, modulos)
            print("\nMódulo ocultado correctamente.")
            input()
            break
        print("Operación cancelada.")