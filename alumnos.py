from conexion import conectar


ULTIMA_OPCION = 5


class GestionAlumnos:

    def __crear_interfaz(self):
        print("=" * 45)
        print("  GESTION DE ALUMNOS")
        print("=" * 45)
        print("  1. Listar todos los alumnos")
        print("  2. Buscar alumno por NIE")
        print("  3. Crear nuevo alumno")
        print("  4. Modificar alumno")
        print("  5. Volver al menu principal")
        print("=" * 45)

    def __listar_alumnos(self):
        conexion = conectar()
        if conexion is None:
            return

        cursor = conexion.cursor()
        cursor.execute("SELECT nie, nombre, apellidos, tramo, bilingue FROM alumnos ORDER BY apellidos")
        alumnos = cursor.fetchall()

        if len(alumnos) == 0:
            print("\nNo hay alumnos registrados.")
        else:
            print("\n{:<12} {:<20} {:<30} {:<8} {:<8}".format(
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

    def __buscar_alumno(self):
        nie = input("\nIntroduzca el NIE del alumno: ").strip()

        conexion = conectar()
        if conexion is None:
            return

        cursor = conexion.cursor()
        cursor.execute(
            "SELECT nie, nombre, apellidos, tramo, bilingue FROM alumnos WHERE nie = %s",
            (nie,)
        )
        alumno = cursor.fetchone()

        if alumno is None:
            print("No se ha encontrado ningun alumno con ese NIE.")
        else:
            nie, nombre, apellidos, tramo, bilingue = alumno
            bilingue_texto = "Si" if bilingue == 0 else "No"
            tramo_texto = tramo if tramo != "0" else "Ninguno"
            print("\n--- Datos del alumno ---")
            print(f"  NIE:      {nie}")
            print(f"  Nombre:   {nombre}")
            print(f"  Apellidos:{apellidos}")
            print(f"  Tramo:    {tramo_texto}")
            print(f"  Bilingue: {bilingue_texto}")

        cursor.close()
        conexion.close()

    def __crear_alumno(self):
        print("\n--- Introducir datos del nuevo alumno ---")
        nie = input("  NIE: ").strip()
        nombre = input("  Nombre: ").strip()
        apellidos = input("  Apellidos: ").strip()

        print("  Tramo: 0 = Ninguno, I = Tramo I, II = Tramo II")
        tramo = input("  Tramo: ").strip()
        if tramo not in ["0", "I", "II"]:
            print("Error: tramo no valido. Debe ser 0, I o II.")
            return

        print("  Bilingue: 0 = Si, 1 = No")
        bilingue_input = input("  Bilingue: ").strip()
        if bilingue_input not in ["0", "1"]:
            print("Error: valor no valido. Debe ser 0 o 1.")
            return
        bilingue = int(bilingue_input)

        conexion = conectar()
        if conexion is None:
            return

        cursor = conexion.cursor()
        try:
            cursor.execute(
                "INSERT INTO alumnos (nie, nombre, apellidos, tramo, bilingue) VALUES (%s, %s, %s, %s, %s)",
                (nie, nombre, apellidos, tramo, bilingue)
            )
            conexion.commit()
            print("Alumno registrado correctamente.")
        except Exception as error:
            print(f"Error al registrar el alumno: {error}")

        cursor.close()
        conexion.close()

    def __modificar_alumno(self):
        nie = input("\nIntroduzca el NIE del alumno a modificar: ").strip()

        conexion = conectar()
        if conexion is None:
            return

        cursor = conexion.cursor()
        cursor.execute(
            "SELECT nie, nombre, apellidos, tramo, bilingue FROM alumnos WHERE nie = %s",
            (nie,)
        )
        alumno = cursor.fetchone()

        if alumno is None:
            print("No se ha encontrado ningun alumno con ese NIE.")
            cursor.close()
            conexion.close()
            return

        nie, nombre, apellidos, tramo, bilingue = alumno
        print("\nDeje el campo en blanco para no modificarlo.")

        nuevo_nombre = input(f"  Nombre [{nombre}]: ").strip()
        nuevos_apellidos = input(f"  Apellidos [{apellidos}]: ").strip()

        print("  Tramo: 0 = Ninguno, I = Tramo I, II = Tramo II")
        nuevo_tramo = input(f"  Tramo [{tramo}]: ").strip()

        print("  Bilingue: 0 = Si, 1 = No")
        nuevo_bilingue = input(f"  Bilingue [{bilingue}]: ").strip()

        # Si el campo se deja en blanco se mantiene el valor anterior
        if nuevo_nombre == "":
            nuevo_nombre = nombre
        if nuevos_apellidos == "":
            nuevos_apellidos = apellidos
        if nuevo_tramo == "":
            nuevo_tramo = tramo
        elif nuevo_tramo not in ["0", "I", "II"]:
            print("Error: tramo no valido. Debe ser 0, I o II.")
            cursor.close()
            conexion.close()
            return
        if nuevo_bilingue == "":
            nuevo_bilingue = bilingue
        elif nuevo_bilingue not in ["0", "1"]:
            print("Error: valor no valido. Debe ser 0 o 1.")
            cursor.close()
            conexion.close()
            return
        else:
            nuevo_bilingue = int(nuevo_bilingue)

        try:
            cursor.execute(
                "UPDATE alumnos SET nombre = %s, apellidos = %s, tramo = %s, bilingue = %s WHERE nie = %s",
                (nuevo_nombre, nuevos_apellidos, nuevo_tramo, nuevo_bilingue, nie)
            )
            conexion.commit()
            print("Datos del alumno actualizados correctamente.")
        except Exception as error:
            print(f"Error al modificar el alumno: {error}")

        cursor.close()
        conexion.close()

    def run(self):
        opcion = 0
        while opcion != ULTIMA_OPCION:
            self.__crear_interfaz()
            opcion = int(input("  Elige una opcion: "))
            if opcion == 1:
                self.__listar_alumnos()
            elif opcion == 2:
                self.__buscar_alumno()
            elif opcion == 3:
                self.__crear_alumno()
            elif opcion == 4:
                self.__modificar_alumno()
            elif opcion == ULTIMA_OPCION:
                print("Volviendo al menu principal...")
            else:
                print("\nOpcion no valida. Prueba de nuevo.")