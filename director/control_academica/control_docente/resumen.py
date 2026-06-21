from basedatos_json import leer_json
from director.utilidades import imprimir_titulo

RUTA_ASISTENCIA = "datos/asistencia_profesores.json"


def resumen_desempeno_docente():
    imprimir_titulo("RESUMEN DE DESEMPEÑO DOCENTE")
    try:
        asistencias = leer_json(RUTA_ASISTENCIA)
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
        print("No existen registros de asistencia.")
        return
    if not isinstance(asistencias, list):
        print("Error: La estructura del archivo es inválida.")
        return
    if len(asistencias) == 0:
        print("No existen registros de asistencia.")
        return
    docentes = {}


    for registro in asistencias:

        # Validar que sea un diccionario
        if not isinstance(registro, dict):
            continue
        id_profesor = registro.get("id_profesor")

        # Validar ID
        if id_profesor is None:
            continue
        try:
            id_profesor = int(id_profesor)
        except (ValueError, TypeError):
            continue

        # Validar nombre
        nombre_profesor = registro.get("nombre_profesor",f"Profesor {id_profesor}")
        if nombre_profesor is None:
            nombre_profesor = f"Profesor {id_profesor}"
        nombre_profesor = str(nombre_profesor).strip()
        if not nombre_profesor:
            nombre_profesor = f"Profesor {id_profesor}"

        # Crear estructura
        if id_profesor not in docentes:
            docentes[id_profesor] = {
                "nombre": nombre_profesor,
                "asistencias": 0,
                "tardanzas": 0,
                "faltas": 0,
                "horas": 0.0}

        # Validar estado
        estado = str(
            registro.get("estado_asistencia","")).strip().lower()
        if estado == "presente":
            docentes[id_profesor]["asistencias"] += 1
        elif estado == "tardanza":
            docentes[id_profesor]["tardanzas"] += 1
        elif estado == "falta":
            docentes[id_profesor]["faltas"] += 1

        # Validar horas trabajadas
        horas = registro.get("horas_trabajadas",0)
        try:
            horas = float(horas)
            if horas < 0:
                horas = 0
        except (ValueError, TypeError):
            horas = 0
        docentes[id_profesor]["horas"] += horas


    if not docentes:
        print("No existen registros válidos para generar el resumen.")
        return


    for id_profesor, datos in sorted(docentes.items()):
        faltas = datos.get("faltas", 0)
        tardanzas = datos.get("tardanzas", 0)

        # Clasificación de desempeño
        if faltas == 0 and tardanzas <= 2:
            desempeno = "Excelente"
        elif faltas <= 2:
            desempeno = "Bueno"
        else:
            desempeno = "Regular"
        print("\n" + "=" * 50)
        print(f"ID Profesor: {id_profesor}")
        print(f"Nombre: "
            f"{datos.get('nombre', 'No registrado')}")
        print(f"Asistencias: "
            f"{datos.get('asistencias', 0)}")
        print(f"Tardanzas: "
            f"{datos.get('tardanzas', 0)}")
        print(f"Faltas: "
            f"{datos.get('faltas', 0)}")
        print(f"Horas trabajadas: "
            f"{round(datos.get('horas', 0), 2)}")
        print(f"Desempeño: "
            f"{desempeno}")
    print("\n" + "=" * 50)