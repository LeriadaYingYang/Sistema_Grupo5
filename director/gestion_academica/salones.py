from basedatos_json import leer_json, guardar_json, generar_id
from director.utilidades import imprimir_titulo

RUTA_CARRERAS = "datos/carreras.json"
RUTA_SALONES = "datos/salones.json"
RUTA_PLANTILLAS = "datos/plantillas_academicas.json"

def leer_texto(mensaje):  #valida que el texto no esté vacío
    while True:
        texto = input(mensaje).strip()
        if texto != "":
            return texto
        print("Este campo no puede estar vacío.")

def leer_entero_positivo(mensaje):  #valida que el número sea entero positivo
    while True:
        try:
            numero = int(input(mensaje))
            if numero > 0:
                return numero
            print("El número debe ser mayor que 0.")
        except ValueError:
            print("Ingrese un número válido.")

def leer_entero_no_negativo(mensaje):  #permite ingresar 0 para volver
    while True:
        try:
            numero = int(input(mensaje))
            if numero >= 0:
                return numero
            print("El número debe ser 0 o mayor.")
        except ValueError:
            print("Ingrese un número válido.")

def buscar_por_id(lista, campo_id, valor_id):  #busca un registro activo por su id
    for item in lista:
        if item[campo_id] == valor_id and item["estado"] == "Activo":
            return item
    return None

def existe_salon(salones, nombre_salon, id_carrera):  #verifica si ya existe un salón activo
    for salon in salones:
        if (salon["estado"] == "Activo"
                and salon["nombre_salon"].lower() == nombre_salon.lower()
                and salon["id_carrera"] == id_carrera):
            return True
    return False

def registrar_salon():  #registra un nuevo salón relacionado a una carrera
    imprimir_titulo("REGISTRAR SALON")

    carreras = leer_json(RUTA_CARRERAS)
    salones = leer_json(RUTA_SALONES)

    if len(carreras) == 0:
        print("Primero debe registrar carreras.")
        input()
        return
    if mostrar_carreras() == 0:
        print("No hay carreras activas.")
        input()
        return
    id_carrera = leer_entero_positivo("\nIngrese ID de carrera: ")
    carrera = buscar_por_id(carreras, "id_carrera", id_carrera)
    if carrera is None:
        print("Carrera no encontrada.")
        input()
        return
    nombre_salon = leer_texto("Nombre del salón: ")
    if existe_salon(salones, nombre_salon, id_carrera):
        print("Ya existe un salón activo con ese nombre para esta carrera.")
        input()
        return
    turno = leer_texto("Turno: ")

    nuevo_salon = {
        "id_salon": generar_id(salones, "id_salon"),
        "nombre_salon": nombre_salon,
        "turno": turno,
        "id_carrera": carrera["id_carrera"],
        "nombre_carrera": carrera["nombre"],
        "id_plantilla": None,
        "nombre_plantilla": "",
        "estado": "Activo"}

    salones.append(nuevo_salon)
    guardar_json(RUTA_SALONES, salones)

    print("\nSalón registrado correctamente.")
    print(f"ID generado: {nuevo_salon['id_salon']}")
    input()

def editar_salon():  #edita los datos de un salón por opciones
    imprimir_titulo("EDITAR SALON")

    salones = leer_json(RUTA_SALONES)

    if len(salones) == 0:
        print("No hay salones registrados.")
        input()
        return

    if mostrar_salones() == 0:
        print("No hay salones activos para editar.")
        input()
        return

    id_salon = leer_entero_positivo("\nIngrese ID del salón: ")
    salon = buscar_por_id(salones, "id_salon", id_salon)

    if salon is None:
        print("Salón no encontrado.")
        input()
        return
    while True:
        imprimir_titulo("DATOS DEL SALON")
        print(f"ID: {salon['id_salon']}")
        print(f"Salón: {salon['nombre_salon']}")
        print(f"Turno: {salon['turno']}")
        print(f"Carrera: {salon['nombre_carrera']}")
        print(f"Plantilla: {salon.get('nombre_plantilla', '')}")

        print("\n¿Qué desea editar?")
        print("1. Nombre del salón")
        print("2. Turno")
        print("3. Guardar y volver")

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            nuevo_nombre = leer_texto("Nuevo nombre del salón: ")
            if existe_salon(salones, nuevo_nombre, salon["id_carrera"]) and nuevo_nombre.lower() != salon["nombre_salon"].lower():
                print("Ya existe otro salón activo con ese nombre para esta carrera.")
            else:
                salon["nombre_salon"] = nuevo_nombre
                print("Nombre actualizado correctamente.")
        elif opcion == "2":
            salon["turno"] = leer_texto("Nuevo turno: ")
            print("Turno actualizado correctamente.")
        elif opcion == "3":
            guardar_json(RUTA_SALONES, salones)
            print("\nSalón actualizado correctamente.")
            input()
            break
        else:
            print("Opción inválida.")

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
    if mostrar_salones() == 0:
        print("No hay salones activos.")
        input()
        return

    id_salon = leer_entero_positivo("\nIngrese ID del salón: ")
    salon = buscar_por_id(salones, "id_salon", id_salon)

    if salon is None:
        print("Salón no encontrado.")
        input()
        return
    if mostrar_plantillas_por_carrera(salon["id_carrera"]) == 0:
        print("No hay plantillas activas para la carrera del salón.")
        input()
        return
    id_plantilla = leer_entero_positivo("\nIngrese ID de la plantilla: ")
    plantilla = buscar_por_id(plantillas, "id_plantilla", id_plantilla)
    if plantilla is None or plantilla["id_carrera"] != salon["id_carrera"]:
        print("Plantilla no válida para la carrera del salón.")
        input()
        return
    if salon.get("id_plantilla") == plantilla["id_plantilla"]:
        print("El salón ya tiene asignada esta plantilla.")
        input()
        return
    confirmar = input(
        f"¿Asignar la plantilla {plantilla['nombre_plantilla']} "
        f"al salón {salon['nombre_salon']}? (s/n): ").lower()
    if confirmar != "s":
        print("Operación cancelada.")
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

def desactivar_salon():  #oculta un salón activo
    imprimir_titulo("DESACTIVAR SALON")

    salones = leer_json(RUTA_SALONES)

    if len(salones) == 0:
        print("No hay salones registrados.")
        input()
        return

    while True:
        if mostrar_salones() == 0:
            print("No hay salones activos para desactivar.")
            input()
            return

        print("0. Volver")
        id_salon = leer_entero_no_negativo("\nIngrese ID del salón a desactivar: ")

        if id_salon == 0:
            break

        salon = buscar_por_id(salones, "id_salon", id_salon)

        if salon is None:
            print("Salón no encontrado.")
            continue

        confirmar = input(f"¿Desea desactivar el salón {salon['nombre_salon']}? (s/n): ").lower()

        if confirmar == "s":
            salon["estado"] = "Oculto"
            guardar_json(RUTA_SALONES, salones)
            print("\nSalón desactivado correctamente.")
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

def mostrar_salones():  #muestra los salones activos para seleccionar
    salones = leer_json(RUTA_SALONES)
    imprimir_titulo("SALONES DISPONIBLES")
    encontrados = 0

    for salon in salones:
        if salon["estado"] == "Activo":
            encontrados += 1
            print(
                f"ID: {salon['id_salon']} | "
                f"Salón: {salon['nombre_salon']} | "
                f"Carrera: {salon['nombre_carrera']}")
    return encontrados

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
    return encontrados

def mostrar_salones_ocultos():  #muestra los salones ocultos
    salones = leer_json(RUTA_SALONES)
    imprimir_titulo("SALONES OCULTOS")
    encontrados = 0

    for salon in salones:
        if salon.get("estado") == "Oculto":
            encontrados += 1
            print(
                f"ID: {salon.get('id_salon', 'Sin ID')} | "
                f"Salón: {salon.get('nombre_salon', 'Sin salón')} | "
                f"Carrera: {salon.get('nombre_carrera', 'Sin carrera')}"
            )

    return encontrados

def activar_salon():  #activa un salón oculto
    imprimir_titulo("ACTIVAR SALON")

    salones = leer_json(RUTA_SALONES)

    if len(salones) == 0:
        print("No hay salones registrados.")
        input()
        return

    while True:
        if mostrar_salones_ocultos() == 0:
            print("No hay salones ocultos para activar.")
            input()
            return

        print("0. Volver")
        id_salon = leer_entero_no_negativo("\nIngrese ID del salón a activar: ")

        if id_salon == 0:
            break

        salon_encontrado = None

        for salon in salones:
            if salon.get("id_salon") == id_salon and salon.get("estado") == "Oculto":
                salon_encontrado = salon
                break

        if salon_encontrado is None:
            print("Salón oculto no encontrado.")
            continue

        confirmar = input(
            f"¿Desea activar el salón {salon_encontrado.get('nombre_salon', 'Sin salón')}? (s/n): "
        ).lower()

        if confirmar == "s":
            salon_encontrado["estado"] = "Activo"
            guardar_json(RUTA_SALONES, salones)
            print("\nSalón activado correctamente.")
            input()
            break

        print("Operación cancelada.")