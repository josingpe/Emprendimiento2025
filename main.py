import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sqlite3
from datetime import datetime
from fpdf import FPDF
import hashlib
from tkcalendar import DateEntry
import pandas as pd

# Conectar a la base de datos SQLite con manejo de errores
try:
    conn = sqlite3.connect("nomina.db")
    cursor = conn.cursor()
except sqlite3.Error as e:
    messagebox.showerror("Error", f"No se pudo conectar a la base de datos: {e}")
    exit()

# Crear tablas si no existen
cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario TEXT UNIQUE,
        clave TEXT
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS empleados (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        codigo TEXT UNIQUE,
        primer_nombre TEXT,
        segundo_nombre TEXT,
        primer_apellido TEXT,
        segundo_apellido TEXT,
        cedula TEXT UNIQUE,
        correo TEXT,
        direccion TEXT,
        pais_nacimiento TEXT,
        ciudad_nacimiento TEXT,
        estado_nacimiento TEXT,
        fecha_nacimiento TEXT,
        edad INTEGER,
        grado_instruccion TEXT,
        carga_familiar TEXT
       
    )
''')
conn.commit()

# Función para encriptar claves
def encriptar_clave(clave):
    return hashlib.sha256(clave.encode()).hexdigest()

# Insertar usuario administrador con clave encriptada
usuario_admin = "admin"
clave_admin = encriptar_clave("1234")

cursor.execute("SELECT * FROM usuarios WHERE usuario = ?", (usuario_admin,))
if not cursor.fetchone():
    cursor.execute("INSERT INTO usuarios (usuario, clave) VALUES (?, ?)", (usuario_admin, clave_admin))
    conn.commit()

def generar_codigo_empleado():
    cursor.execute("SELECT COUNT(*) FROM empleados")
    count = cursor.fetchone()[0] + 1
    return f"E{count:05d}"

def calcular_edad(fecha_nacimiento):
    try:
        fecha_nac = datetime.strptime(fecha_nacimiento, "%d-%m-%Y")
        hoy = datetime.today()
        return hoy.year - fecha_nac.year - ((hoy.month, hoy.day) < (fecha_nac.month, fecha_nac.day))
    except ValueError:
        return ""

def verificar_credenciales():
    usuario = entry_usuario.get()
    clave = encriptar_clave(entry_clave.get())
    cursor.execute("SELECT * FROM usuarios WHERE usuario = ? AND clave = ?", (usuario, clave))
    if cursor.fetchone():
        root.withdraw()
        abrir_menu_principal()
    else:
        messagebox.showerror("Error", "Usuario o clave incorrectos")

def abrir_menu_principal():
    menu = tk.Toplevel()
    menu.title("Menú Principal - Sistema de Nómina")
    menu.geometry("400x350")

    opciones = ["Panel de Control", "Gestión de Empleados", "Cálculo de Nómina", "Reportes", "Configuración"]
    funciones = [lambda: print("Abrir Panel de Control"), abrir_gestion_empleados, lambda: print("Cálculo de Nómina"), generar_reporte_excel, lambda: print("Abrir Configuración")]

    for i, opcion in enumerate(opciones):
        ttk.Button(menu, text=opcion, width=30, command=funciones[i]).pack(pady=5)
    
    # Función para cerrar sesión
    def cerrar_sesion():
        menu.destroy()  # Cierra la ventana del menú
        root.deiconify()  # Muestra nuevamente la ventana de inicio de sesión

    # Botón para cerrar sesión
    ttk.Button(menu, text="Cerrar Sesión", width=30, command=cerrar_sesion).pack(pady=10)

def abrir_gestion_empleados():
    gestion = tk.Toplevel()
    gestion.title("Gestión de Empleados")
    gestion.geometry("800x500")

    ttk.Label(gestion, text="Gestión de Empleados", font=("Arial", 12, "bold")).pack(pady=10)
    frame = ttk.Frame(gestion)
    frame.pack(pady=10)

    labels = ["Código", "1° Nombre", "2° Nombre", "1° Apellido", "2° Apellido", "Cédula", "Correo", "Dirección", "País", "Ciudad", "Estado", "Fecha de Nacimiento", "Edad", "Grado de Instrucción", "Carga Familiar"]
    entries = {}

    for i, label_text in enumerate(labels):
        ttk.Label(frame, text=label_text).grid(row=i//3, column=(i%3)*2, padx=5, pady=5, sticky="e")
        if label_text == "Fecha de Nacimiento":
            entry = DateEntry(frame, date_pattern="dd-mm-yyyy")
        else:
            entry = ttk.Entry(frame, state="readonly" if label_text == "Edad" else "normal")
        entry.grid(row=i//3, column=(i%3)*2 + 1, padx=5, pady=5)
        entries[label_text] = entry

    entries["Código"].insert(0, generar_codigo_empleado())
    entries["Código"].config(state="readonly")
    
    def actualizar_edad(event):
        fecha_nac = entries["Fecha de Nacimiento"].get()
        edad = calcular_edad(fecha_nac)
        entries["Edad"].config(state="normal")
        entries["Edad"].delete(0, tk.END)
        entries["Edad"].insert(0, str(edad))
        entries["Edad"].config(state="readonly")
    
    entries["Fecha de Nacimiento"].bind("<FocusOut>", actualizar_edad)

    def guardar_empleado():
        datos = [entries[label].get() for label in labels]
        if any(not d for d in datos[:-1]):
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return
        cursor.execute("INSERT INTO empleados VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?,?)", datos)
        conn.commit()
        messagebox.showinfo("Éxito", "Empleado guardado correctamente")
        
    def buscar_empleado():
        cedula = entries["Cédula"].get().strip()
        if not cedula:
            messagebox.showerror("Error", "Ingrese un número de cédula para buscar.")
            return

        cursor.execute("SELECT * FROM empleados WHERE cedula = ?", (cedula,))
        empleado = cursor.fetchone()
        if empleado:
            for i, label in enumerate(labels):
                entries[label].config(state="normal")
                entries[label].delete(0, tk.END)
                entries[label].insert(0, str(empleado[i +1]))
                if label == "Edad":
                    entries[label].config(state="readonly")
        else:
            messagebox.showerror("Error", "Empleado no encontrado.")

    ttk.Button(gestion, text="Buscar por Cédula", command=buscar_empleado).pack(pady=5)
    ttk.Button(gestion, text="Guardar", command=guardar_empleado).pack(pady=10)
    ttk.Button(gestion, text="Regresar", command=gestion.destroy).pack(pady=10)

def generar_reporte_pdf():
    # (Código para generar el PDF sin cambios)
    pass
def generar_reporte_excel():
    try:
        cursor.execute("SELECT * FROM empleados")
        empleados = cursor.fetchall()

        if not empleados:
            messagebox.showwarning("Aviso", "No hay datos para generar el reporte.")
            return

        columnas = ["ID", "Código", "1° Nombre", "2° Nombre", "1° Apellido", "2° Apellido", 
                    "Cédula", "Correo", "Dirección", "País", "Ciudad", "Estado", 
                    "Fecha de Nacimiento", "Edad", "Grado de Instrucción", "Carga Familiar"]

        df = pd.DataFrame(empleados, columns=columnas)

        archivo = "reporte_nomina.xlsx"
        df.to_excel(archivo, index=False)

        messagebox.showinfo("Éxito", f"Reporte generado correctamente: {archivo}")

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo generar el reporte: {e}")

# Crear ventana de inicio de sesión
root = tk.Tk()
root.title("Inicio de Sesión - Sistema de Nómina")
root.geometry("300x200")

ttk.Label(root, text="Usuario:").pack(pady=5)
entry_usuario = ttk.Entry(root)
entry_usuario.pack(pady=5)

ttk.Label(root, text="Clave:").pack(pady=5)
entry_clave = ttk.Entry(root, show="*")
entry_clave.pack(pady=5)

ttk.Button(root, text="Iniciar Sesión", command=verificar_credenciales).pack(pady=10)

root.mainloop()
