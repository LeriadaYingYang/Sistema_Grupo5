from datetime import datetime, time
from basedatos_json import leer_json, guardar_json, generar_id
from director.utilidades import imprimir_titulo

RUTA_PLANTILLAS = "datos/plantillas_academicas.json"
RUTA_SALONES = "datos/salones.json"
RUTA_HORARIOS = "datos/horarios.json"
RUTA_ALUMNOS = "datos/alumnos.json"
RUTA_ASIGNACIONES = "datos/alumnos_asignaciones.json"
RUTA_ASISTENCIA_ALUMNOS = "datos/asistencia_alumnos.json"

def normalizar_hora(valor):
    try:
        valor = str(valor).strip().lower()
        # Caso 1: HH:MM correcto
        if ":" in valor and len(valor) <= 5:
            return datetime.strptime(valor, "%H:%M").time()
        # Caso 2: "8 a 9"
        if "a" in valor:
            inicio = valor.split("a")[0].strip()
            if inicio.isdigit():
                return datetime.strptime(f"{int(inicio):02d}:00", "%H:%M").time()
        # Caso 3: solo número
        if valor.isdigit():
            return datetime.strptime(f"{int(valor):02d}:00", "%H:%M").time()
        return None
    except:
        return None

def buscar_por_id(lista, campo_id, valor_id):
    for item in lista:
        if item[campo_id] == valor_id and item["estado"] == "Activo":
            return item
    return None

def mostrar_plantillas(plantillas):
    imprimir_titulo("PLANTILLAS DISPONIBLES")
    for p in plantillas:
        if p["estado"] == "Activo":
            print(f"ID: {p['id_plantilla']} | Carrera: {p['nombre_carrera']} | {p['nombre_plantilla']}")

def mostrar_salones(salones, id_carrera):
    imprimir_titulo("SALONES")
    for s in salones:
        if s["estado"] == "Activo" and s["id_carrera"] == id_carrera:
            print(f"ID: {s['id_salon']} | {s['nombre_salon']} | Turno: {s['turno']}")

def obtener_horario(horarios, id_plantilla, id_salon):
    for h in horarios:
        if h["estado"] == "Activo" and h["id_plantilla"] == id_plantilla and h["id_salon"] == id_salon:
            return h
    return None

def obtener_alumnos(alumnos, asignaciones, id_salon):
    resultado = []
    for a in asignaciones:
        if a["estado"] == "Activo" and a["id_salon"] == id_salon:
            alumno = buscar_por_id(alumnos, "id_alumno", a["id_alumno"])
            if alumno:
                resultado.append(alumno)
    return resultado

def asistencia_registrada(asistencias, id_alumno, fecha, id_horario, orden):
    for a in asistencias:
        if (
            a["estado"] == "Activo"
            and a["id_alumno"] == id_alumno
            and a["fecha"] == fecha
            and a["id_horario"] == id_horario
            and a["orden_dia"] == orden
        ):
            return True
    return False

def determinar_estado(hora_inicio):
    ahora = datetime.now().time()
    inicio_dt = normalizar_hora(hora_inicio)
    if inicio_dt is None:
        return "Error", datetime.now().strftime("%H:%M")
    # comparación directa entre time
    diferencia_min = (datetime.combine(datetime.today(), ahora) - datetime.combine(datetime.today(), inicio_dt)).total_seconds() / 60
    hora_actual = ahora.strftime("%H:%M")
    if diferencia_min <= 5:
        return "Presente", hora_actual
    else:
        return "Tardanza", hora_actual

def pedir_estado_manual():
    while True:
        print("\n1. Presente")
        print("2. Falta")
        print("3. Justificación")
        op = input("Estado: ")
        if op == "1":
            return "Presente"
        elif op == "2":
            return "Falta"
        elif op == "3":
            return "Justificación"
        else:
            print("Opción inválida")

def registrar_asistencia_alumnos():
    imprimir_titulo("REGISTRO DE ASISTENCIA ALUMNOS")
    plantillas = leer_json(RUTA_PLANTILLAS)
    salones = leer_json(RUTA_SALONES)
    horarios = leer_json(RUTA_HORARIOS)
    alumnos = leer_json(RUTA_ALUMNOS)
    asignaciones = leer_json(RUTA_ASIGNACIONES)
    asistencias = leer_json(RUTA_ASISTENCIA_ALUMNOS)
    mostrar_plantillas(plantillas)
    id_plantilla = int(input("ID plantilla: "))
    plantilla = buscar_por_id(plantillas, "id_plantilla", id_plantilla)
    mostrar_salones(salones, plantilla["id_carrera"])
    id_salon = int(input("ID salón: "))
    salon = buscar_por_id(salones, "id_salon", id_salon)
    horario = obtener_horario(horarios, id_plantilla, id_salon)
    for d in horario["dias_horas"]:
        print(f"{d['orden']}. {d['dia']} {d['hora_inicio']} - {d['hora_fin']}")
    orden = int(input("Seleccione día: "))
    dia = next(d for d in horario["dias_horas"] if d["orden"] == orden)
    fecha = input("Fecha (ENTER hoy): ")
    if fecha == "":
        fecha = datetime.now().strftime("%Y-%m-%d")
    alumnos_salon = obtener_alumnos(alumnos, asignaciones, id_salon)
    imprimir_titulo("ASISTENCIA")
    for al in alumnos_salon:
        if asistencia_registrada(asistencias, al["id_alumno"], fecha, horario["id_horario"], orden):
            print(f"{al['nombres']} ya registrado")
            continue
        print(f"\n{al['nombres']} {al['apellidos']}")
        estado_auto, hora_registro = determinar_estado(dia["hora_inicio"])
        print(f"Estado sugerido: {estado_auto}")
        usar_auto = input("Aceptar automático? (s/n): ")
        if usar_auto.lower() == "s":
            estado = estado_auto
        else:
            estado = pedir_estado_manual()
            hora_registro = datetime.now().strftime("%H:%M")
        asistencia = {
            "id_asistencia_alumno": generar_id(asistencias, "id_asistencia_alumno"),
            "fecha": fecha,
            "id_plantilla": plantilla["id_plantilla"],
            "id_salon": salon["id_salon"],
            "id_horario": horario["id_horario"],
            "orden_dia": orden,
            "id_alumno": al["id_alumno"],
            "nombre_alumno": al["nombres"] + " " + al["apellidos"],
            "asistencia": estado,
            "hora_registro": hora_registro,
            "estado": "Activo"
        }
        asistencias.append(asistencia)
    guardar_json(RUTA_ASISTENCIA_ALUMNOS, asistencias)
    print("\n Asistencia registrada correctamente")