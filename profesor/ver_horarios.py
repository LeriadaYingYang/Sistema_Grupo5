from basedatos_json import leer_json
from director.utilidades import imprimir_titulo, pausa

RUTA_PROFESORES_SALONES = "datos/profesores_salones.json"
RUTA_HORARIOS = "datos/horarios.json"

DIAS = {
    "1": "Lunes", "2": "Martes", "3": "Miércoles",
    "4": "Jueves", "5": "Viernes", "6": "Sábado",
    "lunes": "Lunes", "martes": "Martes", "miercoles": "Miércoles",
    "jueves": "Jueves", "viernes": "Viernes", "sabado": "Sábado"
}


def nombre_dia(dia):  # normaliza el nombre del día
    return DIAS.get(str(dia).lower(), dia)


def ver_horarios_profesor(profesor):  # muestra los horarios del salón asignado al profesor
    imprimir_titulo("MIS HORARIOS")

    profesores_salones = leer_json(RUTA_PROFESORES_SALONES)
    horarios = leer_json(RUTA_HORARIOS)

    # Salones asignados al profesor
    salones_asignados = [
        ps for ps in profesores_salones
        if ps["id_profesor"] == profesor["id_profesor"] and ps["estado"] == "Activo"
    ]

    if not salones_asignados:
        print("\nNo tiene salones asignados actualmente.")
        pausa()
        return

    encontro_horario = False

    for asignacion in salones_asignados:
        # Buscar horario del salón y carrera
        horarios_salon = [
            h for h in horarios
            if h["id_salon"] == asignacion["id_salon"]
            and h["id_carrera"] == asignacion["id_carrera"]
            and h["estado"] == "Activo"
        ]

        if not horarios_salon:
            continue

        encontro_horario = True
        imprimir_titulo(f"Salón: {asignacion['nombre_salon']} | {asignacion['nombre_carrera']}")

        for horario in horarios_salon:
            print(f"  Plantilla : {horario.get('nombre_plantilla', '---')}")
            print(f"  Turno     : {horario['turno']}")
            print()

            dias_horas = horario.get("dias_horas", [])
            if not dias_horas:
                print("  Sin horario detallado registrado.")
            else:
                print(f"  {'#':<4} {'Día':<15} {'Hora inicio':<15} {'Hora fin':<10}")
                print("  " + "-" * 44)
                for entrada in sorted(dias_horas, key=lambda x: x["orden"]):
                    dia_nombre = nombre_dia(entrada["dia"])
                    print(f"  {entrada['orden']:<4} {dia_nombre:<15} {entrada['hora_inicio']:<15} {entrada['hora_fin']:<10}")
            print()

    if not encontro_horario:
        print("\nNo se encontraron horarios registrados para sus salones.")

    pausa()