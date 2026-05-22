from conexion import conectar
from alumnos import GestionAlumnos
from carga_csv import CargaCSV
from gestion_datos import GestionDatos

ULTIMA_OPCION = 6


class App:

    def __crear_interfaz(self):
        print("=" * 45)
        print("  BANCO DE LIBROS - IES Arcipreste de Hita")
        print("=" * 45)
        print("  1. Gestion de alumnos")
        print("  2. Gestion de prestamos")
        print("  3. Listados y busquedas")
        print("  4. Gestion de datos")
        print("  5. Copia de seguridad")
        print("  6. Salir")
        print("=" * 45)

    def __gestion_alumnos(self):
        GestionAlumnos().run()

    def __gestion_prestamos(self):
        print("\n[Modulo de prestamos - pendiente de implementar]")

    def __listados_busquedas(self):
        print("\n[Modulo de listados - pendiente de implementar]")

    def __gestion_datos(self):
        GestionDatos().run()

    def __copia_seguridad(self):
        print("\n[Modulo de backup - pendiente de implementar]")

    def __ejecutar_opcion(self, opcion):
        if opcion == 1:
            self.__gestion_alumnos()
        elif opcion == 2:
            self.__gestion_prestamos()
        elif opcion == 3:
            self.__listados_busquedas()
        elif opcion == 4:
            self.__gestion_datos()
        elif opcion == 5:
            self.__copia_seguridad()
        elif opcion == ULTIMA_OPCION:
            print("\nSaliendo de la aplicacion...")
        else:
            print("\nOpcion no valida. Prueba de nuevo.")

    def run(self):
        print("Iniciando aplicacion...")
        conexion = conectar()

        if conexion is None:
            print(
                "Error: no se pudo establecer la conexion. Compruebe que XAMPP esta en ejecucion y que los datos de conexion.py son correctos.")
            return

        print("Conexion establecida correctamente.")
        conexion.close()

        opcion = 0
        while opcion != ULTIMA_OPCION:
            self.__crear_interfaz()
            opcion = int(input("  Elige una opcion: "))
            self.__ejecutar_opcion(opcion)


App().run()