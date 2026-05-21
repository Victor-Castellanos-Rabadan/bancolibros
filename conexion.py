import mysql.connector

HOST = "localhost"
USUARIO = "root"
CONTRASENA = ""
BASE_DATOS = "bancolibros"


def conectar():

    try:
        conexion = mysql.connector.connect(
            host=HOST,
            user=USUARIO,
            password=CONTRASENA,
            database=BASE_DATOS
        )
        return conexion
    except mysql.connector.Error as error:
        print(f"Error al conectar con la base de datos: {error}")
        return None