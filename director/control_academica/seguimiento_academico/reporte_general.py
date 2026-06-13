from basedatos_json import leer_json
from director.utilidades import imprimir_titulo

RUTA_NOTAS = "datos/notas_alumnos.json"

def reporte_academico_general():
    imprimir_titulo("REPORTE ACADÉMICO GENERAL")
    notas = leer_json(RUTA_NOTAS)
    if not notas:
        print("No existen registros de notas.")
        return
    alumnos = {}
    for nota in notas:
        if nota["estado"] != "Activo":
            continue
        id_alumno = nota["id_alumno"]
        if id_alumno not in alumnos:
            alumnos[id_alumno] = {"nombre": nota["nombre_alumno"],"suma": 0,"cantidad": 0}
        alumnos[id_alumno]["suma"] += nota["promedio_modulo"]
        alumnos[id_alumno]["cantidad"] += 1
    if len(alumnos) == 0:
        print("No existen alumnos evaluados.")
        return
    total_alumnos = 0
    suma_general = 0
    aprobados = 0
    desaprobados = 0
    mejor_alumno = ""
    mejor_promedio = -1
    peor_alumno = ""
    peor_promedio = 21
    for datos in alumnos.values():
        promedio = round(datos["suma"] / datos["cantidad"],2)
        total_alumnos += 1
        suma_general += promedio
        if promedio >= 13:
            aprobados += 1
        else:
            desaprobados += 1
        if promedio > mejor_promedio:
            mejor_promedio = promedio
            mejor_alumno = datos["nombre"]
        if promedio < peor_promedio:
            peor_promedio = promedio
            peor_alumno = datos["nombre"]
    promedio_general = round(suma_general / total_alumnos,2)
    imprimir_titulo("RESUMEN GENERAL")
    print(f"Total de alumnos evaluados: {total_alumnos}")
    print(
        f"Promedio académico general: "
        f"{promedio_general}"
    )
    print(f"Aprobados (>=13): {aprobados}")
    print(f"Desaprobados (<13): {desaprobados}")
    print(
        f"\nMejor alumno: "
        f"{mejor_alumno}"
    )
    print(
        f"Promedio: "
        f"{mejor_promedio}"
    )
    print(
        f"\nAlumno con menor rendimiento: "
        f"{peor_alumno}"
    )
    print(
        f"Promedio: "
        f"{peor_promedio}"
    )