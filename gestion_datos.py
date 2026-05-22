import csv
from conexion import conectar
from carga_csv import CargaCSV


ULTIMA_OPCION_DATOS = 5
ULTIMA_OPCION_CURSOS = 3
ULTIMA_OPCION_MATERIAS = 3
ULTIMA_OPCION_LIBROS = 3


class GestionDatos:

    # --------------------------------------------------
    # Menu principal de gestion de datos
    # --------------------------------------------------
    def __crear_interfaz(self):
        print("=" * 45)
        print("  GESTION DE DATOS")
        print("=" * 45)
        print("  1. Cursos")
        print("  2. Materias")
        print("  3. Libros")
        print("  4. Cargar alumnos desde CSV")
        print("  5. Volver al menu principal")
        print("=" * 45)

    # --------------------------------------------------
    # Cursos
    # --------------------------------------------------
    def __menu_cursos(self):
        opcion = 0
        while opcion != ULTIMA_OPCION_CURSOS:
            print("=" * 45)
            print("  CURSOS")
            print("=" * 45)
            print("  1. Listar cursos")
            print("  2. Crear curso")
            print("  3. Volver")
            print("=" * 45)
            opcion = int(input("  Elige una opcion: "))
            if opcion == 1:
                self.__listar_cursos()
            elif opcion == 2:
                self.__crear_curso()
            elif opcion == ULTIMA_OPCION_CURSOS:
                print("Volviendo...")
            else:
                print("\nOpcion no valida. Prueba de nuevo.")

    def __listar_cursos(self):
        conexion = conectar()
        if conexion is None:
            return

        cursor = conexion.cursor()
        cursor.execute("SELECT curso, nivel FROM cursos ORDER BY nivel")
        cursos = cursor.fetchall()

        if len(cursos) == 0:
            print("\nNo hay cursos registrados.")
        else:
            print("\n{:<20} {:<20}".format("CURSO", "NIVEL"))
            print("-" * 40)
            for curso in cursos:
                print("{:<20} {:<20}".format(curso[0], curso[1]))

        cursor.close()
        conexion.close()

    def __crear_curso(self):
        print("\n--- Introducir datos del nuevo curso ---")
        curso = input("  Curso (ej: 1ESO-A): ").strip()
        nivel = input("  Nivel (ej: 1ºESO): ").strip()

        conexion = conectar()
        if conexion is None:
            return

        cursor = conexion.cursor()
        try:
            cursor.execute(
                "INSERT INTO cursos (curso, nivel) VALUES (%s, %s)",
                (curso, nivel)
            )
            conexion.commit()
            print("Curso registrado correctamente.")
        except Exception as error:
            print(f"Error al registrar el curso: {error}")

        cursor.close()
        conexion.close()

    # --------------------------------------------------
    # Materias
    # --------------------------------------------------
    def __menu_materias(self):
        opcion = 0
        while opcion != ULTIMA_OPCION_MATERIAS:
            print("=" * 45)
            print("  MATERIAS")
            print("=" * 45)
            print("  1. Listar materias")
            print("  2. Crear materia")
            print("  3. Volver")
            print("=" * 45)
            opcion = int(input("  Elige una opcion: "))
            if opcion == 1:
                self.__listar_materias()
            elif opcion == 2:
                self.__crear_materia()
            elif opcion == ULTIMA_OPCION_MATERIAS:
                print("Volviendo...")
            else:
                print("\nOpcion no valida. Prueba de nuevo.")

    def __listar_materias(self):
        conexion = conectar()
        if conexion is None:
            return

        cursor = conexion.cursor()
        cursor.execute("SELECT id, nombre, departamento FROM materias ORDER BY nombre")
        materias = cursor.fetchall()

        if len(materias) == 0:
            print("\nNo hay materias registradas.")
        else:
            print("\n{:<6} {:<30} {:<20}".format("ID", "NOMBRE", "DEPARTAMENTO"))
            print("-" * 56)
            for materia in materias:
                print("{:<6} {:<30} {:<20}".format(materia[0], materia[1], materia[2]))

        cursor.close()
        conexion.close()

    def __crear_materia(self):
        print("\n--- Introducir datos de la nueva materia ---")
        nombre = input("  Nombre de la materia: ").strip()
        departamento = input("  Departamento: ").strip()

        conexion = conectar()
        if conexion is None:
            return

        cursor = conexion.cursor()
        try:
            # Calculamos el siguiente ID manualmente
            cursor.execute("SELECT MAX(id) FROM materias")
            resultado = cursor.fetchone()
            siguiente_id = 1 if resultado[0] is None else resultado[0] + 1

            cursor.execute(
                "INSERT INTO materias (id, nombre, departamento) VALUES (%s, %s, %s)",
                (siguiente_id, nombre, departamento)
            )
            conexion.commit()
            print("Materia registrada correctamente.")
        except Exception as error:
            print(f"Error al registrar la materia: {error}")

        cursor.close()
        conexion.close()

    # --------------------------------------------------
    # Libros
    # --------------------------------------------------
    def __menu_libros(self):
        opcion = 0
        while opcion != ULTIMA_OPCION_LIBROS:
            print("=" * 45)
            print("  LIBROS")
            print("=" * 45)
            print("  1. Listar libros")
            print("  2. Crear libro")
            print("  3. Volver")
            print("=" * 45)
            opcion = int(input("  Elige una opcion: "))
            if opcion == 1:
                self.__listar_libros()
            elif opcion == 2:
                self.__crear_libro()
            elif opcion == ULTIMA_OPCION_LIBROS:
                print("Volviendo...")
            else:
                print("\nOpcion no valida. Prueba de nuevo.")

    def __listar_libros(self):
        conexion = conectar()
        if conexion is None:
            return

        cursor = conexion.cursor()
        cursor.execute("""
            SELECT l.isbn, l.titulo, l.autor, l.numero_ejemplares, m.nombre, l.id_curso
            FROM libros l
            JOIN materias m ON l.id_materia = m.id
            ORDER BY l.titulo
        """)
        libros = cursor.fetchall()

        if len(libros) == 0:
            print("\nNo hay libros registrados.")
        else:
            print("\n{:<15} {:<30} {:<20} {:<5} {:<15} {:<10}".format(
                "ISBN", "TITULO", "AUTOR", "EJEM.", "MATERIA", "CURSO"))
            print("-" * 95)
            for libro in libros:
                print("{:<15} {:<30} {:<20} {:<5} {:<15} {:<10}".format(
                    libro[0], libro[1][:28], libro[2][:18], libro[3], libro[4][:13], libro[5]))

        cursor.close()
        conexion.close()

    def __crear_libro(self):
        print("\n--- Introducir datos del nuevo libro ---")
        isbn = input("  ISBN: ").strip()
        titulo = input("  Titulo: ").strip()
        autor = input("  Autor: ").strip()
        numero_ejemplares = input("  Numero de ejemplares: ").strip()

        # Mostrar materias disponibles
        self.__listar_materias()
        id_materia = input("  ID de materia: ").strip()

        # Mostrar cursos disponibles
        self.__listar_cursos()
        id_curso = input("  Curso: ").strip()

        conexion = conectar()
        if conexion is None:
            return

        cursor = conexion.cursor()
        try:
            cursor.execute(
                "INSERT INTO libros (isbn, titulo, autor, numero_ejemplares, id_materia, id_curso) VALUES (%s, %s, %s, %s, %s, %s)",
                (isbn, titulo, autor, int(numero_ejemplares), int(id_materia), id_curso)
            )
            conexion.commit()
            print("Libro registrado correctamente.")
        except Exception as error:
            print(f"Error al registrar el libro: {error}")

        cursor.close()
        conexion.close()

    # --------------------------------------------------
    # Run
    # --------------------------------------------------
    def run(self):
        opcion = 0
        while opcion != ULTIMA_OPCION_DATOS:
            self.__crear_interfaz()
            opcion = int(input("  Elige una opcion: "))
            if opcion == 1:
                self.__menu_cursos()
            elif opcion == 2:
                self.__menu_materias()
            elif opcion == 3:
                self.__menu_libros()
            elif opcion == 4:
                CargaCSV().run()
            elif opcion == ULTIMA_OPCION_DATOS:
                print("Volviendo al menu principal...")
            else:
                print("\nOpcion no valida. Prueba de nuevo.")