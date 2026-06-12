from basedatos_json import leer_json
from director.utilidades import imprimir_titulo, pausa

RUTA_PROFESORES_SALONES = "datos/profesores_salones.json"
RUTA_MODULOS = "datos/modulos.json"
RUTA_UNIDADES = "datos/unidades.json"
RUTA_PLANTILLAS = "datos/plantillas_academicas.json"


def ver_cursos_profesor(profesor):  # muestra los cursos/módulos asignados al profesor según su salón
    imprimir_titulo("MIS CURSOS")

    profesores_salones = leer_json(RUTA_PROFESORES_SALONES)
    modulos = leer_json(RUTA_MODULOS)
    unidades = leer_json(RUTA_UNIDADES)

    # Buscar salones asignados al profesor
    salones_asignados = [
        ps for ps in profesores_salones
        if ps["id_profesor"] == profesor["id_profesor"] and ps["estado"] == "Activo"
    ]

    if not salones_asignados:
        print("\nNo tiene salones asignados actualmente.")
        pausa()
        return

    total_modulos = 0

    for asignacion in salones_asignados:
        imprimir_titulo(f"Carrera: {asignacion['nombre_carrera']}")
        print(f"  Salón  : {asignacion['nombre_salon']}")
        print(f"  Turno  : {asignacion['turno']}")
        print()

        # Buscar módulos del salón
        modulos_salon = [
            m for m in modulos
            if m["id_salon"] == asignacion["id_salon"]
            and m["id_carrera"] == asignacion["id_carrera"]
            and m["estado"] == "Activo"
        ]

        if not modulos_salon:
            print("  No hay módulos registrados para este salón.")
        else:
            # Agrupar por unidad
            unidades_vistas = {}
            for modulo in modulos_salon:
                id_u = modulo["id_unidad"]
                if id_u not in unidades_vistas:
                    unidades_vistas[id_u] = {
                        "nombre": modulo.get("nombre_unidad", f"Unidad {id_u}"),
                        "modulos": []
                    }
                unidades_vistas[id_u]["modulos"].append(modulo)

            for id_u, datos_u in unidades_vistas.items():
                print(f"  📚 {datos_u['nombre']}")
                for m in sorted(datos_u["modulos"], key=lambda x: x.get("orden", 0)):
                    desc = f" - {m['descripcion']}" if m.get("descripcion") else ""
                    print(f"      Módulo {m['orden']}: {m['nombre_modulo']}{desc}")
                    total_modulos += 1
                print()

    print(f"Total de módulos asignados: {total_modulos}")
    pausa()