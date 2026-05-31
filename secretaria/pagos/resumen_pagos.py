from basedatos_json import leer_json
from director.utilidades import imprimir_titulo

RUTA_PLANTILLAS = "datos/plantillas_academicas.json"
RUTA_SALONES = "datos/salones.json"
RUTA_ALUMNOS = "datos/alumnos.json"
RUTA_ASIGNACIONES = "datos/alumnos_asignaciones.json"
RUTA_CARGOS_OFICIALES = "datos/cargos_oficiales.json"
RUTA_DESCUENTOS_ALUMNOS = "datos/descuentos_alumnos.json"
RUTA_CARGOS_EXTRAS = "datos/cargos_extras.json"
RUTA_PAGOS_REALIZADOS = "datos/pagos_realizados.json"

def buscar_por_id(lista, campo_id, valor_id):  #Busca un registro activo usando su campo id
    for item in lista:
        if item[campo_id] == valor_id and item["estado"] == "Activo":
            return item
    return None

def mostrar_plantillas(plantillas):  #Muestra las plantillas activas para elegir una
    imprimir_titulo("=== PLANTILLAS ===")
    for plantilla in plantillas:
        if plantilla["estado"] == "Activo":
            print(f"ID: {plantilla['id_plantilla']} | {plantilla['nombre_plantilla']} | Carrera: {plantilla['nombre_carrera']}")

def mostrar_salones(salones, id_carrera):  #Muestra los salones activos de la carrera seleccionada
    imprimir_titulo("=== SALONES ===")
    for salon in salones:
        if salon["estado"] == "Activo" and salon["id_carrera"] == id_carrera:
            print(f"ID: {salon['id_salon']} | {salon['nombre_salon']} | Turno: {salon['turno']}")

def obtener_alumnos_salon(alumnos, asignaciones, id_salon):  #Obtiene los alumnos asignados al salón elegido
    resultado = []
    for asignacion in asignaciones:
        if asignacion["estado"] == "Activo" and asignacion["id_salon"] == id_salon:
            alumno = buscar_por_id(alumnos, "id_alumno", asignacion["id_alumno"])
            if alumno:
                resultado.append(alumno)
    return resultado


def obtener_cargos_oficiales(cargos, id_plantilla, id_carrera):  #Obtiene los cargos oficiales de una plantilla y carrera
    resultado = []
    for cargo in cargos:
        if (
            cargo["estado"] == "Activo"
            and cargo["id_plantilla"] == id_plantilla
            and cargo["id_carrera"] == id_carrera):
            resultado.append(cargo)
    return resultado

def obtener_descuento_alumno(descuentos, id_alumno, id_cargo_oficial):  #Busca el descuento activo del alumno para un cargo oficial
    for descuento in descuentos:
        if (
            descuento["estado"] == "Activo"
            and descuento["id_alumno"] == id_alumno
            and descuento["id_cargo_oficial"] == id_cargo_oficial):
            return descuento
    return None

def obtener_cargos_extras_alumno(cargos_extras, id_plantilla, id_carrera, id_salon, id_alumno):  #Obtiene cargos extras aplicados por carrera, salón o alumno
    resultado = []
    for cargo in cargos_extras:
        if cargo["estado"] != "Activo":
            continue
        if cargo["id_plantilla"] != id_plantilla:
            continue
        if cargo["aplica_a"] == "Carrera" and cargo["id_carrera"] == id_carrera:
            resultado.append(cargo)
        elif cargo["aplica_a"] == "Salón" and cargo.get("id_salon") == id_salon:
            resultado.append(cargo)
        elif cargo["aplica_a"] == "Alumno" and cargo.get("id_alumno") == id_alumno:
            resultado.append(cargo)
    return resultado

def obtener_total_pagado(pagos, id_alumno, id_plantilla):  #Suma los pagos realizados por el alumno en una plantilla
    total = 0
    for pago in pagos:
        if (
            pago["estado"] == "Activo"
            and pago["id_alumno"] == id_alumno
            and pago["id_plantilla"] == id_plantilla):
            total += pago["monto_pagado"]
    return round(total, 2)

def calcular_deuda_alumno(alumno, plantilla, salon, cargos_oficiales, descuentos, cargos_extras, pagos):  #Calcula cargos, descuentos, pagos y deuda final del alumno
    total_oficial = 0
    total_descuentos = 0
    total_extra = 0
    detalle_oficial = []
    detalle_extra = []
    for cargo in cargos_oficiales:
        descuento = obtener_descuento_alumno(descuentos, alumno["id_alumno"], cargo["id_cargo_oficial"])
        monto_final = cargo["monto"]
        if descuento:
            monto_final = descuento["monto_final"]
            total_descuentos += cargo["monto"] - monto_final
        total_oficial += monto_final
        detalle_oficial.append({
            "cargo": cargo["nombre_cargo"],
            "monto_original": cargo["monto"],
            "monto_final": monto_final,
            "descuento": descuento["nombre_descuento"] if descuento else "Sin descuento"})
    extras = obtener_cargos_extras_alumno(
        cargos_extras,
        plantilla["id_plantilla"],
        plantilla["id_carrera"],
        salon["id_salon"],
        alumno["id_alumno"])
    for extra in extras:
        total_extra += extra["monto"]
        detalle_extra.append({
            "cargo": extra["nombre"],
            "monto": extra["monto"],
            "aplica_a": extra["aplica_a"]})
    total_debe = round(total_oficial + total_extra, 2)
    total_pagado = obtener_total_pagado(pagos, alumno["id_alumno"], plantilla["id_plantilla"])
    deuda = round(total_debe - total_pagado, 2)
    return {
        "alumno": alumno["nombres"] + " " + alumno["apellidos"],
        "dni": alumno["dni"],
        "total_oficial": round(total_oficial, 2),
        "total_descuentos": round(total_descuentos, 2),
        "total_extra": round(total_extra, 2),
        "total_debe": total_debe,
        "total_pagado": total_pagado,
        "deuda": deuda,
        "detalle_oficial": detalle_oficial,
        "detalle_extra": detalle_extra}

def mostrar_resumen_alumno(resumen):  #Imprime el detalle completo de deuda, cargos y pagos de un alumno
    print("\n------------------------------------")
    print(f"Alumno: {resumen['alumno']}")
    print(f"DNI: {resumen['dni']}")
    print("\nCARGOS OFICIALES:")
    for item in resumen["detalle_oficial"]:
        print(f"- {item['cargo']} | Original: S/ {item['monto_original']} | Descuento: {item['descuento']} | Final: S/ {item['monto_final']}")
    print("\nCARGOS EXTRAS:")
    if len(resumen["detalle_extra"]) == 0:
        print("- Sin cargos extras")
    else:
        for item in resumen["detalle_extra"]:
            print(f"- {item['cargo']} | S/ {item['monto']} | Aplica a: {item['aplica_a']}")
    print("\nRESUMEN:")
    print(f"Total cargos oficiales: S/ {resumen['total_oficial']}")
    print(f"Total descuentos aplicados: S/ {resumen['total_descuentos']}")
    print(f"Total cargos extras: S/ {resumen['total_extra']}")
    print(f"Total a pagar: S/ {resumen['total_debe']}")
    print(f"Total pagado: S/ {resumen['total_pagado']}")
    print(f"Deuda: S/ {resumen['deuda']}")

def seleccionar_plantilla_salon():  #Permite elegir la plantilla y salón antes de generar un reporte
    plantillas = leer_json(RUTA_PLANTILLAS)
    salones = leer_json(RUTA_SALONES)
    mostrar_plantillas(plantillas)

#Solicita al usuario que ingrese el ID de la plantilla y salón para generar el resumen financiero
    try:
        id_plantilla = int(input("\nIngrese ID de plantilla: "))
    except ValueError:
        print("Debe ingresar un número.")
        return None, None
    plantilla = buscar_por_id(plantillas, "id_plantilla", id_plantilla)
    if plantilla is None:
        print("Plantilla no válida.")
        return None, None
    mostrar_salones(salones, plantilla["id_carrera"])

#Solicita al usuario que ingrese el ID del salón para generar el resumen financiero
    try:
        id_salon = int(input("\nIngrese ID de salón: "))
    except ValueError:
        print("Debe ingresar un número.")
        return None, None
    salon = buscar_por_id(salones, "id_salon", id_salon)
    if salon is None or salon["id_carrera"] != plantilla["id_carrera"]:
        print("Salón no válido.")
        return None, None
    return plantilla, salon

def resumen_por_salon():  #Genera el resumen financiero de todos los alumnos de un salón
    alumnos = leer_json(RUTA_ALUMNOS)
    asignaciones = leer_json(RUTA_ASIGNACIONES)
    cargos = leer_json(RUTA_CARGOS_OFICIALES)
    descuentos = leer_json(RUTA_DESCUENTOS_ALUMNOS)
    cargos_extras = leer_json(RUTA_CARGOS_EXTRAS)
    pagos = leer_json(RUTA_PAGOS_REALIZADOS)
    plantilla, salon = seleccionar_plantilla_salon()
    if plantilla is None or salon is None:
        return
    alumnos_salon = obtener_alumnos_salon(alumnos, asignaciones, salon["id_salon"])
    cargos_oficiales = obtener_cargos_oficiales(cargos, plantilla["id_plantilla"], plantilla["id_carrera"])
    if len(alumnos_salon) == 0:
        print("No hay alumnos en este salón.")
        return
    if len(cargos_oficiales) == 0:
        print("No hay cargos oficiales para esta plantilla y carrera.")
        return
    print("\n=== RESUMEN POR SALÓN ===")
    print(f"Plantilla: {plantilla['nombre_plantilla']}")
    print(f"Carrera: {plantilla['nombre_carrera']}")
    print(f"Salón: {salon['nombre_salon']} | Turno: {salon['turno']}")
    total_general_debe = 0
    total_general_pagado = 0
    total_general_deuda = 0
    for alumno in alumnos_salon:
        resumen = calcular_deuda_alumno(alumno, plantilla, salon, cargos_oficiales, descuentos, cargos_extras, pagos)
        mostrar_resumen_alumno(resumen)
        total_general_debe += resumen["total_debe"]
        total_general_pagado += resumen["total_pagado"]
        total_general_deuda += resumen["deuda"]
    print("\n=== TOTAL GENERAL DEL SALÓN ===")
    print(f"Total a pagar: S/ {round(total_general_debe, 2)}")
    print(f"Total pagado: S/ {round(total_general_pagado, 2)}")
    print(f"Total deuda: S/ {round(total_general_deuda, 2)}")

def resumen_por_alumno():  #Genera el resumen financiero de un alumno específico
    alumnos = leer_json(RUTA_ALUMNOS)
    asignaciones = leer_json(RUTA_ASIGNACIONES)
    cargos = leer_json(RUTA_CARGOS_OFICIALES)
    descuentos = leer_json(RUTA_DESCUENTOS_ALUMNOS)
    cargos_extras = leer_json(RUTA_CARGOS_EXTRAS)
    pagos = leer_json(RUTA_PAGOS_REALIZADOS)
    plantilla, salon = seleccionar_plantilla_salon()
    if plantilla is None or salon is None:
        return
    alumnos_salon = obtener_alumnos_salon(alumnos, asignaciones, salon["id_salon"])
    if len(alumnos_salon) == 0:
        print("No hay alumnos en este salón.")
        return
    imprimir_titulo("=== ALUMNOS DEL SALÓN ===")
    for alumno in alumnos_salon:
        print(f"ID: {alumno['id_alumno']} | {alumno['nombres']} {alumno['apellidos']} | DNI: {alumno['dni']}")
    try:
        id_alumno = int(input("\nIngresar ID del alumno: "))
    except ValueError:
        print("Debe ingresar un número.")
        return
    alumno = buscar_por_id(alumnos, "id_alumno", id_alumno)
    if alumno is None:
        print("Alumno no válido.")
        return
    cargos_oficiales = obtener_cargos_oficiales(cargos, plantilla["id_plantilla"], plantilla["id_carrera"])
    resumen = calcular_deuda_alumno(alumno, plantilla, salon, cargos_oficiales, descuentos, cargos_extras, pagos)
    mostrar_resumen_alumno(resumen)

def alumnos_con_deuda():  #Lista solo los alumnos que tienen deuda pendiente en el salón
    alumnos = leer_json(RUTA_ALUMNOS)
    asignaciones = leer_json(RUTA_ASIGNACIONES)
    cargos = leer_json(RUTA_CARGOS_OFICIALES)
    descuentos = leer_json(RUTA_DESCUENTOS_ALUMNOS)
    cargos_extras = leer_json(RUTA_CARGOS_EXTRAS)
    pagos = leer_json(RUTA_PAGOS_REALIZADOS)
    plantilla, salon = seleccionar_plantilla_salon()
    if plantilla is None or salon is None:
        return
    alumnos_salon = obtener_alumnos_salon(alumnos, asignaciones, salon["id_salon"])
    cargos_oficiales = obtener_cargos_oficiales(cargos, plantilla["id_plantilla"], plantilla["id_carrera"])
    print("\n=== ALUMNOS CON DEUDA ===")
    encontrados = 0
    for alumno in alumnos_salon:
        resumen = calcular_deuda_alumno(alumno, plantilla, salon, cargos_oficiales, descuentos, cargos_extras, pagos)
        if resumen["deuda"] > 0:
            encontrados += 1
            print("\n-----------------------------")
            print(f"Alumno: {resumen['alumno']}")
            print(f"DNI: {resumen['dni']}")
            print(f"Total a pagar: S/ {resumen['total_debe']}")
            print(f"Pagado: S/ {resumen['total_pagado']}")
            print(f"Deuda: S/ {resumen['deuda']}")
    if encontrados == 0:
        print("No hay alumnos con deuda en este salón.")

def menu_resumen_pagos():  #Muestra el menú para consultar resúmenes financieros
    while True:
        print("""
=== RESUMEN DE PAGOS Y DEUDAS ===
1. Resumen por salón
2. Resumen por alumno
3. Alumnos con deuda
4. Volver
""")
        opcion = input("Seleccionar una opción: ")
        if opcion == "1":
            resumen_por_salon()
        elif opcion == "2":
            resumen_por_alumno()
        elif opcion == "3":
            alumnos_con_deuda()
        elif opcion == "4":
            break
        else:
            print("Opción inválida.")