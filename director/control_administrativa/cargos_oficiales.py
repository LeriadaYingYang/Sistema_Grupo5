from basedatos_json import leer_json, guardar_json, generar_id
from director.utilidades import imprimir_titulo
from basedatos_json import leer_json, guardar_json, generar_id
from director.utilidades import imprimir_titulo, imprimir_menu, limpiar_pantalla, pausa

RUTA_CARGOS = "datos/cargos_oficiales.json"
RUTA_CARRERAS = "datos/carreras.json"
RUTA_PLANTILLAS = "datos/plantillas_academicas.json"
RUTA_CARGOS_OFICIALES = "datos/cargos_oficiales.json"

def obtener_nombre_por_id(lista, campo_id, valor_id, campo_nombre):
    for item in lista:
        if item.get(campo_id) == valor_id:
            return item.get(campo_nombre)
    return "No asignado / General"

def mostrar_cargos_oficiales():
    imprimir_titulo("LISTADO DE CARGOS OFICIALES")
    
    # ENTRADA: Carga de listas desde JSON
    cargos = leer_json(RUTA_CARGOS)
    carreras = leer_json(RUTA_CARRERAS)
    plantillas = leer_json(RUTA_PLANTILLAS)
    
    if not cargos:
        print("No hay cargos oficiales registrados en el sistema.")
        return
    print(f"{'ID':<5} | {'NOMBRE DEL CARGO':<25} | {'MONTO':<10} | {'CARRERA ASOCIADA':<20} | {'ESTADO':<10}")
    print("-" * 80)
    
    # PROCESO: Recorrido y combinación
    for c in cargos:
        # Cruzamos datos usando la función con retorno
        nombre_carrera = obtener_nombre_por_id(carreras, "id_carrera", c.get("id_carrera"), "nombre")
        
        # Manipulación de cadenas para formatear la salida
        nombre_cargo = str(c.get("nombre_cargo", "Sin nombre")).capitalize()
        estado = str(c.get("estado", "Inactivo")).upper()
        
        print(f"{c['id_cargo_oficial']:<5} | {nombre_cargo:<25} | S/ {c['monto']:<7.2f} | {nombre_carrera[:18]:<20} | {estado:<10}")

def agregar_cargo_oficial():
    imprimir_titulo("AGREGAR NUEVO CARGO OFICIAL")
    
    cargos = leer_json(RUTA_CARGOS)
    nombre_cargo = input("Nombre del concepto (ej. Matrícula, Pensión): ").strip().lower()
    
    if not nombre_cargo:
        print("El nombre no puede estar vacío.")
        return

    try:
        monto = float(input("Monto establecido (S/): "))
        if monto < 0:
            print("El monto no puede ser negativo.")
            return
        id_carrera = int(input("ID de la Carrera a la que aplica (0 para todas): "))
        id_plantilla = int(input("ID de la Plantilla Académica (0 si no aplica): "))
    except ValueError:
        print("Error: Debe ingresar valores numéricos válidos.")
        return
    nuevo_cargo = {
        "id_cargo_oficial": generar_id(cargos, "id_cargo_oficial"),
        "nombre_cargo": nombre_cargo,
        "monto": round(monto, 2),
        "id_carrera": id_carrera if id_carrera > 0 else None,
        "id_plantilla": id_plantilla if id_plantilla > 0 else None,
        "estado": "Activo"
    }
    
    # PROCESO Y SALIDA: Modificar la lista por referencia y guardar
    cargos.append(nuevo_cargo)
    guardar_json(RUTA_CARGOS, cargos)
    print(f"\nCargo '{nombre_cargo.upper()}' registrado exitosamente.")

def modificar_estado_cargo():
    imprimir_titulo("ACTIVAR / DESACTIVAR CARGO OFICIAL")
    mostrar_cargos_oficiales()
    
    try:
        id_buscar = int(input("\nIngrese el ID del cargo a modificar: "))
    except ValueError:
        print("ID inválido. Debe ser numérico.")
        return
    cargos = leer_json(RUTA_CARGOS)
    encontrado = False
    
    # Búsqueda secuencial
    for c in cargos:
        if c["id_cargo_oficial"] == id_buscar:
            encontrado = True
            # Inversión de estado lógico
            if c["estado"] == "Activo":
                c["estado"] = "Inactivo"
                print(f"\nCargo '{c['nombre_cargo']}' ha sido DESACTIVADO.")
            else:
                c["estado"] = "Activo"
                print(f"\nCargo '{c['nombre_cargo']}' ha sido ACTIVADO.")
            break   
    if encontrado:
        guardar_json(RUTA_CARGOS, cargos)
    else:
        print("\nNo se encontró ningún cargo con ese ID.")

def menu_cargos_oficiales():
    while True:
        limpiar_pantalla()
        imprimir_titulo("GESTIÓN DE CARGOS OFICIALES")
        imprimir_menu([
            "Ver cargos registrados",
            "Registrar nuevo cargo (Inserción)",
            "Activar / Desactivar cargo (Borrado lógico)",
            "Volver al submenú anterior"
        ])
        
        opc = input("\nSeleccione una opción: ").strip()
        
        if opc == "1":
            limpiar_pantalla()
            mostrar_cargos_oficiales()
            pausa()
        elif opc == "2":
            limpiar_pantalla()
            agregar_cargo_oficial()
            pausa()
        elif opc == "3":
            limpiar_pantalla()
            modificar_estado_cargo()
            pausa()
        elif opc == "4":
            break
        else:
            print("\nOpción no válida.")
            pausa()