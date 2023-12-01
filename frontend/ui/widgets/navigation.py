import flet as ft

from ui.models.navItem import NavigationItems
from ui.widgets.navigationButton import NavigationButton


class AppNavigationRail(ft.UserControl):

    def __init__(self):
        super().__init__()
        self.buttons = None
        self.activeItem = NavigationItems.Prevention

    def build(self):
        self.state = ft.Column(
            controls=self.buttons
        )

        mainScreen = ft.Container(
                                expand=True,
                                content=self.activeItem.value.page
                            )
        screenTitle = ft.Text(
            self.activeItem.value.label,
            color="#AE445A", size=20, weight=ft.FontWeight.W_700
        )

        def onClick(newItem: NavigationItems):
            self.activeItem = newItem
            self.state.controls.clear()
            for item in NavigationItems:
                self.state.controls.append(NavigationButton(item=item, current=self.activeItem, on_click=onClick))
            mainScreen.content=self.activeItem.value.page
            screenTitle.value = self.activeItem.value.label
            self.update()

        self.buttons = [NavigationButton(item=item, current=self.activeItem, on_click=onClick) for item in
                        NavigationItems]
        self.state = ft.Column(
            controls=self.buttons
        )
        return  ft.Row(
                        controls=[
                            ft.Container(
                                width=150,
                                padding=ft.padding.all(10),
                                border_radius=ft.BorderRadius(
                                    top_right=10,
                                    bottom_left=0,
                                    bottom_right=0,
                                    top_left=0,
                                ),
                                bgcolor="#F3F3F3",
                                content=ft.Column(
                                    controls=[
                                        ft.Text("Title",color="#AE445A",size=20,weight=ft.FontWeight.W_700),
                                        self.state
                                    ]
                                )
                            ),
                            ft.Column(
                                expand=True,
                                controls=[
                                    screenTitle,
                                    ft.Container(
                                        content=ft.Container(
                                            content=mainScreen,
                                            alignment=ft.alignment.center,
                                            expand=True,
                                            bgcolor="#E6A39F",
                                            padding=ft.padding.all(10),
                                            border_radius=ft.border_radius.all(8),
                                            margin=ft.padding.all(15)
                                        ),
                                        alignment=ft.alignment.center,
                                        expand=True
                                    )
                                ]
                            )
                        ]
                    )

