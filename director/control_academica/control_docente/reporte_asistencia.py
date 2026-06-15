from basedatos_json import leer_json
from director.utilidades import imprimir_titulo

RUTA_ASISTENCIA = "datos/asistencia_profesores.json"

def reporte_asistencia_docente():
    imprimir_titulo("REPORTE DE ASISTENCIA DOCENTE")
    asistencias = leer_json(RUTA_ASISTENCIA)
    if not asistencias:
        print("No existen registros de asistencia docente.")
        return
    print("\n1. Ver todo")
    print("2. Filtrar por profesor")
    print("3. Filtrar por fecha")
    print("4. Filtrar por estado")
    opcion = input("\nSeleccione opción: ")
    if opcion == "1":
        registros = [a for a in asistencias if a.get("estado") == "Activo"]
        mostrar_registros(registros)
    elif opcion == "2":
        nombre = input("Ingrese nombre del profesor: ").strip().lower()
        registros = [
            a
            for a in asistencias
            if (a.get("estado") == "Activo" and nombre in a.get("nombre_profesor","").lower())]
        mostrar_registros(registros)
    elif opcion == "3":
        fecha = input("Ingrese fecha (YYYY-MM-DD): ").strip()
        registros = [a for a in asistencias
            if (a.get("estado") == "Activo" and a.get("fecha") == fecha)]
        mostrar_registros(registros)
    elif opcion == "4":
        estado = input("Estado (Presente/Tardanza/Falta): ").strip().lower()
        registros = [a for a in asistencias
            if (a.get("estado_asistencia", "").lower() == estado)]
        mostrar_registros(registros)
    else:
        print("Opción inválida.")

def mostrar_registros(registros):
    imprimir_titulo("RESULTADOS")
    if not registros:
        print("No se encontraron registros.")
        return
    for registro in registros:
        print(
            f"\nProfesor: "
            f"{registro.get('nombre_profesor', 'N/A')}"
        )
        print(
            f"Fecha: "
            f"{registro.get('fecha', 'N/A')}"
        )
        print(
            f"Estado: "
            f"{registro.get('estado_asistencia', 'N/A')}"
        )
        print(
            f"Hora Entrada: "
            f"{registro.get('hora_entrada', 'N/A')}"
        )
        print(
            f"Hora Salida: "
            f"{registro.get('hora_salida', 'N/A')}"
        )
        print(
            f"Horas Trabajadas: "
            f"{registro.get('horas_trabajadas', 0)}"
        )
        print("-" * 50)