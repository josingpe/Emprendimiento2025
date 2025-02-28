import flet as ft
import io

def generar_reporte(page):
    contenido = "Este es un reporte de prueba"
    
    # Crear un archivo en memoria
    buffer = io.BytesIO()
    buffer.write(contenido.encode("utf-8"))
    buffer.seek(0)
    
    # Crear un enlace de descarga
    page.download("reporte.txt", buffer.read())

def main(page: ft.Page):
    boton_descargar = ft.ElevatedButton(
        "Descargar Reporte",
        on_click=lambda e: generar_reporte(page)
    )
    
    page.add(boton_descargar)

ft.app(target=main)
