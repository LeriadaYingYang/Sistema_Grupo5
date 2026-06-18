from datetime import datetime
from basedatos_json import leer_json
from director.utilidades import imprimir_titulo

RUTA_ALUMNOS = "datos/asistencia_alumnos.json"
RUTA_PROFESORES = "datos/asistencia_profesores.json"


def validar_fecha(fecha):
    try:
        datetime.strptime(fecha, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def cargar_datos(ruta):
    try:
        datos = leer_json(ruta)
        if not isinstance(datos, list):
            return []
        return datos
    except Exception as e:
        print(f"Error al leer datos: {e}")
        return []


def reporte_inasistencias_alumnos():
    imprimir_titulo("REPORTE INASISTENCIAS - ALUMNOS")
    data = cargar_datos(RUTA_ALUMNOS)
    if not data:
        print("No hay registros.")
        return
    registros = [a for a in data
        if a.get("estado") == "Activo"]
    if not registros:
        print("No existen registros activos.")
        return
    print("\n1. Todas las inasistencias")
    print("2. Filtrar por alumno")
    print("3. Filtrar por fecha")
    opcion = input("\nOpción: ").strip()

    if opcion == "1":
        filtrado = [a for a in registros
            if a.get("asistencia") == "Falta"]
        mostrar_alumnos(filtrado)

    elif opcion == "2":
        nombre = input("Nombre alumno: ").strip().lower()
        if not nombre:
            print("Debe ingresar un nombre.")
            return
        filtrado = [
            a for a in registros
            if (nombre in str(a.get("nombre_alumno","")).lower()
                and a.get("asistencia")== "Falta")]
        mostrar_alumnos(filtrado)

    elif opcion == "3":
        fecha = input("Fecha (YYYY-MM-DD): ").strip()
        if not validar_fecha(fecha):
            print("Fecha inválida.")
            return
        filtrado = [
            a for a in registros
            if (a.get("fecha") == fecha and a.get("asistencia")== "Falta")]
        mostrar_alumnos(filtrado)
    else:
        print("Opción inválida.")


def mostrar_alumnos(lista):
    imprimir_titulo("RESULTADO ALUMNOS")
    if not lista:
        print("Sin inasistencias.")
        return
    print(f"\nTotal encontrados: "
        f"{len(lista)}")
    for alumno in lista:
        print(
            f"\nAlumno: "
            f"{alumno.get('nombre_alumno','N/A')}"
            f"\nFecha: "
            f"{alumno.get('fecha','N/A')}"
            f"\nEstado: "
            f"{alumno.get('asistencia','N/A')}"
            f"\nSalón: "
            f"{alumno.get('nombre_salon','N/A')}"
            f"\n------------------------"
        )


def reporte_inasistencias_profesores():
    imprimir_titulo("REPORTE TARDANZAS - PROFESORES")
    data = cargar_datos(RUTA_PROFESORES)
    if not data:
        print("No hay registros.")
        return
    registros = [
        p for p in data
        if p.get("estado_registro") == "Activo"]
    if not registros:
        print("No existen registros activos.")
        return
    print("\n1. Todas las tardanzas")
    print("2. Filtrar por profesor")
    print("3. Filtrar por fecha")
    opcion = input("\nOpción: ").strip()

    if opcion == "1":
        filtrado = [
            p for p in registros
            if p.get("estado") == "Tardanza"]
        mostrar_profesores(filtrado)

    elif opcion == "2":
        nombre = input("Nombre profesor: ").strip().lower()
        if not nombre:
            print("Debe ingresar un nombre.")
            return
        filtrado = [
            p for p in registros
            if (nombre in str(p.get("nombre_profesor","")).lower()
                and p.get("estado")== "Tardanza")]
        mostrar_profesores(filtrado)

    elif opcion == "3":
        fecha = input("Fecha (YYYY-MM-DD): ").strip()
        if not validar_fecha(fecha):
            print("Fecha inválida.")
            return
        filtrado = [p for p in registros
            if (p.get("fecha") == fecha
                and p.get("estado") == "Tardanza")]
        mostrar_profesores(filtrado)
    else:
        print("Opción inválida.")


def mostrar_profesores(lista):
    imprimir_titulo("RESULTADO PROFESORES")
    if not lista:
        print("Sin registros.")
        return

    print(f"\nTotal encontrados: "
        f"{len(lista)}")
    for profesor in lista:
        print(
            f"\nProfesor: "
            f"{profesor.get('nombre_profesor','N/A')}"
            f"\nFecha: "
            f"{profesor.get('fecha','N/A')}"
            f"\nEntrada: "
            f"{profesor.get('hora_entrada','N/A')}"
            f"\nSalida: "
            f"{profesor.get('hora_salida','N/A')}"
            f"\nHoras trabajadas: "
            f"{profesor.get('horas_trabajadas',0)}"
            f"\nEstado: "
            f"{profesor.get('estado','N/A')}"
            f"\n------------------------"
        )


def reporte_inasistencias():
    imprimir_titulo("REPORTE GENERAL")
    print("1. Alumnos")
    print("2. Profesores")
    print("3. Salir")
    opcion = input("\nOpción: ").strip()
    if opcion == "1":
        reporte_inasistencias_alumnos()
    elif opcion == "2":
        reporte_inasistencias_profesores()
    elif opcion == "3":
        return
    else:
        print("Opción inválida.")