import flet as ft
import sqlite3
import hashlib
import pandas as pd

# Función para encriptar la clave con SHA-256
def encriptar_clave(clave):
    return hashlib.sha256(clave.encode()).hexdigest()

# Función para generar un código único para cada empleado
def generar_codigo_empleado():
    conn = sqlite3.connect("nomina.db")
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM empleados")
    count = cursor.fetchone()[0] + 1
    conn.close()
    return f"E{count:05d}"

# Función para guardar un trabajador en la base de datos
def guardar_trabajador(inputs):
    conn = sqlite3.connect("nomina.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS empleados (
            codigo TEXT PRIMARY KEY,
            nombre1 TEXT,
            nombre2 TEXT,
            apellido1 TEXT,
            apellido2 TEXT,
            cedula TEXT,
            correo TEXT,
            direccion TEXT,
            pais TEXT,
            ciudad TEXT,
            estado TEXT,
            fecha_nacimiento TEXT,
            edad TEXT,
            grado_instruccion TEXT,
            carga_familiar TEXT,
            telefono TEXT  -- Se añadió esta columna para completar 16 campos
        )
    """)
    
    valores = [inputs[label].value for label in inputs]  # Se aseguran 16 valores
    cursor.execute("""
        INSERT INTO empleados VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, valores)
    
    conn.commit()
    conn.close()

# Función para generar un reporte en Excel
def generar_reporte():
    conn = sqlite3.connect("nomina.db")
    df = pd.read_sql_query("SELECT * FROM empleados", conn)
    df.to_excel("reporte_empleados.xlsx", index=False)
    conn.close()

# Función para verificar credenciales de inicio de sesión
def verificar_credenciales(page, usuario, clave):
    conn = sqlite3.connect("nomina.db")
    cursor = conn.cursor()
    
    cursor.execute("CREATE TABLE IF NOT EXISTS usuarios (usuario TEXT PRIMARY KEY, clave TEXT)")
    
    cursor.execute("SELECT clave FROM usuarios WHERE usuario = ?", (usuario,))
    resultado = cursor.fetchone()
    
    conn.close()
    
    if resultado and resultado[0] == encriptar_clave(clave):
        page.snack_bar = ft.SnackBar(ft.Text("Inicio de sesión exitoso"), open=True)
        abrir_gestion_empleados(page)
    else:
        page.snack_bar = ft.SnackBar(ft.Text("Usuario o clave incorrectos"), open=True)
    
    page.update()

# Función para mostrar la pantalla de inicio de sesión con un diseño mejorado
def mostrar_login(page):
    page.bgcolor = "#f4f4f4"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    usuario = ft.TextField(label="Usuario", width=300, bgcolor="#ffffff", border_color="#2196F3")
    clave = ft.TextField(label="Clave", password=True, width=300, bgcolor="#ffffff", border_color="#2196F3")

    boton_login = ft.ElevatedButton(
        text="Iniciar Sesión",
        on_click=lambda e: verificar_credenciales(page, usuario.value, clave.value),
        bgcolor="#2196F3",
        color="white"
    )

    card = ft.Container(
        content=ft.Column(
            [usuario, clave, boton_login],
            spacing=10,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),
        padding=20,
        border_radius=10,
        bgcolor="white",
        shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.GREY_500),
    )

    page.controls.clear()
    page.add(ft.Row([card], alignment=ft.MainAxisAlignment.CENTER))
    page.update()

# Función para mostrar la gestión de empleados
def abrir_gestion_empleados(page):
    page.controls.clear()
    inputs = {}
    labels = ["Código", "1° Nombre", "2° Nombre", "1° Apellido", "2° Apellido", "Cédula", "Correo", "Dirección", "País", "Ciudad", "Estado", "Fecha de Nacimiento", "Edad", "Grado de Instrucción", "Carga Familiar", "Teléfono"]
    
    for label in labels:
        inputs[label] = ft.TextField(label=label, width=180, height=40)
    
    inputs["Código"].value = generar_codigo_empleado()
    inputs["Código"].disabled = True
    
    guardar_button = ft.ElevatedButton("Guardar", on_click=lambda e: [guardar_trabajador(inputs), page.snack_bar.open(True)])
    reporte_button = ft.ElevatedButton("Generar Reporte", on_click=lambda e: generar_reporte())
    regresar_button = ft.ElevatedButton("Regresar", on_click=lambda e: mostrar_login(page))
    
    campos_por_fila = 3
    filas = [
        ft.Row([inputs[label] for label in labels[i:i+campos_por_fila]], spacing=5, alignment=ft.MainAxisAlignment.CENTER)
        for i in range(0, len(labels), campos_por_fila)
    ]
    
    page.add(
        ft.Column(
            [
                ft.Text("Gestión de Empleados", size=20, weight=ft.FontWeight.BOLD),
                *filas,
                ft.Row([guardar_button, reporte_button, regresar_button], alignment=ft.MainAxisAlignment.CENTER)
            ],
            scroll=ft.ScrollMode.ALWAYS,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )
    page.update()

# Función principal que inicia la aplicación
def main(page: ft.Page):
    page.title = "Sistema de Nómina"
    mostrar_login(page)  # Muestra la pantalla de inicio de sesión al iniciar

ft.app(target=main)