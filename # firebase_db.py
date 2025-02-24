# firebase_db.py
import firebase_admin
from firebase_admin import credentials, db

# Ruta a tu archivo JSON de credenciales
cred = credentials.Certificate('C:\\Users\\josin\\Downloads\\python\\clave-firebase.json')


# Inicializar la aplicación de Firebase
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://tu-proyecto.firebaseio.com/'
})

# Referencia a la base de datos de Firebase
ref = db.reference('empleados')

# Función para agregar un empleado
def agregar_empleado(id, nombre, sueldo):
    ref.child(id).set({
        'nombre': nombre,
        'sueldo': sueldo
    })

# Puedes agregar más funciones para leer, modificar o eliminar datos si lo necesitas
