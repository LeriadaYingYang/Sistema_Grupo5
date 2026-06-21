from basedatos_json import leer_json, guardar_json, generar_id
from director.utilidades import imprimir_titulo

RUTA_DESCUENTOS = "datos/descuentos_convenios.json"

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
    nombre = pedir_texto("Nombre del descuento/convenio: ")
    tipo = pedir_tipo_descuento()
    try:
        valor = pedir_valor_descuento(tipo)
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

def pedir_texto(mensaje):
    while True:
        texto = input(mensaje).strip()
        if texto:
            return texto
        print("El campo no puede estar vacío.")


def pedir_valor_descuento(tipo):
    while True:
        try:
            valor = float(input("Valor del descuento: "))
            if valor < 0:
                print("El valor no puede ser negativo.")
            elif tipo == "Porcentaje" and valor > 100:
                print("El porcentaje no puede ser mayor a 100.")
            else:
                return round(valor, 2)
        except ValueError:
            print("Debe ingresar un valor numérico.")
