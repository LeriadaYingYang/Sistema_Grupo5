from basedatos_json import leer_json, guardar_json, generar_id
from director.utilidades import imprimir_titulo
RUTA_DESCUENTOS = "datos/descuentos_convenios.json"
RUTA_DESCUENTOS = "datos/descuentos_convenios.json"

def eliminar_descuento_logico():
    imprimir_titulo("5.2.5. ELIMINAR / DESACTIVAR DESCUENTO")
    descuentos = leer_json(RUTA_DESCUENTOS)
    
    if len(descuentos) == 0:
        print("No hay descuentos registrados en el sistema.")
        return

    print("\nDescuentos y Convenios registrados:")
    for d in descuentos:
        print(f"ID: {d['id_descuento']} | {d['nombre']} ({d['tipo']} - {d['valor']}) | Estado: {d['estado']}")
        
    try:
        id_buscar = int(input("\nIngrese el ID del descuento que desea dar de baja: "))
        encontrado = None
        for d in descuentos:
            if d["id_descuento"] == id_buscar:
                encontrado = d
                break
                
        if encontrado:
            if encontrado["estado"] == "Activo":
                encontrado["estado"] = "Inactivo"
                print(f"\n El descuento '{encontrado['nombre']}' ha sido marcado como Inactivo.")
            else:
                print("\nEl descuento seleccionado ya se encontraba inactivo.")
            
            guardar_json(RUTA_DESCUENTOS, descuentos)
        else:
            print("\n ID de descuento no encontrado.")
    except ValueError:
        print("\n Error: Ingrese un identificador numérico válido.")
        
def pedir_tipo_descuento():  #permite seleccionar si el descuento será por porcentaje o monto fijo
    while True:
        print("""
--- TIPO DE DESCUENTO ---
1. Porcentaje
2. Monto fijo
""")
        opcion = input("Seleccione tipo: ")
        if opcion == "1":
            return "Porcentaje"
        elif opcion == "2":
            return "Monto fijo"
        else:
            print("Opción inválida.")

def crear_descuento_convenio():  #registra un descuento o convenio para aplicar posteriormente a cargos oficiales
    imprimir_titulo("CREAR DESCUENTO O CONVENIO")

    descuentos = leer_json(RUTA_DESCUENTOS)
    nombre = input("Nombre del descuento/convenio: ")
    tipo = pedir_tipo_descuento()
    try:
        valor = float(input("Valor del descuento: "))
    except ValueError:
        print("Debe ingresar un valor válido.")
        return
    motivo = input("Motivo o descripción: ")
    nuevo_descuento = {
        "id_descuento": generar_id(descuentos, "id_descuento"),
        "nombre": nombre,
        "tipo": tipo,
        "valor": valor,
        "motivo": motivo,
        "aplica_a": "Cargo oficial",
        "estado": "Activo"}
    descuentos.append(nuevo_descuento)  #agrega el descuento a la lista de descuentos registrados
    guardar_json(RUTA_DESCUENTOS, descuentos)  #guarda permanentemente el descuento en el archivo json

    print("\nDescuento/convenio creado correctamente.")
    print("Este descuento solo aplica a cargos oficiales.")