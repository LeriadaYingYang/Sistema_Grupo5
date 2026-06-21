from datetime import datetime
from basedatos_json import leer_json, guardar_json, generar_id
from director.utilidades import imprimir_titulo

RUTA_PROFESORES = "datos/profesores.json"
RUTA_PROFESORES_SALONES = "datos/profesores_salones.json"
RUTA_HORARIOS = "datos/horarios.json"
RUTA_ASISTENCIA_PROFESORES = "datos/asistencia_profesores.json"
RUTA_PLANTILLAS = "datos/plantillas_academicas.json"
RUTA_MODULOS = "datos/modulos.json"


def validar_entero(mensaje):
    while True:
        try:
            return int(input(mensaje).strip())
        except ValueError:
            print("Debe ingresar un número válido.")


def validar_fecha():
    while True:
        fecha = input("Fecha (YYYY-MM-DD) [ENTER=hoy]: ").strip()
        if fecha == "":
            return datetime.now().strftime("%Y-%m-%d")
        try:
            datetime.strptime(fecha, "%Y-%m-%d")
            return fecha
        except ValueError:
            print("Formato inválido.")


def normalizar_hora(valor):
    try:
        valor = str(valor).strip().lower()
        if ":" in valor and len(valor) <= 5:
            return datetime.strptime(valor,"%H:%M").time()
        if "a" in valor:
            inicio = valor.split("a")[0].strip()
            if inicio.isdigit():
                return datetime.strptime(f"{int(inicio):02d}:00","%H:%M").time()
        if valor.isdigit():
            return datetime.strptime(f"{int(valor):02d}:00","%H:%M").time()
        return None
    except Exception:
        return None


def hora_actual():
    return datetime.now().strftime("%H:%M")


def calcular_horas(h_inicio, h_fin):
    try:
        inicio = normalizar_hora(h_inicio)
        fin = normalizar_hora(h_fin)
        if inicio is None or fin is None:
            return 0
        diferencia = (datetime.combine(datetime.today(), fin)
            - datetime.combine(datetime.today(), inicio))
        return round(
            max(diferencia.total_seconds() / 3600,0),2)
    except Exception:
        return 0


def determinar_estado(hora_programada,hora_real):
    try:
        programada = normalizar_hora(hora_programada)
        real = datetime.strptime(hora_real,"%H:%M").time()
        if programada is None:
            return "Error"
        diferencia = (datetime.combine(datetime.today(), real)
            - datetime.combine(datetime.today(), programada)).total_seconds() / 60
        if diferencia <= 5:
            return "Presente"
        return "Tardanza"
    except Exception:
        return "Error"


def asistencia_ya_registrada(asistencias,id_profesor,fecha,id_horario,orden):
    for a in asistencias:
        if (a.get("estado_registro") == "Activo"
            and a.get("id_profesor") == id_profesor
            and a.get("fecha") == fecha
            and a.get("id_horario") == id_horario
            and a.get("orden_dia") == orden):
            return True
    return False


def registrar_asistencia_profesores():
    imprimir_titulo("ASISTENCIA PROFESORES")
    try:
        profesores = leer_json(RUTA_PROFESORES) or []
        asignaciones = leer_json(RUTA_PROFESORES_SALONES) or []
        plantillas = leer_json(RUTA_PLANTILLAS) or []
        horarios = leer_json(RUTA_HORARIOS) or []
        modulos = leer_json(RUTA_MODULOS) or []
        asistencias = leer_json(RUTA_ASISTENCIA_PROFESORES) or []
    except Exception as e:
        print(f"Error al cargar datos: {e}")
        return
    if not profesores:
        print("No hay profesores registrados.")
        return
    print("\nPROFESORES")
    for p in profesores:
        if p.get("estado") == "Activo":
            print(
                f"{p.get('id_profesor')} - "
                f"{p.get('nombres')} "
                f"{p.get('apellidos')}"
            )
    id_profesor = validar_entero("\nID profesor: ")
    profesor = next(
        (p for p in profesores
            if p.get("id_profesor")== id_profesor and p.get("estado")== "Activo"),None)
    if not profesor:
        print("Profesor inválido.")
        return
    asignaciones_prof = [
        a for a in asignaciones
        if (a.get("id_profesor") == id_profesor and a.get("estado") == "Activo")]
    if not asignaciones_prof:
        print("El profesor no tiene asignaciones activas.")
        return
    id_plantilla = validar_entero("ID plantilla: ")
    plantilla = next(
        (p for p in plantillas
            if p.get("id_plantilla")
            == id_plantilla and p.get("estado") == "Activo"),None)
    if not plantilla:
        print("Plantilla inválida.")
        return
    id_salon = validar_entero("ID salón: ")
    salon_asignado = any(a.get("id_salon") == id_salon
        for a in asignaciones_prof)
    if not salon_asignado:
        print("El profesor no está asignado a este salón.")
        return
    horario = next(
        (h for h in horarios
            if h.get("id_plantilla") == id_plantilla
            and h.get("id_salon") == id_salon
            and h.get("estado") == "Activo"),None)
    if not horario:
        print("Sin horario.")
        return
    dias_horas = horario.get("dias_horas",[])
    if not dias_horas:
        print("El horario no tiene días.")
        return
    print("\nDÍAS")
    for d in dias_horas:
        print(f"{d.get('orden')} - "
            f"{d.get('dia')} "
            f"{d.get('hora_inicio')}")
    orden = validar_entero("Seleccione día: ")
    dia = next(
        (d for d in dias_horas
            if d.get("orden") == orden),None)
    if not dia:
        print("Día inválido.")
        return
    fecha = validar_fecha()
    hora_real_entrada = hora_actual()
    estado = determinar_estado(dia.get("hora_inicio"),hora_real_entrada)
    if estado == "Error":
        estado = "Tardanza"
    print(f"\nEstado automático: {estado}")
    print("\nMÓDULOS")
    for m in modulos:
        if m.get("estado") == "Activo":
            print(f"{m.get('id_modulo')} - "
                f"{m.get('nombre_modulo')}")
    id_modulo = validar_entero("ID módulo: ")
    modulo = next(
        (m for m in modulos
            if m.get("id_modulo") == id_modulo
            and m.get("estado") == "Activo"),None)
    if not modulo:
        print("Módulo inválido.")
        return
    if asistencia_ya_registrada(asistencias,id_profesor,
        fecha,horario.get("id_horario"),orden):
        print("La asistencia ya fue registrada.")
        return
    input("\nPresione ENTER para registrar salida...")
    hora_real_salida = hora_actual()
    horas = calcular_horas(hora_real_entrada,hora_real_salida)
    asistencia = {
        "id_asistencia_profesor":
            generar_id(asistencias,"id_asistencia_profesor"),
        "fecha": fecha,
        "id_profesor":id_profesor,
        "nombre_profesor":
            f"{profesor.get('nombres')} "
            f"{profesor.get('apellidos')}",
        "id_modulo":id_modulo,
        "id_horario":horario.get("id_horario"),
        "orden_dia":orden,
        "hora_entrada":hora_real_entrada,
        "hora_salida":hora_real_salida,
        "estado":estado,
        "horas_trabajadas":horas,
        "estado_registro":"Activo"}
    asistencias.append(asistencia)
    try:
        guardar_json(RUTA_ASISTENCIA_PROFESORES,asistencias)
        print("\nRegistro completado.")
        print(f"Horas trabajadas: "
            f"{horas}")
    except Exception as e:
        print(f"Error al guardar: {e}")