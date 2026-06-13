from basedatos_json import leer_json
from director.utilidades import imprimir_titulo

RUTA_NOTAS = "datos/notas_alumnos.json"


def alumnos_bajo_rendimiento():

    imprimir_titulo("ALUMNOS CON BAJO RENDIMIENTO")

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

            alumnos[id_alumno] = {
                "nombre": nota["nombre_alumno"],
                "suma": 0,
                "cantidad": 0
            }

        alumnos[id_alumno]["suma"] += nota["promedio_modulo"]
        alumnos[id_alumno]["cantidad"] += 1

    encontrados = False

    print("\nALUMNOS CON PROMEDIO MENOR A 13\n")

    for id_alumno, datos in alumnos.items():

        promedio = round(
            datos["suma"] / datos["cantidad"],
            2
        )

        if promedio < 13:

            encontrados = True

            print(
                f"ID Alumno: {id_alumno}"
                f"\nNombre: {datos['nombre']}"
                f"\nPromedio General: {promedio}"
            )

            print("-" * 40)

    if not encontrados:

        print(
            "No existen alumnos con bajo rendimiento."
        )