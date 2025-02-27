import flet as ft
import sqlite3
import hashlib
import os
import pandas as pd
import sqlite3
import flet as ft
import subprocess
from datetime import datetime


def menu_principal(page):
    page.controls.clear()
    page.add(ft.Text("Menú Principal"))
    page.update()
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
# Función para obtener la tasa de cambio USD/VES
def obtener_tasa_dolar():
    try:
        respuesta = requests.get("https://api.exchangerate-api.com/v4/latest/USD")
        data = respuesta.json()
        return data["rates"].get("VES", "No disponible")
    except Exception as e:
        return f"Error: {e}"
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

    # 🔹 Obtener la tasa de cambio correctamente
    tasa_actual = obtener_tasa_dolar()
    if not tasa_actual:
        tasa_actual = "Error al obtener tasa"

    # 🔹 Crear el texto de la tasa con el valor inicial
    tasa_text = ft.Text(
        f"Tasa USD/VES: {tasa_actual}",
        size=16,
        weight=ft.FontWeight.BOLD,
        color="#2196F3"
    )

    def actualizar_tasa(e):
        nueva_tasa = obtener_tasa_dolar()
        if not nueva_tasa:
            nueva_tasa = "Error al obtener tasa"
        
        tasa_text.value = f"Tasa USD/VES: {nueva_tasa}"
        page.update()

    boton_actualizar = ft.IconButton(
        icon=ft.Icons.REFRESH, on_click=actualizar_tasa, icon_color="#2196F3"
    )

    tasa_container = ft.Container(
        content=ft.Row(
            [tasa_text, boton_actualizar],
            alignment=ft.MainAxisAlignment.END
        ),
        padding=ft.padding.only(top=10, right=20),
        alignment=ft.alignment.top_right
    )

    # 🔹 Agregar la tasa antes de actualizar la página
    page.controls.clear()
    page.add(
        tasa_container,  # Se agrega la tasa a la interfaz
        ft.Row([card], alignment=ft.MainAxisAlignment.CENTER)
    )
    page.update()


    tasa_container = ft.Container(
        content=ft.Row(
            [tasa_text, boton_actualizar],
            alignment=ft.MainAxisAlignment.END  # Alinea la tasa a la derecha
        ),
        padding=ft.padding.only(top=10, right=20),  # Posición superior derecha
        alignment=ft.alignment.top_right
    )

    # Limpiar la página y agregar los elementos
    page.controls.clear()
    page.add(
        tasa_container,  # Primero se muestra la tasa en la parte superior
        ft.Row([card], alignment=ft.MainAxisAlignment.CENTER)
    )
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
import sqlite3
import os
import platform
from datetime import datetime

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
        empleado_id = c.lastrowid
        conn.close()
        codigo_empleado.value = f"EMP{empleado_id:04d}"
        page.update()
        print("Empleado guardado con éxito.")
    
    def regresar_menu(e):
        mostrar_menu_principal(page)
    
    def abrir_reportes(e):
        conn = sqlite3.connect("empleados.db")
        df = pd.read_sql_query("SELECT * FROM empleados", conn)
        conn.close()
        archivo_excel = "Reporte_Empleados.xlsx"
        df.to_excel(archivo_excel, index=False)
        print(f"Reporte generado: {archivo_excel}")
        if platform.system() == "Windows":
            os.startfile(archivo_excel)
        elif platform.system() == "Darwin":  # macOS
            os.system(f"open {archivo_excel}")
        else:  # Linux
            os.system(f"xdg-open {archivo_excel}")
    
    def consultar_empleado(e):
        conn = sqlite3.connect("empleados.db")
        c = conn.cursor()
        c.execute("SELECT * FROM empleados WHERE cedula = ?", (consulta_cedula.value,))
        empleado = c.fetchone()
        conn.close()
        if empleado:
            nombre1.value, nombre2.value, apellido1.value, apellido2.value, cedula.value, correo.value, direccion.value, fecha_nacimiento.value, edad.value, sexo.value, estado_civil.value, cargo.value, departamento.value, fecha_ingreso.value, centro_costo.value, tipo_pago.value, estatus.value, banco.value, numero_cuenta.value = empleado[1:]
        else:
            print("Empleado no encontrado.")
        page.update()

    # Campos de entrada con ajuste de tamaño
    input_width = 250
    consulta_cedula = ft.TextField(label="Consultar por Cédula", width=input_width)
    boton_consulta = ft.ElevatedButton("Buscar", icon=ft.Icons.SEARCH, on_click=consultar_empleado)
    
    nombre1 = ft.TextField(label="1° Nombre", width=input_width)
    nombre2 = ft.TextField(label="2° Nombre", width=input_width)
    apellido1 = ft.TextField(label="1° Apellido", width=input_width)
    apellido2 = ft.TextField(label="2° Apellido", width=input_width)
    cedula = ft.TextField(label="Cédula", width=input_width)
    correo = ft.TextField(label="Correo", width=input_width)
    direccion = ft.TextField(label="Dirección", width=input_width)
    fecha_nacimiento = ft.TextField(label="Fecha de Nacimiento", width=input_width)
    edad = ft.TextField(label="Edad", width=100, disabled=True)
    fecha_nacimiento.on_change = actualizar_edad
    sexo = ft.Dropdown(label="Sexo", options=[ft.dropdown.Option("Masculino"), ft.dropdown.Option("Femenino")], width=input_width)
    estado_civil = ft.Dropdown(label="Estado Civil", options=[ft.dropdown.Option("Soltero"), ft.dropdown.Option("Casado"), ft.dropdown.Option("Divorciado")], width=input_width)
    cargo = ft.TextField(label="Cargo", width=input_width)
    departamento = ft.TextField(label="Departamento", width=input_width)
    fecha_ingreso = ft.TextField(label="Fecha de Ingreso", width=input_width)
    centro_costo = ft.TextField(label="Centro de Costo", width=input_width)
    tipo_pago = ft.Dropdown(label="Tipo de Pago", options=[ft.dropdown.Option("Mensual"), ft.dropdown.Option("Quincenal")], width=input_width)
    estatus = ft.Dropdown(label="Estatus", options=[ft.dropdown.Option("Activo"), ft.dropdown.Option("Inactivo")], width=input_width)
    banco = ft.Dropdown(
    label="Banco",
    options=[
        ft.dropdown.Option("Banco de Venezuela"),
        ft.dropdown.Option("Banco Nacional de Crédito (BNC)"),
        ft.dropdown.Option("BBVA Provincial"),
        ft.dropdown.Option("Banesco"),
        ft.dropdown.Option("Mercantil Banco"),
        ft.dropdown.Option("Banco del Tesoro"),
        ft.dropdown.Option("Bancamiga"),
        ft.dropdown.Option("Banplus"),
        ft.dropdown.Option("Bancaribe"),
        ft.dropdown.Option("Venezolano de Crédito"),
        ft.dropdown.Option("Banco Plaza"),
        ft.dropdown.Option("Banco Fondo Común"),
        ft.dropdown.Option("Banco DELSUR"),
        ft.dropdown.Option("Banco Exterior"),
        ft.dropdown.Option("Banco Sofitasa"),
        ft.dropdown.Option("Bancrecer"),
        ft.dropdown.Option("Banco Caroní"),
        ft.dropdown.Option("Banco Activo"),
        ft.dropdown.Option("100% Banco"),
        ft.dropdown.Option("Mi Banco"),
        ft.dropdown.Option("Bicentenario (banco digital de los trabajadores y trabajadoras)"),
    ],
    width=input_width)
    numero_cuenta = ft.TextField(label="Número de Cuenta", width=input_width)
    codigo_empleado = ft.TextField(label="Código de Empleado", width=input_width, disabled=True)
    
    # Secciones con 4 campos por fila
    datos_personales = ft.Column([
        ft.Text("Datos Personales", size=16, weight=ft.FontWeight.BOLD),
        ft.Row([consulta_cedula, boton_consulta]),
        ft.Row([nombre1, nombre2, apellido1, apellido2], spacing=10),
        ft.Row([cedula, correo, direccion, fecha_nacimiento], spacing=10),
        ft.Row([edad, sexo, estado_civil, cargo], spacing=10),
        ft.Row([departamento, fecha_ingreso, centro_costo, tipo_pago], spacing=10)
    ], spacing=15)
    
    datos_bancarios = ft.Column([
        ft.Text("Información Bancaria", size=16, weight=ft.FontWeight.BOLD),
        ft.Row([estatus, banco, numero_cuenta, codigo_empleado], spacing=10)
    ], spacing=15)

    # Botones centrados
    botones = ft.Row([
        ft.ElevatedButton("Guardar", icon=ft.Icons.SAVE, on_click=guardar_empleado, bgcolor="#2196F3", color="white"),
        ft.ElevatedButton("Regresar", icon=ft.Icons.ARROW_BACK, on_click=regresar_menu, bgcolor="grey", color="white"),
        ft.ElevatedButton("Reportes", icon=ft.Icons.ASSESSMENT, on_click=abrir_reportes, bgcolor="#4CAF50", color="white")
    ], alignment=ft.MainAxisAlignment.CENTER, spacing=20)
    
    # Agregar todo a la página sin división
    page.add(
        ft.Container(
            content=ft.Column([
                ft.Text("Gestión de Empleados", size=24, weight=ft.FontWeight.BOLD, color="#2196F3"),
                ft.Divider(),
                datos_personales,
                datos_bancarios,
                botones
            ], spacing=20, scroll=ft.ScrollMode.ALWAYS),
            expand=True,
            padding=20
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

if __name__ == "__main__":
    ft.app(target=main)

