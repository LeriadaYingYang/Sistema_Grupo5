from director.login_director import login_director
from secretaria.login_secretaria import login_secretaria
from profesor.login_profesor import login_profesor
from alumno.login_alumno import login_alumno
from admin_sistema.login_admin import login_admin

def mostrar_menu_principal():
    print("""
==================================================
                      IISEM
==================================================
==================================================
  SISTEMA DE GESTIÓN ACADÉMICA Y ADMINISTRATIVA
==================================================

MENÚ PRINCIPAL

1. Director
2. Secretaria
3. Profesor
4. Alumno
5. Administrador del Sistema
6. Salir del sistema
""")


def main():
    while True:
        mostrar_menu_principal()
        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            login_director()

        elif opcion == "2":

            login_secretaria()

        elif opcion == "3":

            login_profesor()

        elif opcion == "4":

            login_alumno()

        elif opcion == "5":

            login_admin()

        elif opcion == "6":
            print("\nSaliendo del sistema...")
            break

        else:
            print("\nOpción inválida. Intente nuevamente.")
if __name__ == "__main__":
    main()