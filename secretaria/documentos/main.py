from secretaria.documentos.certificados import menu_certificados
from secretaria.documentos.constancias import menu_constancias
from secretaria.documentos.historial_academico import menu_historial_academico
from secretaria.documentos.solicitudes import menu_solicitudes
from secretaria.utilidades import imprimir_titulo,imprimir_menu

#===========================================
# Archivo: main.py -> documentos
# Participante: Fabrizio Ortega (secretaría)
#===========================================

def menu_documentos(): #Muestra el menú principal de documentos
    while True:
        imprimir_titulo("=== GESTIÓN DE DOCUMENTOS ===")
        imprimir_menu(["Certificados","Constancias","Historial Académico",
                    "Solicitudes","Volver"])

        opcion = input("Seleccionar una opción: ")
        if opcion == "1": #Abre el módulo certificados
            menu_certificados()
        elif opcion == "2": #Abre el módulo constancias
            menu_constancias()
        elif opcion == "3": #Abre historial académico
            menu_historial_academico()
        elif opcion == "4": #Abre solicitudes
            menu_solicitudes()
        elif opcion == "5": #Vuelve al menú secretaría
            print("\nVolviendo al menú secretaría...")
            break
        else: #Muestra mensaje de error
            print("Opción inválida.")