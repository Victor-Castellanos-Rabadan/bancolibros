from conexion import conectar
from datetime import datetime
import csv
import os


class Backup:

    def __crear_interfaz(self):
        print("=" * 45)
        print("  COPIA DE SEGURIDAD")
        print("=" * 45)
        print("  1. Exportar todos los datos a CSV")
        print("  2. Volver al menu principal")
        print("=" * 45)

    def __exportar_tabla(self, cursor, nombre_tabla, ruta_carpeta):
        cursor.execute(f"SELECT * FROM {nombre_tabla}")
        filas = cursor.fetchall()
        columnas = [descripcion[0] for descripcion in cursor.description]

        ruta_fichero = os.path.join(ruta_carpeta, f"{nombre_tabla}.csv")
        fichero = open(ruta_fichero, "w", newline="", encoding="utf-8")
        escritor = csv.writer(fichero)
        escritor.writerow(columnas)
        escritor.writerows(filas)
        fichero.close()

        print(f"  {nombre_tabla}: {len(filas)} registros exportados.")

    def __exportar_todo(self):
        conexion = conectar()
        if conexion is None:
            return

        # Crear carpeta backups con la fecha y hora actual
        fecha_hora = datetime.now().strftime("%Y%m%d_%H%M%S")
        ruta_carpeta = os.path.join("backups", fecha_hora)
        if not os.path.exists(ruta_carpeta):
            os.makedirs(ruta_carpeta)

        cursor = conexion.cursor()
        tablas = ["alumnos", "cursos", "materias", "libros", "alumnoscursoslibros"]

        print(f"\n  Exportando datos a: {ruta_carpeta}\n")
        for tabla in tablas:
            try:
                self.__exportar_tabla(cursor, tabla, ruta_carpeta)
            except Exception as error:
                print(f"  Error al exportar {tabla}: {error}")

        cursor.close()
        conexion.close()
        print(f"\n  Copia de seguridad completada correctamente.")

    def run(self):
        opcion = 0
        while opcion != 2:
            self.__crear_interfaz()
            opcion = int(input("  Elige una opcion: "))
            if opcion == 1:
                self.__exportar_todo()
            elif opcion == 2:
                print("Volviendo al menu principal...")
            else:
                print("\nOpcion no valida. Prueba de nuevo.")