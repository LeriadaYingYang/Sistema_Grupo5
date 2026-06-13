# Sistema Académico - Grupo 5
Integrante
- Fabrizio Ortega

Asignación
- Contról Académico

Observaciones
- Esta parte del proyecto fue desarrollada para el trabajo final del curso Fundamentos de Programación, aplicando estructuras de datos, modularización, funciones, archivos JSON y buenas prácticas de programación.

# Estructura del Sistema

1. Gestión de Horarios
Permite administrar los horarios académicos de los salones y docentes.

Funciones implementadas:
- Configurar horarios
- Modificar horarios
- Consultar horarios
- Asignar horarios a profesores
- Ver carga horaria docente

2. Gestión de Asistencias
Permite registrar y consultar la asistencia de alumnos y profesores.

Funciones implementadas:
- Asistencia de alumnos
- Asistencia de profesores
- Consultar asistencia de alumnos
- Consultar asistencia de profesores
- Reporte de inasistencias

3. Seguimiento Académico
Permite supervisar el rendimiento académico de los estudiantes.

Funciones implementadas:
- Ver notas por módulo
- Ver notas por unidad
- Consultar rendimiento académico
- Alumnos con bajo rendimiento
- Reporte académico general

4. Control Docente
Permite supervisar el desempeño y cumplimiento de los docentes.

Funciones implementadas:
- Ver horas trabajadas
- Control de carga horaria
- Reporte de asistencia docente
- Profesores con faltas
- Resumen de desempeño docente

# Almacenamiento de Datos
Toda la información del sistema se almacena con JSON ubicados dentro de la carpeta "datos/"

Ejemplo:
- alumnos.json
- profesores.json
- horarios.json
- asistencia_alumnos.json
- asistencia_profesores.json
- notas_alumnos.json

# Características Implementadas
- Menús interactivos.
- Persistencia de datos con JSON.
- Validación de entradas.
- Manejo básico de errores.
- Generación automática de identificadores.
- Registro de asistencias en tiempo real.
- Cálculo automático de horas trabajadas.
- Consultas y reportes académicos.
- Consultas y reportes docentes.