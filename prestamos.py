from conexion import conectar
from datetime import date


ULTIMA_OPCION = 4


class GestionPrestamos:

    # --------------------------------------------------
    # Menu principal de gestion de prestamos
    # --------------------------------------------------
    def __crear_interfaz(self):
        print("=" * 45)
        print("  GESTION DE PRESTAMOS")
        print("=" * 45)
        print("  1. Asignar libros a un alumno")
        print("  2. Registrar devolucion de un libro")
        print("  3. Cerrar prestamo de un alumno")
        print("  4. Volver al menu principal")
        print("=" * 45)

    # --------------------------------------------------
    # Buscar alumno
    # --------------------------------------------------
    def __buscar_alumno(self):
        nie = input("\n  Introduzca el NIE del alumno: ").strip()

        conexion = conectar()
        if conexion is None:
            return None, None

        cursor = conexion.cursor()
        cursor.execute(
            "SELECT nie, nombre, apellidos FROM alumnos WHERE nie = %s",
            (nie,)
        )
        alumno = cursor.fetchone()
        cursor.close()
        conexion.close()

        if alumno is None:
            print("  No se ha encontrado ningun alumno con ese NIE.")
            return None, None

        print(f"\n  Alumno: {alumno[1]} {alumno[2]}")
        return alumno[0], alumno

    # --------------------------------------------------
    # Seleccionar curso
    # --------------------------------------------------
    def __seleccionar_curso(self):
        conexion = conectar()
        if conexion is None:
            return None

        cursor = conexion.cursor()
        cursor.execute("SELECT curso, nivel FROM cursos ORDER BY nivel")
        cursos = cursor.fetchall()
        cursor.close()
        conexion.close()

        if len(cursos) == 0:
            print("  No hay cursos registrados.")
            return None

        print("\n{:<20} {:<20}".format("CURSO", "NIVEL"))
        print("-" * 40)
        for curso in cursos:
            print("{:<20} {:<20}".format(curso[0], curso[1]))

        curso_elegido = input("\n  Introduzca el curso: ").strip()
        cursos_validos = [c[0] for c in cursos]
        if curso_elegido not in cursos_validos:
            print("  Curso no valido.")
            return None

        return curso_elegido

    # --------------------------------------------------
    # Asignar libros a un alumno
    # --------------------------------------------------
    def __asignar_libros(self):
        nie, alumno = self.__buscar_alumno()
        if nie is None:
            return

        curso = self.__seleccionar_curso()
        if curso is None:
            return

        conexion = conectar()
        if conexion is None:
            return

        cursor = conexion.cursor()
        cursor.execute(
            "SELECT isbn, titulo, autor FROM libros WHERE id_curso = %s ORDER BY titulo",
            (curso,)
        )
        libros = cursor.fetchall()

        if len(libros) == 0:
            print(f"\n  No hay libros registrados para el curso {curso}.")
            cursor.close()
            conexion.close()
            return

        print(f"\n  Libros disponibles para {curso}:")
        print("\n{:<20} {:<35} {:<20}".format("ISBN", "TITULO", "AUTOR"))
        print("-" * 75)
        for libro in libros:
            print("{:<20} {:<35} {:<20}".format(libro[0], libro[1][:33], libro[2][:18]))

        print("\n  Introduzca el ISBN del libro a asignar.")
        print("  Escriba 'fin' para terminar.")

        while True:
            isbn = input("\n  ISBN: ").strip()
            if isbn.lower() == "fin":
                break

            isbn_validos = [l[0] for l in libros]
            if isbn not in isbn_validos:
                print("  ISBN no valido. Prueba de nuevo.")
                continue

            # Comprobar si el alumno ya tiene ese libro en ese curso con estado P
            cursor.execute(
                "SELECT isbn FROM alumnoscursoslibros WHERE nie = %s AND curso = %s AND isbn = %s AND estado = 'P'",
                (nie, curso, isbn)
            )
            if cursor.fetchone() is not None:
                print("  Este alumno ya tiene ese libro en prestamo activo.")
                continue

            # Comprobar si quedan ejemplares disponibles
            cursor.execute(
                "SELECT numero_ejemplares FROM libros WHERE isbn = %s",
                (isbn,)
            )
            numero_ejemplares = cursor.fetchone()[0]

            cursor.execute(
                "SELECT COUNT(*) FROM alumnoscursoslibros WHERE isbn = %s AND estado = 'P'",
                (isbn,)
            )
            prestamos_activos = cursor.fetchone()[0]

            if prestamos_activos >= numero_ejemplares:
                print(f"  No hay ejemplares disponibles. Todos los ejemplares ({numero_ejemplares}) estan prestados.")
                continue

            try:
                cursor.execute(
                    "INSERT INTO alumnoscursoslibros (nie, curso, isbn, fecha_entrega, estado) VALUES (%s, %s, %s, %s, %s)",
                    (nie, curso, isbn, date.today(), "P")
                )
                conexion.commit()
                print("  Libro asignado correctamente.")
            except Exception as error:
                print(f"  Error al asignar el libro: {error}")

        cursor.close()
        conexion.close()

    # --------------------------------------------------
    # Registrar devolucion de un libro
    # --------------------------------------------------
    def __registrar_devolucion(self):
        nie, alumno = self.__buscar_alumno()
        if nie is None:
            return

        conexion = conectar()
        if conexion is None:
            return

        cursor = conexion.cursor()
        cursor.execute(
            """SELECT acl.isbn, l.titulo, acl.curso, acl.fecha_entrega
               FROM alumnoscursoslibros acl
               JOIN libros l ON acl.isbn = l.isbn
               WHERE acl.nie = %s AND acl.estado = 'P'
               ORDER BY acl.curso, l.titulo""",
            (nie,)
        )
        prestamos = cursor.fetchall()

        if len(prestamos) == 0:
            print("\n  Este alumno no tiene libros en prestamo activo.")
            cursor.close()
            conexion.close()
            return

        print("\n  Libros en prestamo:")
        print("\n{:<20} {:<35} {:<12} {:<12}".format("ISBN", "TITULO", "CURSO", "F.ENTREGA"))
        print("-" * 79)
        for prestamo in prestamos:
            print("{:<20} {:<35} {:<12} {:<12}".format(
                prestamo[0], prestamo[1][:33], prestamo[2], str(prestamo[3])))

        isbn = input("\n  Introduzca el ISBN del libro devuelto: ").strip()
        isbn_validos = [p[0] for p in prestamos]
        if isbn not in isbn_validos:
            print("  ISBN no valido o ese libro no esta en prestamo.")
            cursor.close()
            conexion.close()
            return

        try:
            cursor.execute(
                """UPDATE alumnoscursoslibros
                   SET estado = 'D', fecha_devolucion = %s
                   WHERE nie = %s AND isbn = %s AND estado = 'P'""",
                (date.today(), nie, isbn)
            )
            conexion.commit()
            print("  Devolucion registrada correctamente.")
        except Exception as error:
            print(f"  Error al registrar la devolucion: {error}")

        cursor.close()
        conexion.close()

    # --------------------------------------------------
    # Cerrar prestamo
    # --------------------------------------------------
    def __cerrar_prestamo(self):
        nie, alumno = self.__buscar_alumno()
        if nie is None:
            return

        conexion = conectar()
        if conexion is None:
            return

        cursor = conexion.cursor()
        cursor.execute(
            "SELECT COUNT(*) FROM alumnoscursoslibros WHERE nie = %s AND estado = 'P'",
            (nie,)
        )
        pendientes = cursor.fetchone()[0]

        if pendientes > 0:
            print(f"\n  No se puede cerrar el prestamo.")
            print(f"  El alumno todavia tiene {pendientes} libro/s sin devolver.")
            cursor.close()
            conexion.close()
            return

        cursor.execute(
            "SELECT COUNT(*) FROM alumnoscursoslibros WHERE nie = %s AND estado = 'D'",
            (nie,)
        )
        devueltos = cursor.fetchone()[0]

        if devueltos == 0:
            print("\n  Este alumno no tiene ningun prestamo registrado.")
            cursor.close()
            conexion.close()
            return

        print(f"\n  Todos los libros han sido devueltos ({devueltos} libro/s).")
        print("  El prestamo puede cerrarse correctamente.")
        cursor.close()
        conexion.close()

    # --------------------------------------------------
    # Run
    # --------------------------------------------------
    def run(self):
        opcion = 0
        while opcion != ULTIMA_OPCION:
            self.__crear_interfaz()
            opcion = int(input("  Elige una opcion: "))
            if opcion == 1:
                self.__asignar_libros()
            elif opcion == 2:
                self.__registrar_devolucion()
            elif opcion == 3:
                self.__cerrar_prestamo()
            elif opcion == ULTIMA_OPCION:
                print("Volviendo al menu principal...")
            else:
                print("\nOpcion no valida. Prueba de nuevo.")