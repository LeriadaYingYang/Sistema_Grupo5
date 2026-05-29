from basedatos_json import leer_json, guardar_json, generar_id

RUTA_UNIDADES = "datos/unidades.json"
RUTA_MODULOS = "datos/modulos.json"
RUTA_SALONES = "datos/salones.json"
RUTA_CARRERAS = "datos/carreras.json"
RUTA_PLANTILLAS = "datos/plantillas_academicas.json"

def buscar_por_id(lista, campo_id, valor_id):  #busca un registro activo por su id
    for item in lista:
        if item[campo_id] == valor_id and item["estado"] == "Activo":
            return item
    return None

def unidad_ya_tiene_modulos(modulos, id_unidad):  #verifica si una unidad ya tiene módulos registrados
    for m in modulos:
        if (m["estado"] == "Activo"
            and m["id_unidad"] == id_unidad):
            return True
    return False

def mostrar_carreras(carreras):  #muestra las carreras activas disponibles
    print("\n--- CARRERAS DISPONIBLES ---")
    for c in carreras:
        if c["estado"] == "Activo":
            print(f"ID: {c['id_carrera']} | {c['nombre']}")

def mostrar_plantillas(plantillas, id_carrera): #muestra las plantillas activas de una carrera
    print("\n--- PLANTILLAS DE LA CARRERA ---")
    for p in plantillas:
        if p["estado"] == "Activo" and p["id_carrera"] == id_carrera:
            print(f"ID: {p['id_plantilla']} | {p['nombre_plantilla']}")

def mostrar_salones(salones, id_carrera):  #muestra los salones activos de una carrera
    print("\n--- SALONES DE LA CARRERA ---")
    for s in salones:
        if s["estado"] == "Activo" and s["id_carrera"] == id_carrera:
            print(f"ID: {s['id_salon']} | "
                f"{s['nombre_salon']} | {s['turno']}")

def mostrar_unidades(unidades, id_salon, id_plantilla):  #muestra las unidades de un salón y plantilla
    print("\n--- UNIDADES DEL SALÓN Y PLANTILLA ---")
    encontrados = 0  #cuenta cuántas unidades se encontraron
    for u in unidades:
        if (u["estado"] == "Activo"
            and u.get("id_salon") == id_salon
            and u.get("id_plantilla") == id_plantilla):
            encontrados += 1
            print(f"ID: {u['id_unidad']} | {u['nombre_unidad']}")
    if encontrados == 0:
        print("No hay unidades para este salón y plantilla.")

def registrar_modulo():  #registra uno o varios módulos en una unidad
    print("\n--- REGISTRAR MÓDULOS ---")

    carreras = leer_json(RUTA_CARRERAS)  #carga las carreras registradas
    plantillas = leer_json(RUTA_PLANTILLAS)  #carga las plantillas registradas
    salones = leer_json(RUTA_SALONES)  #carga los salones registrados
    unidades = leer_json(RUTA_UNIDADES)  #carga las unidades registradas
    modulos = leer_json(RUTA_MODULOS)  #carga los módulos registrados

    if len(unidades) == 0:  #valida si existen unidades registradas
        print("Primero debe registrar unidades.")
        return
    mostrar_carreras(carreras)  #muestra las carreras disponibles
    try:
        id_carrera = int(input("\nIngrese ID de carrera: "))  #solicita el id de la carrera
    except ValueError:
        print("Debe ingresar un número.")
        return
    mostrar_plantillas(plantillas, id_carrera)  #muestra las plantillas de la carrera seleccionada
    try:
        id_plantilla = int(input("\nIngrese ID de plantilla: "))  #solicita el id de la plantilla
    except ValueError:
        print("Debe ingresar un número.")
        return
    plantilla = buscar_por_id(plantillas, "id_plantilla", id_plantilla)  #busca la plantilla ingresada
    if plantilla is None or plantilla["id_carrera"] != id_carrera:  #valida que la plantilla pertenezca a la carrera
        print("Plantilla no válida.")
        return
    mostrar_salones(salones, id_carrera)  #muestra los salones de la carrera seleccionada
    try:
        id_salon = int(input("\nIngrese ID de salón: "))  #solicita el id del salón
    except ValueError:
        print("Debe ingresar un número.")
        return
    salon = buscar_por_id(salones, "id_salon", id_salon)  #busca el salón ingresado
    if salon is None or salon["id_carrera"] != id_carrera:  #valida que el salón pertenezca a la carrera
        print("Salón no válido.")
        return
    mostrar_unidades(unidades, id_salon, id_plantilla)  #muestra las unidades del salón y plantilla
    try:
        id_unidad = int(input("\nIngrese ID de unidad: "))  #solicita el id de la unidad
    except ValueError:
        print("Debe ingresar un número.")
        return
    unidad = buscar_por_id(unidades, "id_unidad", id_unidad)  #busca la unidad ingresada
    if (unidad is None
        or unidad.get("id_salon") != id_salon
        or unidad.get("id_plantilla") != id_plantilla):  #valida que la unidad pertenezca al salón y plantilla seleccionados
        print("Unidad no válida.")
        return
    if unidad_ya_tiene_modulos(modulos, id_unidad):  #evita registrar módulos duplicados en la unidad
        print("Esta unidad ya tiene módulos registrados.")
        return
    while True:  #valida la cantidad de módulos a crear
        try:
            cantidad = int(input("¿Cuántos módulos desea crear?: "))
            if cantidad > 0:
                break
            print("Debe ser mayor a 0.")
        except ValueError:
            print("Ingrese un número válido.")
    for i in range(1, cantidad + 1):  #repite el registro según la cantidad indicada
        print(f"\n--- MÓDULO {i} ---")
        nombre = input("Nombre del módulo: ")  #solicita el nombre del módulo
        descripcion = input("Descripción: ")  #solicita la descripción del módulo
        nuevo = {  #crea el diccionario del nuevo módulo
            "id_modulo": generar_id(modulos, "id_modulo"),
            "id_unidad": unidad["id_unidad"],
            "id_salon": unidad.get("id_salon"),
            "nombre_salon": unidad.get("nombre_salon"),
            "turno": unidad.get("turno"),
            "id_plantilla": unidad["id_plantilla"],
            "nombre_plantilla": unidad["nombre_plantilla"],
            "id_carrera": unidad["id_carrera"],
            "nombre_carrera": unidad["nombre_carrera"],
            "nombre_unidad": unidad["nombre_unidad"],
            "nombre_modulo": nombre,
            "descripcion": descripcion,
            "orden": i,
            "estado": "Activo"}
        modulos.append(nuevo)  #agrega el módulo a la lista
        print(f"Módulo agregado: {nombre}")
    guardar_json(RUTA_MODULOS, modulos)  #guarda los módulos en el archivo json
    print("\nMódulos registrados correctamente.")

def ver_modulos():  #muestra los módulos registrados por carrera, plantilla, salón y unidad
    print("\n--- VER MÓDULOS ---")
    carreras = leer_json(RUTA_CARRERAS)  #carga las carreras registradas
    plantillas = leer_json(RUTA_PLANTILLAS)  #carga las plantillas registradas
    salones = leer_json(RUTA_SALONES)  #carga los salones registrados
    unidades = leer_json(RUTA_UNIDADES)  #carga las unidades registradas
    modulos = leer_json(RUTA_MODULOS)  #carga los módulos registrados
    if len(modulos) == 0:  #valida si existen módulos registrados
        print("No hay módulos registrados.")
        return
    mostrar_carreras(carreras)  #muestra las carreras disponibles
    id_carrera = int(input("\nIngrese ID de carrera: "))  #solicita el id de la carrera
    mostrar_plantillas(plantillas, id_carrera)  #muestra las plantillas de la carrera
    id_plantilla = int(input("\nIngrese ID de plantilla: "))  #solicita el id de la plantilla
    mostrar_salones(salones, id_carrera)  #muestra los salones de la carrera
    id_salon = int(input("\nIngrese ID de salón: "))  #solicita el id del salón
    mostrar_unidades(unidades, id_salon, id_plantilla)  #muestra las unidades disponibles
    id_unidad = int(input("\nIngrese ID de unidad: "))  #solicita el id de la unidad
    print("\n--- MÓDULOS DE LA UNIDAD ---")
    encontrados = 0  #cuenta cuántos módulos se encontraron
    for m in modulos:
        if (m["estado"] == "Activo"
            and m["id_unidad"] == id_unidad):
            encontrados += 1
            print("\n-----------------------------")
            print(f"ID: {m['id_modulo']}")
            print(f"Módulo: {m['nombre_modulo']}")
            print(f"Unidad: {m['nombre_unidad']}")
            print(f"Salón: {m.get('nombre_salon')}")
            print(f"Turno: {m.get('turno')}")
            print(f"Descripción: {m['descripcion']}")
    input()  #pausa la pantalla antes de volver al menú
    if encontrados == 0:
        print("No hay módulos para esta unidad.")