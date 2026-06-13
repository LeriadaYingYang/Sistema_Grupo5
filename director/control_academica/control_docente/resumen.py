from basedatos_json import leer_json
from director.utilidades import imprimir_titulo

RUTA_ASISTENCIA = "datos/asistencia_profesores.json"

def resumen_desempeno_docente():
    imprimir_titulo("RESUMEN DE DESEMPEÑO DOCENTE")
    asistencias = leer_json(RUTA_ASISTENCIA)
    if not asistencias:
        print("No existen registros de asistencia.")
        return
    docentes = {}
    for registro in asistencias:
        id_profesor = registro.get("id_profesor")
        if id_profesor is None:
            continue
        if id_profesor not in docentes:
            docentes[id_profesor] = {"nombre": registro.get("nombre_profesor",f"Profesor {id_profesor}"),
                "asistencias": 0,"tardanzas": 0,
                "faltas": 0,"horas": 0}
        estado = str(registro.get("estado_asistencia","")).strip().lower()
        if estado == "presente":
            docentes[id_profesor]["asistencias"] += 1
        elif estado == "tardanza":
            docentes[id_profesor]["tardanzas"] += 1
        elif estado == "falta":
            docentes[id_profesor]["faltas"] += 1
        docentes[id_profesor]["horas"] += registro.get("horas_trabajadas",0)
    for id_profesor, datos in docentes.items():
        faltas = datos["faltas"]
        tardanzas = datos["tardanzas"]
        if faltas == 0 and tardanzas <= 2:
            desempeno = "Excelente"
        elif faltas <= 2:
            desempeno = "Bueno"
        else:
            desempeno = "Regular"
        print("\n" + "=" * 50)
        print(f"ID Profesor: {id_profesor}")
        print(f"Nombre: {datos['nombre']}")
        print(
            f"Asistencias: "
            f"{datos['asistencias']}"
        )
        print(
            f"Tardanzas: "
            f"{datos['tardanzas']}"
        )
        print(
            f"Faltas: "
            f"{datos['faltas']}"
        )
        print(
            f"Horas trabajadas: "
            f"{round(datos['horas'], 2)}"
        )
        print(
            f"Desempeño: "
            f"{desempeno}"
        )
    print("\n" + "=" * 50)