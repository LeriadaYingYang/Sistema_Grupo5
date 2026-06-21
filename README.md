# Sistema de Gestión y Control Académica y Administrativa IISEM

## Descripción General

El Sistema de Gestión y Control Académica y Administrativa IISEM fue desarrollado como proyecto final del curso de Fundamentos de Programación, su propósito es digitalizar y centralizar los procesos académicos, administrativos, docentes y estudiantiles de una institución educativa mediante una aplicación de consola desarrollada en Python.
El sistema fue construido aplicando los principios fundamentales de análisis, diseño e implementación de software, utilizando una arquitectura modular que facilita el mantenimiento, la escalabilidad y la reutilización del código.

---

## Integrantes y Módulos Desarrollados

### Daniel Enrique
Responsable del desarrollo del código central de diversas funciones y modulos.

#### Gestión Académica

* Administración de carreras.
* Gestión de plantillas académicas.
* Gestión de salones.
* Gestión de unidades académicas.
* Gestión de módulos académicos.

#### Desarrollo Base del Sistema

* Diseño de la estructura general del proyecto.
* Implementación de utilidades reutilizables para la interfaz de consola.
* Desarrollo de funciones genéricas para manejo de archivos JSON.
* Generación automática de identificadores únicos.
* Estandarización de menús, títulos y navegación.

---

### Fabrizio Ortega
Responsable del módulo de Control Académico.

#### Funcionalidades Implementadas

* Gestión de horarios.
* Gestión de asistencias.
* Seguimiento académico.
* Control docente.
* Generación de reportes académicos y docentes.

---

### Pablo Díaz
Responsable del módulo de Gestión Docente.

#### Funcionalidades Implementadas

* Registro y administración de docentes.
* Asignación de profesores a salones.
* Consulta de cursos y horarios.
* Registro y control de notas.
* Validaciones y control de integridad de datos.

---

### Edith Huingo
Responsable del módulo de Gestión Estudiantil.

#### Funcionalidades Implementadas

* Registro de alumnos.
* Asignación de alumnos a carreras y salones.
* Consulta de información estudiantil.
* Edición y actualización de datos.
* Optimización y reutilización de funciones de validación.

---

### Juan Xavier
Responsable del módulo de Gestión y Control Administrativa

#### Funcionalidades Implementadas

* Gestión de cargos oficiales.
* Gestión de descuentos y convenios.
* Gestión de cargos extras.
* Resúmenes de pagos y deudas.

---

## Conceptos de Programación Aplicados

Durante el desarrollo del proyecto se aplicaron los principales conceptos estudiados en el curso:

* Programación estructurada.
* Modularización del sistema.
* Entrada, Proceso y Salida
* Diseño basado en funciones.
* Reutilización de código.
* Validación de datos.
* Manejo de estructuras de datos.
* Persistencia de información.
* Gestión de archivos.
* Control de errores.
* Organización jerárquica de información.
* Separación de responsabilidades entre módulos.

Asimismo, todas las funcionalidades fueron diseñadas bajo el enfoque de Entrada, Proceso y Salida (EPS), permitiendo una adecuada captura de información, procesamiento de datos y presentación de resultados al usuario.

---

## Arquitectura Implementada

El sistema se encuentra organizado en cuatro capas principales:

### 1. Capa de Presentación
Encargada de la interacción con el usuario mediante menús, formularios y mensajes mostrados en consola, permite la navegación entre los diferentes módulos del sistema y la visualización de la información procesada.

### 2. Capa de Seguridad y Autenticación
Responsable de controlar el acceso al sistema mediante procesos de autenticación, implementa la validación de credenciales como DNI y contraseña para verificar la identidad de los usuarios antes de permitir el acceso a los módulos correspondientes según su rol institucional, esta capa contribuye a la protección de la información y al control de acceso a las funcionalidades del sistema.

### 3. Capa de Lógica de Negocio
Contiene las reglas de funcionamiento del sistema, validaciones, cálculos y procesos académicos y administrativos, aquí se ejecutan las operaciones relacionadas con la gestión académica, estudiantil, docente, administrativa y de control académico.

### 4. Capa de Persistencia de Datos
Responsable del almacenamiento y recuperación de información utilizando archivos JSON, gestiona la lectura, escritura, actualización y consulta de registros, garantizando la conservación de los datos del sistema entre ejecuciones.

---

## Persistencia de Datos

La información del sistema se almacena mediante archivos JSON, permitiendo mantener los registros de manera estructurada y permanente entre ejecuciones.

Entre los principales beneficios de esta implementación se encuentran:

* Almacenamiento organizado de información.
* Facilidad de lectura y mantenimiento.
* Independencia de bases de datos externas.
* Portabilidad del sistema.
* Simplicidad para fines académicos.

---

## Características Generales

* Sistema completamente modular.
* Menús interactivos.
* Persistencia de datos mediante JSON.
* Validaciones de entrada.
* Manejo de errores.
* Identificadores automáticos.
* Búsquedas y consultas dinámicas.
* Edición y actualización de registros.
* Desactivación lógica de registros.
* Organización jerárquica de la información académica.
* Reutilización de componentes y funciones comunes.

---

## Conclusión

El desarrollo de IISEM permitió aplicar de forma práctica los fundamentos de programación aprendidos durante el curso, integrando técnicas de modularización, estructura, entrada, proceso, salida, persistencia de datos, validación de información y organización por capas. El resultado es un sistema funcional que centraliza procesos académicos y administrativos, demostrando la capacidad de análisis, diseño y construcción de soluciones de software mediante trabajo colaborativo y buenas prácticas de programación.

# Explicando como desarrollo

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