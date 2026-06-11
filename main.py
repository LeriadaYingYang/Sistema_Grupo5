from gestion_academica.login_gestion_academica import login_gestion_academica
from control_academico.login_control_academico import login_control_academico
from gestion_docente.login_gestion_docente import login_gestion_docente
from gestion_estudiantes.login_gestion_estudiantes import login_gestion_estudiantes
from gestion_control_admin.login_control_admin import login_control_admin
from gestion_academica.utilidades import imprimir_titulo, imprimir_menu

def mostrar_menu_principal():
    imprimir_titulo("IISEM")
    imprimir_titulo("SISTEMA DE GESTIÓN ACADÉMICA Y ADMINISTRATIVA")
    imprimir_menu(["Gestion Académica", "Control Académico", "Gestión Docente", "Gestión estudiantes", "Gestión y Control Administrativo","Salir del sistema"])

def main():
    while True:
        mostrar_menu_principal()
        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            login_gestion_academica()
        elif opcion == "2":
            login_control_academico()
        elif opcion == "3":
            login_gestion_docente()
        elif opcion == "4":
            login_gestion_estudiantes()
        elif opcion == "5":
            login_control_admin()
        elif opcion == "6":
            print("\nSaliendo del sistema")
            break
        else:
            print("\nOpción inválida. Intente nuevamente.")
if __name__ == "__main__":
    main()