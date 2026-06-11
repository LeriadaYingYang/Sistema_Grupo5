from datetime import datetime
from basedatos_json import leer_json,guardar_json,generar_id
from control_academico.utilidades import imprimir_titulo

RUTA_HORARIOS = "datos/horarios.json"
RUTA_MATRICULAS = "datos/matriculas.json"
RUTA_ASISTENCIAS = "datos/asistencia_alumnos.json"

ESTADOS_ASISTENCIA = {"P": "Presente","T": "Tardanza","F": "Falta","J": "Justificado"}

def cargar_datos():
    return (leer_json(RUTA_HORARIOS),leer_json(RUTA_MATRICULAS),leer_json(RUTA_ASISTENCIAS))

def buscar_por_id(lista, campo_id, valor_id):
    return next((item for item in lista
            if item[campo_id] == valor_id and item["estado"] in ["Activo", "Activa"]), None)

def pedir_entero(mensaje):
    while True:
        try:
            return int(input(mensaje))
        except ValueError:
            print("Error: debe ingresar un número entero.")


def pedir_fecha():
    while True:
        fecha = input("Ingrese fecha (AAAA-MM-DD): ").strip()
        try:
            datetime.strptime(fecha,"%Y-%m-%d")
            return fecha
        except ValueError:
            print("Formato inválido. Use AAAA-MM-DD.")

def mostrar_horarios(horarios):
    imprimir_titulo("=== HORARIOS DISPONIBLES ===")
    horarios_activos = [horario for horario in horarios
        if horario["estado"] == "Activo"]
    if not horarios_activos:
        print("No existen horarios configurados.")
        return False
    for horario in horarios_activos:
        print(f"ID: {horario['id_horario']} | "
            f"Carrera: {horario['nombre_carrera']} | "
            f"Salón: {horario['nombre_salon']} | "
            f"Turno: {horario['turno']}")
    return True

def mostrar_dias_horario(horario):
    imprimir_titulo("=== DÍAS DEL HORARIO ===")
    for dia in horario["dias_horas"]:
        print(f"{dia['orden']}. "
            f"{dia['dia']} | "
            f"{dia['hora_inicio']} - "
            f"{dia['hora_fin']}")

def obtener_dia_horario(horario,orden_dia):
    return next((dia for dia in horario["dias_horas"]
            if dia["orden"] == orden_dia),None)

def obtener_alumnos_matriculados(matriculas,carrera,salon):
    return [matricula for matricula in matriculas
        if matricula["estado"] == "Activa" and matricula["carrera"].lower() == carrera.lower() and matricula["salon"].lower() == salon.lower()]

def pedir_asistencia():
    while True:
        opcion = input("(P)resente | " "(T)ardanza | " "(F)alta | " "(J)ustificado: ").upper().strip()
        if opcion in ESTADOS_ASISTENCIA:
            return ESTADOS_ASISTENCIA[opcion]
        print("Opción inválida.")

def asistencia_ya_registrada(asistencias,fecha,id_horario,orden_dia,id_alumno):
    return any(asistencia["estado"] == "Activo" and asistencia["fecha"] == fecha and asistencia["id_horario"] == id_horario
        and asistencia["orden_dia"] == orden_dia and asistencia["id_alumno"] == id_alumno for asistencia in asistencias)

def crear_asistencia(asistencias,fecha,horario,dia_horario,alumno,asistencia):
    return {"id_asistencia_alumno":
            generar_id(asistencias,"id_asistencia_alumno"),
        "fecha": fecha,
        "id_plantilla": horario["id_plantilla"],
        "nombre_plantilla": horario["nombre_plantilla"],
        "id_carrera": horario["id_carrera"],
        "nombre_carrera": horario["nombre_carrera"],
        "id_salon": horario["id_salon"],
        "nombre_salon": horario["nombre_salon"],
        "turno": horario["turno"],
        "id_horario": horario["id_horario"],
        "orden_dia": dia_horario["orden"],
        "dia": dia_horario["dia"],
        "hora_inicio": dia_horario["hora_inicio"],
        "hora_fin": dia_horario["hora_fin"],
        "id_alumno": alumno["id_alumno"],
        "nombre_alumno": alumno["nombre_alumno"],
        "dni": alumno["dni"],
        "asistencia": asistencia,
        "estado": "Activo"}

def registrar_asistencia_alumnos():

    imprimir_titulo("=== REGISTRAR ASISTENCIA ALUMNOS ===")
    (horarios,matriculas,asistencias) = cargar_datos()
    if not horarios:
        print("Primero debe configurar horarios.")
        return
    if not matriculas:
        print("No existen matrículas registradas.")
        return
    if not mostrar_horarios(horarios):
        return
    id_horario = pedir_entero("\nIngrese ID horario: ")
    horario = buscar_por_id(horarios,"id_horario",id_horario)
    if horario is None:
        print("Horario no encontrado.")
        return
    mostrar_dias_horario(horario)
    orden_dia = pedir_entero("\nSeleccione día: ")
    dia_horario = obtener_dia_horario(horario,orden_dia)
    if dia_horario is None:
        print("Día inválido.")
        return
    fecha = pedir_fecha()
    alumnos = (obtener_alumnos_matriculados(matriculas,horario["nombre_carrera"],horario["nombre_salon"]))
    if not alumnos:
        print("No existen alumnos matriculados para este salón.")
        return
    imprimir_titulo("=== REGISTRO DE ASISTENCIA ===")
    registros = 0
    for alumno in alumnos:
        print(f"\nAlumno: "
            f"{alumno['nombre_alumno']}")
        asistencia = pedir_asistencia()
        if asistencia_ya_registrada(asistencias,fecha,horario["id_horario"],orden_dia,alumno["id_alumno"]):
            print("Asistencia ya registrada.")
            continue
        nuevo_registro = (
            crear_asistencia(asistencias,fecha,horario,
                dia_horario,alumno,asistencia))
        asistencias.append(nuevo_registro)
        registros += 1
    guardar_json(RUTA_ASISTENCIAS,asistencias)
    print(f"\nSe registraron "
        f"{registros} asistencias.")