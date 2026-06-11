from director.login_director import login_director
from registro_usuarios import crear_sesion_usuario
from secretaria.login_secretaria import login_secretaria
from profesor.login_profesor import login_profesor
from alumno.login_alumno import login_alumno
from admin_sistema.login_admin import login_admin
from director.utilidades import imprimir_titulo, imprimir_menu, limpiar_pantalla, pausa

def mostrar_menu_principal():
    imprimir_titulo("IISEM")
    imprimir_titulo("SISTEMA DE GESTIÓN ACADÉMICA Y ADMINISTRATIVA")
    imprimir_menu(["Director", "Secretaria", "Profesor", "Alumno", "Administrador","Salir del sistema"])
def main():
    while True:
        limpiar_pantalla()
        imprimir_titulo("SISTEMA IISEM")
        print("1. Ingresar al Sistema (Login)")
        print("2. Registrar Nuevo Usuario (Crear Sesión)")
        print("3. Salir de la Aplicación")
        
        opc_inicial = input("\nSeleccione una opción: ").strip()
        
        if opc_inicial == "1":
            while True:
                limpiar_pantalla()
                imprimir_titulo("SISTEMA DE GESTIÓN ACADÉMICA Y ADMINISTRATIVA")
                imprimir_menu(["Director", "Secretaria", "Profesor", "Alumno", "Administrador", "Volver"])
                
                opcion = input("\nSeleccione su rol de ingreso: ").strip()
                if opcion == "1": login_director()
                elif opcion == "2": login_secretaria()
                elif opcion == "3": login_profesor()
                elif opcion == "4": login_alumno()
                elif opcion == "5": login_admin()
                elif opcion == "6": break
                else:
                    print("\n Opción inválida.")
                    pausa()       
        elif opc_inicial == "2":
            crear_sesion_usuario()
            
        elif opc_inicial == "3":
            print("\nSaliendo del sistema de forma segura. ¡Hasta pronto!")
            break
        else:
            print("\n Opción inválida.")
            pausa()
if __name__ == "__main__":
    main()