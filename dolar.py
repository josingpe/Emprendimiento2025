import flet as ft
import requests

def obtener_tasa_dolar():
    try:
        response = requests.get("https://api.exchangerate-api.com/v4/latest/USD")
        data = response.json()
        return data["rates"].get("VES", "No disponible")
    except Exception as e:
        return f"Error: {e}"

def main(page: ft.Page):
    page.title = "Tasa de Cambio USD/VES"
    
    tasa_text = ft.Text(f"Tasa USD/VES: {obtener_tasa_dolar()}", size=18, weight=ft.FontWeight.BOLD, color="blue")
    
    def actualizar_tasa(e):
        tasa_text.value = f"Tasa USD/VES: {obtener_tasa_dolar()}"
        page.update()

    boton_actualizar = ft.ElevatedButton("Actualizar Tasa", icon=ft.Icons.REFRESH, on_click=actualizar_tasa)

    page.add(tasa_text, boton_actualizar)

ft.app(target=main)
