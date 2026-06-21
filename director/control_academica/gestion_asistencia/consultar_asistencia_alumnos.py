from datetime import datetime
from basedatos_json import leer_json
from director.utilidades import imprimir_titulo

RUTA_ASISTENCIA = "datos/asistencia_alumnos.json"


def validar_fecha(fecha):
    try:
        datetime.strptime(fecha, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def cargar_asistencias():
    try:
        datos = leer_json(RUTA_ASISTENCIA)
        if not isinstance(datos, list):
            return []
        return datos
    except Exception as e:
        print(f"Error al leer archivo: {e}")
        return []


def consultar_asistencia_alumnos():
    imprimir_titulo("CONSULTA ASISTENCIA ALUMNOS")
    asistencias = cargar_asistencias()
    if not asistencias:
        print("No hay registros.")
        return
    asistencias_activas = [a for a in asistencias
        if a.get("estado") == "Activo"]
    if not asistencias_activas:
        print("No existen registros activos.")
        return
    print("\n1. Ver todo")
    print("2. Filtrar por alumno")
    print("3. Filtrar por fecha")
    opcion = input("\nOpción: ").strip()
    if opcion == "1":
        mostrar(asistencias_activas)
    elif opcion == "2":
        nombre = input("Nombre alumno: ").strip().lower()
        if not nombre:
            print("Debe ingresar un nombre.")
            return
        filtrado = [
            a for a in asistencias_activas
            if nombre in str(
                a.get("nombre_alumno","")).lower()]
        mostrar(filtrado)
    elif opcion == "3":
        fecha = input("Fecha (YYYY-MM-DD): ").strip()
        if not validar_fecha(fecha):
            print("Fecha inválida.")
            return
        filtrado = [a for a in asistencias_activas
            if a.get("fecha") == fecha]
        mostrar(filtrado)
    else:
        print("Opción inválida.")


def mostrar(lista):
    imprimir_titulo("RESULTADOS")
    if not lista:
        print("Sin resultados.")
        return
    print(f"\nTotal registros: "
        f"{len(lista)}")
    for asistencia in lista:
        nombre = asistencia.get("nombre_alumno","N/A")
        fecha = asistencia.get("fecha","N/A")
        estado = asistencia.get("asistencia","N/A")
        hora_registro = asistencia.get("hora_registro","N/A")
        id_alumno = asistencia.get("id_alumno","N/A")
        print(
            f"\nID Alumno: {id_alumno}"
            f"\nAlumno: {nombre}"
            f"\nFecha: {fecha}"
            f"\nEstado: {estado}"
            f"\nHora registro: {hora_registro}"
            f"\n--------------------------"
        )