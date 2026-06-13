from director.gestion_estudiante.crear_alumno import crear_alumno
from director.gestion_estudiante.asignar_alumno import asignar_alumno
from director.gestion_estudiante.ver_datos_alumnos import menu_ver_datos_alumnos
from director.gestion_estudiante.editar_alumno import editar_alumno
from director.gestion_estudiante.ver_historial_academico import ver_historial_academico
from director.utilidades import imprimir_titulo, imprimir_menu, limpiar_pantalla, pausa

_ACCIONES = {
    "1": ("Crear Alumno", crear_alumno),
    "2": ("Asignar Alumno a Carrera y Salón", asignar_alumno),
    "3": ("Ver Datos de Alumno", menu_ver_datos_alumnos),
    "4": ("Editar Alumno", editar_alumno),
    "5": ("Ver historial Academico", ver_historial_academico),
}

def menu_alumnos():
    while True:
        imprimir_titulo("GESTIÓN DE ALUMNOS")
        imprimir_menu(["Crear Alumno", "Asignar Alumno a Carrera y Salón",
                       "Ver Datos de Alumno","Editar Alumno", "Ver historial Academico","Volver"])

        opcion = input("Seleccione una opción: ")
        if opcion == "6":
            print("\nVolviendo al menú director.")
            break
        elif opcion in _ACCIONES:
            nombre, funcion = _ACCIONES[opcion]
            print(f"\n→ Ha seleccionado: {nombre}")
            pausa()
            limpiar_pantalla()
            funcion()
        else:
            print("Opción inválida.")