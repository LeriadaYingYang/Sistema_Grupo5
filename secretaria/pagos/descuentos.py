from basedatos_json import leer_json, guardar_json, generar_id
from secretaria.utilidades import imprimir_titulo

RUTA_DESCUENTOS = "datos/descuentos_convenios.json"

def pedir_tipo_descuento():  #Permite seleccionar si el descuento será por porcentaje o monto fijo
    while True:
        print("""
=== TIPO DE DESCUENTO ===
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

def crear_descuento_convenio():  #Registra un descuento o convenio para aplicar posteriormente a cargos oficiales
    imprimir_titulo("=== CREAR DESCUENTO O CONVENIO ===")
    descuentos = leer_json(RUTA_DESCUENTOS)
    nombre = input("Nombre del descuento/convenio: ")
    tipo = pedir_tipo_descuento()

#Controlando errores al ingresar valor del descuento
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
    descuentos.append(nuevo_descuento)  # Agrega el descuento a la lista de descuentos registrados
    guardar_json(RUTA_DESCUENTOS, descuentos)  # Guarda permanentemente el descuento en el archivo json
    print("\n=== DESCUENTO/CONVENIO CREADO CORRECTAMENTE ===")
    print("Este descuento solo aplica a cargos oficiales.")