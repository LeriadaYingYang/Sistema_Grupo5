# Sistema_Grupo5
## Aporte de Daniel Enrqiue – Módulo de Gestión Académica entre otros Modulos
Durante el desarrollo del Sistema de Gestión y Control Académica y Administrativa IISEM, participé en el diseño e implementación del módulo de Gestión Académica, encargado de administrar la estructura académica de la institución.
Las funcionalidades desarrolladas incluyen:
### Gestión de Carreras
* Registrar carreras.
* Editar carreras.
* Buscar carreras.
* Visualizar carreras registradas.
* Desactivar carreras.
### Gestión de Plantillas Académicas
* Crear plantillas académicas.
* Editar plantillas.
* Asignar carreras a plantillas.
* Visualizar plantillas.
* Desactivar plantillas.
### Gestión de Salones
* Registrar salones.
* Editar salones.
* Asignar plantillas académicas a salones.
* Visualizar salones.
* Cerrar salones.
### Gestión de Módulos
* Registrar módulos académicos.
* Editar módulos.
* Asignar módulos a unidades.
* Visualizar módulos.
* Desactivar módulos.
### Gestión de Unidades
* Registrar unidades académicas.
* Editar unidades.
* Visualizar unidades.
* Desactivar unidades.
### Utilidades Generales
Asimismo, desarrollé funciones reutilizables para estandarizar la interfaz del sistema en consola, incluyendo:
* Impresión de títulos y encabezados.
* Impresión de menús dinámicos.
* Pausas de navegación.
* Utilidades de presentación para mejorar la experiencia de usuario.
### Persistencia de Datos
Se implementó el manejo de archivos JSON mediante funciones genéricas para:
* Lectura de archivos JSON.
* Escritura y actualización de registros.
* Generación automática de identificadores únicos.
* Administración de la persistencia de datos del sistema.
La estructura desarrollada permite mantener una relación jerárquica entre carreras, plantillas académicas, salones, módulos y unidades, garantizando la organización y consistencia de la información académica institucional.

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
# Sistema de Gestión Académica

Sistema desarrollado por el integrante pablo diaz desarrollo la parte de gestion docente.

## Módulos principales

### `profesor/` — Sesión del docente
| Archivo | Función principal |
|---|---|
| `login_profesor.py` | Solicita usuario y contraseña para iniciar sesión |
| `main,py` | Menú con opciones: cursos, alumnos, notas, horarios |
| `ver_cursos.py` | Muestra módulos agrupados por unidad del salón asignado |
| `ver_alumnos.py` | Lista alumnos inscritos con DNI y turno |
| `ver_horarios.py` | Muestra días y horas de clase del salón |
| `registrar_notas.py` | Flujo completo: salón → unidad → módulo → alumno → notas. Calcula promedio vigesimal y condición (A–D / Desaprobado) |

### `profesores/` — Administración (director)
| Archivo | Función principal |
|---|---|
| `main.py` | Menú CRUD de profesores |
| `crear_profesor.py` | Registra profesor validando DNI (8 dígitos) y celular (9 dígitos) |
| `editar_profesor.py` | Busca por nombre o DNI y edita campos individuales |
| `asignar_profesor.py` | Vincula un profesor activo a un salón activo sin duplicados |
| `ver_datos_profesores.py` | Consulta todos los profesores o busca por nombre/DNI, mostrando sus salones asignados |
---

## Lo que mejoré

- **Validaciones de entrada**: DNI (8 dígitos), celular (9 dígitos) y campos vacíos se validan antes de guardar.
- **Prevención de duplicados**: Se verifica DNI repetido al crear/editar profesor, y asignación duplicada al asignar profesor a salón.
- **Borrado lógico**: Ningún registro se elimina físicamente; se marca con `estado = "Activo/Inactivo"`.
- **Cálculo automático de promedios**: `registrar_notas.py` recalcula el promedio vigesimal cada vez que se ingresa una nota y lo guarda junto con la condición final.
- **Separación por roles**: El módulo `profesor/` gestiona la sesión activa del docente, mientras `profesores/` es de uso exclusivo del administrador.
