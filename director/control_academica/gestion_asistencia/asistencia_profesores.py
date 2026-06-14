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
        if ":" in valor and len(valor) <= 5:
            return datetime.strptime(valor, "%H:%M").time()
        if "a" in valor:
            inicio = valor.split("a")[0].strip()
            if inicio.isdigit():
                return datetime.strptime(f"{int(inicio):02d}:00","%H:%M").time()
        if valor.isdigit():
            return datetime.strptime(f"{int(valor):02d}:00","%H:%M").time()
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
        diferencia = (datetime.combine(datetime.today(), f) - datetime.combine(datetime.today(), i))
        return round(max(diferencia.total_seconds() / 3600, 0),2)
    except:
        return 0


def determinar_estado(hora_programada, hora_real):
    try:
        prog = normalizar_hora(hora_programada)
        real = datetime.strptime(hora_real,"%H:%M").time()
        if prog is None:
            return "Error"
        minutos = (datetime.combine(datetime.today(), real)- datetime.combine(datetime.today(), prog)).total_seconds() / 60
        if minutos <= 5:
            return "Presente"
        return "Tardanza"
    except:
        return "Error"


def asistencia_ya_registrada(asistencias,id_profesor,fecha,id_horario,orden):
    for a in asistencias:
        estado_registro = (a.get("estado_registro") or a.get("estado"))
        if (
            estado_registro == "Activo"
            and a.get("id_profesor") == id_profesor
            and a.get("fecha") == fecha
            and a.get("id_horario") == id_horario
            and a.get("orden_dia") == orden
        ):
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
    print("\nPROFESORES")
    for p in profesores:
        if p.get("estado") == "Activo":
            print(
                f"{p['id_profesor']} - "
                f"{p['nombres']} {p['apellidos']}"
            )
    try:
        id_profesor = int(input("\nID profesor: "))
    except ValueError:
        print("ID inválido.")
        return
    profesor = next(
        (p for p in profesores if p["id_profesor"] == id_profesor),None)
    if not profesor:
        print("Profesor no encontrado.")
        return
    asignaciones_prof = [a for a in asignaciones if a["id_profesor"] == id_profesor and a["estado"] == "Activo"]
    if not asignaciones_prof:
        print("Profesor sin asignaciones.")
        return
    try:
        id_plantilla = int(input("ID plantilla: "))
    except ValueError:
        print("ID inválido.")
        return
    plantilla = next(
        (p for p in plantillas if p["id_plantilla"] == id_plantilla),None)
    if not plantilla:
        print("Plantilla inválida.")
        return
    try:
        id_salon = int(input("ID salón: "))
    except ValueError:
        print("ID inválido.")
        return
    horario = next(
        (h for h in horarios if h["id_plantilla"] == id_plantilla and h["id_salon"] == id_salon),None)
    if not horario:
        print("Horario no encontrado.")
        return
    print("\nHORARIOS")
    for d in horario["dias_horas"]:
        print(
            f"{d['orden']} - "
            f"{d['dia']} "
            f"{d['hora_inicio']}"
        )
    try:
        orden = int(input("Seleccione día: "))
    except ValueError:
        print("Valor inválido.")
        return
    dia = next(
        (d for d in horario["dias_horas"] if d["orden"] == orden),None)
    if not dia:
        print("Día inválido.")
        return
    fecha = input(
        "Fecha (ENTER hoy): ").strip()
    if fecha == "":
        fecha = datetime.now().strftime("%Y-%m-%d")
    if asistencia_ya_registrada(asistencias,id_profesor,fecha,horario["id_horario"],orden):
        print("Ya existe asistencia registrada.")
        return
    hora_real_entrada = hora_actual()
    estado_sugerido = determinar_estado(dia["hora_inicio"],hora_real_entrada)
    if estado_sugerido == "Error":
        estado_sugerido = "Tardanza"
    print(
        f"\nEstado sugerido: "
        f"{estado_sugerido}"
    )
    print("\nSeleccione estado:")
    print("1. Presente")
    print("2. Tardanza")
    print("3. Falta")
    print("4. Justificación")
    op = input("Opción: ")
    if op == "1":
        estado = "Presente"
    elif op == "2":
        estado = "Tardanza"
    elif op == "3":
        estado = "Falta"
    elif op == "4":
        estado = "Justificación"
    else:
        print("Opción inválida.")
        return
    justificacion = ""
    if estado == "Justificación":
        justificacion = input("Motivo de la justificación: ")
    try:
        id_modulo = int(input("ID módulo: "))
    except ValueError:
        print("ID inválido.")
        return

    modulo = next(
        (m for m in modulos if m["id_modulo"] == id_modulo),None)
    if not modulo:
        print("Módulo no encontrado.")
        return
    if estado == "Falta":
        hora_real_salida = "-"
        horas = 0
    else:
        input(
            "\nPresione ENTER para registrar salida...")
        hora_real_salida = hora_actual()
        horas = calcular_horas(hora_real_entrada,hora_real_salida)
    asistencia = {
        "id_asistencia_profesor":
        generar_id(asistencias,"id_asistencia_profesor"),
        "fecha": fecha,
        "id_profesor":
        profesor["id_profesor"],
        "nombre_profesor":profesor["nombres"]+ " "+ profesor["apellidos"],
        "id_modulo":modulo["id_modulo"],
        "nombre_modulo":modulo.get("nombre_modulo",""),
        "hora_entrada":hora_real_entrada,
        "hora_salida":hora_real_salida,
        "estado":estado,
        "justificacion":justificacion,
        "horas_trabajadas":horas,
        "id_horario":horario["id_horario"],
        "orden_dia":orden,
        "estado_registro":"Activo"}
    asistencias.append(asistencia)
    guardar_json(RUTA_ASISTENCIA_PROFESORES,asistencias)
    print("\nRegistro completado")
    print(f"Profesor: {asistencia['nombre_profesor']}")
    print(f"Estado: {estado}")
    print(f"Horas trabajadas: {horas}")
