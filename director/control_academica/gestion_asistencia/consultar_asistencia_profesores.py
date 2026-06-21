from datetime import datetime
from basedatos_json import leer_json
from director.utilidades import imprimir_titulo

RUTA_ASISTENCIA = "datos/asistencia_profesores.json"


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


def consultar_asistencia_profesores():
    imprimir_titulo("CONSULTA ASISTENCIA PROFESORES")
    asistencias = cargar_asistencias()
    if not asistencias:
        print("No hay registros.")
        return
    asistencias_activas = [
        a for a in asistencias
        if a.get("estado_registro") == "Activo"]
    if not asistencias_activas:
        print("No existen registros activos.")
        return
    print("\n1. Ver todo")
    print("2. Filtrar por profesor")
    print("3. Filtrar por fecha")
    opcion = input("\nOpción: ").strip()
    if opcion == "1":
        mostrar(asistencias_activas)
    elif opcion == "2":
        nombre = input("Nombre profesor: ").strip().lower()
        if not nombre:
            print("Debe ingresar un nombre.")
            return
        filtrado = [
            a for a in asistencias_activas
            if nombre in str(
                a.get("nombre_profesor","")).lower()]
        mostrar(filtrado)
    elif opcion == "3":
        fecha = input("Fecha (YYYY-MM-DD): ").strip()
        if not validar_fecha(fecha):
            print("Formato de fecha inválido.")
            return
        filtrado = [
            a for a in asistencias_activas
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
        nombre = asistencia.get("nombre_profesor","N/A")
        fecha = asistencia.get("fecha","N/A")
        entrada = asistencia.get("hora_entrada","N/A")
        salida = asistencia.get("hora_salida","N/A")
        horas = asistencia.get("horas_trabajadas",0)
        estado = asistencia.get("estado","N/A")
        id_profesor = asistencia.get("id_profesor","N/A")
        id_modulo = asistencia.get("id_modulo","N/A")
        print(
            f"\nID Profesor: {id_profesor}"
            f"\nProfesor: {nombre}"
            f"\nFecha: {fecha}"
            f"\nMódulo: {id_modulo}"
            f"\nHora entrada: {entrada}"
            f"\nHora salida: {salida}"
            f"\nHoras trabajadas: {horas}"
            f"\nEstado: {estado}"
            f"\n--------------------------------"
        )