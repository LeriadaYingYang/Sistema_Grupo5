from basedatos_json import leer_json
from director.utilidades import imprimir_titulo

RUTA_ASISTENCIA = "datos/asistencia_profesores.json"


def profesores_con_faltas():
    imprimir_titulo("PROFESORES CON FALTAS")
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
        print("Error: El archivo debe contener una lista de registros.")
        return
    if len(asistencias) == 0:
        print("No existen registros de asistencia.")
        return
    faltas_por_profesor = {}


    for registro in asistencias:
        # Validar que sea un diccionario
        if not isinstance(registro, dict):
            continue
        estado_asistencia = registro.get("estado_asistencia",registro.get("estado", ""))
        if estado_asistencia is None:
            continue
        if str(estado_asistencia).strip().lower() != "falta":
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
        nombre_profesor = registro.get("nombre_profesor","")
        if not nombre_profesor:
            nombre_profesor = f"Profesor {id_profesor}"

        # Validar fecha
        fecha = registro.get("fecha")
        if fecha is None or str(fecha).strip() == "":
            fecha = "Sin fecha"

        # Crear registro del profesor
        if id_profesor not in faltas_por_profesor:
            faltas_por_profesor[id_profesor] = {"nombre": str(nombre_profesor).strip(),"cantidad": 0,"fechas": []}
        faltas_por_profesor[id_profesor]["cantidad"] += 1
        faltas_por_profesor[id_profesor]["fechas"].append(fecha)


    if not faltas_por_profesor:
        print("No existen profesores con faltas registradas.")
        return


    for id_profesor, datos in sorted(faltas_por_profesor.items()):
        print("\n" + "=" * 50)
        print(f"ID Profesor: {id_profesor}")
        print(f"Nombre: "
            f"{datos.get('nombre', 'No registrado')}")
        print(f"Cantidad de faltas: "
            f"{datos.get('cantidad', 0)}")
        print("\nFechas registradas:")
        fechas = datos.get("fechas", [])
        if fechas:
            for fecha in fechas:
                print(f" - {fecha}")
        else:
            print(" - Sin fechas registradas")
    print("\n" + "=" * 50)