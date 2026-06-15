from basedatos_json import leer_json, guardar_json, generar_id
from director.utilidades import imprimir_titulo
from basedatos_json import leer_json, guardar_json, generar_id
from director.utilidades import imprimir_titulo, imprimir_menu, limpiar_pantalla, pausa

RUTA_PLANTILLAS = "datos/plantillas_academicas.json"
RUTA_SALONES = "datos/salones.json"
RUTA_ALUMNOS = "datos/alumnos.json"
RUTA_ASIGNACIONES = "datos/alumnos_asignaciones.json"
RUTA_CARGOS_EXTRAS = "datos/cargos_extras.json"
RUTA_CARRERAS = "datos/carreras.json"
 

def buscar_nombre_relacionado(lista, campo_id, valor_id, campo_nombre):
    if not valor_id:
        return "N/A"
    for item in lista:
        if item.get(campo_id) == valor_id:
            return str(item.get(campo_nombre, "Desconocido")).title()
    return "No encontrado"
def mostrar_cargos_extras():
    imprimir_titulo("LISTADO DE CARGOS EXTRAS (MULTAS, CONSTANCIAS)")
    # ENTRADA: Carga de múltiples arreglos para combinación
    cargos = leer_json(RUTA_CARGOS_EXTRAS)
    alumnos = leer_json(RUTA_ALUMNOS)
    salones = leer_json(RUTA_SALONES)
    carreras = leer_json(RUTA_CARRERAS)
    
    if not cargos:
        print("No hay cargos extras registrados.")
        return
    print(f"{'ID':<4} | {'CARGO':<20} | {'MONTO':<8} | {'DESTINATARIO (ALUMNO/SALÓN/CARRERA)':<35} | {'ESTADO':<8}")
    print("-" * 85)
    
    # PROCESO: Recorrido y combinación lógica
    for c in cargos:
        nombre_cargo = str(c.get("nombre", "Sin nombre")).capitalize()
        monto = c.get("monto", 0.0)
        estado = str(c.get("estado", "Inactivo")).upper()
        
        # Estructura combinada: determinamos jerárquicamente a quién aplica
        destinatario = "General (Todos)"
        if c.get("id_alumno"):
            destinatario = "Alu: " + buscar_nombre_relacionado(alumnos, "id_alumno", c["id_alumno"], "nombres")
        elif c.get("id_salon"):
            destinatario = "Salón: " + buscar_nombre_relacionado(salones, "id_salon", c["id_salon"], "nombre")
        elif c.get("id_carrera"):
            destinatario = "Carrera: " + buscar_nombre_relacionado(carreras, "id_carrera", c["id_carrera"], "nombre")
        print(f"{c.get('id_cargo_extra', 0):<4} | {nombre_cargo[:20]:<20} | S/ {monto:<5.2f} | {destinatario[:35]:<35} | {estado:<8}")
def agregar_cargo_extra():
    imprimir_titulo("AGREGAR NUEVO CARGO EXTRA")
    cargos = leer_json(RUTA_CARGOS_EXTRAS)
    nombre = input("Nombre del cargo extra (ej. Multa biblioteca, Certificado): ").strip().lower()
    if not nombre:
        print("El nombre no puede estar vacío.")
        return
    try:
        monto = float(input("Monto (S/): "))
        if monto < 0:
            print("El monto no puede ser negativo.")
            return
        print("\n¿A quién aplica este cargo?")
        print("1. A un Alumno específico")
        print("2. A un Salón completo")
        print("3. A una Carrera completa")
        print("4. General (Aplica a todos)")
        opcion_aplica = input("Seleccione (1-4): ").strip()
        
        id_alumno = id_salon = id_carrera = None
        
        if opcion_aplica == "1":
            id_alumno = int(input("Ingrese ID del Alumno: "))
        elif opcion_aplica == "2":
            id_salon = int(input("Ingrese ID del Salón: "))
        elif opcion_aplica == "3":
            id_carrera = int(input("Ingrese ID de la Carrera: "))
    except ValueError:
        print("Error: Entrada numérica inválida.")
        return

    nuevo_cargo = {
        "id_cargo_extra": generar_id(cargos, "id_cargo_extra"),
        "nombre": nombre,
        "monto": round(monto, 2),
        "id_alumno": id_alumno,
        "id_salon": id_salon,
        "id_carrera": id_carrera,
        "estado": "Activo"
    }
    
    # SALIDA: Pasamos por referencia y guardamos
    cargos.append(nuevo_cargo)
    guardar_json(RUTA_CARGOS_EXTRAS, cargos)
    print(f"\nCargo extra '{nombre.capitalize()}' agregado exitosamente.")

def modificar_estado_cargo_extra():
    imprimir_titulo("DESACTIVAR / ACTIVAR CARGO EXTRA")
    mostrar_cargos_extras()
    
    try:
        id_buscar = int(input("\nIngrese el ID del cargo extra a modificar: "))
    except ValueError:
        print("Error: Debe ingresar un ID numérico.")
        return
    cargos = leer_json(RUTA_CARGOS_EXTRAS)
    encontrado = False
    
    # Recorrido y modificación
    for c in cargos:
        if c.get("id_cargo_extra") == id_buscar:
            encontrado = True
            if c.get("estado") == "Activo":
                c["estado"] = "Inactivo"
                print(f"\nCargo '{c['nombre']}' ha sido DESACTIVADO.")
            else:
                c["estado"] = "Activo"
                print(f"\nCargo '{c['nombre']}' ha sido ACTIVADO.")
            break
    if encontrado:
        guardar_json(RUTA_CARGOS_EXTRAS, cargos)
    else:
        print("\nNo se encontró un cargo extra con ese ID.")
def menu_cargos_extras():
    while True:
        limpiar_pantalla()
        imprimir_titulo("GESTIÓN DE CARGOS EXTRAS")
        imprimir_menu([
            "Ver cargos extras registrados (Estructuras Combinadas)",
            "Registrar nuevo cargo extra (Inserción)",
            "Activar / Desactivar cargo extra (Borrado lógico)",
            "Volver al submenú anterior"
        ])
        
        opc = input("\nSeleccione una opción: ").strip()
        
        if opc == "1":
            limpiar_pantalla()
            mostrar_cargos_extras()
            pausa()
        elif opc == "2":
            limpiar_pantalla()
            agregar_cargo_extra()
            pausa()
        elif opc == "3":
            limpiar_pantalla()
            modificar_estado_cargo_extra()
            pausa()
        elif opc == "4":
            break
        else:
            print("\nOpción no válida.")
            pausa()