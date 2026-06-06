from basedatos_json import leer_json, guardar_json
from director.utilidades import imprimir_titulo

RUTA_PROFESORES = "datos/profesores.json"

def mostrar_profesor(profesor):  #muestra los datos principales del profesor encontrado
    print("\n-----------------------------")
    print(f"ID: {profesor['id_profesor']}")
    print(f"Nombres: {profesor['nombres']}")
    print(f"Apellidos: {profesor['apellidos']}")
    print(f"DNI: {profesor['dni']}")
    print(f"Correo: {profesor['correo']}")
    print(f"Celular: {profesor['celular']}")

def buscar_por_nombre(profesores):  #busca profesores activos por nombre o apellido aproximado
    texto = input("Ingrese nombre o apellido aproximado: ").lower()
    encontrados = []
    for profesor in profesores:
        nombre_completo = f"{profesor['nombres']} {profesor['apellidos']}".lower()

        if profesor["estado"] == "Activo" and texto in nombre_completo:
            encontrados.append(profesor)
    return encontrados

def buscar_por_dni(profesores):  #busca profesores activos usando el dni exacto
    dni = input("Ingrese DNI: ")
    encontrados = []
    for profesor in profesores:
        if profesor["estado"] == "Activo" and profesor["dni"] == dni:
            encontrados.append(profesor)
    return encontrados

def elegir_profesor(encontrados):  #permite elegir qué profesor se editará de la lista encontrada
    if len(encontrados) == 0:
        print("No se encontraron profesores.")
        return None
    imprimir_titulo("PROFESORES ENCONTRADOS")
    for profesor in encontrados:
        mostrar_profesor(profesor)
    try:
        id_profesor = int(input("\nIngrese ID del profesor que desea editar: "))
    except ValueError:
        print("Debe ingresar un número.")
        return None
    for profesor in encontrados:
        if profesor["id_profesor"] == id_profesor:
            return profesor
    print("ID no válido.")
    return None

def editar_campos(profesor):  #permite modificar uno o varios datos personales del profesor
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
6. Salir
""")

        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            profesor["nombres"] = input("Nuevo nombre: ")
        elif opcion == "2":
            profesor["apellidos"] = input("Nuevo apellido: ")
        elif opcion == "3":
            profesor["dni"] = input("Nuevo DNI: ")
        elif opcion == "4":
            profesor["correo"] = input("Nuevo correo: ")
        elif opcion == "5":
            profesor["celular"] = input("Nuevo celular: ")
        elif opcion == "6":
            break
        else:
            print("Opción inválida.")
            continue

        print("\nDato actualizado correctamente.")
        continuar = input("¿Desea cambiar otro dato? (si/no): ").lower()
        if continuar != "si":
            break


def editar_profesor():  #busca un profesor y guarda los cambios realizados en sus datos
    imprimir_titulo("EDITAR DATOS DE PROFESOR")
    profesores = leer_json(RUTA_PROFESORES)  # carga la lista de profesores registrados
    if len(profesores) == 0:
        print("No hay profesores registrados.")
        return

    print("""
Buscar profesor por:

1. Nombre o apellido
2. DNI
3. Volver
""")

    opcion = input("Seleccione una opción: ")
    if opcion == "1":
        encontrados = buscar_por_nombre(profesores)
    elif opcion == "2":
        encontrados = buscar_por_dni(profesores)
    elif opcion == "3":
        return
    else:
        print("Opción inválida.")
        return
    profesor = elegir_profesor(encontrados)
    if profesor is None:
        return
    editar_campos(profesor)
    guardar_json(RUTA_PROFESORES, profesores)  # guarda los cambios en el archivo json
    print("\nProfesor actualizado correctamente.")