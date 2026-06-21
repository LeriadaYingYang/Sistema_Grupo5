from basedatos_json import leer_json
from director.utilidades import imprimir_titulo, pausa

RUTA_PROFESORES_SALONES = "datos/profesores_salones.json"
RUTA_MODULOS = "datos/modulos.json"
RUTA_UNIDADES = "datos/unidades.json"
RUTA_PLANTILLAS = "datos/plantillas_academicas.json"

def ver_cursos_profesor(profesor):
    """Muestra los cursos/módulos asignados al profesor de forma segura."""
    imprimir_titulo("MIS CURSOS")

    # 1. Validación del parámetro de entrada
    if not isinstance(profesor, dict) or "id_profesor" not in profesor:
        print(" Error interno: Datos del profesor inválidos o no proporcionados.")
        pausa()
        return

    try:
        # 2. Carga segura de JSONs (previene errores si el archivo devuelve None)
        profesores_salones = leer_json(RUTA_PROFESORES_SALONES) or []
        modulos = leer_json(RUTA_MODULOS) or []
        # unidades = leer_json(RUTA_UNIDADES) or [] # (Nota: no se está usando en la lógica actual, pero es bueno tenerlo protegido)

        id_profesor = profesor.get("id_profesor")

        # 3. Filtrado seguro usando .get()
        salones_asignados = [
            ps for ps in profesores_salones
            if ps.get("id_profesor") == id_profesor and ps.get("estado") == "Activo"
        ]

        if not salones_asignados:
            print("\nNo tiene salones asignados actualmente.")
            return # El bloque finally ejecutará la pausa al salir

        total_modulos = 0

        for asignacion in salones_asignados:
            # 4. Extracción con valores por defecto (Fallbacks)
            nombre_carrera = asignacion.get("nombre_carrera", "Carrera Desconocida")
            nombre_salon = asignacion.get("nombre_salon", "Salón Desconocido")
            turno = asignacion.get("turno", "Turno no especificado")
            id_salon = asignacion.get("id_salon")
            id_carrera = asignacion.get("id_carrera")

            imprimir_titulo(f"Carrera: {nombre_carrera}")
            print(f"  Salón  : {nombre_salon}")
            print(f"  Turno  : {turno}\n")

            # Prevención de procesamiento si faltan identificadores clave
            if id_salon is None or id_carrera is None:
                print("  ⚠️ Advertencia: Faltan datos críticos en este salón. No se pueden cargar los módulos.\n")
                continue

            # Buscar módulos del salón de forma segura
            modulos_salon = [
                m for m in modulos
                if m.get("id_salon") == id_salon
                and m.get("id_carrera") == id_carrera
                and m.get("estado") == "Activo"
            ]

            if not modulos_salon:
                print("  No hay módulos registrados para este salón.\n")
            else:
                # Agrupar por unidad
                unidades_vistas = {}
                for modulo in modulos_salon:
                    # Si no hay id_unidad, lo asignamos a un grupo "0" por defecto
                    id_u = modulo.get("id_unidad", 0)

                    if id_u not in unidades_vistas:
                        unidades_vistas[id_u] = {
                            "nombre": modulo.get("nombre_unidad", f"Unidad {id_u}"),
                            "modulos": []
                        }
                    unidades_vistas[id_u]["modulos"].append(modulo)

                # Mostrar módulos agrupados
                for id_u, datos_u in unidades_vistas.items():
                    print(f"   {datos_u['nombre']}")

                    # Ordenar y mostrar de forma segura
                    for m in sorted(datos_u["modulos"], key=lambda x: x.get("orden", 0)):
                        desc_raw = m.get("descripcion", "")
                        desc = f" - {desc_raw}" if desc_raw else ""
                        orden_mod = m.get("orden", "?")
                        nombre_mod = m.get("nombre_modulo", "Módulo sin nombre")

                        print(f"      Módulo {orden_mod}: {nombre_mod}{desc}")
                        total_modulos += 1
                    print()

        print(f"Total de módulos asignados: {total_modulos}")

    except Exception as e:
        # 5. Captura genérica para archivos dañados o estructuras inesperadas
        print(f"\n Ocurrió un error inesperado al procesar los cursos: {e}")
        print("Verifique que los archivos JSON no estén corruptos.")

    finally:
        # 6. Siempre pausar al terminar (sea exitoso o con error)
        pausa()