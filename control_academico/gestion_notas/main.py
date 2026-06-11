from control_academico.gestion_notas.registrar_nota import registrar_notas
from control_academico.gestion_notas.consultar_notas import consultar_notas
from control_academico.gestion_notas.modificar_nota import menu_modificar_notas
from control_academico.gestion_notas.eliminar_nota import menu_eliminar_notas
from control_academico.utilidades import imprimir_titulo,pausa,limpiar_pantalla

def menu_notas():
    while True:
        limpiar_pantalla()
        imprimir_titulo("=== GESTIÓN DE NOTAS ===")
        print("1. Registrar nota")
        print("2. Consultar notas")
        print("3. Modificar nota")
        print("4. Eliminar nota")
        print("5. Volver")
        opcion = input("\nSeleccione una opción: ")
        limpiar_pantalla()
        if opcion == "1":registrar_notas()
        elif opcion == "2":consultar_notas()
        elif opcion == "3":menu_modificar_notas()
        elif opcion == "4":menu_eliminar_notas()
        elif opcion == "5":
            break
        else:
            print("Opción inválida.")
        pausa()