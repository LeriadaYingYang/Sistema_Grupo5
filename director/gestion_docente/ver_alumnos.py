from basedatos_json import leer_json
from director.utilidades import imprimir_titulo, pausa

RUTA_PROFESORES_SALONES = "datos/profesores_salones.json"
RUTA_ASIGNACIONES = "datos/alumnos_asignaciones.json"
RUTA_ALUMNOS = "datos/alumnos.json"

def ver_alumnos_inscritos(profesor):
    """Muestra los alumnos inscritos en los salones asignados a un profesor."""
    imprimir_titulo("ALUMNOS INSCRITOS")

    # 1. Validación del parámetro de entrada
    # Verificamos que el argumento 'profesor' sea un diccionario válido y tenga su ID
    if not isinstance(profesor, dict) or "id_profesor" not in profesor:
        print("Error interno: Datos del profesor inválidos o no proporcionados.")
        pausa()
        return

    try:
        # 2. Carga segura de datos (se añade 'or []' por si el JSON devuelve None o está vacío)
        profesores_salones = leer_json(RUTA_PROFESORES_SALONES) or []
        asignaciones = leer_json(RUTA_ASIGNACIONES) or []
        alumnos = leer_json(RUTA_ALUMNOS) or []

        # 3. Filtrar salones del profesor usando .get() para evitar KeyErrors
        salones_asignados = [
            ps for ps in profesores_salones
            if ps.get("id_profesor") == profesor["id_profesor"] and ps.get("estado") == "Activo"
        ]

        if not salones_asignados:
            print("\nNo tiene salones asignados actualmente.")
            return # El finally al final ejecutará la pausa()

        # 4. Procesar y mostrar alumnos por salón
        for asignacion in salones_asignados:
            # Extracción segura con valores por defecto
            nombre_salon = asignacion.get("nombre_salon", "Desconocido")
            nombre_carrera = asignacion.get("nombre_carrera", "Desconocida")
            turno_salon = asignacion.get("turno", "Desconocido")
            id_salon = asignacion.get("id_salon")
            id_carrera = asignacion.get("id_carrera")

            imprimir_titulo(f"Salón: {nombre_salon} | Carrera: {nombre_carrera} | Turno: {turno_salon}")

            # Validar que los IDs existan antes de intentar buscar alumnos
            if id_salon is None or id_carrera is None:
                print("  Advertencia: El salón tiene datos incompletos y no se puede procesar.\n")
                continue

            # Buscar alumnos asignados a este salón y carrera
            alumnos_salon = [
                a for a in asignaciones
                if a.get("id_salon") == id_salon
                and a.get("id_carrera") == id_carrera
                and a.get("estado") == "Activo"
            ]

            if not alumnos_salon:
                print("  No hay alumnos inscritos en este salón.\n")
            else:
                # Cabecera de la tabla ajustada para que los nombres largos encajen
                print(f"  {'N°':<5} {'Nombre completo':<35} {'DNI':<15} {'Turno':<10}")
                print("  " + "-" * 70)

                for i, asig in enumerate(alumnos_salon, start=1):
                    id_alumno = asig.get("id_alumno")

                    # Buscar datos completos en la tabla de alumnos
                    alumno_detalle = next(
                        (al for al in alumnos if al.get("id_alumno") == id_alumno and al.get("estado") == "Activo"),
                        None
                    )

                    # 5. Fallbacks (valores de respaldo) en caso falten datos en el JSON
                    if alumno_detalle:
                        nombres = alumno_detalle.get('nombres', '')
                        apellidos = alumno_detalle.get('apellidos', '')
                        nombre = f"{nombres} {apellidos}".strip()
                        dni = alumno_detalle.get("dni", asig.get("dni", "---"))
                    else:
                        nombre = asig.get("nombre_alumno", "Nombre no registrado")
                        dni = asig.get("dni", "---")

                    turno_alumno = asig.get("turno", "---")

                    # Limitamos el nombre a 33 caracteres [:33] para que no rompa la tabla si es muy largo
                    print(f"  {i:<5} {nombre[:33]:<35} {dni:<15} {turno_alumno:<10}")

                print(f"\n  Total de alumnos: {len(alumnos_salon)}\n")

    except Exception as e:
        # 6. Captura de errores inesperados (archivos corruptos, errores de lectura)
        print(f"\n❌ Ocurrió un error inesperado al procesar la información: {e}")
        print("Verifique que los archivos de base de datos JSON existan y tengan el formato correcto.")

    finally:
        # Esto asegura que la pausa siempre se ejecute al terminar o al fallar
        pausa()