from conexion import conectar
from alumnos import GestionAlumnos
from carga_csv import CargaCSV
from prestamos import GestionPrestamos
from listados import GestionListados


ULTIMA_OPCION = 7


class App:

    def __crear_interfaz(self):
        print("=" * 45)
        print("  BANCO DE LIBROS - IES Arcipreste de Hita")
        print("=" * 45)
        print("  1. Gestion de alumnos")
        print("  2. Gestion de prestamos")
        print("  3. Listados y busquedas")
        print("  4. Cargar alumnos desde CSV")
        print("  5. Contratos")
        print("  6. Copia de seguridad")
        print("  7. Salir")
        print("=" * 45)

    def __gestion_alumnos(self):
        GestionAlumnos().run()

    def __gestion_prestamos(self):
        GestionPrestamos().run()

    def __listados_busquedas(self):
        GestionListados().run()

    def __cargar_csv(self):
        CargaCSV().run()


    def __ejecutar_opcion(self, opcion):
        if opcion == 1:
            self.__gestion_alumnos()
        elif opcion == 2:
            self.__gestion_prestamos()
        elif opcion == 3:
            self.__listados_busquedas()
        elif opcion == 4:
            self.__cargar_csv()
        elif opcion == 5:
            self.__contratos()
        elif opcion == 6:
            self.__copia_seguridad()
        elif opcion == ULTIMA_OPCION:
            print("\nSaliendo de la aplicacion...")
        else:
            print("\nOpcion no valida. Prueba de nuevo.")

    def run(self):
        print("Iniciando aplicacion...")
        conexion = conectar()

        if conexion is None:
            print("Error: no se pudo establecer la conexion. Compruebe que XAMPP esta en ejecucion y que los datos de conexion.py son correctos.")
            return

        print("Conexion establecida correctamente.")
        conexion.close()

        opcion = 0
        while opcion != ULTIMA_OPCION:
            self.__crear_interfaz()
            opcion = int(input("  Elige una opcion: "))
            self.__ejecutar_opcion(opcion)


App().run()