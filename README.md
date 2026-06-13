
# Sistema de Gestión Académica

- Sistema de consola en Python para la administración de profesores, alumnos, cursos, horarios y notas. Los datos se persisten en archivos JSON locales.

## Estructura del Proyecto

Proyecto Sistemas/

├── director/
│
├── profesor/                  # Módulo para el docente en sesión
│   ├── login_profesor.py      # Autenticación del profesor
│   ├── main,py                # Menú principal del profesor
│   ├── ver_cursos.py          # Ver cursos y módulos asignados
│   ├── ver_alumnos.py         # Ver alumnos inscritos por salón
│   ├── ver_horarios.py        # Consultar horarios de clase
│   └── registrar_notas.py     # Registrar y actualizar notas
│
├── profesores/                # Módulo administrativo (director)
│   ├── main.py                # Menú de gestión de profesores
│   ├── crear_profesor.py      # Registrar nuevo profesor
│   ├── editar_profesor.py     # Editar datos de un profesor
│   ├── asignar_profesor.py    # Asignar profesor a un salón
│   └── ver_datos_profesores.py# Consultar información de profesores
│
└── datos/                     # Persistencia en JSON
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

### Toda la información se almacena en archivos .json dentro de la carpeta datos/. Las operaciones de lectura y escritura se centralizan en el módulo basedatos_json, usando las funciones leer_json(), guardar_json() y generar_id(). Los registros usan el campo "estado": "Activo" para el borrado lógico, evitando eliminar datos permanentemente.

## Las Mejoras>

- Validaciones de entrada: DNI (8 dígitos), celular (9 dígitos) y campos vacíos se validan antes de guardar.
- Prevención de duplicados: Se verifica DNI repetido al crear/editar profesor, y asignación duplicada al asignar profesor a salón.
- Cálculo automático de promedios: registrar_notas.py recalcula el promedio vigesimal cada vez que se ingresa una nota y lo guarda junto con la condición final.
- Separación por roles: El módulo profesor/ gestiona la sesión activa del docente, mientras profesores/ es de uso exclusivo del administrador.