import flet as ft

# Función para mostrar la pantalla de inicio de sesión
def mostrar_login(page):
    page.bgcolor = ft.colors.BLUE_50  # Color de fondo suave
    
    # URL de la imagen de fondo con un tamaño más grande
    fondo_imagen_url = "https://i.ibb.co/N2yyYy0W/rrhh.jpg"  # Cambia esto por una URL de imagen válida más grande

    # Crea la imagen de fondo que ocupará toda la pantalla
    fondo = ft.Image(
        src=fondo_imagen_url,
        fit=ft.ImageFit.COVER,  # Asegura que la imagen cubra toda la pantalla
        expand=True,  # La imagen se expande para ocupar todo el fondo
    )

    # Definimos los campos de texto para el usuario y la clave
    usuario = ft.TextField(label="Usuario", width=300, bgcolor="white", border_color="#2196F3")
    clave = ft.TextField(label="Clave", password=True, width=300, bgcolor="white", border_color="#2196F3")

    # Botón para iniciar sesión
    boton_login = ft.ElevatedButton(
        text="Iniciar Sesión",
        on_click=lambda e: print(f"Usuario: {usuario.value}, Clave: {clave.value}"),
        bgcolor="#2196F3", color="white"
    )

    # Crea el contenedor de la tarjeta con los campos de usuario, contraseña y botón
    card = ft.Container(
        content=ft.Column(
            [usuario, clave, boton_login],
            spacing=15, alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),
        padding=30, border_radius=10, bgcolor="white",
        shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.GREY_500),
        width=350, height=300,
        alignment=ft.alignment.center  # Centra el contenido dentro de la tarjeta
    )

    # Limpia la pantalla y agrega los elementos
    page.controls.clear()

    page.add(
        ft.Stack(
            controls=[fondo, card],  # Fondo en la parte inferior, tarjeta centrada encima
            expand=True,
            alignment=ft.alignment.center  # Centra la tarjeta en la pantalla
        )
    )

    page.update()

# Función principal que ejecuta la aplicación
def main(page):
    page.window_width = 500
    page.window_height = 500
    page.window_resizable = False
    mostrar_login(page)

# Ejecuta la aplicación de Flet
ft.app(target=main)
