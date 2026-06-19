import re
from basedatos_json import leer_json, guardar_json
from director.utilidades import imprimir_titulo

RUTA_PROFESORES = "datos/profesores.json"

# ==========================================
# FUNCIONES REUTILIZABLES DE VALIDACIÓN
# ==========================================

def solicitar_opcion_menu(mensaje, opciones_validas):
    """Obliga al usuario a elegir una opción válida de un menú."""
    while True:
        valor = input(mensaje).strip()
        if valor in opciones_validas:
            return valor
        print(f"❌ Error: Opción inválida. Elija una de las siguientes opciones: {', '.join(opciones_validas)}")

def solicitar_texto_no_vacio(mensaje):
    """Solicita un texto asegurando que no esté vacío."""
    while True:
        dato = input(mensaje).strip()
        if dato:
            return dato
        print("❌ Error: Este campo no puede estar vacío ni contener solo espacios.")

def solicitar_nombre_apellido(mensaje):
    """Solicita nombres o apellidos (solo letras y espacios), con formato Title Case."""
    while True:
        dato = input(mensaje).strip()
        if not dato:
            print("❌ Error: El campo no puede estar vacío.")
            continue
        if len(dato) > 60:
            print("❌ Error: El texto es demasiado largo (máximo 60 caracteres).")
            continue
        if re.fullmatch(r"[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+", dato):
            return dato.title()
        print("❌ Error: Solo se permiten letras y espacios. Sin números ni caracteres especiales.")

def solicitar_dni_edicion(profesores, id_actual, mensaje):
    """Solicita un DNI válido de 8 dígitos y verifica que no pertenezca a otro profesor."""
    while True:
        dato = input(mensaje).strip()
        if not re.fullmatch(r"\d{8}", dato):
            print("❌ Error: El DNI debe contener exactamente 8 dígitos numéricos.")
            continue
        if dni_duplicado(profesores, dato, id_actual):
            print("❌ Error: Ese DNI ya está registrado a nombre de otro profesor.")
            continue
        return dato

def solicitar_correo(mensaje):
    """Solicita un correo electrónico con formato válido."""
    while True:
        dato = input(mensaje).strip()
        patron = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if re.fullmatch(patron, dato):
            return dato.lower()
        print("❌ Error: Formato de correo inválido (ejemplo: usuario@dominio.com). No incluya espacios.")

def solicitar_celular(mensaje):
    """Solicita un número telefónico de exactamente 9 dígitos."""
    while True:
        dato = input(mensaje).strip()
        if re.fullmatch(r"\d{9}", dato):
            return dato
        print("❌ Error: El celular debe contener exactamente 9 dígitos numéricos.")

def solicitar_id(mensaje):
    """Solicita un ID numérico numérico asegurando que no existan errores de tipo."""
    while True:
        valor = input(mensaje).strip()
        if not valor:
            print("❌ Error: El ID no puede estar vacío.")
            continue
        try:
            return int(valor)
        except ValueError:
            print("❌ Error: Debe ingresar exclusivamente un número entero válido.")

# ==========================================
# LÓGICA PRINCIPAL DEL SISTEMA
# ==========================================

def mostrar_profesor(profesor):
    """Muestra la información de un profesor."""
    print("\n-----------------------------")
    print(f"ID: {profesor['id_profesor']}")
    print(f"Nombres: {profesor['nombres']}")
    print(f"Apellidos: {profesor['apellidos']}")
    print(f"DNI: {profesor['dni']}")
    print(f"Correo: {profesor['correo']}")
    print(f"Celular: {profesor['celular']}")

def buscar_por_nombre(profesores):
    """Busca profesores activos por nombre o apellido validando entrada vacía."""
    texto = solicitar_texto_no_vacio("Ingrese nombre o apellido aproximado: ").lower()

    return [
        profesor for profesor in profesores
        if (
            profesor.get("estado") == "Activo"
            and texto in f"{profesor['nombres']} {profesor['apellidos']}".lower()
        )
    ]

def buscar_por_dni(profesores):
    """Busca profesores activos obligando a que el criterio sea un DNI de 8 dígitos."""
    while True:
        dni = input("Ingrese DNI a buscar (8 dígitos): ").strip()
        if re.fullmatch(r"\d{8}", dni):
            break
        print("❌ Error: Ingrese un DNI válido de 8 números.")

    return [
        profesor for profesor in profesores
        if (
            profesor.get("estado") == "Activo"
            and profesor.get("dni") == dni
        )
    ]

def elegir_profesor(encontrados):
    """Permite seleccionar un profesor forzando un ID válido."""
    if not encontrados:
        print("❌ No se encontraron profesores con ese criterio.")
        return None

    imprimir_titulo("PROFESORES ENCONTRADOS")
    for profesor in encontrados:
        mostrar_profesor(profesor)

    # Ciclo para forzar selección de un ID que realmente esté en los resultados
    while True:
        id_profesor = solicitar_id("\nIngrese ID del profesor que desea editar (0 para cancelar): ")
        if id_profesor == 0:
            return None
            
        for profesor in encontrados:
            if profesor["id_profesor"] == id_profesor:
                return profesor
                
        print("❌ Error: El ID no corresponde a ninguno de los profesores encontrados.")

def dni_duplicado(profesores, dni, id_actual):
    """Verifica si el DNI pertenece a otro profesor."""
    return any(
        profesor.get("dni") == dni
        and profesor.get("id_profesor") != id_actual
        for profesor in profesores
    )

def editar_campos(profesor, profesores):
    """Menú validado para editar los datos del profesor seleccionado."""
    while True:
        print(f"""
Profesor seleccionado:
{profesor['nombres']} {profesor['apellidos']}

¿Qué dato desea editar?

1. Nombres:      {profesor['nombres']}
2. Apellidos:    {profesor['apellidos']}
3. DNI:          {profesor['dni']}
4. Correo:       {profesor['correo']}
5. Celular:      {profesor['celular']}
6. Finalizar edición
""")

        opcion = solicitar_opcion_menu("Seleccione una opción (1-6): ", ["1", "2", "3", "4", "5", "6"])

        if opcion == "1":
            profesor["nombres"] = solicitar_nombre_apellido("Nuevo nombre: ")
            print("\n✅ Nombre actualizado.")

        elif opcion == "2":
            profesor["apellidos"] = solicitar_nombre_apellido("Nuevo apellido: ")
            print("\n✅ Apellido actualizado.")

        elif opcion == "3":
            profesor["dni"] = solicitar_dni_edicion(profesores, profesor["id_profesor"], "Nuevo DNI: ")
            print("\n✅ DNI actualizado.")

        elif opcion == "4":
            profesor["correo"] = solicitar_correo("Nuevo correo: ")
            print("\n✅ Correo actualizado.")

        elif opcion == "5":
            profesor["celular"] = solicitar_celular("Nuevo celular: ")
            print("\n✅ Celular actualizado.")

        elif opcion == "6":
            break

        continuar = solicitar_opcion_menu("\n¿Desea cambiar otro dato? (si/no): ", ["si", "no"])
        if continuar == "no":
            break

def editar_profesor():
    """Flujo principal para buscar y editar un profesor."""
    imprimir_titulo("EDITAR DATOS DE PROFESOR")

    profesores = leer_json(RUTA_PROFESORES)

    if not any(profesor.get("estado") == "Activo" for profesor in profesores):
        print("❌ No hay profesores activos registrados.")
        return

    print("""
Buscar profesor por:

1. Nombre o apellido
2. DNI
3. Volver
""")

    opcion = solicitar_opcion_menu("Seleccione una opción (1-3): ", ["1", "2", "3"])

    if opcion == "1":
        encontrados = buscar_por_nombre(profesores)
    elif opcion == "2":
        encontrados = buscar_por_dni(profesores)
    else:
        return

    profesor = elegir_profesor(encontrados)

    if profesor is None:
        return

    editar_campos(profesor, profesores)
    guardar_json(RUTA_PROFESORES, profesores)

    print("\n✅ Profesor actualizado en el sistema correctamente.")