from datetime import datetime
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
        if ":" in valor and len(valor) <= 5:
            return datetime.strptime(valor, "%H:%M").time()
        if "a" in valor:
            inicio = valor.split("a")[0].strip()
            if inicio.isdigit():
                return datetime.strptime(f"{int(inicio):02d}:00","%H:%M").time()
        if valor.isdigit():
            return datetime.strptime(f"{int(valor):02d}:00","%H:%M").time()
        return None
    except Exception:
        return None


def validar_entero(mensaje):
    while True:
        try:
            return int(input(mensaje).strip())
        except ValueError:
            print("Debe ingresar un número válido.")


def validar_fecha():
    while True:
        fecha = input("Fecha (YYYY-MM-DD) [ENTER = hoy]: ").strip()
        if fecha == "":
            return datetime.now().strftime("%Y-%m-%d")
        try:
            datetime.strptime(fecha, "%Y-%m-%d")
            return fecha
        except ValueError:
            print("Formato inválido. Use YYYY-MM-DD.")


def confirmar_si_no(mensaje):
    while True:
        respuesta = input(mensaje).strip().lower()
        if respuesta in ("s", "n"):
            return respuesta
        print("Ingrese solamente S o N.")


def buscar_por_id(lista, campo_id, valor_id):
    if not isinstance(lista, list):
        return None
    for item in lista:
        if (item.get(campo_id) == valor_id and item.get("estado") == "Activo"):
            return item
    return None


def mostrar_plantillas(plantillas):
    imprimir_titulo("PLANTILLAS DISPONIBLES")
    encontradas = False
    for p in plantillas:
        if p.get("estado") == "Activo":
            encontradas = True
            print(f"ID: {p.get('id_plantilla')} | "
                f"Carrera: {p.get('nombre_carrera')} | "
                f"{p.get('nombre_plantilla')}")
    if not encontradas:
        print("No existen plantillas activas.")


def mostrar_salones(salones, id_carrera):
    imprimir_titulo("SALONES")
    encontrados = False
    for s in salones:
        if (s.get("estado") == "Activo" and s.get("id_carrera") == id_carrera):
            encontrados = True
            print(f"ID: {s.get('id_salon')} | "
                f"{s.get('nombre_salon')} | "
                f"Turno: {s.get('turno')}")
    if not encontrados:
        print("No existen salones para esta carrera.")


def obtener_horario(horarios, id_plantilla, id_salon):
    if not isinstance(horarios, list):
        return None
    for h in horarios:
        if (h.get("estado") == "Activo"
            and h.get("id_plantilla") == id_plantilla
            and h.get("id_salon") == id_salon):
            return h
    return None


def obtener_alumnos(alumnos, asignaciones, id_salon):
    resultado = []
    for asignacion in asignaciones:
        if (asignacion.get("estado") == "Activo" and asignacion.get("id_salon") == id_salon):
            alumno = buscar_por_id(alumnos,"id_alumno",asignacion.get("id_alumno"))
            if alumno:
                resultado.append(alumno)
    return resultado


def asistencia_registrada(asistencias,id_alumno,fecha,id_horario,orden):
    for asistencia in asistencias:
        if (asistencia.get("estado") == "Activo"
            and asistencia.get("id_alumno") == id_alumno
            and asistencia.get("fecha") == fecha
            and asistencia.get("id_horario") == id_horario
            and asistencia.get("orden_dia") == orden):
            return True
    return False


def determinar_estado(hora_inicio):
    ahora = datetime.now().time()
    inicio_dt = normalizar_hora(hora_inicio)
    if inicio_dt is None:
        return "Error", datetime.now().strftime("%H:%M")
    diferencia_min = (datetime.combine(datetime.today(), ahora)
        - datetime.combine(datetime.today(), inicio_dt)).total_seconds() / 60
    hora_actual = ahora.strftime("%H:%M")
    if diferencia_min <= 5:
        return "Presente", hora_actual
    return "Tardanza", hora_actual


def pedir_estado_manual():
    while True:
        print("\n1. Presente")
        print("2. Falta")
        print("3. Justificación")
        opcion = input("Estado: ").strip()
        if opcion == "1":
            return "Presente"
        if opcion == "2":
            return "Falta"
        if opcion == "3":
            return "Justificación"
        print("Opción inválida.")


def registrar_asistencia_alumnos():
    imprimir_titulo("REGISTRO DE ASISTENCIA ALUMNOS")
    try:
        plantillas = leer_json(RUTA_PLANTILLAS) or []
        salones = leer_json(RUTA_SALONES) or []
        horarios = leer_json(RUTA_HORARIOS) or []
        alumnos = leer_json(RUTA_ALUMNOS) or []
        asignaciones = leer_json(RUTA_ASIGNACIONES) or []
        asistencias = leer_json(RUTA_ASISTENCIA_ALUMNOS) or []
    except Exception as e:
        print(f"Error al cargar archivos: {e}")
        return
    if not plantillas:
        print("No existen plantillas registradas.")
        return
    mostrar_plantillas(plantillas)
    id_plantilla = validar_entero("\nID plantilla: ")
    plantilla = buscar_por_id(plantillas,"id_plantilla",id_plantilla)
    if not plantilla:
        print("La plantilla no existe o está inactiva.")
        return
    mostrar_salones(salones,plantilla.get("id_carrera"))
    id_salon = validar_entero("\nID salón: ")
    salon = buscar_por_id(salones,"id_salon",id_salon)
    if not salon:
        print("El salón no existe o está inactivo.")
        return
    horario = obtener_horario(horarios,id_plantilla,id_salon)
    if not horario:
        print("No existe horario para la plantilla y salón seleccionados.")
        return
    dias_horas = horario.get("dias_horas", [])
    if not dias_horas:
        print("El horario no tiene días registrados.")
        return
    print("\nDÍAS DISPONIBLES")
    for dia in dias_horas:
        print(f"{dia.get('orden')}. "
            f"{dia.get('dia')} "
            f"{dia.get('hora_inicio')} - "
            f"{dia.get('hora_fin')}")
    orden = validar_entero("\nSeleccione día: ")
    dia_seleccionado = next(
        (d for d in dias_horas
            if d.get("orden") == orden),None)
    if not dia_seleccionado:
        print("Día inválido.")
        return
    fecha = validar_fecha()
    alumnos_salon = obtener_alumnos(alumnos,asignaciones,id_salon)
    if not alumnos_salon:
        print("No existen alumnos asignados a este salón.")
        return
    imprimir_titulo("ASISTENCIA")
    registros_nuevos = 0
    for alumno in alumnos_salon:
        if asistencia_registrada(
            asistencias,
            alumno.get("id_alumno"),
            fecha,
            horario.get("id_horario"),
            orden):
            print(f"{alumno.get('nombres')} "
                f"{alumno.get('apellidos')} "
                f"ya registrado.")
            continue
        print(f"\n{alumno.get('nombres')} "
            f"{alumno.get('apellidos')}")
        estado_auto, hora_registro = determinar_estado(dia_seleccionado.get("hora_inicio"))
        print(f"Estado sugerido: {estado_auto}")
        usar_auto = confirmar_si_no("Aceptar automático? (s/n): ")
        if usar_auto == "s":
            estado = estado_auto
        else:
            estado = pedir_estado_manual()
            hora_registro = datetime.now().strftime("%H:%M")
        asistencia = {
            "id_asistencia_alumno":
                generar_id(asistencias,"id_asistencia_alumno"),
            "fecha": fecha,
            "id_plantilla":plantilla.get("id_plantilla"),
            "id_salon":salon.get("id_salon"),
            "id_horario":horario.get("id_horario"),
            "orden_dia": orden,
            "id_alumno":alumno.get("id_alumno"),
            "nombre_alumno":f"{alumno.get('nombres')} "
                f"{alumno.get('apellidos')}",
            "asistencia": estado,
            "hora_registro":hora_registro,"estado": "Activo"}
        asistencias.append(asistencia)
        registros_nuevos += 1
    try:
        guardar_json(RUTA_ASISTENCIA_ALUMNOS,asistencias)
        print(f"\nAsistencia registrada correctamente.")
        print(f"Registros nuevos: "
            f"{registros_nuevos}")
    except Exception as e:
        print(f"Error al guardar la asistencia: "
            f"{e}")