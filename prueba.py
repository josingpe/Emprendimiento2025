import flet as ft
from datetime import datetime
import sqlite3
import pandas as pd
import subprocess
import main  # Importar el módulo sin llamar directamente a funciones

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
        c.execute("""
            INSERT INTO empleados (nombre1, nombre2, apellido1, apellido2, cedula, correo, direccion, fecha_nacimiento, edad, sexo, estado_civil, cargo, departamento, fecha_ingreso, centro_costo, tipo_pago, estatus, banco, numero_cuenta) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", 
            (nombre1.value, nombre2.value, apellido1.value, apellido2.value, cedula.value, correo.value, direccion.value, fecha_nacimiento.value, edad.value, sexo.value, estado_civil.value, cargo.value, departamento.value, fecha_ingreso.value, centro_costo.value, tipo_pago.value, estatus.value, banco.value, numero_cuenta.value))
        
        conn.commit()
        empleado_id = c.lastrowid  # Obtener el ID del empleado recién insertado
        conn.close()
        codigo_empleado.value = f"EMP{empleado_id:04d}"
        page.update()
        print("Empleado guardado con éxito.")
    
    def regresar_menu(e):
        main.menu_principal(page)  # Evita importaciones circulares
    
    def abrir_reportes(e):
        conn = sqlite3.connect("empleados.db")
        df = pd.read_sql_query("SELECT * FROM empleados", conn)
        conn.close()
        archivo_excel = "Reporte_Empleados.xlsx"
        df.to_excel(archivo_excel, index=False)
        print(f"Reporte generado: {archivo_excel}")
        subprocess.Popen(["start", "excel", archivo_excel], shell=True)
    
    # Campos de entrada
    nombre1, nombre2 = ft.TextField(label="1° Nombre", width=150), ft.TextField(label="2° Nombre", width=150)
    apellido1, apellido2 = ft.TextField(label="1° Apellido", width=150), ft.TextField(label="2° Apellido", width=150)
    cedula, correo = ft.TextField(label="Cédula", width=150), ft.TextField(label="Correo", width=200)
    direccion = ft.TextField(label="Dirección", width=310)
    fecha_nacimiento = ft.TextField(label="Fecha de Nacimiento", width=150)
    edad = ft.TextField(label="Edad", width=80, disabled=True)
    fecha_nacimiento.on_change = actualizar_edad
    sexo = ft.Dropdown(label="Sexo", options=[ft.dropdown.Option("Masculino"), ft.dropdown.Option("Femenino")], width=150)
    estado_civil = ft.Dropdown(label="Estado Civil", options=[ft.dropdown.Option("Soltero"), ft.dropdown.Option("Casado"), ft.dropdown.Option("Divorciado")], width=150)
    cargo, departamento = ft.TextField(label="Cargo", width=150), ft.TextField(label="Departamento", width=150)
    fecha_ingreso, centro_costo = ft.TextField(label="Fecha de Ingreso", width=150), ft.TextField(label="Centro de Costo", width=150)
    tipo_pago = ft.Dropdown(label="Tipo de Pago", options=[ft.dropdown.Option("Mensual"), ft.dropdown.Option("Quincenal")], width=150)
    estatus = ft.Dropdown(label="Estatus", options=[ft.dropdown.Option("Activo"), ft.dropdown.Option("Inactivo")], width=150)
    banco, numero_cuenta = ft.TextField(label="Banco", width=150), ft.TextField(label="Número de Cuenta", width=200)
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
