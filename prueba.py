import flet as ft
import sqlite3
import hashlib
import os
import pandas as pd
from datetime import datetime
import flet as ft
from main import mostrar_menu_principal

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
                ft.Divider(),
                ft.ElevatedButton("Panel de Control", on_click=lambda e: abrir_panel_control(page)),
                ft.ElevatedButton("Gestión de Empleados", on_click=lambda e: abrir_gestion_empleados(page)),
                ft.ElevatedButton("Cálculo de Nómina", on_click=lambda e: abrir_calculo_nomina(page)),
                ft.ElevatedButton("Reportes", on_click=lambda e: abrir_reportes(page)),
                ft.ElevatedButton("Configuración", on_click=lambda e: abrir_configuracion(page)),
                ft.Divider(),
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

# Definir la función calcular_edad
from datetime import datetime

def calcular_edad(fecha_nacimiento):
    hoy = datetime.today()
    edad = hoy.year - fecha_nacimiento.year
    if hoy.month < fecha_nacimiento.month or (hoy.month == fecha_nacimiento.month and hoy.day < fecha_nacimiento.day):
        edad -= 1
    return edad

# El resto del código permanece igual...

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
        "sexo": inputs["Sexo"].value,
        "estado_civil": inputs["Estado Civil"].value,
        "telefono": inputs["Teléfono"].value,
        # Nuevos campos laborales
        "profesion": inputs["Profesión"].value,
        "cargo": inputs["Cargo"].value,
        "departamento": inputs["Departamento"].value,
        "nomina": inputs["Nomina"].value,
        "division": inputs["División"].value,
        "banco": inputs["Banco"].value,
        "cuenta": inputs["Cuenta"].value,
        "fecha_ingreso": inputs["Fecha de Ingreso"].value,
        "centro_costo": inputs["Centro de Costo"].value,
        "estatus": inputs["Estatus"].value,
        "tipo_pago": inputs["Tipo de Pago"].value,
    }

    try:
        conn = sqlite3.connect("nomina.db")
        cursor = conn.cursor()
        cursor.execute(""" 
            INSERT INTO empleados (codigo, nombre1, nombre2, apellido1, apellido2, cedula, correo, direccion,
                                   pais, ciudad, estado, fecha_nacimiento, edad, grado_instruccion, carga_familiar,
                                   sexo, estado_civil, telefono, profesion, cargo, departamento, nomina, division,
                                   banco, cuenta, fecha_ingreso, centro_costo, estatus, tipo_pago)
            VALUES (:codigo, :nombre1, :nombre2, :apellido1, :apellido2, :cedula, :correo, :direccion,
                    :pais, :ciudad, :estado, :fecha_nacimiento, :edad, :grado_instruccion, :carga_familiar,
                    :sexo, :estado_civil, :telefono, :profesion, :cargo, :departamento, :nomina, :division,
                    :banco, :cuenta, :fecha_ingreso, :centro_costo, :estatus, :tipo_pago)
        """, datos)
        conn.commit()
        conn.close()

        page.snack_bar = ft.SnackBar(content=ft.Text("Empleado guardado con éxito"), open=True)
        page.update()  # Asegúrate de actualizar la página aquí
        abrir_gestion_empleados(page)  # Recargar la página después de guardar

    except sqlite3.Error as e:
        page.snack_bar = ft.SnackBar(content=ft.Text(f"Error en la base de datos: {e}"), open=True)
        page.update()

# Función para mostrar la gestión de empleados
import flet as ft
from datetime import datetime
import sqlite3

# Conectar a la base de datos
conn = sqlite3.connect("empleados.db")
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS empleados (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre1 TEXT,
                nombre2 TEXT,
                apellido1 TEXT,
                apellido2 TEXT,
                cedula TEXT,
                correo TEXT,
                direccion TEXT,
                fecha_nacimiento TEXT,
                edad INTEGER,
                sexo TEXT,
                estado_civil TEXT,
                cargo TEXT,
                departamento TEXT,
                fecha_ingreso TEXT,
                centro_costo TEXT,
                tipo_pago TEXT,
                estatus TEXT,
                banco TEXT,
                numero_cuenta TEXT
            )''')
conn.commit()

import flet as ft
from datetime import datetime
import sqlite3

import flet as ft
from datetime import datetime
import sqlite3
import pandas as pd
import subprocess


def abrir_gestion_empleados(page):
    page.controls.clear()
    
    def calcular_edad(fecha_nacimiento):
        hoy = datetime.today()
        return hoy.year - fecha_nacimiento.year - ((hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day))

    def actualizar_edad(e):
        try:
            fecha_valida = datetime.strptime(fecha_nacimiento.value, "%Y-%m-%d")
            edad.value = str(calcular_edad(fecha_valida))
        except ValueError:
            edad.value = "Fecha inválida"
        page.update()
    
    def guardar_empleado(e):
        conn = sqlite3.connect("empleados.db")
        c = conn.cursor()
        c.execute("INSERT INTO empleados (nombre1, nombre2, apellido1, apellido2, cedula, correo, direccion, fecha_nacimiento, edad, sexo, estado_civil, cargo, departamento, fecha_ingreso, centro_costo, tipo_pago, estatus, banco, numero_cuenta) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                  (nombre1.value, nombre2.value, apellido1.value, apellido2.value, cedula.value, correo.value, direccion.value, fecha_nacimiento.value, edad.value, sexo.value, estado_civil.value, cargo.value, departamento.value, fecha_ingreso.value, centro_costo.value, tipo_pago.value, estatus.value, banco.value, numero_cuenta.value))
        conn.commit()
        empleado_id = c.lastrowid  # Obtener el ID del empleado recién insertado
        conn.close()
        codigo_empleado.value = f"EMP{empleado_id:04d}"
        page.update()
        print("Empleado guardado con éxito.")
    
    def regresar_menu(e):
        from main import menu_principal
        menu_principal(page)
    
    def abrir_reportes(e):
        conn = sqlite3.connect("empleados.db")
        df = pd.read_sql_query("SELECT * FROM empleados", conn)
        conn.close()
        archivo_excel = "Reporte_Empleados.xlsx"
        df.to_excel(archivo_excel, index=False)
        print(f"Reporte generado: {archivo_excel}")
        subprocess.Popen(["start", "excel", archivo_excel], shell=True)
    
    # Campos de entrada
    nombre1 = ft.TextField(label="1° Nombre", width=150)
    nombre2 = ft.TextField(label="2° Nombre", width=150)
    apellido1 = ft.TextField(label="1° Apellido", width=150)
    apellido2 = ft.TextField(label="2° Apellido", width=150)
    cedula = ft.TextField(label="Cédula", width=150)
    correo = ft.TextField(label="Correo", width=200)
    direccion = ft.TextField(label="Dirección", width=310)
    fecha_nacimiento = ft.TextField(label="Fecha de Nacimiento", width=150)
    edad = ft.TextField(label="Edad", width=80, disabled=True)
    fecha_nacimiento.on_change = actualizar_edad
    sexo = ft.Dropdown(label="Sexo", options=[ft.dropdown.Option("Masculino"), ft.dropdown.Option("Femenino")], width=150)
    estado_civil = ft.Dropdown(label="Estado Civil", options=[ft.dropdown.Option("Soltero"), ft.dropdown.Option("Casado"), ft.dropdown.Option("Divorciado")], width=150)
    cargo = ft.TextField(label="Cargo", width=150)
    departamento = ft.TextField(label="Departamento", width=150)
    fecha_ingreso = ft.TextField(label="Fecha de Ingreso", width=150)
    centro_costo = ft.TextField(label="Centro de Costo", width=150)
    tipo_pago = ft.Dropdown(label="Tipo de Pago", options=[ft.dropdown.Option("Mensual"), ft.dropdown.Option("Quincenal")], width=150)
    estatus = ft.Dropdown(label="Estatus", options=[ft.dropdown.Option("Activo"), ft.dropdown.Option("Inactivo")], width=150)
    banco = ft.TextField(label="Banco", width=150)
    numero_cuenta = ft.TextField(label="Número de Cuenta", width=200)
    codigo_empleado = ft.TextField(label="Código de Empleado", width=150, disabled=True)
    
    # Secciones
    datos_personales = ft.Column([
        ft.Text("Datos Personales", size=16, weight=ft.FontWeight.BOLD),
        ft.Row([nombre1, nombre2]),
        ft.Row([apellido1, apellido2]),
        ft.Row([cedula, correo]),
        ft.Row([direccion]),
        ft.Row([fecha_nacimiento, edad]),
        ft.Row([sexo, estado_civil]),
    ], spacing=5)
    
    datos_laborales = ft.Column([
        ft.Text("Datos Laborales", size=16, weight=ft.FontWeight.BOLD),
        ft.Row([cargo, departamento]),
        ft.Row([fecha_ingreso, centro_costo]),
        ft.Row([tipo_pago, estatus]),
    ], spacing=5)
    
    datos_bancarios = ft.Column([
        ft.Text("Información Bancaria", size=16, weight=ft.FontWeight.BOLD),
        ft.Row([banco, numero_cuenta]),
        ft.Row([codigo_empleado]),
    ], spacing=5)
    
    # Botones
    botones = ft.Row([
        ft.ElevatedButton("Guardar", icon=ft.Icons.SAVE, on_click=guardar_empleado),
        ft.ElevatedButton("Regresar", icon=ft.Icons.ARROW_BACK, on_click=regresar_menu),
        ft.ElevatedButton("Reportes", icon=ft.Icons.ASSESSMENT, on_click=abrir_reportes)
    ], alignment=ft.MainAxisAlignment.CENTER)
    
    # Agregar todo a la página con barra de desplazamiento
    page.add(
        ft.Container(
            content=ft.Column([
                ft.Text("Gestión de Empleados", size=20, weight=ft.FontWeight.BOLD),
                datos_personales,
                datos_laborales,
                datos_bancarios,
                botones
            ], spacing=10, scroll=ft.ScrollMode.ALWAYS),
            expand=True,
            padding=10
        )
    )
    page.update()





# Funciones para las demás secciones como Panel de Control, Cálculo de Nómina, Reportes y Configuración

# Función principal que inicia la aplicación
def main(page: ft.Page):
    inicializar_bd()
    page.title = "Sistema de Nómina"
    mostrar_login(page)

ft.app(target=main)


