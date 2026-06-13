# Sistema_Grupo5
 
 Integrante: Edith Huingo

 Asignación: Gestión de Estudiantes

CAMBIOS Y MEJORAS QUE SE HIZO EN GESTION DE ESTUDIANTES

Se optimizaron los módulos del sistema de alumnos, eliminando código repetido y añadiendo validaciones.

En utilidades.py agregué las funciones pedir_entero() y validar_no_vacio() para no repetir la misma lógica en cada módulo.

En crear_alumno.py añadí validaciones para que el DNI sea de 8 dígitos numéricos, el celular de 9 dígitos numéricos y el correo tenga formato ejemplo@gmail.com. También agregué una verificación para que no se puedan registrar dos alumnos con el mismo DNI.

En asignar_alumno.py unifiqué las tres funciones de mostrar datos en una sola genérica y junté las validaciones previas en una lista en lugar de tenerlas separadas en cinco bloques.

En editar_alumno.py el menú de edición ahora se genera desde una lista CAMPOS_EDITABLES en lugar de tener un elif por cada campo. También agregué validación de campo vacío y de DNI duplicado al momento de editar.

En ver_datos_alumnos.py eliminé el patrón repetido de contar alumnos encontrados creando una función genérica, y cambié el menú para que se despache desde un diccionario en lugar de una cadena de elif.

En ver_historial_academico.py reemplacé el pass vacío por un mensaje que avisa que el módulo está en construcción.