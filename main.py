from director.login_director import login_director

from director.utilidades import imprimir_titulo, imprimir_menu, limpiar_pantalla

def mostrar_menu_principal():
    imprimir_titulo("IISEM")
    imprimir_titulo("SISTEMA DE GESTIÓN ACADÉMICA Y ADMINISTRATIVA")
    imprimir_menu(["Director", "Secretaria", "Profesor", "Alumno", "Administrador","Salir del sistema"])

def main():
    while True:
        mostrar_menu_principal()
        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            login_director()

        elif opcion == "6":
            print("\nSaliendo del sistema")
            break

        else:
            print("\nOpción inválida. Intente nuevamente.")
if __name__ == "__main__":
    main()