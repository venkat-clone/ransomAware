import flet as ft


class AppButton(ft.UserControl):
    def __init__(self, onTap, btnText: str,enabled:bool = True):
        super().__init__()
        self.onTap = onTap
        self.btnText = btnText
        self.disabled = not enabled

    def build(self):
        return ft.GestureDetector(
            on_tap=self.onTap,
            content=ft.Container(
                border_radius=ft.border_radius.all(6),
                bgcolor="#AE445A" if self.disabled else "#AE445A",
                padding=ft.padding.symmetric(vertical=10, horizontal=20),
                content=ft.Text(self.btnText, size=16, weight=ft.FontWeight.W_700)
            )
        )
