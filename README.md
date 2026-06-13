# Sistema de Gestión Académica

Sistema de consola en Python para la administración de profesores, alumnos, cursos, horarios y notas. Los datos se persisten en archivos JSON locales.

---

## 🗂️ Estructura del Proyecto

<pre>
Proyecto Sistemas/
├── profesor/                   # Módulo para el docente en sesión
│   ├── login_profesor.py       # Autenticación del profesor
│   ├── main,py                 # Menú principal del profesor
│   ├── ver_cursos.py           # Ver cursos y módulos asignados
│   ├── ver_alumnos.py          # Ver alumnos inscritos por salón
│   ├── ver_horarios.py         # Consultar horarios de clase
│   └── registrar_notas.py      # Registrar y actualizar notas
│
├── profesores/                 # Módulo administrativo (director)
│   ├── main.py                 # Menú de gestión de profesores
│   ├── crear_profesor.py       # Registrar nuevo profesor
│   ├── editar_profesor.py      # Editar datos de un profesor
│   ├── asignar_profesor.py     # Asignar profesor a un salón
│   └── ver_datos_profesores.py # Consultar información de profesores
│
└── datos/                      # Persistencia en JSON
    ├── profesores.json
    ├── profesores_salones.json
    ├── salones.json
    ├── alumnos.json
    ├── alumnos_asignaciones.json
    ├── unidades.json
    ├── modulos.json
    ├── tablillas_notas.json
    ├── notas_alumnos.json
    └── horarios.json
</pre>

---

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

## Persistencia

Toda la información se almacena en archivos `.json` dentro de la carpeta `datos/`. Las operaciones de lectura y escritura se centralizan en el módulo `basedatos_json`, usando las funciones `leer_json()`, `guardar_json()` y `generar_id()`.

Los registros usan el campo `"estado": "Activo"` para el borrado lógico, evitando eliminar datos permanentemente.

---

## Lo que mejoré

- **Validaciones de entrada**: DNI (8 dígitos), celular (9 dígitos) y campos vacíos se validan antes de guardar.
- **Prevención de duplicados**: Se verifica DNI repetido al crear/editar profesor, y asignación duplicada al asignar profesor a salón.
- **Borrado lógico**: Ningún registro se elimina físicamente; se marca con `estado = "Activo/Inactivo"`.
- **Cálculo automático de promedios**: `registrar_notas.py` recalcula el promedio vigesimal cada vez que se ingresa una nota y lo guarda junto con la condición final.
- **Separación por roles**: El módulo `profesor/` gestiona la sesión activa del docente, mientras `profesores/` es de uso exclusivo del administrador.
