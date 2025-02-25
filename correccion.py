import flet as ft
import sqlite3
import hashlib
import os
import pandas as pd
from datetime import datetime


def conectar_bd():
    return sqlite3.connect("nomina.db")


def encriptar_clave(clave):
    return hashlib.sha256(clave.encode()).hexdigest()


def inicializar_bd():
    conn = conectar_bd()
    cursor = conn.cursor()

    # Crear tablas si no existen
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE NOT NULL,
            clave TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS empleados (
            codigo TEXT PRIMARY KEY,
            nombre1 TEXT, nombre2 TEXT,
            apellido1 TEXT, apellido2 TEXT,
            cedula TEXT UNIQUE, correo TEXT,
            direccion TEXT, pais TEXT, ciudad TEXT, estado TEXT,
            fecha_nacimiento TEXT, edad INTEGER,
            grado_instruccion TEXT, carga_familiar INTEGER,
            sexo TEXT, estado_civil TEXT, telefono TEXT,
            profesion TEXT, cargo TEXT, departamento TEXT,
            nomina TEXT, division TEXT, banco TEXT,
            cuenta TEXT, fecha_ingreso TEXT, centro_costo TEXT,
            estatus TEXT, tipo_pago TEXT
        )
    """)

    # Insertar usuario admin si no existe
    cursor.execute("SELECT * FROM usuarios WHERE usuario = 'admin'")
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO usuarios (usuario, clave) VALUES (?, ?)", 
                       ("admin", encriptar_clave("1234")))
        conn.commit()

    conn.close()


def verificar_credenciales(page, usuario, clave):
    if not usuario or not clave:
        page.snack_bar = ft.SnackBar(content=ft.Text("Debe ingresar usuario y clave"), open=True)
        page.update()
        return

    try:
        conn = conectar_bd()
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


def guardar_empleado(page, inputs):
    datos = {key: value.value for key, value in inputs.items()}
    try:
        conn = conectar_bd()
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
        page.update()
        abrir_gestion_empleados(page)
    except sqlite3.Error as e:
        page.snack_bar = ft.SnackBar(content=ft.Text(f"Error en la base de datos: {e}"), open=True)
        page.update()


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
    
    # Campos de entrada
    inputs = {
        "Código": ft.TextField(label="Código", width=150, disabled=True),
        "1° Nombre": ft.TextField(label="1° Nombre", width=150),
        "2° Nombre": ft.TextField(label="2° Nombre", width=150),
        "1° Apellido": ft.TextField(label="1° Apellido", width=150),
        "2° Apellido": ft.TextField(label="2° Apellido", width=150),
        "Cédula": ft.TextField(label="Cédula", width=150),
        "Correo": ft.TextField(label="Correo", width=200),
        "Dirección": ft.TextField(label="Dirección", width=310),
        "Fecha de Nacimiento": ft.TextField(label="Fecha de Nacimiento", width=150),
        "Edad": ft.TextField(label="Edad", width=80, disabled=True),
        "Sexo": ft.Dropdown(label="Sexo", options=[ft.dropdown.Option("Masculino"), ft.dropdown.Option("Femenino")], width=150),
        "Estado Civil": ft.Dropdown(label="Estado Civil", options=[ft.dropdown.Option("Soltero"), ft.dropdown.Option("Casado"), ft.dropdown.Option("Divorciado")], width=150),
        "Cargo": ft.TextField(label="Cargo", width=150),
        "Departamento": ft.TextField(label="Departamento", width=150),
        "Fecha de Ingreso": ft.TextField(label="Fecha de Ingreso", width=150),
        "Centro de Costo": ft.TextField(label="Centro de Costo", width=150),
        "Tipo de Pago": ft.Dropdown(label="Tipo de Pago", options=[ft.dropdown.Option("Mensual"), ft.dropdown.Option("Quincenal")], width=150),
        "Estatus": ft.Dropdown(label="Estatus", options=[ft.dropdown.Option("Activo"), ft.dropdown.Option("Inactivo")], width=150),
        "Banco": ft.TextField(label="Banco", width=150),
        "Número de Cuenta": ft.TextField(label="Número de Cuenta", width=200),
    }

    fecha_nacimiento = inputs["Fecha de Nacimiento"]
    fecha_nacimiento.on_change = actualizar_edad
    
    # Guardar empleado
    botones = ft.Row([
        ft.ElevatedButton("Guardar", icon=ft.Icons.SAVE, on_click=lambda e: guardar_empleado(page, inputs)),
        ft.ElevatedButton("Regresar", icon=ft.Icons.ARROW_BACK, on_click=lambda e: mostrar_menu_principal(page)),
    ])

    # Layout de la página
    page.add(ft.Column([
        ft.Text("Gestión de Empleados", size=20, weight=ft.FontWeight.BOLD),
        *[ft.Row([field]) for field in inputs.values()],
        botones
    ], spacing=10, scroll=ft.ScrollMode.ALWAYS))
    page.update()


def main(page: ft.Page):
    inicializar_bd()
    page.title = "Sistema de Nómina"
    mostrar_login(page)


if __name__ == "__main__":
    ft.app(target=main)
