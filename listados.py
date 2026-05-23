from conexion import conectar


ULTIMA_OPCION = 4


class GestionListados:

    # --------------------------------------------------
    # Menu principal
    # --------------------------------------------------
    def __crear_interfaz(self):
        print("=" * 45)
        print("  LISTADOS Y BUSQUEDAS")
        print("=" * 45)
        print("  1. Listado de alumnos")
        print("  2. Listado de libros")
        print("  3. Listado de prestamos")
        print("  4. Volver al menu principal")
        print("=" * 45)

    # --------------------------------------------------
    # Alumnos
    # --------------------------------------------------
    def __menu_alumnos(self):
        print("=" * 45)
        print("  LISTADO DE ALUMNOS")
        print("=" * 45)
        print("  1. Todos los alumnos")
        print("  2. Buscar por nombre o apellidos")
        print("  3. Volver")
        print("=" * 45)
        opcion = int(input("  Elige una opcion: "))
        if opcion == 1:
            self.__todos_alumnos()
        elif opcion == 2:
            self.__buscar_alumnos()
        elif opcion == 3:
            pass
        else:
            print("\nOpcion no valida. Prueba de nuevo.")

    def __todos_alumnos(self):
        conexion = conectar()
        if conexion is None:
            return

        cursor = conexion.cursor()
        cursor.execute(
            "SELECT nie, nombre, apellidos, tramo, bilingue FROM alumnos ORDER BY apellidos"
        )
        alumnos = cursor.fetchall()

        if len(alumnos) == 0:
            print("\n  No hay alumnos registrados.")
        else:
            print(f"\n  Total de alumnos: {len(alumnos)}\n")
            print("{:<12} {:<20} {:<30} {:<8} {:<8}".format(
                "NIE", "NOMBRE", "APELLIDOS", "TRAMO", "BILINGUE"))
            print("-" * 80)
            for alumno in alumnos:
                nie, nombre, apellidos, tramo, bilingue = alumno
                bilingue_texto = "Si" if bilingue == 0 else "No"
                tramo_texto = tramo if tramo != "0" else "Ninguno"
                print("{:<12} {:<20} {:<30} {:<8} {:<8}".format(
                    nie, nombre, apellidos, tramo_texto, bilingue_texto))

        cursor.close()
        conexion.close()

    def __buscar_alumnos(self):
        texto = input("\n  Introduzca nombre o apellidos a buscar: ").strip()

        conexion = conectar()
        if conexion is None:
            return

        cursor = conexion.cursor()
        cursor.execute(
            """SELECT nie, nombre, apellidos, tramo, bilingue FROM alumnos
               WHERE nombre LIKE %s OR apellidos LIKE %s
               ORDER BY apellidos""",
            (f"%{texto}%", f"%{texto}%")
        )
        alumnos = cursor.fetchall()

        if len(alumnos) == 0:
            print("  No se han encontrado alumnos con ese criterio.")
        else:
            print(f"\n  Resultados encontrados: {len(alumnos)}\n")
            print("{:<12} {:<20} {:<30} {:<8} {:<8}".format(
                "NIE", "NOMBRE", "APELLIDOS", "TRAMO", "BILINGUE"))
            print("-" * 80)
            for alumno in alumnos:
                nie, nombre, apellidos, tramo, bilingue = alumno
                bilingue_texto = "Si" if bilingue == 0 else "No"
                tramo_texto = tramo if tramo != "0" else "Ninguno"
                print("{:<12} {:<20} {:<30} {:<8} {:<8}".format(
                    nie, nombre, apellidos, tramo_texto, bilingue_texto))

        cursor.close()
        conexion.close()

    # --------------------------------------------------
    # Libros
    # --------------------------------------------------
    def __menu_libros(self):
        print("=" * 45)
        print("  LISTADO DE LIBROS")
        print("=" * 45)
        print("  1. Todos los libros")
        print("  2. Buscar por materia o curso")
        print("  3. Volver")
        print("=" * 45)
        opcion = int(input("  Elige una opcion: "))
        if opcion == 1:
            self.__todos_libros()
        elif opcion == 2:
            self.__buscar_libros()
        elif opcion == 3:
            pass
        else:
            print("\nOpcion no valida. Prueba de nuevo.")

    def __todos_libros(self):
        conexion = conectar()
        if conexion is None:
            return

        cursor = conexion.cursor()
        cursor.execute("""
            SELECT l.isbn, l.titulo, l.autor, l.numero_ejemplares, m.nombre, l.id_curso
            FROM libros l
            JOIN materias m ON l.id_materia = m.id
            ORDER BY l.id_curso, l.titulo
        """)
        libros = cursor.fetchall()

        if len(libros) == 0:
            print("\n  No hay libros registrados.")
        else:
            print(f"\n  Total de libros: {len(libros)}\n")
            print("{:<18} {:<30} {:<20} {:<6} {:<18} {:<10}".format(
                "ISBN", "TITULO", "AUTOR", "EJEM.", "MATERIA", "CURSO"))
            print("-" * 102)
            for libro in libros:
                print("{:<18} {:<30} {:<20} {:<6} {:<18} {:<10}".format(
                    libro[0], libro[1][:28], libro[2][:18], libro[3], libro[4][:16], libro[5]))

        cursor.close()
        conexion.close()

    def __buscar_libros(self):
        print("\n  Filtrar por:")
        print("  1. Materia")
        print("  2. Curso")
        opcion = input("\n  Elige una opcion: ").strip()

        conexion = conectar()
        if conexion is None:
            return

        cursor = conexion.cursor()

        if opcion == "1":
            texto = input("  Introduzca el nombre de la materia: ").strip()
            cursor.execute("""
                SELECT l.isbn, l.titulo, l.autor, l.numero_ejemplares, m.nombre, l.id_curso
                FROM libros l
                JOIN materias m ON l.id_materia = m.id
                WHERE m.nombre LIKE %s
                ORDER BY l.titulo
            """, (f"%{texto}%",))
        elif opcion == "2":
            texto = input("  Introduzca el curso: ").strip()
            cursor.execute("""
                SELECT l.isbn, l.titulo, l.autor, l.numero_ejemplares, m.nombre, l.id_curso
                FROM libros l
                JOIN materias m ON l.id_materia = m.id
                WHERE l.id_curso LIKE %s
                ORDER BY l.titulo
            """, (f"%{texto}%",))
        else:
            print("  Opcion no valida.")
            cursor.close()
            conexion.close()
            return

        libros = cursor.fetchall()

        if len(libros) == 0:
            print("  No se han encontrado libros con ese criterio.")
        else:
            print(f"\n  Resultados encontrados: {len(libros)}\n")
            print("{:<18} {:<30} {:<20} {:<6} {:<18} {:<10}".format(
                "ISBN", "TITULO", "AUTOR", "EJEM.", "MATERIA", "CURSO"))
            print("-" * 102)
            for libro in libros:
                print("{:<18} {:<30} {:<20} {:<6} {:<18} {:<10}".format(
                    libro[0], libro[1][:28], libro[2][:18], libro[3], libro[4][:16], libro[5]))

        cursor.close()
        conexion.close()

    # --------------------------------------------------
    # Prestamos
    # --------------------------------------------------
    def __menu_prestamos(self):
        print("=" * 45)
        print("  LISTADO DE PRESTAMOS")
        print("=" * 45)
        print("  1. Todos los prestamos")
        print("  2. Buscar por NIE de alumno")
        print("  3. Volver")
        print("=" * 45)
        opcion = int(input("  Elige una opcion: "))
        if opcion == 1:
            self.__todos_prestamos()
        elif opcion == 2:
            self.__buscar_prestamos_alumno()
        elif opcion == 3:
            pass
        else:
            print("\nOpcion no valida. Prueba de nuevo.")

    def __todos_prestamos(self):
        conexion = conectar()
        if conexion is None:
            return

        cursor = conexion.cursor()
        cursor.execute("""
            SELECT a.nie, a.nombre, a.apellidos, acl.isbn, l.titulo, acl.curso,
                   acl.fecha_entrega, acl.fecha_devolucion, acl.estado
            FROM alumnoscursoslibros acl
            JOIN alumnos a ON acl.nie = a.nie
            JOIN libros l ON acl.isbn = l.isbn
            ORDER BY a.apellidos, l.titulo
        """)
        prestamos = cursor.fetchall()

        if len(prestamos) == 0:
            print("\n  No hay prestamos registrados.")
        else:
            print(f"\n  Total de prestamos: {len(prestamos)}\n")
            print("{:<12} {:<20} {:<20} {:<18} {:<25} {:<10} {:<12} {:<12} {:<8}".format(
                "NIE", "NOMBRE", "APELLIDOS", "ISBN", "TITULO", "CURSO", "F.ENTREGA", "F.DEVOL.", "ESTADO"))
            print("-" * 137)
            for prestamo in prestamos:
                fecha_devolucion = str(prestamo[7]) if prestamo[7] else "Pendiente"
                estado_texto = "Activo" if prestamo[8] == "P" else "Devuelto"
                print("{:<12} {:<20} {:<20} {:<18} {:<25} {:<10} {:<12} {:<12} {:<8}".format(
                    prestamo[0], prestamo[1][:18], prestamo[2][:18],
                    prestamo[3], prestamo[4][:23], prestamo[5],
                    str(prestamo[6]), fecha_devolucion, estado_texto))

        cursor.close()
        conexion.close()

    def __buscar_prestamos_alumno(self):
        nie = input("\n  Introduzca el NIE del alumno: ").strip()

        conexion = conectar()
        if conexion is None:
            return

        cursor = conexion.cursor()
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

        print(f"\n  Alumno: {alumno[1]} {alumno[2]}")

        cursor.execute("""
            SELECT acl.isbn, l.titulo, acl.curso, acl.fecha_entrega, acl.fecha_devolucion, acl.estado
            FROM alumnoscursoslibros acl
            JOIN libros l ON acl.isbn = l.isbn
            WHERE acl.nie = %s
            ORDER BY acl.estado, l.titulo
        """, (nie,))
        prestamos = cursor.fetchall()

        if len(prestamos) == 0:
            print("  Este alumno no tiene prestamos registrados.")
        else:
            print(f"\n  Total de prestamos: {len(prestamos)}\n")
            print("{:<18} {:<30} {:<10} {:<12} {:<12} {:<8}".format(
                "ISBN", "TITULO", "CURSO", "F.ENTREGA", "F.DEVOL.", "ESTADO"))
            print("-" * 90)
            for prestamo in prestamos:
                fecha_devolucion = str(prestamo[4]) if prestamo[4] else "Pendiente"
                estado_texto = "Activo" if prestamo[5] == "P" else "Devuelto"
                print("{:<18} {:<30} {:<10} {:<12} {:<12} {:<8}".format(
                    prestamo[0], prestamo[1][:28], prestamo[2],
                    str(prestamo[3]), fecha_devolucion, estado_texto))

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
                self.__menu_alumnos()
            elif opcion == 2:
                self.__menu_libros()
            elif opcion == 3:
                self.__menu_prestamos()
            elif opcion == ULTIMA_OPCION:
                print("Volviendo al menu principal...")
            else:
                print("\nOpcion no valida. Prueba de nuevo.")