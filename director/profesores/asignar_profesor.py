from basedatos_json import leer_json, guardar_json, generar_id
from director.utilidades import imprimir_titulo

RUTA_PROFESORES = "datos/profesores.json"
RUTA_SALONES = "datos/salones.json"
RUTA_PROFESORES_SALONES = "datos/profesores_salones.json"

def buscar_por_id(lista, campo_id, valor_id):  # busca un registro activo utilizando su identificador
    for item in lista:
        if item[campo_id] == valor_id and item["estado"] == "Activo":
            return item
    return None

def mostrar_profesores(profesores):  # muestra los profesores activos disponibles para asignar
    imprimir_titulo("PROFESORES DISPONIBLES")

    for profesor in profesores:
        if profesor["estado"] == "Activo":
            print(f"ID: {profesor['id_profesor']} | {profesor['nombres']} {profesor['apellidos']}")

def mostrar_salones(salones):  # muestra los salones activos donde se puede asignar un profesor
    imprimir_titulo("SALONES DISPONIBLES")
    for salon in salones:
        if salon["estado"] == "Activo":
            print(
                f"ID: {salon['id_salon']} | "
                f"Salón: {salon['nombre_salon']} | "
                f"Carrera: {salon['nombre_carrera']} | "
                f"Turno: {salon['turno']}"
            )

def ya_existe_asignacion(asignaciones, id_profesor, id_salon):  # verifica si el profesor ya está asignado al salón
    for asignacion in asignaciones:
        if (
            asignacion["id_profesor"] == id_profesor
            and asignacion["id_salon"] == id_salon
            and asignacion["estado"] == "Activo"):
            return True
    return False


def asignar_profesor():  # asigna un profesor registrado a un salón disponible
    imprimir_titulo("ASIGNAR PROFESOR A SALÓN")
    profesores = leer_json(RUTA_PROFESORES)  #carga los profesores registrados
    salones = leer_json(RUTA_SALONES)  #carga los salones registrados
    asignaciones = leer_json(RUTA_PROFESORES_SALONES)  #carga asignaciones existentes
    if len(profesores) == 0:
        print("Primero debe registrar profesores.")
        return
    if len(salones) == 0:
        print("Primero debe registrar salones.")
        return
    mostrar_profesores(profesores)
    try:
        id_profesor = int(input("\nIngrese ID del profesor: "))
    except ValueError:
        print("Debe ingresar un número.")
        return
    profesor = buscar_por_id(profesores, "id_profesor", id_profesor)
    if profesor is None:
        print("Profesor no encontrado.")
        return
    mostrar_salones(salones)
    try:
        id_salon = int(input("\nIngrese ID del salón: "))
    except ValueError:
        print("Debe ingresar un número.")
        return
    salon = buscar_por_id(salones, "id_salon", id_salon)
    if salon is None:
        print("Salón no encontrado.")
        return
    if ya_existe_asignacion(asignaciones, id_profesor, id_salon):
        print("Este profesor ya está asignado a este salón.")
        return
    nueva_asignacion = {
        "id_profesor_salon": generar_id(asignaciones, "id_profesor_salon"),
        "id_profesor": profesor["id_profesor"],
        "nombre_profesor": profesor["nombres"] + " " + profesor["apellidos"],
        "id_salon": salon["id_salon"],
        "nombre_salon": salon["nombre_salon"],
        "turno": salon["turno"],
        "id_carrera": salon["id_carrera"],
        "nombre_carrera": salon["nombre_carrera"],
        "estado": "Activo"}
    asignaciones.append(nueva_asignacion)  #agrega la nueva asignación del profesor al salón
    guardar_json(RUTA_PROFESORES_SALONES, asignaciones)  #guarda la asignación en el archivo json
    print("\nProfesor asignado correctamente.")
    print(f"Profesor: {nueva_asignacion['nombre_profesor']}")
    print(f"Carrera: {nueva_asignacion['nombre_carrera']}")
    print(f"Salón: {nueva_asignacion['nombre_salon']}")
    print(f"Turno: {nueva_asignacion['turno']}")