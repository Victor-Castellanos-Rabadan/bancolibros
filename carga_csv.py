import csv
from conexion import conectar


class CargaCSV:

    def __crear_interfaz(self):
        print("=" * 45)
        print("  CARGA DE ALUMNOS DESDE CSV")
        print("=" * 45)

    def __cargar_csv(self):
        ruta = input("\n  Introduzca la ruta del fichero CSV: ").strip()

        try:
            fichero = open(ruta, newline='', encoding='utf-8')
        except FileNotFoundError:
            print("Error: no se ha encontrado el fichero.")
            return

        lector = csv.DictReader(fichero)

        conexion = conectar()
        if conexion is None:
            fichero.close()
            return

        cursor = conexion.cursor()
        insertados = 0
        omitidos = 0

        for fila in lector:
            try:
                cursor.execute(
                    "INSERT INTO alumnos (nie, nombre, apellidos, tramo, bilingue) VALUES (%s, %s, %s, %s, %s)",
                    (fila['nie'], fila['nombre'], fila['apellidos'], fila['tramo'], int(fila['bilingue']))
                )
                insertados += 1
            except Exception:
                # Si el NIE ya existe u otro error se omite esa fila
                omitidos += 1

        conexion.commit()
        print(f"\n  Proceso finalizado.")
        print(f"  Alumnos insertados: {insertados}")
        print(f"  Alumnos omitidos:   {omitidos}")

        cursor.close()
        conexion.close()
        fichero.close()

    def run(self):
        self.__crear_interfaz()
        self.__cargar_csv()