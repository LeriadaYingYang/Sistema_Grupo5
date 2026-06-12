from basedatos_json import leer_json
from director.utilidades import imprimir_titulo, imprimir_menu
from profesor.main import menu_profesor

RUTA_PROFESORES = "datos/profesores.json"


def login_profesor():  #autentica al profesor con su DNI y contraseña
    imprimir_titulo("LOGIN PROFESOR")

    profesores = leer_json(RUTA_PROFESORES)

    dni = input("Ingrese su DNI: ").strip()
    password = input("Ingrese su contraseña: ").strip()

    profesor_encontrado = None
    for profesor in profesores:
        if profesor["dni"] == dni and profesor["estado"] == "Activo":
            profesor_encontrado = profesor
            break

    if profesor_encontrado is None:
        print("\nAcceso denegado. DNI no encontrado o cuenta inactiva.")
        return

    # Contraseña simple: DNI como contraseña por defecto
    if password != profesor_encontrado["dni"]:
        print("\nContraseña incorrecta.")
        return

    print(f"\nBienvenido/a, Prof. {profesor_encontrado['nombres']} {profesor_encontrado['apellidos']}")
    menu_profesor(profesor_encontrado)