from basedatos_json import leer_json
from director.utilidades import imprimir_titulo

RUTA_ALUMNOS = "datos/asistencia_alumnos.json"
RUTA_PROFESORES = "datos/asistencia_profesores.json"


def reporte_inasistencias_alumnos():
    imprimir_titulo("REPORTE INASISTENCIAS - ALUMNOS")
    data = leer_json(RUTA_ALUMNOS)
    if not data:
        print("No hay registros.")
        return
    print("\n1. Todas las inasistencias")
    print("2. Por alumno")
    print("3. Por fecha")
    op = input("Opción: ")
    if op == "1":
        filtrado = [a for a in data if a.get("asistencia") == "Falta"]
        mostrar_alumnos(filtrado)
    elif op == "2":
        nombre = input("Nombre alumno: ").lower()
        filtrado = [a for a in data if nombre in a.get("nombre_alumno", "").lower() and a.get("asistencia") == "Falta"]
        mostrar_alumnos(filtrado)
    elif op == "3":
        fecha = input("Fecha (YYYY-MM-DD): ")
        filtrado = [a for a in data if a.get("fecha") == fecha and a.get("asistencia") == "Falta"]
        mostrar_alumnos(filtrado)
    else:
        print("Opción inválida")


def mostrar_alumnos(lista):
    imprimir_titulo("RESULTADO ALUMNOS")
    if not lista:
        print("Sin inasistencias.")
        return
    total = 0
    for a in lista:
        total += 1
        print(
            f"\nAlumno: {a.get('nombre_alumno', '-')}"
            f"\nFecha: {a.get('fecha', '-')}"
            f"\nEstado: {a.get('asistencia', '-')}"
            f"\nSalón: {a.get('nombre_salon', '-')}"
            f"\n--------------------"
        )
    print(f"\nTOTAL INASISTENCIAS: {total}")


def reporte_inasistencias_profesores():
    imprimir_titulo("REPORTE ASISTENCIA - PROFESORES")
    data = leer_json(RUTA_PROFESORES)
    if not data:
        print("No hay registros.")
        return
    print("\n1. Ver faltas")
    print("2. Ver tardanzas")
    print("3. Ver justificaciones")
    print("4. Filtrar por profesor")
    print("5. Filtrar por fecha")
    op = input("Opción: ")
    if op == "1":
        filtrado = [p for p in data if p.get("estado") == "Falta"]
        mostrar_profesores(filtrado)
    elif op == "2":
        filtrado = [p for p in data if p.get("estado") == "Tardanza"]
        mostrar_profesores(filtrado)
    elif op == "3":
        filtrado = [p for p in data if p.get("estado") == "Justificado"]
        mostrar_profesores(filtrado)
    elif op == "4":
        nombre = input("Nombre profesor: ").lower()
        filtrado = [p for p in data if nombre in p.get("nombre_profesor", "").lower()]
        mostrar_profesores(filtrado)
    elif op == "5":
        fecha = input("Fecha (YYYY-MM-DD): ")
        filtrado = [p for p in data if p.get("fecha") == fecha]
        mostrar_profesores(filtrado)
    else:
        print("Opción inválida")


def mostrar_profesores(lista):
    imprimir_titulo("RESULTADO PROFESORES")
    if not lista:
        print("Sin registros.")
        return
    total = 0
    for p in lista:
        total += 1
        print(
            f"\nProfesor: {p.get('nombre_profesor', 'No registrado')}"
            f"\nFecha: {p.get('fecha', '-')}"
            f"\nEntrada: {p.get('hora_entrada', '-')}"
            f"\nSalida: {p.get('hora_salida', '-')}"
            f"\nHoras trabajadas: {p.get('horas_trabajadas', 0)}"
            f"\nEstado: {p.get('estado', '-')}"
            f"\nJustificación: {p.get('justificacion', '-')}"
            f"\n--------------------"
        )
    print(f"\nTOTAL REGISTROS: {total}")


def reporte_inasistencias():
    imprimir_titulo("REPORTE GENERAL")
    print("1. Alumnos")
    print("2. Profesores")
    print("3. Salir")
    op = input("Opción: ")
    if op == "1":
        reporte_inasistencias_alumnos()
    elif op == "2":
        reporte_inasistencias_profesores()
    elif op == "3":
        return
    else:
        print("Opción inválida")