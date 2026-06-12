from basedatos_json import leer_json
from director.utilidades import imprimir_titulo

RUTA_NOTAS = "datos/notas_alumnos.json"
RUTA_CARRERAS = "datos/carreras.json"
RUTA_UNIDADES = "datos/unidades.json"
RUTA_MODULOS = "datos/modulos.json"
RUTA_SALONES = "datos/salones.json"
RUTA_PLANTILLAS = "datos/plantillas_academicas.json"

def calcular_promedio(lista):  #calcula el promedio de una lista
    if len(lista) == 0:
        return None
    return round(sum(lista) / len(lista))

def obtener_condicion(promedio):  #obtiene la condición según el promedio
    if promedio is None:
        return ""
    if promedio >= 18:
        return "A"
    elif promedio >= 15:
        return "B"
    elif promedio >= 13:
        return "C"
    elif promedio >= 11:
        return "D"
    else:
        return "DESAPROBADO"

def buscar_por_id(lista, campo_id, valor_id):  #busca un registro activo por su id
    for item in lista:
        if item[campo_id] == valor_id and item["estado"] == "Activo":
            return item
    return None

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

def mostrar_unidades(unidades, id_salon, id_plantilla):  #muestra unidades del salón
    imprimir_titulo("UNIDADES DEL SALÓN")
    encontrados = 0
    for unidad in unidades:
        if (
            unidad["estado"] == "Activo"
            and unidad.get("id_salon") == id_salon
            and unidad.get("id_plantilla") == id_plantilla):
            encontrados += 1
            print(f"ID: {unidad['id_unidad']} | {unidad['nombre_unidad']}")
    if encontrados == 0:
        print("No hay unidades para este salón y plantilla.")

def obtener_modulos(modulos, id_unidad):  #obtiene módulos de la unidad
    resultado = []
    for modulo in modulos:
        if modulo["estado"] == "Activo" and modulo["id_unidad"] == id_unidad:
            resultado.append(modulo)
    return sorted(resultado, key=lambda x: x.get("orden", x["id_modulo"]))

def buscar_registro(notas, id_alumno, id_unidad, id_modulo):  #busca registro de notas
    for registro in notas:
        if (
            registro["estado"] == "Activo"
            and registro["id_alumno"] == id_alumno
            and registro["id_unidad"] == id_unidad
            and registro["id_modulo"] == id_modulo):
            return registro
    return None

def obtener_alumnos(notas, id_carrera, id_salon, id_unidad):  #obtiene alumnos con notas
    alumnos = []
    for registro in notas:
        if (
            registro["estado"] == "Activo"
            and registro["id_carrera"] == id_carrera
            and registro.get("id_salon") == id_salon
            and registro["id_unidad"] == id_unidad):
            alumno = {
                "id_alumno": registro["id_alumno"],
                "nombre_alumno": registro["nombre_alumno"]}
            if alumno not in alumnos:
                alumnos.append(alumno)
    return alumnos

def ver_notas_por_unidad():  #muestra el reporte de notas por unidad
    carreras = leer_json(RUTA_CARRERAS)
    plantillas = leer_json(RUTA_PLANTILLAS)
    salones = leer_json(RUTA_SALONES)
    unidades = leer_json(RUTA_UNIDADES)
    modulos = leer_json(RUTA_MODULOS)
    notas = leer_json(RUTA_NOTAS)
    if len(notas) == 0:
        print("No hay notas registradas.")
        return
    mostrar_carreras(carreras)
    try:
        id_carrera = int(input("\nIngrese ID de carrera: "))
    except ValueError:
        print("Debe ingresar un número.")
        return
    carrera = buscar_por_id(carreras, "id_carrera", id_carrera)
    if carrera is None:
        print("Carrera no encontrada.")
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
    modulos_unidad = obtener_modulos(modulos, id_unidad)
    alumnos = obtener_alumnos(notas, id_carrera, id_salon, id_unidad)
    if len(alumnos) == 0:
        print("No hay alumnos con notas registradas.")
        return
    print("\n--- ALUMNOS CON NOTAS ---")
    for alumno in alumnos:
        print(f"ID: {alumno['id_alumno']} | {alumno['nombre_alumno']}")
    try:
        id_alumno_elegido = int(input("\nIngrese ID del alumno para ver sus notas: "))
    except ValueError:
        print("Debe ingresar un número.")
        return
    alumno_elegido = None
    for alumno in alumnos:
        if alumno["id_alumno"] == id_alumno_elegido:
            alumno_elegido = alumno
            break
    if alumno_elegido is None:
        print("Alumno no válido.")
        return
    print("\n--- REPORTE DE NOTAS ---")
    print(f"Carrera: {carrera['nombre']}")
    print(f"Plantilla: {plantilla['nombre_plantilla']}")
    print(f"Salón: {salon['nombre_salon']}")
    print(f"Turno: {salon['turno']}")
    print(f"Unidad: {unidad['nombre_unidad']}")
    print("\n-----------------------------")
    print(f"Alumno: {alumno_elegido['nombre_alumno']}")
    promedios = []
    for modulo in modulos_unidad:
        registro = buscar_registro(
            notas,
            alumno_elegido["id_alumno"],
            id_unidad,
            modulo["id_modulo"])
        print(f"\nMódulo: {modulo['nombre_modulo']}")
        if registro is None:
            print("Sin notas.")
            continue
        for nota in registro["notas"]:
            valor = nota["nota"] if nota["nota"] != "" else "Sin nota"
            print(f"  {nota['nombre_nota']}: {valor}")
        print(f"  Promedio: {registro['promedio_modulo']}")
        if registro["promedio_modulo"] is not None:
            promedios.append(registro["promedio_modulo"])
    promedio_final = calcular_promedio(promedios)
    condicion = obtener_condicion(promedio_final)
    print(f"\n>>> PROMEDIO FINAL: {promedio_final}")
    print(f">>> CONDICIÓN: {condicion}")