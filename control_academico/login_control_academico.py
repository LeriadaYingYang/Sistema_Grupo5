from control_academico.main import menu_control_academico

#===========================================
# Archivo: login_control_academico.py
# Participante: Fabrizio Ortega (control académico)
#===========================================

def login_control_academico():
    print("\n=== BIENVENIDO A LA IISEM INGRESE SUS DATOS ===")
    print("=== LOGIN CONTROL ACADÉMICO ===")
    usuario = input("Usuario: ")
    password = input("Contraseña: ")

    print("\nValidando acceso de control académico...")
    menu_control_academico()