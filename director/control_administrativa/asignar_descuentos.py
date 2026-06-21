from basedatos_json import leer_json, guardar_json, generar_id
from director.utilidades import imprimir_titulo

RUTA_PLANTILLAS = "datos/plantillas_academicas.json"
RUTA_SALONES = "datos/salones.json"
RUTA_ALUMNOS = "datos/alumnos.json"
RUTA_ASIGNACIONES = "datos/alumnos_asignaciones.json"
RUTA_CARGOS_OFICIALES = "datos/cargos_oficiales.json"
RUTA_DESCUENTOS = "datos/descuentos_convenios.json"
RUTA_DESCUENTOS_ALUMNOS = "datos/descuentos_alumnos.json"

def buscar_por_id(lista, campo_id, valor_id):  #busca un registro activo utilizando su identificador
    for item in lista:
        if item[campo_id] == valor_id and item["estado"] == "Activo":
            return item
    return None

def calcular_monto_final(monto, descuento):  #calcula el monto final luego de aplicar un descuento o convenio
    if descuento["tipo"] == "Porcentaje":
        return round(monto - (monto * descuento["valor"] / 100), 2)

    if descuento["tipo"] == "Monto fijo":
        final = monto - descuento["valor"]
        return round(final if final > 0 else 0, 2)

    return monto


def mostrar_plantillas(plantillas):  #muestra las plantillas disponibles para asignar descuentos
    imprimir_titulo("PLANTILLAS")
    for plantilla in plantillas:
        if plantilla["estado"] == "Activo":
            print(
                f"ID: {plantilla['id_plantilla']} | "
                f"{plantilla['nombre_plantilla']} | "
                f"Carrera: {plantilla['nombre_carrera']}")

def mostrar_salones(salones, id_carrera):  #muestra los salones de la carrera seleccionada
    imprimir_titulo("SALONES")
    for salon in salones:
        if salon["estado"] == "Activo" and salon["id_carrera"] == id_carrera:
            print(
                f"ID: {salon['id_salon']} | "
                f"{salon['nombre_salon']} | "
                f"Turno: {salon['turno']}")


def mostrar_alumnos_salon(alumnos, asignaciones, id_salon):  #muestra los alumnos asignados al salón seleccionado
    imprimir_titulo("ALUMNOS DEL SALÓN")
    encontrados = 0
    for asignacion in asignaciones:
        if asignacion["estado"] == "Activo" and asignacion["id_salon"] == id_salon:
            alumno = buscar_por_id(
                alumnos,
                "id_alumno",
                asignacion["id_alumno"])
            if alumno:
                encontrados += 1
                print(
                    f"ID: {alumno['id_alumno']} | "
                    f"{alumno['nombres']} {alumno['apellidos']} | "
                    f"DNI: {alumno['dni']}")
    if encontrados == 0:
        print("No hay alumnos asignados a este salón.")


def mostrar_cargos_oficiales(cargos, id_plantilla, id_carrera):  #muestra los cargos oficiales disponibles para aplicar descuentos
    imprimir_titulo("CARGOS OFICIALES")
    encontrados = 0
    for cargo in cargos:
        if (
            cargo["estado"] == "Activo"
            and cargo["id_plantilla"] == id_plantilla
            and cargo["id_carrera"] == id_carrera):
            encontrados += 1
            print(
                f"ID: {cargo['id_cargo_oficial']} | "
                f"{cargo['nombre_cargo']} | "
                f"S/ {cargo['monto']} | "
                f"{cargo['frecuencia']}")
    if encontrados == 0:
        print("No hay cargos oficiales para esta plantilla y carrera.")

def mostrar_descuentos(descuentos):  # muestra los descuentos y convenios disponibles
    imprimir_titulo("DESCUENTOS / CONVENIOS")
    for descuento in descuentos:
        if descuento["estado"] == "Activo":
            print(
                f"ID: {descuento['id_descuento']} | "
                f"{descuento['nombre']} | "
                f"{descuento['tipo']} | "
                f"{descuento['valor']}")

def descuento_ya_asignado(asignaciones, id_alumno, id_cargo_oficial):  # verifica si el alumno ya tiene descuento para ese cargo
    for asignacion in asignaciones:
        if (
            asignacion["estado"] == "Activo"
            and asignacion["id_alumno"] == id_alumno
            and asignacion["id_cargo_oficial"] == id_cargo_oficial):
            return True
    return False

def asignar_descuento_alumno():  #asigna un descuento o convenio a un alumno para un cargo oficial específico
    imprimir_titulo("ASIGNAR DESCUENTO / CONVENIO")
    plantillas = leer_json(RUTA_PLANTILLAS)
    salones = leer_json(RUTA_SALONES)
    alumnos = leer_json(RUTA_ALUMNOS)
    asignaciones_alumnos = leer_json(RUTA_ASIGNACIONES)
    cargos = leer_json(RUTA_CARGOS_OFICIALES)
    descuentos = leer_json(RUTA_DESCUENTOS)
    descuentos_alumnos = leer_json(RUTA_DESCUENTOS_ALUMNOS)
    if len(cargos) == 0:
        print("Primero debe crear cargos oficiales.")
        return
    if len(descuentos) == 0:
        print("Primero debe crear descuentos o convenios.")
        return
    mostrar_plantillas(plantillas)
    try:
        id_plantilla = int(input("\nIngrese ID de plantilla: "))
    except ValueError:
        print("Debe ingresar un número.")
        return
    plantilla = buscar_por_id(plantillas, "id_plantilla", id_plantilla)
    if plantilla is None:
        print("Plantilla no válida.")
        return
    mostrar_salones(salones, plantilla["id_carrera"])
    try:
        id_salon = int(input("\nIngrese ID de salón: "))
    except ValueError:
        print("Debe ingresar un número.")
        return
    salon = buscar_por_id(salones, "id_salon", id_salon)
    if salon is None or salon["id_carrera"] != plantilla["id_carrera"]:
        print("Salón no válido.")
        return
    mostrar_alumnos_salon(alumnos, asignaciones_alumnos, id_salon)
    try:
        id_alumno = int(input("\nIngrese ID del alumno: "))
    except ValueError:
        print("Debe ingresar un número.")
        return
    alumno = buscar_por_id(alumnos, "id_alumno", id_alumno)
    if alumno is None:
        print("Alumno no válido.")
        return
    mostrar_cargos_oficiales(cargos, id_plantilla, plantilla["id_carrera"])
    try:
        id_cargo = int(input("\nIngrese ID del cargo oficial: "))
    except ValueError:
        print("Debe ingresar un número.")
        return
    cargo = buscar_por_id(cargos, "id_cargo_oficial", id_cargo)
    if cargo is None or cargo["id_plantilla"] != id_plantilla:
        print("Cargo oficial no válido.")
        return
    if descuento_ya_asignado(descuentos_alumnos, id_alumno, id_cargo):
        print("Este alumno ya tiene un descuento activo para este cargo oficial.")
        return
    mostrar_descuentos(descuentos)
    try:
        id_descuento = int(input("\nIngrese ID del descuento/convenio: "))
    except ValueError:
        print("Debe ingresar un número.")
        return
    descuento = buscar_por_id(descuentos, "id_descuento", id_descuento)
    if descuento is None:
        print("Descuento no válido.")
        return
    monto_final = calcular_monto_final(cargo["monto"], descuento)
    nueva_asignacion = {
        "id_descuento_alumno": generar_id(descuentos_alumnos, "id_descuento_alumno"),
        "id_alumno": alumno["id_alumno"],
        "nombre_alumno": alumno["nombres"] + " " + alumno["apellidos"],
        "dni": alumno["dni"],
        "id_plantilla": plantilla["id_plantilla"],
        "nombre_plantilla": plantilla["nombre_plantilla"],
        "id_carrera": plantilla["id_carrera"],
        "nombre_carrera": plantilla["nombre_carrera"],
        "id_salon": salon["id_salon"],
        "nombre_salon": salon["nombre_salon"],
        "turno": salon["turno"],
        "id_cargo_oficial": cargo["id_cargo_oficial"],
        "nombre_cargo": cargo["nombre_cargo"],
        "monto_original": cargo["monto"],
        "id_descuento": descuento["id_descuento"],
        "nombre_descuento": descuento["nombre"],
        "tipo_descuento": descuento["tipo"],
        "valor_descuento": descuento["valor"],
        "monto_final": monto_final,
        "estado": "Activo"}
    descuentos_alumnos.append(nueva_asignacion)  #registra la asignación del descuento para el alumno
    guardar_json(RUTA_DESCUENTOS_ALUMNOS, descuentos_alumnos)  #guarda la asignación en el archivo json
    print("\nDescuento asignado correctamente.")
    print(f"Alumno: {nueva_asignacion['nombre_alumno']}")
    print(f"Cargo oficial: {nueva_asignacion['nombre_cargo']}")
    print(f"Monto original: S/ {nueva_asignacion['monto_original']}")
    print(f"Descuento: {nueva_asignacion['nombre_descuento']}")
    print(f"Monto final: S/ {nueva_asignacion['monto_final']}")

# ====================================================================
# --- NUEVAS FUNCIONES AGREGADAS A PARTIR DE AQUÍ ---
# ====================================================================

def pedir_entero_asignacion(mensaje):
    """Sistema anti-errores para pedir un ID numérico."""
    while True:
        try:
            valor = int(input(mensaje))
            if valor < 0:
                print("Error: No se permiten números negativos.")
            else:
                return valor
        except ValueError:
            print("Error: Debe ingresar un número entero válido (sin letras).")

def ver_descuentos_asignados():
    imprimir_titulo("DESCUENTOS ASIGNADOS A ALUMNOS")
    asignaciones = leer_json(RUTA_DESCUENTOS_ALUMNOS) or []
    
    if len(asignaciones) == 0:
        print("No hay descuentos asignados en el sistema.")
        return False
        
    for a in asignaciones:
        print("\n-----------------------------")
        print(f"ID Asignación: {a.get('id_descuento_alumno')}")
        print(f"Alumno: {a.get('nombre_alumno')} | DNI: {a.get('dni')}")
        print(f"Cargo: {a.get('nombre_cargo')} | Monto original: S/ {a.get('monto_original')}")
        print(f"Descuento: {a.get('nombre_descuento')} ({a.get('valor_descuento')} {a.get('tipo_descuento')})")
        print(f"Monto final a pagar: S/ {a.get('monto_final')} | Estado: {a.get('estado')}")
        
    return True

def modificar_descuento_asignado():
    imprimir_titulo("MODIFICAR DESCUENTO ASIGNADO")
    asignaciones = leer_json(RUTA_DESCUENTOS_ALUMNOS) or []
    descuentos = leer_json(RUTA_DESCUENTOS) or []
    
    if not ver_descuentos_asignados():
        return
        
    id_asignacion = pedir_entero_asignacion("\nIngrese el ID de la asignación que desea modificar: ")
    
    asignacion = None
    for a in asignaciones:
        if a.get("id_descuento_alumno") == id_asignacion:
            asignacion = a
            break
            
    if asignacion is None:
        print("Error: No se encontró la asignación.")
        return
        
    if asignacion.get("estado") != "Activo":
        print("Error: No se puede modificar una asignación inactiva. Restáurela primero.")
        return

    print(f"\nAlumno: {asignacion['nombre_alumno']} | Cargo: {asignacion['nombre_cargo']}")
    print("Seleccione el NUEVO descuento que desea aplicarle a este alumno:")
    
    mostrar_descuentos(descuentos)
    id_nuevo_desc = pedir_entero_asignacion("\nIngrese el ID del nuevo descuento: ")
    
    nuevo_descuento = buscar_por_id(descuentos, "id_descuento", id_nuevo_desc)
    if nuevo_descuento is None:
        print("Error: Descuento no válido o inactivo.")
        return
        
    # Recalculamos el nuevo monto final usando la función original
    nuevo_monto_final = calcular_monto_final(asignacion["monto_original"], nuevo_descuento)
    
    # Actualizamos los datos de la asignación
    asignacion["id_descuento"] = nuevo_descuento["id_descuento"]
    asignacion["nombre_descuento"] = nuevo_descuento["nombre"]
    asignacion["tipo_descuento"] = nuevo_descuento["tipo"]
    asignacion["valor_descuento"] = nuevo_descuento["valor"]
    asignacion["monto_final"] = nuevo_monto_final
    
    guardar_json(RUTA_DESCUENTOS_ALUMNOS, asignaciones)
    print("\n✅ Asignación actualizada correctamente.")
    print(f"El nuevo monto final a pagar es: S/ {nuevo_monto_final}")

def eliminar_descuento_asignado():
    imprimir_titulo("ELIMINAR / RESTAURAR ASIGNACIÓN")
    asignaciones = leer_json(RUTA_DESCUENTOS_ALUMNOS) or []
    
    if not ver_descuentos_asignados():
        return
        
    id_asignacion = pedir_entero_asignacion("\nIngrese el ID de la asignación a eliminar/restaurar: ")
    
    for a in asignaciones:
        if a.get("id_descuento_alumno") == id_asignacion:
            if a.get("estado") == "Activo":
                a["estado"] = "Inactivo"
                print(f"\n Se ha eliminado el descuento del alumno {a['nombre_alumno']}.")
            else:
                a["estado"] = "Activo"
                print(f"\n Se ha restaurado el descuento del alumno {a['nombre_alumno']}.")
                
            guardar_json(RUTA_DESCUENTOS_ALUMNOS, asignaciones)
            return
            
    print("Error: No se encontró la asignación.")

def menu_asignar_descuentos():
    while True:
        imprimir_titulo("GESTIÓN DE ASIGNACIONES DE DESCUENTOS")
        print("1. Asignar nuevo descuento a alumno")
        print("2. Ver descuentos asignados a alumnos")
        print("3. Modificar un descuento asignado")
        print("4. Eliminar / Restaurar una asignación")
        print("5. Volver")
        
        opcion = input("\nSeleccione una opción: ").strip()
        
        if opcion == "1":
            asignar_descuento_alumno()
        elif opcion == "2":
            ver_descuentos_asignados()
        elif opcion == "3":
            modificar_descuento_asignado()
        elif opcion == "4":
            eliminar_descuento_asignado()
        elif opcion == "5":
            break
        else:
            print("Opción inválida.")