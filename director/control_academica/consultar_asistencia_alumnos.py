from basedatos_json import leer_json
from director.utilidades import imprimir_titulo

RUTA_ASISTENCIA = "datos/asistencia_alumnos.json"


def consultar_asistencia_alumnos():
    imprimir_titulo("CONSULTA ASISTENCIA ALUMNOS")

    asistencias = leer_json(RUTA_ASISTENCIA)

    if not asistencias:
        print("No hay registros.")
        return

    print("\n1. Ver todo")
    print("2. Filtrar por alumno")
    print("3. Filtrar por fecha")

    op = input("Opción: ")

    if op == "1":
        mostrar(asistencias)

    elif op == "2":
        nombre = input("Nombre alumno: ").lower()
        filtrado = [a for a in asistencias if nombre in a["nombre_alumno"].lower()]
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
            f"\nAlumno: {a.get('nombre_alumno', 'N/A')}"
            f"\nFecha: {a.get('fecha', 'N/A')}"
            f"\nEstado: {a.get('asistencia', 'N/A')}"
            f"\nHora entrada: {a.get('hora_entrada', 'N/A')}"
            f"\nHora salida: {a.get('hora_salida', 'N/A')}"
            f"\n------------------------"
        )