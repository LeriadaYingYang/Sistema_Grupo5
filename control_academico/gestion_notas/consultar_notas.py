from basedatos_json import leer_json
from control_academico.utilidades import imprimir_titulo

RUTA_NOTAS = "datos/notas_alumnos.json"

def cargar_notas():
    return leer_json(RUTA_NOTAS)

def pedir_entero(mensaje):
    while True:
        try:
            return int(input(mensaje))
        except ValueError:
            print("Error: debe ingresar un número entero.")

def obtener_notas_activas(notas):
    return [nota for nota in notas
        if nota["estado"] == "Activo"]

def mostrar_detalle_notas(registro):
    print(f"\nAlumno: "
        f"{registro['nombre_alumno']}")
    print(f"Promedio módulo: "
        f"{registro['promedio_modulo']}")
    print("-" * 40)
    for nota in registro["notas"]:
        print(f"{nota['nombre_nota']}: "
            f"{nota['nota']}")

def mostrar_resultados(registros):
    if not registros:
        print("No se encontraron registros.")
        return
    for registro in registros:
        mostrar_detalle_notas(registro)
        print()

def buscar_por_alumno(notas):
    imprimir_titulo("=== CONSULTAR POR ALUMNO ===")
    id_alumno = pedir_entero("Ingrese ID alumno: ")
    resultados = [nota for nota in notas
        if nota["id_alumno"] == id_alumno]
    mostrar_resultados(resultados)

def buscar_por_modulo(notas):
    imprimir_titulo("=== CONSULTAR POR MÓDULO ===")
    id_modulo = pedir_entero("Ingrese ID módulo: ")
    resultados = [
        nota for nota in notas
        if nota["id_modulo"] == id_modulo]
    mostrar_resultados(resultados)

def buscar_por_unidad(notas):
    imprimir_titulo("=== CONSULTAR POR UNIDAD ===")
    id_unidad = pedir_entero("Ingrese ID unidad: ")
    resultados = [nota for nota in notas
        if nota["id_unidad"] == id_unidad]
    mostrar_resultados(resultados)

def buscar_por_carrera(notas):

    imprimir_titulo("=== CONSULTAR POR CARRERA ===")
    id_carrera = pedir_entero("Ingrese ID carrera: ")
    resultados = [nota for nota in notas
        if nota["id_carrera"] == id_carrera]
    mostrar_resultados(resultados)

def promedio_por_alumno(notas):
    imprimir_titulo("=== PROMEDIO POR ALUMNO ===")
    id_alumno = pedir_entero("Ingrese ID alumno: ")
    registros = [nota for nota in notas
        if nota["id_alumno"]== id_alumno]
    if not registros:
        print("No se encontraron registros.")
        return
    nombre = registros[0]["nombre_alumno"]
    promedio_general = round(
        sum(registro["promedio_modulo"]
            for registro in registros)/ len(registros),2)
    print(f"\nAlumno: {nombre}")
    print(f"Promedio general: "
        f"{promedio_general}")

def mostrar_todas(notas):
    imprimir_titulo("=== TODAS LAS NOTAS ===")
    mostrar_resultados(notas)

def consultar_notas():
    notas = (obtener_notas_activas(cargar_notas()))
    if not notas:
        print("No existen notas registradas.")
        return
    while True:
        imprimir_titulo("=== CONSULTAR NOTAS ===")
        print("1. Buscar notas por alumno")
        print("2. Buscar notas por módulo")
        print("3. Buscar notas por unidad")
        print("4. Buscar notas por carrera")
        print("5. Ver promedio por alumno")
        print("6. Mostrar todas las notas")
        print("7. Volver")
        opcion = input("\nSeleccione una opción: ").strip()
        if opcion == "1":buscar_por_alumno(notas)
        elif opcion == "2":buscar_por_modulo(notas)
        elif opcion == "3":buscar_por_unidad(notas)
        elif opcion == "4":buscar_por_carrera(notas)
        elif opcion == "5":promedio_por_alumno(notas)
        elif opcion == "6":mostrar_todas(notas)
        elif opcion == "7":
            break
        else:
            print("Opción inválida.")