from basedatos_json import leer_json, guardar_json, generar_id
from director.utilidades import imprimir_titulo, imprimir_menu, limpiar_pantalla, pausa

RUTA_DESCUENTOS = "datos/descuentos_convenios.json"

def mostrar_descuentos():
    imprimir_titulo("CATÁLOGO DE DESCUENTOS Y CONVENIOS")
    
    # ENTRADA: Carga del arreglo de diccionarios
    descuentos = leer_json(RUTA_DESCUENTOS)
    
    if not descuentos:
        print("No hay descuentos registrados en el sistema.")
        return

    print(f"{'ID':<4} | {'NOMBRE DEL DESCUENTO':<30} | {'TIPO':<12} | {'VALOR':<8} | {'ESTADO':<8}")
    print("-" * 75)
    
    # PROCESO: Recorrido secuencial
    for d in descuentos:
        nombre = str(d.get("nombre", "Sin nombre")).title()
        tipo = str(d.get("tipo", "Fijo")).capitalize()
        valor = d.get("valor", 0.0)
        estado = str(d.get("estado", "Inactivo")).upper()
        
        # Formato condicional según el tipo de descuento
        str_valor = f"{valor}%" if tipo == "Porcentaje" else f"S/ {valor:.2f}"
        
        print(f"{d.get('id_descuento', 0):<4} | {nombre[:30]:<30} | {tipo:<12} | {str_valor:<8} | {estado:<8}")

def agregar_descuento():
    imprimir_titulo("AGREGAR NUEVO DESCUENTO O CONVENIO")
    
    descuentos = leer_json(RUTA_DESCUENTOS)
    
    # Normalización de entrada
    nombre = input("Nombre del descuento (ej. Beca Orfandad, Convenio PNP): ").strip().lower()
    
    if not nombre:
        print("El nombre no puede estar vacío.")
        return
        
    print("\nTipo de Descuento:")
    print("1. Porcentaje (ej. 15% de descuento)")
    print("2. Monto Fijo (ej. S/ 50.00 de descuento)")
    opc_tipo = input("Seleccione (1-2): ").strip()
    
    tipo_str = "Porcentaje" if opc_tipo == "1" else "Fijo" if opc_tipo == "2" else None
    
    if not tipo_str:
        print("Opción de tipo inválida.")
        return

    try:
        valor = float(input(f"Ingrese el valor del descuento ({'%' if tipo_str == 'Porcentaje' else 'S/'}): "))
        if valor <= 0:
            print("El valor debe ser mayor a 0.")
            return
        if tipo_str == "Porcentaje" and valor > 100:
            print("El porcentaje no puede superar el 100%.")
            return
    except ValueError:
        print("Error: Entrada numérica inválida.")
        return

    nuevo_descuento = {
        "id_descuento": generar_id(descuentos, "id_descuento"),
        "nombre": nombre,
        "tipo": tipo_str,
        "valor": round(valor, 2),
        "estado": "Activo"
    }
    
    # SALIDA: Pasamos por referencia y guardamos
    descuentos.append(nuevo_descuento)
    guardar_json(RUTA_DESCUENTOS, descuentos)
    print(f"\nDescuento '{nombre.title()}' agregado exitosamente.")

def modificar_estado_descuento():
    imprimir_titulo("DESACTIVAR / ACTIVAR DESCUENTO")
    mostrar_descuentos()
    
    try:
        id_buscar = int(input("\nIngrese el ID del descuento a modificar: "))
    except ValueError:
        print("Error: Debe ingresar un ID numérico.")
        return
    descuentos = leer_json(RUTA_DESCUENTOS)
    encontrado = False
    
    # Búsqueda textual exacta por ID
    for d in descuentos:
        if d.get("id_descuento") == id_buscar:
            encontrado = True
            if d.get("estado") == "Activo":
                d["estado"] = "Inactivo"
                print(f"\nDescuento '{d['nombre']}' ha sido DESACTIVADO.")
            else:
                d["estado"] = "Activo"
                print(f"\nDescuento '{d['nombre']}' ha sido ACTIVADO.")
            break
            
    if encontrado:
        guardar_json(RUTA_DESCUENTOS, descuentos)
    else:
        print("\nNo se encontró un descuento con ese ID.")

def menu_descuentos():
    while True:
        limpiar_pantalla()
        imprimir_titulo("GESTIÓN DE CATÁLOGO DE DESCUENTOS")
        imprimir_menu([
            "Ver descuentos registrados",
            "Agregar nuevo descuento",
            "Activar / Desactivar descuento",
            "Volver al submenú anterior"
        ])
        
        opc = input("\nSeleccione una opción: ").strip()
        
        if opc == "1":
            limpiar_pantalla()
            mostrar_descuentos()
            pausa()
        elif opc == "2":
            limpiar_pantalla()
            agregar_descuento()
            pausa()
        elif opc == "3":
            limpiar_pantalla()
            modificar_estado_descuento()
            pausa()
        elif opc == "4":
            break
        else:
            print("\nOpción no válida.")
            pausa()