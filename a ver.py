import flet as ft
import requests  # Importación correcta

# Función para obtener la tasa de cambio USD/VES
def obtener_tasa_dolar():
    try:
        respuesta = requests.get("https://api.exchangerate-api.com/v4/latest/USD")
        data = respuesta.json()
        return data["rates"].get("VES", "No disponible")
    except Exception as e:
        return f"Error: {e}"

# Función para mostrar la pantalla de inicio de sesión con la tasa del dólar en la parte superior derecha
def mostrar_login(page):
    page.bgcolor = ft.colors.WHITE  # Color de fondo suave
    
    # URL de la imagen
    fondo_imagen_url = "https://i.ibb.co/XftFnLvx/1740690784448.jpg"

    # Imagen pequeña en la parte superior izquierda
    imagen_pequena = ft.Image(
        src=fondo_imagen_url,
        width=100,  # Ajusta el tamaño de la imagen
        height=100,
        fit=ft.ImageFit.CONTAIN
    )
    
    # Contenedor de la imagen pequeña en la parte superior izquierda
    imagen_container = ft.Container(
        content=imagen_pequena,
        alignment=ft.alignment.top_left,
        padding=ft.padding.only(top=10, left=10)  # Ajusta la posición de la imagen
    )

    # Tasa de cambio USD/VES en la parte superior derecha con color azul corporativo
    tasa_text = ft.Text(
        f"Tasa USD/VES: {obtener_tasa_dolar()}",
        size=16,
        weight=ft.FontWeight.BOLD,
        color="#2196F3"
    )

    def actualizar_tasa(e):
        tasa_text.value = f"Tasa USD/VES: {obtener_tasa_dolar()}"
        page.update()

    boton_actualizar = ft.IconButton(
        icon=ft.icons.REFRESH, on_click=actualizar_tasa, icon_color="#2196F3"
    )

    tasa_container = ft.Container(
        content=ft.Row(
            [tasa_text, boton_actualizar],
            alignment=ft.MainAxisAlignment.END  # Alinea la tasa a la derecha
        ),
        padding=ft.padding.only(top=10, right=20),  # Posición superior derecha
        alignment=ft.alignment.top_right
    )

    # Campos de usuario y contraseña
    usuario = ft.TextField(label="Usuario", width=300, bgcolor="white", border_color="#2196F3")
    clave = ft.TextField(label="Clave", password=True, width=300, bgcolor="white", border_color="#2196F3")

    # Botón de inicio de sesión
    boton_login = ft.ElevatedButton(
        text="Iniciar Sesión",
        on_click=lambda e: print(f"Usuario: {usuario.value}, Clave: {clave.value}"),
        bgcolor="#2196F3",
        color="white"
    )

    # Contenedor de la tarjeta de inicio de sesión centrada
    card = ft.Container(
        content=ft.Column(
            [usuario, clave, boton_login],
            spacing=15,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),
        padding=30,
        border_radius=10,
        bgcolor="white",
        shadow=ft.BoxShadow(blur_radius=10, color=ft.colors.GREY_500),
        width=350,
        height=300,
        alignment=ft.alignment.center
    )

    # Contenedor centrado de la tarjeta
    card_container = ft.Container(
        content=card,
        alignment=ft.alignment.center
    )

    # Limpia la pantalla y agrega los elementos
    page.controls.clear()
    page.add(
        ft.Stack(
            controls=[imagen_container, tasa_container, card_container],  # Solo la imagen pequeña, la tasa y la tarjeta de inicio de sesión centrada
            expand=True
        )
    )
    page.update()

# Función principal
def main(page):
    page.window_width = 800
    page.window_height = 800
    page.window_resizable = True  # Permite redimensionar la ventana
    mostrar_login(page)

# Ejecuta la aplicación
ft.app(target=main)
