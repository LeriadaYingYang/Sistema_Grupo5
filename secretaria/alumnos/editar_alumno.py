from basedatos_json import leer_json, guardar_json
from secretaria.utilidades import imprimir_titulo

RUTA_ALUMNOS = "datos/alumnos.json"

def mostrar_alumno(alumno):  #Muestra los datos principales de un alumno
    print("\n-----------------------------")
    print(f"ID: {alumno['id_alumno']}")
    print(f"Nombres: {alumno['nombres']}")
    print(f"Apellidos: {alumno['apellidos']}")
    print(f"DNI: {alumno['dni']}")
    print(f"Correo: {alumno['correo']}")
    print(f"Celular: {alumno['celular']}")

def buscar_por_nombre(alumnos):  #Busca alumnos activos por nombre o apellido
    texto = input("Ingresar nombre/apellido aproximado: ").lower()
    encontrados = []
    for alumno in alumnos:
        nombre_completo = f"{alumno['nombres']} {alumno['apellidos']}".lower()
        if alumno["estado"] == "Activo" and texto in nombre_completo:
            encontrados.append(alumno)
    return encontrados

def buscar_por_dni(alumnos):  #Busca alumnos activos por DNI
    dni = input("Ingresar DNI: ")
    encontrados = []
    for alumno in alumnos:
        if alumno["estado"] == "Activo" and alumno["dni"] == dni:
            encontrados.append(alumno)
    return encontrados

def elegir_alumno(encontrados):  #Selecciona un alumno de la lista encontrada
    if len(encontrados) == 0:
        print("No se encontraron alumnos.")
        return None
    imprimir_titulo("=== ALUMNOS ENCONTRADOS ===")
    for alumno in encontrados:
        mostrar_alumno(alumno)

#Controlando errores al ingresar ID
    try:
        id_alumno = int(input("\nIngresar el ID del alumno que desea editar: "))
    except ValueError:
        print("Debe ingresar un número.")
        return None
    for alumno in encontrados:
        if alumno["id_alumno"] == id_alumno:
            return alumno
    print("ID no válido.")
    return None

def editar_campo(alumno):  #Permite editar uno o varios datos del alumno seleccionado
    while True:
        print(f"""
Alumno seleccionado:
{alumno['nombres']} {alumno['apellidos']}

¿Qué dato desea editar?
ID: {alumno['id_alumno']}
1. Nombres   : {alumno['nombres']}
2. Apellidos : {alumno['apellidos']}
3. DNI       : {alumno['dni']}
4. Correo    : {alumno['correo']}
5. Celular   : {alumno['celular']}
6. Salir""")
        opcion = input("Seleccionar una opción: ")
        if opcion == "1":
            alumno["nombres"] = input("Nuevo nombre: ")
        elif opcion == "2":
            alumno["apellidos"] = input("Nuevo apellido: ")
        elif opcion == "3":
            alumno["dni"] = input("Nuevo DNI: ")
        elif opcion == "4":
            alumno["correo"] = input("Nuevo correo: ")
        elif opcion == "5":
            alumno["celular"] = input("Nuevo celular: ")
        elif opcion == "6":
            break
        else:
            print("Opción inválida.")
            continue
        print("\nDato actualizado correctamente.")
        continuar = input("¿Cambiar otro dato? (si/no): ").lower()
        if continuar != "si":
            break

def editar_alumno():  #Permite buscar y editar datos de un alumno
    print("\n=== EDITAR DATOS DE ALUMNO ===")
    alumnos = leer_json(RUTA_ALUMNOS)  #Carga los alumnos registrados
    if len(alumnos) == 0:
        print("No hay alumnos registrados.")
        return
    print("""
Buscar alumno por:

1. Nombre o apellido
2. DNI
3. Volver""")
    opcion = input("Seleccionar una opción: ")
    if opcion == "1":
        encontrados = buscar_por_nombre(alumnos)
    elif opcion == "2":
        encontrados = buscar_por_dni(alumnos)
    elif opcion == "3":
        return
    else:
        print("Opción inválida.")
        return
    alumno = elegir_alumno(encontrados)  #Obtiene el alumno seleccionado
    if alumno is None:
        return
    editar_campo(alumno)  #Edita los datos del alumno
    guardar_json(RUTA_ALUMNOS, alumnos)  #Guarda los cambios en el archivo json
    print("\n === ALUMNO ACTUALIZADO CORRECTAMENTE ===")
