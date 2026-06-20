# Sistema de Gestión y Control Académica y Administrativa IISEM

Integrante: Edith Huingo

Asignación: Gestión de Estudiantes

## Módulos del sistema

| Archivo | Función principal |
|---|---|
| `main.py` | Menú con 5 opciones: Crear, Asignar, Ver, Editar, Historial |
| `crear_alumno.py` | Registra alumno validando DNI (8 dígitos), celular (9 dígitos), correo (@gmail.com) y nombres (solo letras) |
| `asignar_alumno.py` | Asigna alumno a carrera y salón mostrando datos del alumno |
| `editar_alumno.py` | Busca por ID y edita campos individuales con validación |
| `ver_datos_alumnos.py` | Consulta todos o busca por ID, nombre o DNI |
| `ver_historial_academico.py` | Muestra notas, promedio y condición del alumno |

## Validaciones implementadas
- **Nombres/Apellidos**: solo letras y espacios, no vacío
- **DNI**: exactamente 8 dígitos numéricos
- **Celular**: exactamente 9 dígitos numéricos
- **Correo**: debe terminar en @gmail.com
- **Notas**: valor entero entre 0 y 20
- **Campos vacíos**: ningún campo puede quedar vacío
- **DNI duplicado**: se verifica al crear y editar
- **Reintento**: todas las validaciones repiten hasta que el dato sea correcto

## Persistencia
Los datos se almacenan en archivos JSON dentro de la carpeta `datos/`.
Las operaciones de lectura y escritura se centralizan en `basedatos_json.py`
con las funciones `leer_json()`, `guardar_json()` y `generar_id()`.
