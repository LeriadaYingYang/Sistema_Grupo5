from basedatos_json import leer_json, guardar_json, generar_id

RUTA_UNIDADES = "datos/unidades.json"
RUTA_MODULOS = "datos/modulos.json"
RUTA_SALONES = "datos/salones.json"
RUTA_CARRERAS = "datos/carreras.json"
RUTA_PLANTILLAS = "datos/plantillas_academicas.json"

def buscar_por_id(lista, campo_id, valor_id):
    for item in lista:
        if item[campo_id] == valor_id and item["estado"] == "Activo":
            return item
    return None

def unidad_ya_tiene_modulos(modulos, id_unidad):
    for m in modulos:
        if (
            m["estado"] == "Activo"
            and m["id_unidad"] == id_unidad):
            return True
    return False

def mostrar_carreras(carreras):
    print("\n=== CARRERAS DISPONIBLES ===")
    for c in carreras:
        if c["estado"] == "Activo":
            print(f"ID: {c['id_carrera']} | {c['nombre']}")

def mostrar_plantillas(plantillas, id_carrera):
    print("\n=== PLANTILLAS DE LA CARRERA ===")
    for p in plantillas:
        if p["estado"] == "Activo" and p["id_carrera"] == id_carrera:
            print(f"ID: {p['id_plantilla']} | {p['nombre_plantilla']}")

def mostrar_salones(salones, id_carrera):
    print("\n=== SALONES DE LA CARRERA ===")
    for s in salones:
        if s["estado"] == "Activo" and s["id_carrera"] == id_carrera:
            print(
                f"ID: {s['id_salon']} | "
                f"{s['nombre_salon']} | {s['turno']}")

def mostrar_unidades(unidades, id_salon, id_plantilla):
    print("\n=== UNIDADES DEL SALÓN Y PLANTILLA ===")

    encontrados = 0

    for u in unidades:
        if (
            u["estado"] == "Activo"
            and u.get("id_salon") == id_salon
            and u.get("id_plantilla") == id_plantilla):
            encontrados += 1
            print(f"ID: {u['id_unidad']} | {u['nombre_unidad']}")

    if encontrados == 0:
        print("No hay unidades para este salón y plantilla.")

def registrar_modulo():
    print("\n=== REGISTRAR MÓDULOS ===")

    carreras = leer_json(RUTA_CARRERAS)
    plantillas = leer_json(RUTA_PLANTILLAS)
    salones = leer_json(RUTA_SALONES)
    unidades = leer_json(RUTA_UNIDADES)
    modulos = leer_json(RUTA_MODULOS)

    if len(unidades) == 0:
        print("Primero debe registrar unidades.")
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

    salon = buscar_por_id(salones, "id_salon", id_salon)

    if salon is None or salon["id_carrera"] != id_carrera:
        print("Salón no válido.")
        return

    mostrar_unidades(unidades, id_salon, id_plantilla)

    try:
        id_unidad = int(input("\nIngrese ID de unidad: "))
    except ValueError:
        print("Debe ingresar un número.")
        return

    unidad = buscar_por_id(unidades, "id_unidad", id_unidad)

    if (
        unidad is None
        or unidad.get("id_salon") != id_salon
        or unidad.get("id_plantilla") != id_plantilla):
        print("Unidad no válida.")
        return

    if unidad_ya_tiene_modulos(modulos, id_unidad):
        print("Esta unidad ya tiene módulos registrados.")
        return

    while True:
        try:
            cantidad = int(input("¿Cuántos módulos desea crear?: "))
            if cantidad > 0:
                break
            print("Debe ser mayor a 0.")
        except ValueError:
            print("Ingrese un número válido.")

    for i in range(1, cantidad + 1):
        print(f"\n--- Módulo {i} ---")

        nombre = input("Nombre del módulo: ")
        descripcion = input("Descripción: ")

        nuevo = {
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
            "estado": "Activo"
        }

        modulos.append(nuevo)
        print(f"Módulo agregado: {nombre}")

    guardar_json(RUTA_MODULOS, modulos)

    print("\nMódulos registrados correctamente.")

def ver_modulos():
    print("\n=== VER MÓDULOS ===")

    carreras = leer_json(RUTA_CARRERAS)
    plantillas = leer_json(RUTA_PLANTILLAS)
    salones = leer_json(RUTA_SALONES)
    unidades = leer_json(RUTA_UNIDADES)
    modulos = leer_json(RUTA_MODULOS)

    if len(modulos) == 0:
        print("No hay módulos registrados.")
        return

    mostrar_carreras(carreras)
    id_carrera = int(input("\nIngrese ID de carrera: "))

    mostrar_plantillas(plantillas, id_carrera)
    id_plantilla = int(input("\nIngrese ID de plantilla: "))

    mostrar_salones(salones, id_carrera)
    id_salon = int(input("\nIngrese ID de salón: "))

    mostrar_unidades(unidades, id_salon, id_plantilla)
    id_unidad = int(input("\nIngrese ID de unidad: "))

    print("\n=== MÓDULOS DE LA UNIDAD ===")

    encontrados = 0

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

    if encontrados == 0:
        print("No hay módulos para esta unidad.")