import flet as ft
import sqlite3
import hashlib
import os
import pandas as pd
import sqlite3
import flet as ft

# Función para encriptar la clave con SHA-256
def encriptar_clave(clave):
    return hashlib.sha256(clave.encode()).hexdigest()

# Función para inicializar la base de datos y crear las tablas necesarias
def inicializar_bd():
    conn = sqlite3.connect("nomina.db")
    cursor = conn.cursor()

    # Crear tabla de usuarios
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE NOT NULL,
            clave TEXT NOT NULL
        )
    """)

    # Crear tabla de empleados
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS empleados (
            codigo TEXT PRIMARY KEY,
            nombre1 TEXT, nombre2 TEXT,
            apellido1 TEXT, apellido2 TEXT,
            cedula TEXT UNIQUE, correo TEXT,
            direccion TEXT, pais TEXT, ciudad TEXT, estado TEXT,
            fecha_nacimiento TEXT, edad INTEGER,
            grado_instruccion TEXT, carga_familiar INTEGER
        )
    """)

    # Verificar si el usuario "admin" ya existe
    cursor.execute("SELECT * FROM usuarios WHERE usuario = 'admin'")
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO usuarios (usuario, clave) VALUES (?, ?)", 
                       ("admin", encriptar_clave("1234")))
        conn.commit()

    conn.close()

# Función para verificar las credenciales del usuario
def verificar_credenciales(page, usuario, clave):
    if not usuario or not clave:
        page.snack_bar = ft.SnackBar(content=ft.Text("Debe ingresar usuario y clave"), open=True)
        page.update()
        return

    try:
        conn = sqlite3.connect("nomina.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM usuarios WHERE usuario = ? AND clave = ?", 
                       (usuario, encriptar_clave(clave)))
        resultado = cursor.fetchone()
        conn.close()

        if resultado:
            page.controls.clear()
            mostrar_menu_principal(page)  
        else:
            page.snack_bar = ft.SnackBar(content=ft.Text("Usuario o clave incorrectos"), open=True)
            page.update()
    except sqlite3.Error as e:
        page.snack_bar = ft.SnackBar(content=ft.Text(f"Error en la base de datos: {e}"), open=True)
        page.update()

# Función para mostrar la pantalla de inicio de sesión
def mostrar_login(page):
    page.bgcolor = "#f4f4f4"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    usuario = ft.TextField(label="Usuario", width=300, bgcolor="white", border_color="#2196F3")
    clave = ft.TextField(label="Clave", password=True, width=300, bgcolor="white", border_color="#2196F3")

    boton_login = ft.ElevatedButton(
        text="Iniciar Sesión",
        on_click=lambda e: verificar_credenciales(page, usuario.value, clave.value),
        bgcolor="#2196F3", color="white"
    )

    card = ft.Container(
        content=ft.Column(
            [usuario, clave, boton_login],
            spacing=10, alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),
        padding=20, border_radius=10, bgcolor="white",
        shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.GREY_500),
    )

    page.controls.clear()
    page.add(ft.Row([card], alignment=ft.MainAxisAlignment.CENTER))
    page.update()

# Función para mostrar el menú principal
def mostrar_menu_principal(page):
    page.controls.clear()
    page.add(
        ft.Column(
            [
                ft.Text("Menú Principal", size=24, weight=ft.FontWeight.BOLD),
                ft.Divider(),  # Línea divisoria para organización visual
                
                ft.ElevatedButton("Panel de Control", on_click=lambda e: abrir_panel_control(page)),
                ft.ElevatedButton("Gestión de Empleados", on_click=lambda e: abrir_gestion_empleados(page)),
                ft.ElevatedButton("Cálculo de Nómina", on_click=lambda e: abrir_calculo_nomina(page)),
                ft.ElevatedButton("Reportes", on_click=lambda e: abrir_reportes(page)),
                ft.ElevatedButton("Configuración", on_click=lambda e: abrir_configuracion(page)),

                ft.Divider(),  # Separador antes de cerrar sesión
                ft.ElevatedButton("Cerrar Sesión", on_click=lambda e: mostrar_login(page), bgcolor="red", color="white"),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )
    page.update()


# Función para generar un código único para empleados
def generar_codigo_empleado():
    conn = sqlite3.connect("nomina.db")
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM empleados")
    count = cursor.fetchone()[0] + 1
    conn.close()
    return f"E{count:05d}"

# Función para guardar un empleado en la base de datos
# Función para guardar un empleado en la base de datos
def guardar_empleado(page, inputs):
    # Renombramos las claves del diccionario para que coincidan con los nombres correctos de las columnas en SQLite
    datos = {
        "codigo": inputs["Código"].value,
        "nombre1": inputs["1° Nombre"].value,
        "nombre2": inputs["2° Nombre"].value,
        "apellido1": inputs["1° Apellido"].value,
        "apellido2": inputs["2° Apellido"].value,
        "cedula": inputs["Cédula"].value,
        "correo": inputs["Correo"].value,
        "direccion": inputs["Dirección"].value,
        "pais": inputs["País"].value,
        "ciudad": inputs["Ciudad"].value,
        "estado": inputs["Estado"].value,
        "fecha_nacimiento": inputs["Fecha de Nacimiento"].value,
        "edad": inputs["Edad"].value,
        "grado_instruccion": inputs["Grado de Instrucción"].value,
        "carga_familiar": inputs["Carga Familiar"].value,
    }

    try:
        conn = sqlite3.connect("nomina.db")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO empleados (codigo, nombre1, nombre2, apellido1, apellido2, cedula, correo, direccion,
                                   pais, ciudad, estado, fecha_nacimiento, edad, grado_instruccion, carga_familiar)
            VALUES (:codigo, :nombre1, :nombre2, :apellido1, :apellido2, :cedula, :correo, :direccion,
                    :pais, :ciudad, :estado, :fecha_nacimiento, :edad, :grado_instruccion, :carga_familiar)
        """, datos)
        conn.commit()
        conn.close()

        page.snack_bar = ft.SnackBar(content=ft.Text("Empleado guardado con éxito"), open=True)
        page.update()
        abrir_gestion_empleados(page)  # Recargar la página después de guardar

    except sqlite3.Error as e:
        page.snack_bar = ft.SnackBar(content=ft.Text(f"Error en la base de datos: {e}"), open=True)
        page.update()


# Función para mostrar la gestión de empleados
# Crear los controles (campos de entrada)
    inputs = {}
    labels = ["Código", "1° Nombre", "2° Nombre", "1° Apellido", "2° Apellido", "Cédula", "Correo",
              "Dirección", "País", "Ciudad", "Estado", "Fecha de Nacimiento", "Edad", "Grado de Instrucción", "Carga Familiar"]

    for label in labels:
        inputs[label] = ft.TextField(label=label, width=180, height=40)

    # Código de empleado generado automáticamente
    inputs["Código"].value = generar_codigo_empleado()
    inputs["Código"].disabled = True

    # Crear el campo de texto para la fecha de nacimiento (usuario la escribe manualmente)
    fecha_nacimiento = ft.TextField(label="Fecha de Nacimiento (YYYY-MM-DD)", width=180, height=40)
    inputs["Fecha de Nacimiento"] = fecha_nacimiento

    # Campo de edad, que se calculará automáticamente
    edad = ft.TextField(label="Edad", width=180, height=40, disabled=True)
    inputs["Edad"] = edad

    # Función para actualizar la edad cuando se ingrese una fecha válida
    def actualizar_edad(e):
        try:
            # Intentar convertir la fecha ingresada en formato YYYY-MM-DD
            fecha_valida = datetime.strptime(fecha_nacimiento.value, "%Y-%m-%d")
            edad.value = calcular_edad(fecha_valida)
        except ValueError:
            edad.value = "Fecha inválida"
        page.update()

    # Establecer el evento para el cambio de la fecha
    fecha_nacimiento.on_change = actualizar_edad

    # Crear botones
    guardar_button = ft.ElevatedButton("Guardar", on_click=lambda e: guardar_empleado(page, inputs))
    regresar_button = ft.ElevatedButton("Regresar", on_click=lambda e: mostrar_menu_principal(page))

    # Agrupar los campos en filas
    campos_por_fila = 3
    filas = [
        ft.Row([inputs[label] for label in labels[i:i + campos_por_fila]], spacing=5,
               alignment=ft.MainAxisAlignment.CENTER)
        for i in range(0, len(labels), campos_por_fila)
    ]

    # Agregar los controles a la página
    page.add(
        ft.Column(
            [
                ft.Text("Gestión de Empleados", size=20, weight=ft.FontWeight.BOLD),
                *filas,
                ft.Row([guardar_button, regresar_button], alignment=ft.MainAxisAlignment.CENTER)
            ],
            scroll=ft.ScrollMode.ALWAYS,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )

    page.update()

# Función para abrir la sección "Panel de Control"
def abrir_panel_control(page):
    page.controls.clear()
    page.add(
        ft.Column(
            [
                ft.Text("Panel de Control", size=20, weight=ft.FontWeight.BOLD),
                ft.ElevatedButton("Volver al Menú", on_click=lambda e: mostrar_menu_principal(page))
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )
    page.update()

# Función para abrir la sección "Cálculo de Nómina"
def abrir_calculo_nomina(page):
    page.controls.clear()
    page.add(
        ft.Column(
            [
                ft.Text("Cálculo de Nómina", size=20, weight=ft.FontWeight.BOLD),
                ft.ElevatedButton("Volver al Menú", on_click=lambda e: mostrar_menu_principal(page))
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )
    page.update()

# Función para abrir la sección "Reportes"
def abrir_reportes(page):
    page.controls.clear()
    page.add(
        ft.Column(
            [
                ft.Text("Reportes", size=20, weight=ft.FontWeight.BOLD),
                ft.ElevatedButton("Volver al Menú", on_click=lambda e: mostrar_menu_principal(page))
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )
    page.update()

# Función para abrir la sección "Configuración"
def abrir_configuracion(page):
    page.controls.clear()
    page.add(
        ft.Column(
            [
                ft.Text("Configuración", size=20, weight=ft.FontWeight.BOLD),
                ft.ElevatedButton("Volver al Menú", on_click=lambda e: mostrar_menu_principal(page))
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )
    page.update()
# Función para generar y descargar el reporte en Excel
def generar_reporte_empleados(page):
    try:
        conn = sqlite3.connect("nomina.db")
        query = "SELECT * FROM empleados"
        df = pd.read_sql_query(query, conn)  # Cargar datos en un DataFrame
        conn.close()

        if df.empty:
            page.snack_bar = ft.SnackBar(content=ft.Text("No hay empleados registrados"), open=True)
            page.update()
            return
        
        file_path = "empleados_reporte.xlsx"
        df.to_excel(file_path, index=False)  # Guardar en Excel

        # Crear un enlace de descarga
        page.add(
            ft.Text("Reporte generado con éxito:", size=16, weight=ft.FontWeight.BOLD),
            ft.TextButton("Descargar Reporte", on_click=lambda e: page.launch_url(file_path))
        )
        page.update()

    except Exception as e:
        page.snack_bar = ft.SnackBar(content=ft.Text(f"Error generando reporte: {e}"), open=True)
        page.update()

# Función para abrir la sección "Reportes"
def abrir_reportes(page):
    page.controls.clear()
    page.add(
        ft.Column(
            [
                ft.Text("Reportes", size=20, weight=ft.FontWeight.BOLD),
                ft.ElevatedButton("Generar Reporte de Empleados", on_click=lambda e: generar_reporte_empleados(page)),
                ft.ElevatedButton("Volver al Menú", on_click=lambda e: mostrar_menu_principal(page))
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )
    page.update()
# Función para mostrar el menú principal
def mostrar_menu_principal(page):
    page.controls.clear()
    page.add(
        ft.Column(
            [
                ft.Text("Menú Principal", size=20, weight=ft.FontWeight.BOLD),
                ft.ElevatedButton("Panel de Control", on_click=lambda e: abrir_panel_control(page)),
                ft.ElevatedButton("Gestión de Empleados", on_click=lambda e: abrir_gestion_empleados(page)),
                ft.ElevatedButton("Cálculo de Nómina", on_click=lambda e: abrir_calculo_nomina(page)),
                ft.ElevatedButton("Reportes", on_click=lambda e: abrir_reportes(page)),
                ft.ElevatedButton("Configuración", on_click=lambda e: abrir_configuracion(page)),
                ft.ElevatedButton("Cerrar Sesión", on_click=lambda e: mostrar_login(page))
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )
    page.update()

def actualizar_github(mensaje):
    try:
        os.system("git add .")
        os.system(f'git commit -m "{mensaje}"')
        os.system("git push origin main")
        print("Código actualizado en GitHub correctamente.")
    except Exception as e:
        print(f"Error al actualizar en GitHub: {e}")
# Función principal que inicia la aplicación
def main(page: ft.Page):
    inicializar_bd()  # Crear la base de datos y tablas si no existen
    actualizar_github("Inicialización de la base de datos")  # Agregar aquí la actualización automática
    page.title = "Sistema de Nómina"
    mostrar_login(page)  # Muestra la pantalla de inicio de sesión

ft.app(target=main)




