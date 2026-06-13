from basedatos_json import leer_json
from director.utilidades import imprimir_titulo

RUTA_NOTAS = "datos/notas_alumnos.json"

def ver_notas_modulo():
    imprimir_titulo("VER NOTAS POR MÓDULO")
    notas = leer_json(RUTA_NOTAS)
    if not notas:
        print("No existen registros de notas.")
        return
    modulos = sorted(list(set(nota["id_modulo"] for nota in notas if nota["estado"] == "Activo")))
    print("\nMÓDULOS DISPONIBLES")
    for modulo in modulos:
        print(f"Módulo ID: {modulo}")
    try:
        id_modulo = int(input("\nIngrese ID del módulo: "))
    except ValueError:
        print("Debe ingresar un número.")
        return
    resultados = [nota for nota in notas
        if (nota["estado"] == "Activo" and nota["id_modulo"] == id_modulo)]
    if len(resultados) == 0:
        print("No existen notas para ese módulo.")
        return
    imprimir_titulo("NOTAS DEL MÓDULO")
    suma = 0
    for registro in resultados:
        promedio = registro["promedio_modulo"]
        suma += promedio
        print(
            f"\nAlumno: {registro['nombre_alumno']}"
            f"\nID Unidad: {registro['id_unidad']}"
            f"\nPromedio Módulo: {promedio}"
        )
        print("\nDetalle:")
        for grupo in registro["grupos"]:
            print(f"\nGrupo: {grupo['nombre_grupo']}")
            print(
                f"Promedio Grupo: "
                f"{grupo['promedio_grupo']}"
            )
            for actividad in grupo["actividades"]:
                print(
                    f"  - {actividad['nombre_actividad']}: "
                    f"{actividad['nota']}"
                )
        print("\n" + "-" * 40)
    promedio_general = round(suma / len(resultados),2)
    print(
        f"\nPROMEDIO GENERAL DEL MÓDULO: "
        f"{promedio_general}"
    )