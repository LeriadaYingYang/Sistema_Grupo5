from basedatos_json import leer_json
from director.utilidades import imprimir_titulo, pausa

RUTA_PROFESORES_SALONES = "datos/profesores_salones.json"
RUTA_ASIGNACIONES = "datos/alumnos_asignaciones.json"
RUTA_ALUMNOS = "datos/alumnos.json"


def ver_alumnos_inscritos(profesor):  # muestra los alumnos inscritos en los salones del profesor
    imprimir_titulo("ALUMNOS INSCRITOS")

    profesores_salones = leer_json(RUTA_PROFESORES_SALONES)
    asignaciones = leer_json(RUTA_ASIGNACIONES)
    alumnos = leer_json(RUTA_ALUMNOS)

    # Salones del profesor
    salones_asignados = [
        ps for ps in profesores_salones
        if ps["id_profesor"] == profesor["id_profesor"] and ps["estado"] == "Activo"
    ]

    if not salones_asignados:
        print("\nNo tiene salones asignados.")
        pausa()
        return

    for asignacion in salones_asignados:
        imprimir_titulo(f"Salón: {asignacion['nombre_salon']} | {asignacion['nombre_carrera']} | Turno: {asignacion['turno']}")

        # Alumnos del salón
        alumnos_salon = [
            a for a in asignaciones
            if a["id_salon"] == asignacion["id_salon"]
            and a["id_carrera"] == asignacion["id_carrera"]
            and a["estado"] == "Activo"
        ]

        if not alumnos_salon:
            print("  No hay alumnos inscritos en este salón.")
        else:
            print(f"  {'N°':<5} {'Nombre completo':<30} {'DNI':<15} {'Turno':<10}")
            print("  " + "-" * 60)
            for i, asig in enumerate(alumnos_salon, start=1):
                # Buscar datos completos del alumno
                alumno_detalle = next(
                    (al for al in alumnos if al["id_alumno"] == asig["id_alumno"] and al["estado"] == "Activo"),
                    None
                )
                nombre = asig.get("nombre_alumno", "Sin nombre")
                dni = asig.get("dni", "---")
                turno = asig.get("turno", "---")

                if alumno_detalle:
                    nombre = f"{alumno_detalle['nombres']} {alumno_detalle['apellidos']}"

                print(f"  {i:<5} {nombre:<30} {dni:<15} {turno:<10}")

            print(f"\n  Total de alumnos: {len(alumnos_salon)}")
        print()

    pausa()