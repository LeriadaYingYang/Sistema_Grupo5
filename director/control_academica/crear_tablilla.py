from basedatos_json import leer_json, guardar_json, generar_id
from director.utilidades import imprimir_titulo

RUTA_UNIDADES = "datos/unidades.json"
RUTA_MODULOS = "datos/modulos.json"
RUTA_TABLILLAS = "datos/tablillas_notas.json"
RUTA_CARRERAS = "datos/carreras.json"
RUTA_PLANTILLAS = "datos/plantillas_academicas.json"
RUTA_SALONES = "datos/salones.json"

def buscar_por_id(lista, campo_id, valor_id):  #busca un registro activo por su id
    for item in lista:
        if item[campo_id] == valor_id and item["estado"] == "Activo":
            return item
    return None

def tablilla_ya_existe(tablillas, id_unidad, id_modulo):  #verifica si la tablilla ya existe
    for t in tablillas:
        if (
            t["id_unidad"] == id_unidad
            and t["id_modulo"] == id_modulo
            and t["estado"] == "Activo"):
            return True
    return False

def mostrar_carreras(carreras):  #muestra las carreras disponibles
    imprimir_titulo("CARRERAS DISPONIBLES")
    for carrera in carreras:
        if carrera["estado"] == "Activo":
            print(f"ID: {carrera['id_carrera']} | {carrera['nombre']}")

def mostrar_plantillas(plantillas, id_carrera):  #muestra plantillas de la carrera
    imprimir_titulo("PLANTILLAS DE LA CARRERA")
    encontrados = 0
    for plantilla in plantillas:
        if plantilla["estado"] == "Activo" and plantilla["id_carrera"] == id_carrera:
            encontrados += 1
            print(f"ID: {plantilla['id_plantilla']} | {plantilla['nombre_plantilla']}")
    if encontrados == 0:
        print("No hay plantillas para esta carrera.")

def mostrar_salones(salones, id_carrera):  #muestra salones de la carrera
    imprimir_titulo("SALONES DE LA CARRERA")
    encontrados = 0
    for salon in salones:
        if salon["estado"] == "Activo" and salon["id_carrera"] == id_carrera:
            encontrados += 1
            print(f"ID: {salon['id_salon']} | {salon['nombre_salon']} | Turno: {salon['turno']}")
    if encontrados == 0:
        print("No hay salones para esta carrera.")

def mostrar_unidades(unidades, id_salon, id_plantilla):  #muestra unidades disponibles
    imprimir_titulo("UNIDADES DISPONIBLES")
    encontrados = 0
    for unidad in unidades:
        if (
            unidad["estado"] == "Activo"
            and unidad.get("id_salon") == id_salon
            and unidad.get("id_plantilla") == id_plantilla):
            encontrados += 1
            print(f"ID: {unidad['id_unidad']} | {unidad['nombre_unidad']}")
    if encontrados == 0:
        print("No hay unidades para ese salón y plantilla.")

def mostrar_modulos_por_unidad(modulos, id_unidad):  #muestra módulos de la unidad
    imprimir_titulo("MÓDULOS DE LA UNIDAD")
    encontrados = 0
    for modulo in modulos:
        if modulo["estado"] == "Activo" and modulo["id_unidad"] == id_unidad:
            encontrados += 1
            print(f"ID: {modulo['id_modulo']} | {modulo['nombre_modulo']}")
    if encontrados == 0:
        print("No hay módulos registrados.")

def pedir_notas_tablilla():  #solicita las notas que tendrá la tablilla
    notas = []
    while True:
        try:
            cantidad = int(input("¿Cuántas notas tendrá este módulo?: "))
            if cantidad > 0:
                break
            print("Debe ser mayor a 0.")
        except ValueError:
            print("Ingrese un número válido.")
    for i in range(cantidad):
        nombre = input(f"Nombre de la nota {i + 1}: ")
        notas.append({
            "orden": i + 1,
            "nombre_nota": nombre})
    return notas

def crear_tablilla_notas():  #crea una tablilla de notas para un módulo
    imprimir_titulo("CREAR TABLILLA DE NOTAS")
    carreras = leer_json(RUTA_CARRERAS)
    plantillas = leer_json(RUTA_PLANTILLAS)
    salones = leer_json(RUTA_SALONES)
    unidades = leer_json(RUTA_UNIDADES)
    modulos = leer_json(RUTA_MODULOS)
    tablillas = leer_json(RUTA_TABLILLAS)
    if len(unidades) == 0 or len(modulos) == 0:
        print("Debe registrar unidades y módulos primero.")
        return
    mostrar_carreras(carreras)
    try:
        id_carrera = int(input("\nIngrese ID de carrera: "))
    except ValueError:
        print("Debe ingresar un número.")
        return
    mostrar_plantillas(plantillas, id_carrera)
    try:
        id_plantilla = int(input("\nIngrese ID de plantilla: "))
    except ValueError:
        print("Debe ingresar un número.")
        return
    plantilla = buscar_por_id(plantillas, "id_plantilla", id_plantilla)
    if plantilla is None or plantilla["id_carrera"] != id_carrera:
        print("Plantilla no válida.")
        return
    mostrar_salones(salones, id_carrera)
    try:
        id_salon = int(input("\nIngrese ID de salón: "))
    except ValueError:
        print("Debe ingresar un número.")
        return
    mostrar_unidades(unidades, id_salon, id_plantilla)
    try:
        id_unidad = int(input("\nIngrese ID de unidad: "))
    except ValueError:
        print("Debe ingresar un número.")
        return
    unidad = buscar_por_id(unidades, "id_unidad", id_unidad)
    if unidad is None:
        print("Unidad no encontrada.")
        return
    mostrar_modulos_por_unidad(modulos, id_unidad)
    try:
        id_modulo = int(input("\nIngrese ID de módulo: "))
    except ValueError:
        print("Debe ingresar un número.")
        return
    modulo = buscar_por_id(modulos, "id_modulo", id_modulo)
    if modulo is None or modulo["id_unidad"] != id_unidad:
        print("Módulo no válido.")
        return
    if tablilla_ya_existe(tablillas, id_unidad, id_modulo):
        print("Ya existe tablilla para esta unidad y módulo.")
        return
    notas = pedir_notas_tablilla()
    nueva = {
        "id_tablilla": generar_id(tablillas, "id_tablilla"),
        "id_unidad": unidad["id_unidad"],
        "nombre_unidad": unidad["nombre_unidad"],
        "id_modulo": modulo["id_modulo"],
        "nombre_modulo": modulo["nombre_modulo"],
        "id_carrera": unidad["id_carrera"],
        "nombre_carrera": unidad["nombre_carrera"],
        "id_salon": unidad.get("id_salon"),
        "nombre_salon": unidad.get("nombre_salon"),
        "turno": unidad.get("turno"),
        "id_plantilla": unidad["id_plantilla"],
        "nombre_plantilla": unidad["nombre_plantilla"],
        "notas": notas,
        "estado": "Activo"}
    tablillas.append(nueva)  #agrega la tablilla
    guardar_json(RUTA_TABLILLAS, tablillas)  #guarda la tablilla
    print("\nTablilla creada correctamente.")
    print(f"Unidad: {nueva['nombre_unidad']}")
    print(f"Módulo: {nueva['nombre_modulo']}")