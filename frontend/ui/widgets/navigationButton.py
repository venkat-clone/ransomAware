import flet as ft

from ui.models.navItem import NavigationItems

activeColor = ft.colors.BLUE
disableColor = ft.colors.GREY_50


class NavigationButton(ft.UserControl):

    def __init__(self, item: NavigationItems, current: NavigationItems, on_click):
        super().__init__()
        self.active = item == current
        self.label = item.value.label
        self.onClick = on_click
        self.item = item

    def build(self):
        def click(e):
            self.onClick(self.item)

        if self.active:
            return ft.Container(
                height=40,
                bgcolor="#AE445A",
                expand=True,
                alignment=ft.alignment.center_left,
                padding=ft.padding.all(8),
                border_radius=ft.border_radius.all(4),
                content=ft.Text(self.label, color=ft.colors.WHITE),
            )
        else:
            return ft.GestureDetector(
                on_tap=click,
                content=ft.Container(
                    height=40,
                    alignment=ft.alignment.center_left,
                    padding=ft.padding.all(8),
                    content=ft.Text(self.label, color="#555555"),
                ),
            )
