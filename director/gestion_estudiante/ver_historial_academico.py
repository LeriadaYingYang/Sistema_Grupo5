from basedatos_json import leer_json
from director.utilidades import imprimir_titulo, pausa

def ver_historial_academico():
    # Esta vista reúne datos personales, asignación y notas de un alumno activo.
    imprimir_titulo("HISTORIAL ACADÉMICO DE ALUMNOS")

    # Primero se consulta el padrón de alumnos para validar que exista el DNI buscado.
    alumnos = leer_json("datos/alumnos.json")
    if not alumnos:
        print("No hay alumnos registrados.")
        pausa()
        return

    # Se pide el DNI porque es la clave más directa para encontrar al alumno.
    dni = input("Ingrese DNI del alumno: ").strip()
    alumno = None
    for a in alumnos:
        if a["dni"] == dni and a["estado"] == "Activo":
            alumno = a
            break

    if alumno is None:
        print("Alumno no encontrado.")
        pausa()
        return

    # Se muestran primero los datos básicos del estudiante.
    print("\n ------ DATOS DEL ALUMNO ------")
    print(f"Alumno : {alumno['nombres']} {alumno['apellidos']}")
    print(f"DNI: {alumno['dni']}")
    print(f"Correo: {alumno['correo']}")
    print(f"Celular: {alumno['celular']}")
    print(f"Estado: {alumno['estado']}")

    # Luego se busca su asignación actual para mostrar carrera, salón y turno.
    asignaciones = leer_json("datos/alumnos_asignaciones.json")
    for asig in asignaciones:

        if asig['id_alumno'] == alumno['id_alumno'] and asig["estado"] == "Activo":
            print(f"Carrera: {asig['nombre_carrera']}")
            print(f"Salon: {asig['nombre_salon']} - Turno: {asig['turno']}")
            break

    # Se cargan las notas y los catálogos de unidades y módulos para ordenar el historial.
    notas = leer_json("datos/notas_alumnos.json")
    unidades = leer_json("datos/unidades.json")
    modulos = leer_json("datos/modulos.json")

    # Se filtran solo las notas activas del alumno actual.
    notas_alumno = []
    for r in notas:
        if r["id_alumno"] == alumno["id_alumno"] and r["estado"] == "Activo":
            notas_alumno.append(r)

    if not notas_alumno:
        print("\nNo tiene notas registradas.")
        pausa()
        return

    # Se obtiene una lista de unidades sin repetir para mostrarlas en orden.
    ids_unidad = []
    for r in notas_alumno:
        if r["id_unidad"] not in ids_unidad:
            ids_unidad.append(r["id_unidad"])

    # Se ordenan las unidades según el campo orden de cada registro.
    unidades_ordenadas = []
    for id_u in ids_unidad:
        orden_u = 0
        for u in unidades:
            if u["id_unidad"] == id_u and u["estado"] == "Activo":
                orden_u = u["orden"]
                break
        unidades_ordenadas.append((orden_u, id_u))
    unidades_ordenadas.sort()

    todos_promedios = []
    for orden_u, id_u in unidades_ordenadas:
        # Se busca el nombre de la unidad para imprimir un encabezado claro.
        nombre_unidad = ""
        for u in unidades:
            if u["id_unidad"] == id_u and u["estado"] == "Activo":
                nombre_unidad = u["nombre_unidad"]
                break

        print(f"\n=== {nombre_unidad} ===")

        # Dentro de cada unidad, los módulos también se ordenan antes de mostrarlos.
        modulos_unidad = []
        for reg in notas_alumno:
            if reg["id_unidad"] == id_u:
                orden_m = 0
                for m in modulos:
                    if m["id_modulo"] == reg["id_modulo"] and m["estado"] == "Activo":
                        orden_m = m["orden"]
                        break
                modulos_unidad.append((orden_m, reg))
        modulos_unidad.sort()

        for orden_m, reg in modulos_unidad:
            # Se obtiene el nombre del módulo para que el reporte sea entendible.
            nombre_modulo = ""
            for m in modulos:
                if m["id_modulo"] == reg["id_modulo"] and m["estado"] == "Activo":
                    nombre_modulo = m["nombre_modulo"]
                    break

            print(f"\n Modulo: {nombre_modulo}")
            # Cada nota se imprime con su nombre y su valor; si está vacía, se muestra como pendiente.
            for n in reg["notas"]:
                valor = n["nota"] if n["nota"] != "" else "Sin nota"
                print(f"   {n['nombre_nota']}: {valor}")
            print(f"  Promedio: {reg['promedio_modulo']}")
            # Los promedios válidos se guardan para calcular la condición final.
            if reg["promedio_modulo"] is not None:
                todos_promedios.append(reg["promedio_modulo"])

    if todos_promedios:
        # El promedio final se redondea y luego se convierte en una condición académica.
        promedio_final = round(sum(todos_promedios) / len(todos_promedios))
        if promedio_final >= 18:
            condicion = "A"
        elif promedio_final >= 15:
            condicion = "B"
        elif promedio_final >= 13:
            condicion = "C"
        elif promedio_final >= 11:
            condicion = "D"
        else:
            condicion = "DESAPROBADO"
        print(f"\n>>>>> PROMEDIO FINAL: {promedio_final}")
        print(f">>>>> CONDICION: {condicion}")

    pausa()