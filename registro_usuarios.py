import os
from basedatos_json import leer_json, guardar_json, generar_id
from director.utilidades import imprimir_titulo, imprimir_menu, pausa, limpiar_pantalla

RUTA_CARRERAS = "datos/carreras.json"
RUTA_ALUMNOS = "datos/alumnos.json"
RUTA_PROFESORES = "datos/profesores.json"
RUTA_USUARIOS_SISTEMA = "datos/usuarios_sistema.json"

def generar_correo_institucional(nombres, apellidos, dni):
    """
    Función pura con retorno. Genera un correo institucional único
    basado en la primera letra del nombre, el apellido paterno y el DNI.
    """
    primer_nombre = nombres.strip().split()[0].lower() if nombres else "user"
    primer_apellido = apellidos.strip().split()[0].lower() if apellidos else "ln"
    dni_limpio = dni.strip()
    
    correo = f"{primer_nombre[0]}{primer_apellido}{dni_limpio}@iisem.edu.pe"
    return correo

def seleccionar_carrera_registro():
    """
    Muestra las carreras del JSON por referencia y permite elegir una.
    Si se solicita, permite registrar una nueva carrera en caliente.
    """
    carreras = leer_json(RUTA_CARRERAS)
    
    while True:
        limpiar_pantalla()
        imprimir_titulo("SELECCIÓN DE CARRERA")
        
        # Listamos las carreras activas
        carreras_activas = [c for c in carreras if c["estado"] == "Activo"]
        for i, car in enumerate(carreras_activas, start=1):
            print(f"{i}. {car['nombre'].upper()} ({car['descripcion']})")
        print(f"{len(carreras_activas) + 1}. [ + Agregar otra carrera al sistema ]")
        
        try:
            opc = int(input("\nSeleccione una opción de carrera: "))
            
            # Caso: Elegir carrera existente
            if 1 <= opc <= len(carreras_activas):
                return carreras_activas[opc - 1]
            # Caso: Crear nueva carrera para el futuro
            elif opc == len(carreras_activas) + 1:
                imprimir_titulo("AGREGAR NUEVA CARRERA")
                nuevo_nombre = input("Nombre de la nueva carrera: ").strip().lower()
                nueva_desc = input("Descripción breve: ").strip()
                while True:
                    try:
                        nueva_duracion = int(input("Duración en meses: "))
                        break
                    except ValueError:
                        print(" Ingrese un número válido.")
                nueva_car_dict = {
                    "id_carrera": generar_id(carreras, "id_carrera"),
                    "nombre": nuevo_nombre,
                    "descripcion": nueva_desc,
                    "duracion_meses": nueva_duracion,
                    "estado": "Activo"
                }
                carreras.append(nueva_car_dict)
                guardar_json(RUTA_CARRERAS, carreras)
                print("\n Nueva carrera incorporada con éxito al catálogo institucional.")
                pausa()     
            else:
                print(" Opción fuera de rango.")
                pausa()
        except ValueError:
            print(" Entrada inválida. Ingrese un número.")
            pausa()
def crear_sesion_usuario():
    """
    Interfaz de usuario encapsulada para la creación de cuentas de acceso.
    Satisface el rol, género, grado, carrera, correo automático y estados.
    """
    limpiar_pantalla()
    imprimir_titulo("CREAR SESIÓN / REGISTRO DE USUARIO")
    
    # 1. Selección de Cargo / Rol
    print("Seleccione su cargo en la institución:")
    print("1. Director\n2. Secretaria\n3. Profesor\n4. Alumno\n5. Administrador del Sistema")
    opc_cargo = input("\nOpción de cargo: ").strip()
    
    roles_map = {"1": "Director", "2": "Secretaria", "3": "Profesor", "4": "Alumno", "5": "Administrador"}
    if opc_cargo not in roles_map:
        print(" Opción de cargo no válida. Operación cancelada.")
        pausa()
        return
    cargo_elegido = roles_map[opc_cargo]
    
    # 2. Captura de Datos Básicos
    nombres = input("\nNombres completos: ").strip()
    apellidos = input("Apellidos completos: ").strip()
    dni = input("Número de DNI: ").strip()
    correo_personal = input("Correo electrónico personal: ").strip()
    celular = input("Número de celular: ").strip()
    
    # 3. Selección de Género
    print("\nSeleccione Género:")
    print("1. Masculino\n2. Femenino\n3. No especificar")
    opc_gen = input("Opción: ").strip()
    genero = "Masculino" if opc_gen == "1" else "Femenino" if opc_gen == "2" else "No especificado"
    
    # 4. Grado de Instrucción / Grado Académico
    grado = input("\nGrado académico o ciclo actual (ej: Bachiller, V Ciclo, Licenciado): ").strip()
    
    # 5. Selección y enlace de Carrera
    carrera_vinculada = seleccionar_carrera_registro()
    
    # 6. Selección del Estado del Usuario (Requerimiento de Estados)
    print("\nDefina el estado inicial del usuario en el sistema:")
    print("1. Activo\n2. Suspendido\n3. Retirado")
    opc_est = input("Opción: ").strip()
    estado_usuario = "Activo" if opc_est == "1" else "Suspendido" if opc_est == "2" else "Retirado"
    
    # 7. Generación automática del Correo Institucional (Lógica de negocio integrada)
    correo_institucional = generar_correo_institucional(nombres, apellidos, dni)
    
    # Contraseña por defecto basada en el DNI para el primer inicio de sesión
    password_defecto = dni
    
    # 8. Guardado modular segmentado según el Dominio/Cargo del Usuario
    if cargo_elegido == "Alumno":
        alumnos_lista = leer_json(RUTA_ALUMNOS)
        nuevo_item = {
            "id_alumno": generar_id(alumnos_lista, "id_alumno"),
            "nombres": nombres.lower(),
            "apellidos": apellidos.lower(),
            "dni": dni,
            "correo": correo_institucional,
            "correo_personal": correo_personal,
            "celular": celular,
            "genero": genero,
            "grado_instruccion": grado,
            "carrera": carrera_vinculada["nombre"],
            "id_carrera": carrera_vinculada["id_carrera"],
            "estado": estado_usuario
        }
        alumnos_lista.append(nuevo_item)
        guardar_json(RUTA_ALUMNOS, alumnos_lista)
    elif cargo_elegido == "Profesor":
        profesores_lista = leer_json(RUTA_PROFESORES)
        nuevo_item = {
            "id_profesor": generar_id(profesores_lista, "id_profesor"),
            "nombres": nombres.lower(),
            "apellidos": apellidos.lower(),
            "dni": dni,
            "correo": correo_institucional,
            "correo_personal": correo_personal,
            "celular": celular,
            "genero": genero,
            "grado_instruccion": grado,
            "carrera_principal": carrera_vinculada["nombre"],
            "estado": estado_usuario
        }
        profesores_lista.append(nuevo_item)
        guardar_json(RUTA_PROFESORES, profesores_lista)
    else:
        # Administrativos (Director, Secretaria, Admin) van a una tabla de control de accesos
        usuarios_sys = leer_json(RUTA_USUARIOS_SISTEMA)
        nuevo_item = {
            "id_usuario": generar_id(usuarios_sys, "id_usuario"),
            "username": correo_institucional.split("@")[0],
            "password": password_defecto,
            "cargo": cargo_elegido,
            "nombres": nombres,
            "apellidos": apellidos,
            "dni": dni,
            "correo_institucional": correo_institucional,
            "genero": genero,
            "estado": estado_usuario
        }
        usuarios_sys.append(nuevo_item)
        guardar_json(RUTA_USUARIOS_SISTEMA, usuarios_sys)

    limpiar_pantalla()
    imprimir_titulo(" REGISTRO PROCESADO EXITOSAMENTE")
    print(f"Ficha de Cuenta Generada para: {cargo_elegido.upper()}")
    print(f" Usuario: {nombres.upper()} {apellidos.upper()}")
    print(f" DNI: {dni} | Género: {genero}")
    print(f" Grado/Ciclo: {grado}")
    print(f" Carrera Asignada: {carrera_vinculada['nombre'].upper()}")
    print(f" Correo Personal: {correo_personal}")
    print(f" CORREO INSTITUCIONAL: {correo_institucional}")
    print(f" Contraseña de Acceso Base: {password_defecto}")
    print(f" Estado Actual en Plataforma: {estado_usuario}")
    print("-" * 40)
    pausa()