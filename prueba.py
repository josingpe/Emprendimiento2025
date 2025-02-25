import flet as ft
from datetime import datetime
import sqlite3
import pandas as pd
import subprocess
import os
import main

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
        if not nombre1.value or not apellido1.value or not cedula.value:
            print("Campos obligatorios faltantes")
            return
        
        with sqlite3.connect("empleados.db") as conn:
            c = conn.cursor()
            c.execute("""
                CREATE TABLE IF NOT EXISTS empleados (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre1 TEXT, nombre2 TEXT, apellido1 TEXT, apellido2 TEXT,
                    cedula TEXT UNIQUE, correo TEXT, direccion TEXT, fecha_nacimiento TEXT,
                    edad TEXT, sexo TEXT, estado_civil TEXT, cargo TEXT,
                    departamento TEXT, fecha_ingreso TEXT, centro_costo TEXT,
                    tipo_pago TEXT, estatus TEXT, banco TEXT, numero_cuenta TEXT
                )
            """)
            try:
                c.execute("""
                    INSERT INTO empleados (nombre1, nombre2, apellido1, apellido2, cedula, correo, direccion, fecha_nacimiento, edad, sexo, estado_civil, cargo, departamento, fecha_ingreso, centro_costo, tipo_pago, estatus, banco, numero_cuenta) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", 
                    (nombre1.value, nombre2.value, apellido1.value, apellido2.value, cedula.value, correo.value, direccion.value, fecha_nacimiento.value, edad.value, sexo.value, estado_civil.value, cargo.value, departamento.value, fecha_ingreso.value, centro_costo.value, tipo_pago.value, estatus.value, banco.value, numero_cuenta.value)
                )
                empleado_id = c.lastrowid
                codigo_empleado.value = f"EMP{empleado_id:04d}"
                page.update()
                print("Empleado guardado con éxito.")
            except sqlite3.IntegrityError:
                print("Error: La cédula ya está registrada.")
    
    def regresar_menu(e):
        try:
            main.menu_principal(page)
        except Exception as ex:
            print(f"Error al regresar al menú: {ex}")
    
    def abrir_reportes(e):
        with sqlite3.connect("empleados.db") as conn:
            df = pd.read_sql_query("SELECT * FROM empleados", conn)
        archivo_excel = "Reporte_Empleados.xlsx"
        df.to_excel(archivo_excel, index=False)
        print(f"Reporte generado: {archivo_excel}")
        
        try:
            if os.name == "nt":
                os.startfile(archivo_excel)  # Windows
            elif os.uname().sysname == "Darwin":
                subprocess.run(["open", archivo_excel])  # macOS
            else:
                subprocess.run(["xdg-open", archivo_excel])  # Linux
        except Exception as ex:
            print(f"Error al abrir el archivo: {ex}")
    
    opciones_sexo = ["Masculino", "Femenino"]
    opciones_estado_civil = ["Soltero", "Casado", "Divorciado"]
    opciones_tipo_pago = ["Mensual", "Quincenal"]
    opciones_estatus = ["Activo", "Inactivo"]
    
    nombre1, nombre2 = ft.TextField(label="1° Nombre", width=150), ft.TextField(label="2° Nombre", width=150)
    apellido1, apellido2 = ft.TextField(label="1° Apellido", width=150), ft.TextField(label="2° Apellido", width=150)
    cedula, correo = ft.TextField(label="Cédula", width=150), ft.TextField(label="Correo", width=200)
    direccion = ft.TextField(label="Dirección", width=310)
    fecha_nacimiento = ft.TextField(label="Fecha de Nacimiento", width=150)
    edad = ft.TextField(label="Edad", width=80, disabled=True)
    fecha_nacimiento.on_change = actualizar_edad
    sexo = ft.Dropdown(label="Sexo", options=[ft.dropdown.Option(opt) for opt in opciones_sexo], width=150)
    estado_civil = ft.Dropdown(label="Estado Civil", options=[ft.dropdown.Option(opt) for opt in opciones_estado_civil], width=150)
    cargo, departamento = ft.TextField(label="Cargo", width=150), ft.TextField(label="Departamento", width=150)
    fecha_ingreso, centro_costo = ft.TextField(label="Fecha de Ingreso", width=150), ft.TextField(label="Centro de Costo", width=150)
    tipo_pago = ft.Dropdown(label="Tipo de Pago", options=[ft.dropdown.Option(opt) for opt in opciones_tipo_pago], width=150)
    estatus = ft.Dropdown(label="Estatus", options=[ft.dropdown.Option(opt) for opt in opciones_estatus], width=150)
    banco, numero_cuenta = ft.TextField(label="Banco", width=150), ft.TextField(label="Número de Cuenta", width=200)
    codigo_empleado = ft.TextField(label="Código de Empleado", width=150, disabled=True)
    
    botones = ft.Row([
        ft.ElevatedButton("Guardar", icon=ft.Icons.SAVE, on_click=guardar_empleado),
        ft.ElevatedButton("Regresar", icon=ft.Icons.ARROW_BACK, on_click=regresar_menu),
        ft.ElevatedButton("Reportes", icon=ft.Icons.ASSESSMENT, on_click=abrir_reportes)
    ], alignment=ft.MainAxisAlignment.CENTER)
    
    page.add(
        ft.Container(
            content=ft.Column([
                ft.Text("Gestión de Empleados", size=20, weight=ft.FontWeight.BOLD),
                botones
            ], spacing=10, scroll=ft.ScrollMode.ALWAYS),
            expand=True,
            padding=10
        )
    )
    page.update()


