from datetime import datetime
from basedatos_json import leer_json, guardar_json, generar_id
from director.utilidades import imprimir_titulo

RUTA_PROFESORES = "datos/profesores.json"
RUTA_PROFESORES_SALONES = "datos/profesores_salones.json"
RUTA_HORARIOS = "datos/horarios.json"
RUTA_ASISTENCIA_PROFESORES = "datos/asistencia_profesores.json"
RUTA_PLANTILLAS = "datos/plantillas_academicas.json"
RUTA_MODULOS = "datos/modulos.json"

def normalizar_hora(valor):
    try:
        valor = str(valor).strip().lower()
        # HH:MM
        if ":" in valor and len(valor) <= 5:
            return datetime.strptime(valor, "%H:%M").time()
        # "8 a 9"
        if "a" in valor:
            inicio = valor.split("a")[0].strip()
            if inicio.isdigit():
                return datetime.strptime(f"{int(inicio):02d}:00", "%H:%M").time()
        # "8"
        if valor.isdigit():
            return datetime.strptime(f"{int(valor):02d}:00", "%H:%M").time()
        return None
    except:
        return None

def hora_actual():
    return datetime.now().strftime("%H:%M")

def calcular_horas(h_inicio, h_fin):
    try:
        i = normalizar_hora(h_inicio)
        f = normalizar_hora(h_fin)
        if i is None or f is None:
            return 0
        diff = datetime.combine(datetime.today(), f) - datetime.combine(datetime.today(), i)
        return round(max(diff.total_seconds() / 3600, 0), 2)
    except:
        return 0

def determinar_estado(hora_programada, hora_real):
    try:
        prog = normalizar_hora(hora_programada)
        real = datetime.strptime(hora_real, "%H:%M").time()
        if prog is None:
            return "Error"
        minutos = (datetime.combine(datetime.today(), real) - datetime.combine(datetime.today(), prog)).total_seconds() / 60
        return "Presente" if minutos <= 5 else "Tardanza"
    except:
        return "Error"

def asistencia_ya_registrada(asistencias, id_profesor, fecha, id_horario, orden):
    for a in asistencias:
        if (a["estado"] == "Activo" and a["id_profesor"] == id_profesor
            and a["fecha"] == fecha and a["id_horario"] == id_horario and a["orden_dia"] == orden):
            return True
    return False

def registrar_asistencia_profesores():
    imprimir_titulo("ASISTENCIA PROFESORES")
    profesores = leer_json(RUTA_PROFESORES)
    asignaciones = leer_json(RUTA_PROFESORES_SALONES)
    plantillas = leer_json(RUTA_PLANTILLAS)
    horarios = leer_json(RUTA_HORARIOS)
    modulos = leer_json(RUTA_MODULOS)
    asistencias = leer_json(RUTA_ASISTENCIA_PROFESORES)
    if not profesores:
        print("No hay profesores registrados.")
        return
    for p in profesores:
        print(f"{p['id_profesor']} - {p['nombres']} {p['apellidos']}")
    id_profesor = int(input("ID profesor: "))
    asignaciones_prof = [
        a for a in asignaciones
        if a["id_profesor"] == id_profesor and a["estado"] == "Activo"
    ]
    id_plantilla = int(input("ID plantilla: "))
    plantilla = next(
        (p for p in plantillas if p["id_plantilla"] == id_plantilla),
        None
    )
    if not plantilla:
        print("Plantilla inválida")
        return
    id_salon = int(input("ID salón: "))
    horario = next(
        (h for h in horarios if h["id_plantilla"] == id_plantilla and h["id_salon"] == id_salon),None)
    if not horario:
        print("Sin horario")
        return
    for d in horario["dias_horas"]:
        print(f"{d['orden']} - {d['dia']} {d['hora_inicio']}")
    orden = int(input("Seleccione día: "))
    dia = next(
        (d for d in horario["dias_horas"] if d["orden"] == orden),
        None
    )
    if not dia:
        print("Día inválido")
        return
    fecha = input("Fecha (ENTER hoy): ")
    if fecha == "":
        fecha = datetime.now().strftime("%Y-%m-%d")
    hora_real_entrada = hora_actual()
    estado = determinar_estado(dia["hora_inicio"], hora_real_entrada)
    if estado == "Error":
        estado = "Tardanza"
    print(f"Estado automático: {estado}")
    modulo = int(input("ID módulo: "))
    mod = next(
        (m for m in modulos if m["id_modulo"] == modulo),
        None
    )
    if asistencia_ya_registrada(asistencias, id_profesor, fecha, horario["id_horario"], orden):
        print("Ya registrado")
        return
    input("Presione ENTER para registrar salida...")
    hora_real_salida = hora_actual()
    horas = calcular_horas(hora_real_entrada, hora_real_salida)
    asistencia = {
        "id_asistencia_profesor": generar_id(asistencias, "id_asistencia_profesor"),
        "fecha": fecha,
        "id_profesor": id_profesor,
        "hora_entrada": hora_real_entrada,
        "hora_salida": hora_real_salida,
        "estado": estado,
        "horas_trabajadas": horas,
        "id_horario": horario["id_horario"],
        "orden_dia": orden,
        "estado_registro": "Activo"
    }
    asistencias.append(asistencia)
    guardar_json(RUTA_ASISTENCIA_PROFESORES, asistencias)
    print("\nRegistro completado")
    print(f" Horas trabajadas: {horas}")