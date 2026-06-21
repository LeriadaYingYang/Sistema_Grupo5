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

def nombre_dia(dia):
    """Normaliza el nombre del día de forma segura, incluso si el valor es nulo."""
    if dia is None:
        return "Desconocido"
    return DIAS.get(str(dia).lower(), str(dia))

def ver_horarios_profesor(profesor):
    """Muestra los horarios del salón asignado al profesor de forma segura."""
    imprimir_titulo("MIS HORARIOS")

    # 1. Validación del parámetro de entrada
    if not isinstance(profesor, dict) or "id_profesor" not in profesor:
        print("Error interno: Datos del profesor inválidos o no proporcionados.")
        pausa()
        return

    try:
        # 2. Carga segura de JSONs (previniendo valores nulos)
        profesores_salones = leer_json(RUTA_PROFESORES_SALONES) or []
        horarios = leer_json(RUTA_HORARIOS) or []

        id_profesor = profesor.get("id_profesor")

        # 3. Filtrado de salones con .get()
        salones_asignados = [
            ps for ps in profesores_salones
            if ps.get("id_profesor") == id_profesor and ps.get("estado") == "Activo"
        ]

        if not salones_asignados:
            print("\nNo tiene salones asignados actualmente.")
            return

        encontro_horario = False

        for asignacion in salones_asignados:
            id_salon = asignacion.get("id_salon")
            id_carrera = asignacion.get("id_carrera")

            # Evitar buscar si faltan los IDs clave
            if id_salon is None or id_carrera is None:
                continue

            # Buscar horario del salón y carrera de forma segura
            horarios_salon = [
                h for h in horarios
                if h.get("id_salon") == id_salon
                and h.get("id_carrera") == id_carrera
                and h.get("estado") == "Activo"
            ]

            if not horarios_salon:
                continue

            encontro_horario = True

            # 4. Valores de respaldo para la cabecera
            nombre_salon = asignacion.get("nombre_salon", "Salón Desconocido")
            nombre_carrera = asignacion.get("nombre_carrera", "Carrera Desconocida")

            imprimir_titulo(f"Salón: {nombre_salon} | {nombre_carrera}")

            for horario in horarios_salon:
                print(f"  Plantilla : {horario.get('nombre_plantilla', '---')}")
                print(f"  Turno     : {horario.get('turno', '---')}")
                print()

                # Validar que dias_horas exista y sea realmente una lista
                dias_horas = horario.get("dias_horas")
                if not dias_horas or not isinstance(dias_horas, list):
                    print("  Sin horario detallado registrado.\n")
                    continue

                print(f"  {'#':<4} {'Día':<15} {'Hora inicio':<15} {'Hora fin':<10}")
                print("  " + "-" * 44)

                # 5. Ordenamiento seguro de la lista de horarios
                for entrada in sorted(dias_horas, key=lambda x: x.get("orden", 0) if isinstance(x, dict) else 0):
                    # Verificamos que la entrada del día sea un diccionario válido
                    if not isinstance(entrada, dict):
                        continue

                    orden = entrada.get("orden", "?")
                    dia_nombre = nombre_dia(entrada.get("dia", "---"))
                    hora_inicio = entrada.get("hora_inicio", "---")
                    hora_fin = entrada.get("hora_fin", "---")

                    print(f"  {orden:<4} {dia_nombre:<15} {hora_inicio:<15} {hora_fin:<10}")
                print()

        if not encontro_horario:
            print("\nNo se encontraron horarios registrados para sus salones.")

    except Exception as e:
        # 6. Captura de errores inesperados
        print(f"\n❌ Ocurrió un error inesperado al procesar los horarios: {e}")
        print("Verifique que los archivos JSON tengan la estructura correcta.")

    finally:
        # 7. Pausa obligatoria al finalizar
        pausa()