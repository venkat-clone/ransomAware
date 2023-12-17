import flet as ft


class StatusTextTemplate(ft.UserControl):

    def __init__(self):
        super().__init__()
        self.initStatus()

    def initStatus(self):
        self.statusText = ft.Text(value="", color=ft.colors.LIGHT_BLUE)
        self.statusContainer = ft.Container(
            content=self.statusText
        )
        self.stack = []
        self.statusContainer.height = 0
    def updateStatus(self, status: str, color=None, addToStack: bool = False):
        self.statusContainer.height = None
        if addToStack:
            self.stack.append(status)
            self.statusText.value = '\n'.join(self.stack)
        else:
            self.statusText.value = status
        self.statusText.color = color if color is not None else ft.colors.BLACK
        self.update()
        print(status)

    def hideStatus(self):
        self.statusContainer.height = 0
        self.update()

    def clear(self):
        self.stack.clear()
