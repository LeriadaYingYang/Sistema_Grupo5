from basedatos_json import leer_json
from director.utilidades import imprimir_titulo
from datetime import datetime

RUTA_ASISTENCIA = "datos/asistencia_profesores.json"

def validar_fecha(fecha):
    try:
        datetime.strptime(str(fecha), "%Y-%m-%d")
        return True
    except (ValueError, TypeError):
        return False

def validar_hora(hora):
    try:
        datetime.strptime(str(hora), "%H:%M")
        return True
    except (ValueError, TypeError):
        return False

def reporte_asistencia_docente():
    imprimir_titulo("REPORTE DE ASISTENCIA DOCENTE")
    try:
        asistencias = leer_json(RUTA_ASISTENCIA)
    except FileNotFoundError:
        print("Error: archivo de asistencias no encontrado.")
        return
    except PermissionError:
        print("Error: permisos insuficientes para leer el archivo.")
        return
    except Exception as e:
        print(f"Error al leer el archivo de asistencias: {e}")
        return


    if asistencias is None:
        print("No existen registros de asistencia.")
        return
    if not isinstance(asistencias, list):
        print("Error: estructura de datos inválida.")
        return
    if len(asistencias) == 0:
        print("No existen registros de asistencia docente.")
        return


    print("\n1. Ver todo")
    print("2. Filtrar por profesor")
    print("3. Filtrar por fecha")
    print("4. Filtrar por estado")
    opcion = input("\nSeleccione opción: ").strip()
    registros = []


    if opcion == "1":
        registros = [a for a in asistencias
            if isinstance(a, dict) and str(a.get("estado", "")).strip().lower() == "activo"]
    elif opcion == "2":
        nombre = input("Ingrese nombre del profesor: ").strip().lower()
        if not nombre:
            print("Debe ingresar un nombre.")
            return
        registros = [a for a in asistencias
            if isinstance(a, dict)and str(a.get("estado", "")).strip().lower() == "activo"
            and nombre in str(a.get("nombre_profesor", "")).lower()]
    elif opcion == "3":
        fecha = input("Ingrese fecha (YYYY-MM-DD): ").strip()
        if not validar_fecha(fecha):
            print("Formato de fecha inválido. Use YYYY-MM-DD.")
            return
        registros = [a for a in asistencias
            if isinstance(a, dict)and str(a.get("estado", "")).strip().lower() == "activo"
            and str(a.get("fecha", "")).strip() == fecha]
    elif opcion == "4":
        estado = input("Estado (Presente/Tardanza/Falta): ").strip().lower()
        estados_validos = ("presente","tardanza","falta")
        if estado not in estados_validos:
            print("Estado inválido. Debe ser: Presente, Tardanza o Falta.")
            return
        registros = [
            a for a in asistencias
            if isinstance(a, dict) and str(
                a.get("estado_asistencia","")).strip().lower() == estado]
    else:
        print("Opción inválida.")
        return


    if not registros:
        print("\nNo se encontraron registros ""para el criterio seleccionado.")
        return
    try:
        mostrar_registros(registros)
    except Exception as e:
        print(f"Error al mostrar registros: {e}")


def mostrar_registros(registros):
    imprimir_titulo("RESULTADOS")
    if not isinstance(registros, list):
        print("Error: registros inválidos.")
        return
    if not registros:
        print("No se encontraron registros.")
        return
    for registro in registros:
        if not isinstance(registro, dict):
            continue
        nombre = str(registro.get("nombre_profesor","N/A")).strip()
        fecha = str(registro.get("fecha","N/A")).strip()
        estado = str(registro.get("estado_asistencia","N/A")).strip()
        hora_entrada = registro.get("hora_entrada","N/A")
        hora_salida = registro.get("hora_salida","N/A")
        horas_trabajadas = registro.get("horas_trabajadas",0)

        # Validar horas
        if hora_entrada != "N/A":
            if not validar_hora(hora_entrada):
                hora_entrada = "Hora inválida"
        if hora_salida != "N/A":
            if not validar_hora(hora_salida):
                hora_salida = "Hora inválida"

        # Validar horas trabajadas
        try:
            horas_trabajadas = float(horas_trabajadas)
            if horas_trabajadas < 0:
                horas_trabajadas = 0
        except (ValueError, TypeError):
            horas_trabajadas = 0
        print(f"\nProfesor: {nombre}")
        print(f"Fecha: {fecha}")
        print(f"Estado: {estado}")
        print(f"Hora Entrada: {hora_entrada}")
        print(f"Hora Salida: {hora_salida}")
        print(f"Horas Trabajadas: "
            f"{horas_trabajadas}")
        print("-" * 50)