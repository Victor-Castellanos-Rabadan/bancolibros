from conexion import conectar
from datetime import date
import os


ULTIMA_OPCION = 3


class GestionContratos:

    # --------------------------------------------------
    # Menu principal
    # --------------------------------------------------
    def __crear_interfaz(self):
        print("=" * 45)
        print("  GESTION DE CONTRATOS")
        print("=" * 45)
        print("  1. Generar contrato de un alumno")
        print("  2. Ver contratos generados")
        print("  3. Volver al menu principal")
        print("=" * 45)

    # --------------------------------------------------
    # Generar contrato
    # --------------------------------------------------
    def __generar_contrato(self):
        nie = input("\n  Introduzca el NIE del alumno: ").strip()

        conexion = conectar()
        if conexion is None:
            return

        cursor = conexion.cursor()

        # Buscar alumno
        cursor.execute(
            "SELECT nie, nombre, apellidos FROM alumnos WHERE nie = %s",
            (nie,)
        )
        alumno = cursor.fetchone()

        if alumno is None:
            print("  No se ha encontrado ningun alumno con ese NIE.")
            cursor.close()
            conexion.close()
            return

        # Buscar prestamos activos del alumno
        cursor.execute(
            """SELECT acl.isbn, l.titulo, acl.curso
               FROM alumnoscursoslibros acl
               JOIN libros l ON acl.isbn = l.isbn
               WHERE acl.nie = %s AND acl.estado = 'P'
               ORDER BY acl.curso, l.titulo""",
            (nie,)
        )
        prestamos = cursor.fetchall()

        if len(prestamos) == 0:
            print("  Este alumno no tiene libros en prestamo activo.")
            cursor.close()
            conexion.close()
            return

        cursor.close()
        conexion.close()

        # Construir el contenido del contrato
        hoy = date.today().strftime("%d/%m/%Y")
        nie_alumno, nombre, apellidos = alumno
        curso = prestamos[0][2]

        lineas = []
        lineas.append("=" * 50)
        lineas.append("        IES ARCIPRESTE DE HITA")
        lineas.append("    CONTRATO DE PRESTAMO DE LIBROS")
        lineas.append("=" * 50)
        lineas.append(f"Fecha: {hoy}")
        lineas.append("")
        lineas.append("DATOS DEL ALUMNO")
        lineas.append(f"NIE:      {nie_alumno}")
        lineas.append(f"Nombre:   {nombre} {apellidos}")
        lineas.append(f"Curso:    {curso}")
        lineas.append("")
        lineas.append("LIBROS PRESTADOS")
        lineas.append("-" * 50)
        lineas.append("{:<18} {:<30}".format("ISBN", "TITULO"))
        lineas.append("-" * 50)
        for prestamo in prestamos:
            lineas.append("{:<18} {:<30}".format(prestamo[0], prestamo[1][:28]))
        lineas.append("-" * 50)
        lineas.append("")
        lineas.append("El alumno se compromete a devolver los libros")
        lineas.append("en buen estado al finalizar el curso.")
        lineas.append("")
        lineas.append("Firma del alumno o tutor: ___________________")
        lineas.append("=" * 50)

        # Crear carpeta contratos si no existe
        if not os.path.exists("contratos"):
            os.makedirs("contratos")

        # Guardar el fichero
        nombre_fichero = f"contratos/contrato_{nie_alumno}_{date.today()}.txt"
        fichero = open(nombre_fichero, "w", encoding="utf-8")
        for linea in lineas:
            fichero.write(linea + "\n")
        fichero.close()

        # Mostrar por pantalla
        print()
        for linea in lineas:
            print(linea)

        print(f"\n  Contrato guardado en: {nombre_fichero}")

    # --------------------------------------------------
    # Ver contratos generados
    # --------------------------------------------------
    def __ver_contratos(self):
        if not os.path.exists("contratos"):
            print("\n  No hay contratos generados todavia.")
            return

        ficheros = os.listdir("contratos")
        ficheros_txt = [f for f in ficheros if f.endswith(".txt")]

        if len(ficheros_txt) == 0:
            print("\n  No hay contratos generados todavia.")
            return

        print(f"\n  Contratos generados: {len(ficheros_txt)}\n")
        for i, fichero in enumerate(sorted(ficheros_txt)):
            print(f"  {i + 1}. {fichero}")

    # --------------------------------------------------
    # Run
    # --------------------------------------------------
    def run(self):
        opcion = 0
        while opcion != ULTIMA_OPCION:
            self.__crear_interfaz()
            opcion = int(input("  Elige una opcion: "))
            if opcion == 1:
                self.__generar_contrato()
            elif opcion == 2:
                self.__ver_contratos()
            elif opcion == ULTIMA_OPCION:
                print("Volviendo al menu principal...")
            else:
                print("\nOpcion no valida. Prueba de nuevo.")