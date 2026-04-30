import mysql.connector

def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",#tu_contraseña aqui va tu contraseña de la base de datos cambienlo si en su mysql tienen otra clave de ingreso
        database="instituto_db"#aqui coloquen el nombre que vamos a trabajar para la base de datos
    )