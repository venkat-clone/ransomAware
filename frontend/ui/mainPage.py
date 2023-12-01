import flet as ft
from flet import Text, TextAlign
from ui.widgets.navigation import AppNavigationRail


def mainPage(page: ft.Page):

    page.title = "RansomeAwaere"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.bgcolor = "#EEC4C1"
    page.padding = ft.padding.all(0)

    page.add(
        ft.Column(
            expand=True,
            controls=[
                ft.Container(
                    height=80,
                    alignment=ft.alignment.center,
                    content=Text("RansomAware", expand=True, text_align=TextAlign.CENTER, color="#1D1A39", size=30,
                                 weight=ft.FontWeight.W_800, ),
                ),
                ft.Container(
                    expand=True,
                    content=AppNavigationRail()
                ),
            ]
        ),
    )
