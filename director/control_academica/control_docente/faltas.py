from basedatos_json import leer_json
from director.utilidades import imprimir_titulo

RUTA_ASISTENCIA = "datos/asistencia_profesores.json"

def profesores_con_faltas():
    imprimir_titulo("PROFESORES CON FALTAS")
    asistencias = leer_json(RUTA_ASISTENCIA)
    if not asistencias:
        print("No existen registros de asistencia.")
        return
    faltas_por_profesor = {}
    for registro in asistencias:
        estado_asistencia = registro.get("estado_asistencia",registro.get("estado", ""))
        if str(estado_asistencia).lower() != "falta":
            continue
        id_profesor = registro.get("id_profesor")
        if id_profesor not in faltas_por_profesor:
            faltas_por_profesor[id_profesor] = {"nombre": registro.get("nombre_profesor",f"Profesor {id_profesor}"),"cantidad": 0,"fechas": []}
        faltas_por_profesor[id_profesor]["cantidad"] += 1
        faltas_por_profesor[id_profesor]["fechas"].append(registro.get("fecha", "Sin fecha"))
    if not faltas_por_profesor:
        print("No existen profesores con faltas registradas.")
        return
    for id_profesor, datos in faltas_por_profesor.items():
        print("\n" + "=" * 50)
        print(f"ID Profesor: {id_profesor}")
        print(f"Nombre: {datos['nombre']}")
        print(f"Cantidad de faltas: {datos['cantidad']}")
        print("\nFechas registradas:")
        for fecha in datos["fechas"]:
            print(f" - {fecha}")
    print("\n" + "=" * 50)