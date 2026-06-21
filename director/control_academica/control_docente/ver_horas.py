from basedatos_json import leer_json
from director.utilidades import imprimir_titulo

RUTA_ASISTENCIA_PROFESORES = "datos/asistencia_profesores.json"

def ver_horas_trabajadas():

    imprimir_titulo("VER HORAS TRABAJADAS")
    try:
        asistencias = leer_json(RUTA_ASISTENCIA_PROFESORES)
    except FileNotFoundError:
        print("Error: No se encontró el archivo de asistencias.")
        return
    except PermissionError:
        print("Error: No tiene permisos para acceder al archivo.")
        return
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        return


    if asistencias is None:
        print("No existen registros de asistencia docente.")
        return
    if not isinstance(asistencias, list):
        print("Error: La estructura del archivo es inválida.")
        return
    if len(asistencias) == 0:
        print("No existen registros de asistencia docente.")
        return


    profesores = {}
    for asistencia in asistencias:
        if not isinstance(asistencia, dict):
            continue
        estado = str(asistencia.get("estado","")).strip().lower()
        if estado != "activo":
            continue
        id_profesor = asistencia.get("id_profesor")
        if id_profesor is None:
            continue
        try:
            id_profesor = int(id_profesor)
        except (ValueError, TypeError):
            continue
        nombre = asistencia.get("nombre_profesor")
        if nombre is None:
            nombre = f"Profesor {id_profesor}"
        nombre = str(nombre).strip()
        if not nombre:
            nombre = f"Profesor {id_profesor}"
        profesores[id_profesor] = nombre
    if not profesores:
        print("No existen profesores con registros.")
        return


    print("\nPROFESORES DISPONIBLES\n")
    for id_profesor, nombre in sorted(profesores.items()):
        print(f"ID: {id_profesor} | "
            f"{nombre}")


    while True:
        entrada = input("\nIngrese ID del profesor: ").strip()
        if not entrada:
            print("El ID no puede estar vacío.")
            continue
        if not entrada.isdigit():
            print("Debe ingresar un número entero.")
            continue
        id_profesor = int(entrada)
        if id_profesor not in profesores:
            print("El ID ingresado no existe.")
            continue
        break


    registros = []
    for asistencia in asistencias:
        if not isinstance(asistencia, dict):
            continue
        estado = str(
            asistencia.get("estado","")).strip().lower()
        if estado != "activo":
            continue
        try:
            id_actual = int(
                asistencia.get("id_profesor"))
        except (ValueError, TypeError):
            continue
        if id_actual == id_profesor:
            registros.append(asistencia)
    if not registros:
        print("No existen registros para este profesor.")
        return


    imprimir_titulo("HORAS TRABAJADAS")
    nombre_profesor = registros[0].get("nombre_profesor",f"Profesor {id_profesor}")
    print(f"\nProfesor: {nombre_profesor}")
    total_horas = 0.0
    for registro in registros:
        fecha = registro.get("fecha","Sin fecha")
        hora_entrada = registro.get("hora_entrada","N/A")
        hora_salida = registro.get("hora_salida","N/A")
        horas = registro.get("horas_trabajadas",0)
        try:
            horas = float(horas)
            if horas < 0:
                horas = 0
        except (ValueError, TypeError):
            horas = 0
        total_horas += horas
        print(f"\nFecha: {fecha}"
            f"\nHora Entrada: {hora_entrada}"
            f"\nHora Salida: {hora_salida}"
            f"\nHoras Trabajadas: {horas}")
        print("-" * 40)
    print(f"\nTOTAL DE HORAS TRABAJADAS: "
        f"{round(total_horas, 2)}")