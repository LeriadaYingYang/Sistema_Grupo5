from secretaria.main import menu_secretaria

#===========================================
# Archivo: login_secretaria.py
# Participante: Fabrizio Ortega (secretaría)
#===========================================

def login_secretaria():
    print("\n=== BIENVENIDO A LA IISEM INGRESE SUS DATOS ===")
    print("=== LOGIN SECRETARIA ===")
    usuario = input("Usuario: ")
    password = input("Contraseña: ")

    print("\nValidando acceso de secretaría...")
    menu_secretaria()