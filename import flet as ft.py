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
import flet as ft
from datetime import datetime

# Función para calcular la edad
def calcular_edad(fecha_nacimiento):
    hoy = datetime.today()
    diferencia = hoy - fecha_nacimiento
    edad = diferencia.days // 365  # Aproximadamente el número de años
    return edad

# Función para abrir la gestión de empleados
import flet as ft
from datetime import datetime

# Función para calcular la edad basada en la fecha de nacimiento
def calcular_edad(fecha_nacimiento):
    today = datetime.today()
    edad = today.year - fecha_nacimiento.year - ((today.month, today.day) < (fecha_nacimiento.month, fecha_nacimiento.day))
    return str(edad)

# Función para generar un código de empleado automático (simulado aquí)
def generar_codigo_empleado():
    return "EMP" + str(datetime.now().strftime("%Y%m%d%H%M%S"))

# Función para manejar el guardado del empleado
def guardar_empleado(page, inputs):
    # Aquí puedes agregar la lógica para guardar los datos del empleado
    print("Empleado Guardado:", {key: value.value for key, value in inputs.items()})

# Función para mostrar el menú principal (puedes definirla según tu necesidad)
def mostrar_menu_principal(page):
    print("Regresando al menú principal...")
    page.update()

# Función para mostrar la pantalla de gestión de empleados
def mostrar_gestion_empleados(page):
    # Crear los controles (campos de entrada)
    inputs = {}

    # Labels de "Datos del Trabajador"
    labels_trabajador = [
        "ID-Trabajador", "Documento de Identidad", "Nacionalidad", "1° Apellido", "2° Apellido",
        "1° Nombre", "2° Nombre", "Fecha de Nacimiento", "Edad", "Sexo", "Estado Civil", "Dirección", "Teléfono"
    ]
    
    # Labels de "Datos Laborales"
    labels_laborales = [
        "Profesión", "Cargo", "Departamento", "Nomina", "División", "Banco", "Cuenta",
        "Fecha de Ingreso", "Centro de Costo", "Estatus", "Tipo de Pago"
    ]
    
    # Unir todos los labels en una sola lista
    labels = labels_trabajador + labels_laborales

    # Crear los campos de texto para cada label
    for label in labels:
        inputs[label] = ft.TextField(label=label, width=180, height=40)

    # Código de empleado generado automáticamente
    inputs["ID-Trabajador"].value = generar_codigo_empleado()
    inputs["ID-Trabajador"].disabled = True

    # Campo de texto para la fecha de nacimiento (usuario la escribe manualmente)
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
                ft.Text("Datos del Trabajador", size=18, weight=ft.FontWeight.BOLD),
                *filas[:len(labels_trabajador)],  # Solo mostrar los primeros campos para "Datos del Trabajador"
                ft.Text("Datos Laborales", size=18, weight=ft.FontWeight.BOLD),
                *filas[len(labels_trabajador):],  # Mostrar los campos para "Datos Laborales"
                ft.Row([guardar_button, regresar_button], alignment=ft.MainAxisAlignment.CENTER)
            ],
            scroll=ft.ScrollMode.ALWAYS,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )

    page.update()

# Función principal que ejecuta la aplicación
def main(page):
    page.window_width = 800
    page.window_height = 600
    page.window_resizable = False
    mostrar_gestion_empleados(page)

# Ejecuta la aplicación de Flet
ft.app(target=main)







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

