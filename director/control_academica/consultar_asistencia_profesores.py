from basedatos_json import leer_json
from director.utilidades import imprimir_titulo

RUTA_ASISTENCIA = "datos/asistencia_profesores.json"


def consultar_asistencia_profesores():
    imprimir_titulo("CONSULTA ASISTENCIA PROFESORES")

    asistencias = leer_json(RUTA_ASISTENCIA)

    if not asistencias:
        print("No hay registros.")
        return

    print("\n1. Ver todo")
    print("2. Filtrar por profesor")
    print("3. Filtrar por fecha")

    op = input("Opción: ")

    if op == "1":
        mostrar(asistencias)

    elif op == "2":
        nombre = input("Nombre profesor: ").lower()
        filtrado = [a for a in asistencias if nombre in a["nombre_profesor"].lower()]
        mostrar(filtrado)

    elif op == "3":
        fecha = input("Fecha (YYYY-MM-DD): ")
        filtrado = [a for a in asistencias if a["fecha"] == fecha]
        mostrar(filtrado)

    else:
        print("Opción inválida")


def mostrar(lista):
    imprimir_titulo("RESULTADOS")

    if not lista:
        print("Sin resultados")
        return

    for a in lista:
        print(
            f"\nProfesor: {a.get('nombre_profesor','-')}"
            f"\nFecha: {a['fecha']}"
            f"\nEntrada: {a.get('hora_entrada','-')}"
            f"\nSalida: {a.get('hora_salida','-')}"
            f"\nHoras trabajadas: {a.get('horas_trabajadas','0')}"
            f"\nEstado: {a.get('estado','-')}"
            f"\n------------------------"
        )