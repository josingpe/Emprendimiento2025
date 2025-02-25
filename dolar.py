import flet as ft
from datetime import datetime
import sqlite3
import pandas as pd
import subprocess
import os
import requests
import main

def obtener_tasa_dolar():
    try:
        response = requests.get("https://api.exchangerate-api.com/v4/latest/USD")
        data = response.json()
        return data["rates"].get("VES", "No disponible")
    except Exception as e:
        print(f"Error obteniendo la tasa: {e}")
        return "Error"

def mostrar_menu_principal(page):
    page.controls.clear()
    
    tasa = ft.Text(f"Tasa USD/VES: {obtener_tasa_dolar()}", size=16, weight=ft.FontWeight.BOLD, color="blue")
    fecha_hora = ft.Text(f"Fecha y hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", size=14, color="gray")
    
    def actualizar_tasa(e):
        tasa.value = f"Tasa USD/VES: {obtener_tasa_dolar()}"
        fecha_hora.value = f"Fecha y hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        page.update()
    
    page.add(
        ft.Row([
            ft.Text("Menú Principal", size=24, weight=ft.FontWeight.BOLD),
            ft.Container(
                content=ft.Row([
                    tasa,
                    ft.ElevatedButton("Actualizar", icon=ft.Icons.REFRESH, on_click=actualizar_tasa)
                ], alignment=ft.MainAxisAlignment.END),
                alignment=ft.alignment.top_right
            )
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        ft.Divider(),
        
        ft.Column([
            ft.ElevatedButton("Panel de Control", on_click=lambda e: abrir_panel_control(page)),
            ft.ElevatedButton("Gestión de Empleados", on_click=lambda e: abrir_gestion_empleados(page)),
            ft.ElevatedButton("Cálculo de Nómina", on_click=lambda e: abrir_calculo_nomina(page)),
            ft.ElevatedButton("Reportes", on_click=lambda e: abrir_reportes(page)),
            ft.ElevatedButton("Configuración", on_click=lambda e: abrir_configuracion(page)),
            
            ft.Divider(),
            ft.ElevatedButton("Cerrar Sesión", on_click=lambda e: mostrar_login(page), bgcolor="red", color="white"),
            
            ft.Container(
                content=fecha_hora,
                alignment=ft.alignment.bottom_center
            )
        ], alignment=ft.MainAxisAlignment.CENTER)
    )
    page.update()

def abrir_gestion_empleados(page):
    page.controls.clear()
    
    tasa = ft.Text(f"Tasa USD/VES: {obtener_tasa_dolar()}", size=16, weight=ft.FontWeight.BOLD, color="blue")
    
    def actualizar_tasa(e):
        tasa.value = f"Tasa USD/VES: {obtener_tasa_dolar()}"
        page.update()
    
    def regresar_menu(e):
        try:
            mostrar_menu_principal(page)
        except Exception as ex:
            print(f"Error al regresar al menú: {ex}")
    
    botones = ft.Row([
        ft.ElevatedButton("Actualizar Tasa", icon=ft.Icons.REFRESH, on_click=actualizar_tasa),
        ft.ElevatedButton("Regresar", icon=ft.Icons.ARROW_BACK, on_click=regresar_menu)
    ], alignment=ft.MainAxisAlignment.CENTER)
    
    page.add(
        ft.Container(
            content=ft.Column([
                ft.Text("Gestión de Empleados", size=20, weight=ft.FontWeight.BOLD),
                tasa,
                botones
            ], spacing=10, scroll=ft.ScrollMode.ALWAYS),
            expand=True,
            padding=10
        )
    )
    page.update()
