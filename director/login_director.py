from director.main import menu_director
from director.utilidades import limpiar_pantalla


def login_director():
    print("=== BIENVENIDO A LA IISEM INGRESE SUS DATOS ===")
    print("=== LOGIN DIRECTOR ===")
    usuario = input("Usuario: ")
    password = input("Contraseña: ")

    print("\nValidando acceso del director")
    menu_director()