from basedatos_json import leer_json, guardar_json, generar_id
from director.utilidades import imprimir_titulo
from director.utilidades import imprimir_titulo, imprimir_menu, limpiar_pantalla, pausa

RUTA_PLANTILLAS = "datos/plantillas_academicas.json"
RUTA_SALONES = "datos/salones.json"
RUTA_ALUMNOS = "datos/alumnos.json"
RUTA_ASIGNACIONES = "datos/alumnos_asignaciones.json"
RUTA_CARGOS_OFICIALES = "datos/cargos_oficiales.json"
RUTA_DESCUENTOS = "datos/descuentos_convenios.json"
RUTA_DESCUENTOS_ALUMNOS = "datos/descuentos_alumnos.json"
RUTA_ASIGNACIONES = "datos/descuentos_alumnos.json"

def buscar_diccionario_por_id(lista, campo_id, valor_id):
    for item in lista:
        if item.get(campo_id) == valor_id:
            return item
    return None
def mostrar_asignaciones():
    imprimir_titulo("DESCUENTOS ASIGNADOS A ALUMNOS")
    
    asignaciones = leer_json(RUTA_ASIGNACIONES)
    alumnos = leer_json(RUTA_ALUMNOS)
    descuentos = leer_json(RUTA_DESCUENTOS)
    
    if not asignaciones:
        print("No hay descuentos asignados a ningún alumno actualmente.")
        return
    print(f"{'ID ASIG.':<8} | {'ALUMNO':<30} | {'DESCUENTO / CONVENIO':<25} | {'ESTADO':<10}")
    print("-" * 80)
    
    # PROCESO: Recorrido y cruce de datos
    for asig in asignaciones:
        # Buscamos los datos relacionados usando nuestros arreglos paralelos lógicos
        alumno = buscar_diccionario_por_id(alumnos, "id_alumno", asig.get("id_alumno"))
        descuento = buscar_diccionario_por_id(descuentos, "id_descuento", asig.get("id_descuento"))
        
        # Validaciones por si se borró algún dato maestro
        nombre_alumno = alumno.get("nombres", "Desconocido").title() if alumno else "No encontrado"
        nombre_descuento = descuento.get("nombre", "Desconocido").title() if descuento else "No encontrado"
        estado = str(asig.get("estado", "Inactivo")).upper()
        
        print(f"{asig.get('id_asignacion', 0):<8} | {nombre_alumno[:30]:<30} | {nombre_descuento[:25]:<25} | {estado:<10}")
def asignar_nuevo_descuento():
    imprimir_titulo("ASIGNAR NUEVO DESCUENTO A ALUMNO")
    
    asignaciones = leer_json(RUTA_ASIGNACIONES)
    alumnos = leer_json(RUTA_ALUMNOS)
    descuentos = leer_json(RUTA_DESCUENTOS)
    
    # 1. Buscar Alumno
    dni_buscar = input("Ingrese el DNI del alumno: ").strip()
    
    alumno_encontrado = None
    for alum in alumnos:
        if alum.get("dni") == dni_buscar:
            alumno_encontrado = alum
            break
    if not alumno_encontrado:
        print(f"\nNo se encontró ningún alumno con el DNI {dni_buscar}.")
        return  
    print(f"\nAlumno encontrado: {alumno_encontrado.get('nombres').title()} {alumno_encontrado.get('apellidos').title()}")
    
    # 2. Seleccionar Descuento
    print("\nDescuentos Activos Disponibles:")
    hay_descuentos = False
    for desc in descuentos:
        if desc.get("estado") == "Activo":
            hay_descuentos = True
            print(f"- ID: {desc.get('id_descuento')} | {desc.get('nombre').title()} ({desc.get('tipo')} de {desc.get('valor')})")
    if not hay_descuentos:
        print("No hay descuentos activos en el catálogo en este momento.")
        return
    try:
        id_desc = int(input("\nIngrese el ID del descuento a asignar: "))
    except ValueError:
        print("Error: Debe ingresar un número válido.")
        return
    # Verificar que el descuento exista
    descuento_seleccionado = buscar_diccionario_por_id(descuentos, "id_descuento", id_desc)
    if not descuento_seleccionado or descuento_seleccionado.get("estado") != "Activo":
        print("El ID de descuento no es válido o está inactivo.")
        return
    # Evitar duplicidad
    for asig in asignaciones:
        if asig.get("id_alumno") == alumno_encontrado["id_alumno"] and asig.get("id_descuento") == id_desc:
            print("\nEste alumno ya tiene asignado este descuento.")
            return
    # 3. Crear Asignación
    nueva_asignacion = {
        "id_asignacion": generar_id(asignaciones, "id_asignacion"),
        "id_alumno": alumno_encontrado["id_alumno"],
        "id_descuento": id_desc,
        "estado": "Activo"
    }
    
    asignaciones.append(nueva_asignacion)
    guardar_json(RUTA_ASIGNACIONES, asignaciones)
    print(f"\nDescuento asignado exitosamente al alumno.")
def modificar_estado_asignacion():
    imprimir_titulo("REVOCAR / REACTIVAR DESCUENTO DE ALUMNO")
    mostrar_asignaciones()
    
    try:
        id_buscar = int(input("\nIngrese el ID de la ASIGNACIÓN a modificar: "))
    except ValueError:
        print("Error: Debe ingresar un ID numérico válido.")
        return
    asignaciones = leer_json(RUTA_ASIGNACIONES)
    encontrado = False
    
    for asig in asignaciones:
        if asig.get("id_asignacion") == id_buscar:
            encontrado = True
            if asig.get("estado") == "Activo":
                asig["estado"] = "Inactivo"
                print("\nLa asignación ha sido REVOCADA (Inactiva).")
            else:
                asig["estado"] = "Activo"
                print("\nLa asignación ha sido REACTIVADA.")
            break
    if encontrado:
        guardar_json(RUTA_ASIGNACIONES, asignaciones)
    else:
        print("\nNo se encontró una asignación con ese ID.")
def menu_asignar_descuentos():
    while True:
        limpiar_pantalla()
        imprimir_titulo("GESTIÓN DE ASIGNACIÓN DE DESCUENTOS")
        imprimir_menu([
            "Ver descuentos asignados a alumnos",
            "Asignar nuevo descuento a un alumno",
            "Revocar / Reactivar asignación (Borrado lógico)",
            "Volver al submenú anterior"
        ])
        
        opc = input("\nSeleccione una opción: ").strip()
        
        if opc == "1":
            limpiar_pantalla()
            mostrar_asignaciones()
            pausa()
        elif opc == "2":
            limpiar_pantalla()
            asignar_nuevo_descuento()
            pausa()
        elif opc == "3":
            limpiar_pantalla()
            modificar_estado_asignacion()
            pausa()
        elif opc == "4":
            break
        else:
            print("\nOpción no válida.")
            pausa()