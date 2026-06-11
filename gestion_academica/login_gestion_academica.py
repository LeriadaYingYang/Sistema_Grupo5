from gestion_academica.main import menu_gestion_academica
from gestion_academica.utilidades import limpiar_pantalla


def login_gestion_academica():
    print("=== BIENVENIDO A LA IISEM INGRESE SUS DATOS ===")
    print("=== LOGIN DIRECTOR ===")
    usuario = input("Usuario: ")
    password = input("Contraseña: ")

    print("\nValidando acceso del director")
    menu_gestion_academica()