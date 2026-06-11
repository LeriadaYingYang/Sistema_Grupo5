from basedatos_json import leer_json
from control_academico.utilidades import imprimir_titulo

RUTA_ASISTENCIAS = "datos/asistencia_alumnos.json"
ESTADOS_ASISTENCIA = ["Presente","Tardanza","Falta","Justificado"]

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
        f"Alumno: {asistencia['nombre_alumno']} | "
        f"Carrera: {asistencia['nombre_carrera']} | "
        f"Salón: {asistencia['nombre_salon']} | "
        f"Asistencia: {asistencia['asistencia']}")

def mostrar_resultados(registros):
    if not registros:
        print("No se encontraron registros.")
        return
    print()
    for registro in registros:
        mostrar_registro(registro)
    print(f"\nTotal encontrados: "
        f"{len(registros)}")

def buscar_por_alumno(asistencias):
    imprimir_titulo("=== BUSCAR POR ALUMNO ===")
    id_alumno = pedir_entero("Ingrese ID alumno: ")
    resultados = [asistencia for asistencia in asistencias
        if asistencia["id_alumno"] == id_alumno]
    mostrar_resultados(resultados)

def buscar_por_fecha(asistencias):
    imprimir_titulo("=== BUSCAR POR FECHA ===")
    fecha = pedir_texto("Ingrese fecha (AAAA-MM-DD): ")
    resultados = [asistencia for asistencia in asistencias
        if asistencia["fecha"] == fecha]
    mostrar_resultados(resultados)

def buscar_por_salon(asistencias):
    imprimir_titulo("=== BUSCAR POR SALÓN ===")
    id_salon = pedir_entero("Ingrese ID salón: ")
    resultados = [asistencia for asistencia in asistencias
        if asistencia["id_salon"] == id_salon]
    mostrar_resultados(resultados)

def buscar_por_carrera(asistencias):
    imprimir_titulo("=== BUSCAR POR CARRERA ===")
    id_carrera = pedir_entero("Ingrese ID carrera: ")
    resultados = [asistencia for asistencia in asistencias
        if asistencia["id_carrera"] == id_carrera]
    mostrar_resultados(resultados)

def generar_resumen(registros):
    resumen = {estado: 0 for estado in ESTADOS_ASISTENCIA}
    for registro in registros:
        estado = registro["asistencia"]
        if estado in resumen:
            resumen[estado] += 1
    return resumen

def resumen_por_alumno(asistencias):
    imprimir_titulo("=== RESUMEN POR ALUMNO ===")
    id_alumno = pedir_entero("Ingrese ID alumno: ")
    registros = [asistencia for asistencia in asistencias
        if asistencia["id_alumno"] == id_alumno]
    if not registros:
        print("No se encontraron registros.")
        return
    nombre = registros[0]["nombre_alumno"]
    resumen = generar_resumen(registros)
    imprimir_titulo(f"RESUMEN DE {nombre}")
    for estado, cantidad in resumen.items():
        print(f"{estado}: "
            f"{cantidad}")
    print(f"\nTotal: "
        f"{len(registros)}")

def mostrar_todas(asistencias):
    imprimir_titulo("=== TODAS LAS ASISTENCIAS ===")
    mostrar_resultados(asistencias)

def ver_asistencia_alumnos():
    asistencias = (obtener_asistencias_activas(cargar_asistencias()))
    if not asistencias:
        print("No existen asistencias registradas.")
        return
    while True:
        imprimir_titulo("=== VER ASISTENCIA ALUMNOS ===")
        print("1. Buscar por alumno")
        print("2. Buscar por fecha")
        print("3. Buscar por salón")
        print("4. Buscar por carrera")
        print("5. Ver resumen por alumno")
        print("6. Mostrar todas")
        print("7. Volver")
        opcion = input("\nSeleccione una opción: ").strip()
        if opcion == "1":buscar_por_alumno(asistencias)
        elif opcion == "2":buscar_por_fecha(asistencias)
        elif opcion == "3":buscar_por_salon(asistencias)
        elif opcion == "4":buscar_por_carrera(asistencias)
        elif opcion == "5":
            resumen_por_alumno(asistencias)
        elif opcion == "6":mostrar_todas(asistencias)
        elif opcion == "7":
            break
        else:
            print("Opción inválida.")