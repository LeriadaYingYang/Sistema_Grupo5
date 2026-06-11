from basedatos_json import leer_json, guardar_json, generar_id
from director.utilidades import imprimir_titulo

RUTA_UNIDADES = "datos/unidades.json"
RUTA_MODULOS = "datos/modulos.json"
RUTA_TABLILLAS = "datos/tablillas_notas.json"
RUTA_ALUMNOS = "datos/alumnos.json"
RUTA_ASIGNACIONES = "datos/alumnos_asignaciones.json"
RUTA_NOTAS = "datos/notas_alumnos.json"
RUTA_CARRERAS = "datos/carreras.json"
RUTA_PLANTILLAS = "datos/plantillas_academicas.json"
RUTA_SALONES = "datos/salones.json"

def buscar_por_id(lista, campo_id, valor_id):  #busca un registro activo por su id
    for item in lista:
        if item[campo_id] == valor_id and item["estado"] == "Activo":
            return item
    return None

def mostrar_carreras(carreras):  #muestra carreras disponibles
    imprimir_titulo("CARRERAS")
    for carrera in carreras:
        if carrera["estado"] == "Activo":
            print(f"ID: {carrera['id_carrera']} | {carrera['nombre']}")

def mostrar_plantillas(plantillas, id_carrera):  #muestra plantillas de la carrera
    imprimir_titulo("PLANTILLAS")
    for plantilla in plantillas:
        if plantilla["estado"] == "Activo" and plantilla["id_carrera"] == id_carrera:
            print(f"ID: {plantilla['id_plantilla']} | {plantilla['nombre_plantilla']}")

def mostrar_salones(salones, id_carrera):  #muestra salones de la carrera
    imprimir_titulo("SALONES")
    for salon in salones:
        if salon["estado"] == "Activo" and salon["id_carrera"] == id_carrera:
            print(f"ID: {salon['id_salon']} | {salon['nombre_salon']} | {salon['turno']}")

def mostrar_unidades(unidades, id_salon, id_plantilla):  #muestra unidades disponibles
    imprimir_titulo("UNIDADES")
    for unidad in unidades:
        if (
            unidad["estado"] == "Activo"
            and unidad.get("id_salon") == id_salon
            and unidad.get("id_plantilla") == id_plantilla):
            print(f"ID: {unidad['id_unidad']} | {unidad['nombre_unidad']}")

def mostrar_modulos(modulos, id_unidad):  #muestra módulos de la unidad
    imprimir_titulo("MÓDULOS")
    for modulo in modulos:
        if modulo["estado"] == "Activo" and modulo["id_unidad"] == id_unidad:
            print(f"ID: {modulo['id_modulo']} | {modulo['nombre_modulo']}")

def mostrar_alumnos_por_salon(alumnos, asignaciones, id_salon):  #muestra alumnos del salón
    imprimir_titulo("ALUMNOS DEL SALÓN")
    for asignacion in asignaciones:
        if asignacion["estado"] == "Activo" and asignacion["id_salon"] == id_salon:
            alumno = buscar_por_id(alumnos, "id_alumno", asignacion["id_alumno"])
            if alumno:
                print(f"ID: {alumno['id_alumno']} | {alumno['nombres']} {alumno['apellidos']}")

def obtener_tablilla(tablillas, id_unidad, id_modulo):  #obtiene la tablilla del módulo
    for tablilla in tablillas:
        if (
            tablilla["id_unidad"] == id_unidad
            and tablilla["id_modulo"] == id_modulo
            and tablilla["estado"] == "Activo"):
            return tablilla
    return None

def buscar_nota_existente(notas, id_alumno, id_unidad, id_modulo):  #busca un registro existente
    for registro in notas:
        if (
            registro["id_alumno"] == id_alumno
            and registro["id_unidad"] == id_unidad
            and registro["id_modulo"] == id_modulo
            and registro["estado"] == "Activo"):
            return registro
    return None

def pedir_nota(nombre):  #solicita una nota válida
    while True:
        try:
            nota = float(input(f"Ingrese nota para {nombre}: "))
            if 0 <= nota <= 20:
                return nota
        except ValueError:
            pass
        print("Nota inválida.")

def calcular_promedio(notas):  #calcula promedio del módulo
    validas = [n["nota"] for n in notas if n["nota"] != ""]
    if len(validas) == 0:
        return None
    return round(sum(validas) / len(validas))

def crear_registro(notas_guardadas, alumno, unidad, modulo, tablilla):  #crea registro inicial de notas
    lista = []
    for nota in tablilla["notas"]:
        lista.append({
            "orden": nota["orden"],
            "nombre_nota": nota["nombre_nota"],
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

def registrar_modificar_notas():  #registra o modifica notas de alumnos
    carreras = leer_json(RUTA_CARRERAS)
    plantillas = leer_json(RUTA_PLANTILLAS)
    salones = leer_json(RUTA_SALONES)
    unidades = leer_json(RUTA_UNIDADES)
    modulos = leer_json(RUTA_MODULOS)
    alumnos = leer_json(RUTA_ALUMNOS)
    asignaciones = leer_json(RUTA_ASIGNACIONES)
    tablillas = leer_json(RUTA_TABLILLAS)
    notas = leer_json(RUTA_NOTAS)

    imprimir_titulo("REGISTRAR / MODIFICAR NOTAS")
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
    while True:
        imprimir_titulo("NOTAS")
        for nota in registro["notas"]:
            valor = nota["nota"] if nota["nota"] != "" else "Sin nota"
            print(f"{nota['orden']}. {nota['nombre_nota']} -> {valor}")
        try:
            orden = int(input("\nSeleccione número de nota: "))
        except ValueError:
            print("Debe ingresar un número.")
            continue
        nota_encontrada = False
        for nota in registro["notas"]:
            if nota["orden"] == orden:
                nota["nota"] = pedir_nota(nota["nombre_nota"])
                nota_encontrada = True
                break
        if not nota_encontrada:
            print("Número de nota inválido.")
            continue
        registro["promedio_modulo"] = calcular_promedio(registro["notas"])
        guardar_json(RUTA_NOTAS, notas)
        print("\nNota guardada.")
        print(f"Promedio actual: {registro['promedio_modulo']}")
        continuar = input("\n¿Desea modificar otra nota? (si/no): ").lower()
        if continuar != "si":
            print("Saliendo a gestión de notas...")
            break