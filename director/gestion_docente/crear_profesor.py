from basedatos_json import leer_json, guardar_json, generar_id
from director.utilidades import imprimir_titulo

RUTA_PROFESORES = "datos/profesores.json"

def crear_profesor():  #registra un nuevo profesor y guarda sus datos personales en el sistema
    imprimir_titulo("REGISTRAR PROFESOR")
    profesores = leer_json(RUTA_PROFESORES)  #carga la lista actual de profesores registrados
    nombres = input("Nombres: ")
    apellidos = input("Apellidos: ")
    dni = input("DNI: ")
    correo = input("Correo: ")
    celular = input("Celular: ")
    nuevo_profesor = {
        "id_profesor": generar_id(profesores, "id_profesor"),
        "nombres": nombres,
        "apellidos": apellidos,
        "dni": dni,
        "correo": correo,
        "celular": celular,
        "estado": "Activo"}

    profesores.append(nuevo_profesor)  # agrega el nuevo profesor a la lista de registros
    guardar_json(RUTA_PROFESORES, profesores)  # guarda el nuevo registro en el archivo json
    print("\nProfesor registrado correctamente.")
    print(f"ID profesor generado: {nuevo_profesor['id_profesor']}")