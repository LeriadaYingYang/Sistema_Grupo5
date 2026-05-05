from basedatos_json import leer_json, guardar_json, generar_id

RUTA_UNIDADES = "datos/unidades.json"
RUTA_MODULOS = "datos/modulos.json"
RUTA_TABLILLAS = "datos/tablillas_notas.json"
RUTA_ALUMNOS = "datos/alumnos.json"
RUTA_ASIGNACIONES = "datos/alumnos_asignaciones.json"
RUTA_NOTAS = "datos/notas_alumnos.json"
RUTA_CARRERAS = "datos/carreras.json"
RUTA_PLANTILLAS = "datos/plantillas_academicas.json"
RUTA_SALONES = "datos/salones.json"

def buscar_por_id(lista, campo_id, valor_id):
    for item in lista:
        if item[campo_id] == valor_id and item["estado"] == "Activo":
            return item
    return None

def mostrar_carreras(carreras):
    print("\n=== CARRERAS ===")
    for c in carreras:
        if c["estado"] == "Activo":
            print(f"ID: {c['id_carrera']} | {c['nombre']}")

def mostrar_plantillas(plantillas, id_carrera):
    print("\n=== PLANTILLAS ===")
    for p in plantillas:
        if p["estado"] == "Activo" and p["id_carrera"] == id_carrera:
            print(f"ID: {p['id_plantilla']} | {p['nombre_plantilla']}")

def mostrar_salones(salones, id_carrera):
    print("\n=== SALONES ===")
    for s in salones:
        if s["estado"] == "Activo" and s["id_carrera"] == id_carrera:
            print(f"ID: {s['id_salon']} | {s['nombre_salon']} | {s['turno']}")

def mostrar_unidades(unidades, id_salon, id_plantilla):
    print("\n=== UNIDADES ===")
    for u in unidades:
        if (
            u["estado"] == "Activo"
            and u.get("id_salon") == id_salon
            and u.get("id_plantilla") == id_plantilla):
            print(f"ID: {u['id_unidad']} | {u['nombre_unidad']}")

def mostrar_modulos(modulos, id_unidad):
    print("\n=== MÓDULOS ===")
    for m in modulos:
        if m["estado"] == "Activo" and m["id_unidad"] == id_unidad:
            print(f"ID: {m['id_modulo']} | {m['nombre_modulo']}")

def mostrar_alumnos_por_salon(alumnos, asignaciones, id_salon):
    print("\n=== ALUMNOS DEL SALÓN ===")

    for a in asignaciones:
        if a["estado"] == "Activo" and a["id_salon"] == id_salon:
            alumno = buscar_por_id(alumnos, "id_alumno", a["id_alumno"])
            if alumno:
                print(
                    f"ID: {alumno['id_alumno']} | "
                    f"{alumno['nombres']} {alumno['apellidos']}")

def obtener_tablilla(tablillas, id_unidad, id_modulo):
    for t in tablillas:
        if t["id_unidad"] == id_unidad and t["id_modulo"] == id_modulo and t["estado"] == "Activo":
            return t
    return None

def buscar_nota_existente(notas, id_alumno, id_unidad, id_modulo):
    for r in notas:
        if (
            r["id_alumno"] == id_alumno
            and r["id_unidad"] == id_unidad
            and r["id_modulo"] == id_modulo
            and r["estado"] == "Activo"):
            return r
    return None

def pedir_nota(nombre):
    while True:
        try:
            n = float(input(f"Ingrese nota para {nombre}: "))
            if 0 <= n <= 20:
                return n
        except:
            pass
        print("Nota inválida.")

def calcular_promedio(notas):
    validas = [n["nota"] for n in notas if n["nota"] != ""]
    if not validas:
        return None
    return round(sum(validas) / len(validas))

def crear_registro(notas_guardadas, alumno, unidad, modulo, tablilla):
    lista = []

    for n in tablilla["notas"]:
        lista.append({
            "orden": n["orden"],
            "nombre_nota": n["nombre_nota"],
            "nota": ""})

    nuevo = {
        "id_registro_nota": generar_id(notas_guardadas, "id_registro_nota"),
        "id_alumno": alumno["id_alumno"],
        "nombre_alumno": alumno["nombres"] + " " + alumno["apellidos"],
        "id_carrera": unidad["id_carrera"],
        "id_salon": unidad["id_salon"],
        "id_unidad": unidad["id_unidad"],
        "id_modulo": modulo["id_modulo"],
        "notas": lista,
        "promedio_modulo": None,
        "estado": "Activo"}

    notas_guardadas.append(nuevo)
    return nuevo

def registrar_modificar_notas():

    carreras = leer_json(RUTA_CARRERAS)
    plantillas = leer_json(RUTA_PLANTILLAS)
    salones = leer_json(RUTA_SALONES)
    unidades = leer_json(RUTA_UNIDADES)
    modulos = leer_json(RUTA_MODULOS)
    alumnos = leer_json(RUTA_ALUMNOS)
    asignaciones = leer_json(RUTA_ASIGNACIONES)
    tablillas = leer_json(RUTA_TABLILLAS)
    notas = leer_json(RUTA_NOTAS)

    print("\n=== REGISTRAR / MODIFICAR NOTAS ===")

    mostrar_carreras(carreras)
    id_carrera = int(input("ID carrera: "))

    mostrar_plantillas(plantillas, id_carrera)
    id_plantilla = int(input("ID plantilla: "))

    mostrar_salones(salones, id_carrera)
    id_salon = int(input("ID salón: "))

    mostrar_unidades(unidades, id_salon, id_plantilla)
    id_unidad = int(input("ID unidad: "))

    unidad = buscar_por_id(unidades, "id_unidad", id_unidad)

    mostrar_modulos(modulos, id_unidad)
    id_modulo = int(input("ID módulo: "))

    modulo = buscar_por_id(modulos, "id_modulo", id_modulo)

    tablilla = obtener_tablilla(tablillas, id_unidad, id_modulo)
    if tablilla is None:
        print("Primero cree la tablilla.")
        return

    mostrar_alumnos_por_salon(alumnos, asignaciones, id_salon)
    id_alumno = int(input("ID alumno: "))

    alumno = buscar_por_id(alumnos, "id_alumno", id_alumno)

    registro = buscar_nota_existente(notas, id_alumno, id_unidad, id_modulo)

    if registro is None:
        registro = crear_registro(notas, alumno, unidad, modulo, tablilla)

    print("\n=== NOTAS ===")
    while True:

        print("\n=== NOTAS ===")
        for n in registro["notas"]:
            valor = n["nota"] if n["nota"] != "" else "Sin nota"
            print(f"{n['orden']}. {n['nombre_nota']} → {valor}")

        try:
            orden = int(input("\nSeleccione número de nota: "))
        except ValueError:
            print("Debe ingresar un número.")
            continue

        nota_encontrada = False

        for n in registro["notas"]:
            if n["orden"] == orden:
                n["nota"] = pedir_nota(n["nombre_nota"])
                nota_encontrada = True
                break

        if not nota_encontrada:
            print("Número de nota inválido.")
            continue

        registro["promedio_modulo"] = calcular_promedio(registro["notas"])

        guardar_json(RUTA_NOTAS, notas)

        print("\nNota guardada")
        print("Promedio actual:", registro["promedio_modulo"])

        continuar = input("\n¿Desea modificar otra nota? (si/no): ").lower()

        if continuar != "si":
            print("Saliendo a gestión de notas...")
            break