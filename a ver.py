# Función asincrónica para obtener la tasa de cambio USD/VES
import flet as ft
import asyncio
import httpx

# Función para obtener la tasa del dólar de forma asíncrona
async def obtener_tasa_dolar():
    try:
        async with httpx.AsyncClient() as client:
            respuesta = await client.get("https://api.exchangerate-api.com/v4/latest/USD")
            data = respuesta.json()
            return data["rates"].get("VES", "No disponible")
    except Exception as e:
        return f"Error: {e}"

# Función para mostrar la pantalla de inicio de sesión con la tasa del dólar y la imagen
def mostrar_login(page):
    page.bgcolor = ft.Colors.WHITE  # Corregido `ft.colors` -> `ft.Colors`
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # URL de la imagen
    fondo_imagen_url = "https://i.ibb.co/XftFnLvx/1740690784448.jpg"

    # Imagen pequeña en la parte superior izquierda
    imagen_pequena = ft.Image(
        src=fondo_imagen_url,
        width=100,
        height=100,
        fit=ft.ImageFit.CONTAIN
    )
    
    imagen_container = ft.Container(
        content=imagen_pequena,
        alignment=ft.alignment.top_left,
        padding=ft.padding.only(top=10, left=10)  
    )

    # Texto de la tasa de cambio (se actualizará después)
    tasa_text = ft.Text(
        "Tasa USD/VES: Cargando...",
        size=16,
        weight=ft.FontWeight.BOLD,
        color="#2196F3"
    )

    # Función para actualizar la tasa de forma correcta sin usar event loops en hilos secundarios
    def actualizar_tasa(e=None):
        tasa = asyncio.run(obtener_tasa_dolar())  # Se usa `asyncio.run()` en lugar de `get_event_loop()`
        tasa_text.value = f"Tasa USD/VES: {tasa}"
        page.update()

    boton_actualizar = ft.IconButton(
        icon=ft.Icons.REFRESH,  # Corregido `ft.icons` -> `ft.Icons`
        on_click=actualizar_tasa,
        icon_color="#2196F3"
    )

    tasa_container = ft.Container(
        content=ft.Row(
            [tasa_text, boton_actualizar],
            alignment=ft.MainAxisAlignment.END  
        ),
        padding=ft.padding.only(top=10, right=20),
        alignment=ft.alignment.top_right
    )

    # Campos de usuario y contraseña
    usuario = ft.TextField(label="Usuario", width=300, bgcolor="white", border_color="#2196F3")
    clave = ft.TextField(label="Clave", password=True, width=300, bgcolor="white", border_color="#2196F3")

    # Botón de inicio de sesión
    boton_login = ft.ElevatedButton(
    text="Iniciar Sesión",
    on_click=lambda e: verificar_credenciales(page, usuario.value, clave.value),  # Agregar validación
    bgcolor="#2196F3",
    color="white"

    )

    # Tarjeta de inicio de sesión
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
        shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.GREY_500),  # Corregido `ft.colors` -> `ft.Colors`
        width=350,
        height=300,
        alignment=ft.alignment.center
    )

    card_container = ft.Container(
        content=card,
        alignment=ft.alignment.center
    )

    # Limpiar la pantalla y agregar elementos
    page.controls.clear()
    page.add(
        ft.Stack(
            controls=[imagen_container, tasa_container, card_container],
            expand=True
        )
    )
    page.update()

    # Llamar a la actualización de la tasa al inicio
    actualizar_tasa()

# Función principal
def main(page):
    page.window_width = 800
    page.window_height = 800
    page.window_resizable = True  
    mostrar_login(page)

# Ejecutar la aplicación
ft.app(target=main)