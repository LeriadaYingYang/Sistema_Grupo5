from director.main import menu_director
from director.utilidades import limpiar_pantalla
from basedatos_json import leer_json

RUTA_LOGIN = "datos/login_director.json"


def login_director():
    limpiar_pantalla()

    print("=== BIENVENIDO A LA IISEM INGRESE SUS DATOS ===")
    print("=== LOGIN DIRECTOR ===")

    usuario = input("Usuario: ").strip()
    password = input("Contraseña: ").strip()

    usuarios = leer_json(RUTA_LOGIN)

    acceso = False

    for director in usuarios:
        if (
            director["usuario"] == usuario
            and director["password"] == password):
            acceso = True
            break

    if acceso:
        print("\nAcceso concedido.")
        input("Presione ENTER para continuar...")
        menu_director()
    else:
        print("\nUsuario o contraseña incorrectos.")
        input("Presione ENTER para continuar...")