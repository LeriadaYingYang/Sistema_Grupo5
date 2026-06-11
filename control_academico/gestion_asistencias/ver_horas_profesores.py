from basedatos_json import leer_json
from control_academico.utilidades import imprimir_titulo

RUTA_ASISTENCIAS = "datos/asistencia_profesores.json"

def cargar_asistencias():
    return leer_json(RUTA_ASISTENCIAS)

def pedir_entero(mensaje):
    while True:
        try:
            return int(input(mensaje))
        except ValueError:
            print("Error: debe ingresar un número entero.")

def pedir_texto(mensaje):
    return input(mensaje).strip()

def obtener_asistencias_activas(asistencias):
    return [asistencia for asistencia in asistencias
        if asistencia["estado"] == "Activo"]

def mostrar_registro(asistencia):
    print(f"Fecha: {asistencia['fecha']} | "
        f"Profesor: {asistencia['nombre_profesor']} | "
        f"Carrera: {asistencia['nombre_carrera']} | "
        f"Horas: {asistencia['horas_trabajadas']}")

def mostrar_resultados(registros):
    if not registros:
        print("No se encontraron registros.")
        return
    total_horas = 0
    print()
    for registro in registros:
        mostrar_registro(registro)
        total_horas += registro["horas_trabajadas"]
    print(f"\nRegistros encontrados: "
        f"{len(registros)}")
    print(f"Total horas: "
        f"{total_horas}")

def buscar_por_profesor(asistencias):
    imprimir_titulo("=== HORAS POR PROFESOR ===")
    id_profesor = pedir_entero("Ingrese ID profesor: ")
    resultados = [asistencia for asistencia in asistencias
        if asistencia["id_profesor"] == id_profesor]
    mostrar_resultados(resultados)

def buscar_por_fecha(asistencias):
    imprimir_titulo("=== HORAS POR FECHA ===")
    fecha = pedir_texto("Ingrese fecha (AAAA-MM-DD): ")
    resultados = [asistencia for asistencia in asistencias
        if asistencia["fecha"] == fecha]
    mostrar_resultados(resultados)

def buscar_por_carrera(asistencias):
    imprimir_titulo("=== HORAS POR CARRERA ===")
    id_carrera = pedir_entero("Ingrese ID carrera: ")
    resultados = [asistencia for asistencia in asistencias
        if asistencia["id_carrera"]== id_carrera]
    mostrar_resultados(resultados)

def total_horas_trabajadas(asistencias):
    imprimir_titulo("=== TOTAL HORAS TRABAJADAS ===")
    total = sum(asistencia["horas_trabajadas"]
        for asistencia in asistencias)
    print(f"Total general de horas: "
        f"{total}")

def ver_horas_profesores():
    asistencias = (obtener_asistencias_activas(cargar_asistencias()))
    if not asistencias:
        print("No existen horas registradas.")
        return
    while True:
        imprimir_titulo("=== VER HORAS PROFESORES ===")
        print("1. Buscar horas por profesor")
        print("2. Ver horas por fecha")
        print("3. Ver horas por carrera")
        print("4. Ver total de horas trabajadas")
        print("5. Volver")
        opcion = input("\nSeleccione una opción: ").strip()
        if opcion == "1":buscar_por_profesor(asistencias)
        elif opcion == "2":buscar_por_fecha(asistencias)
        elif opcion == "3":buscar_por_carrera(asistencias)
        elif opcion == "4":total_horas_trabajadas(asistencias)
        elif opcion == "5":
            break
        else:
            print("Opción inválida.")