import flet as ft

from ui.widgets.appButton import AppButton


class LoadingButton(ft.UserControl):
    def __init__(self, onTap, btnText: str, onError=None, onSuccess=None, onComplete=None, button=None,
                 enabled: bool = True):
        super().__init__()
        self.onTap = onTap
        self.btnText = btnText
        self.onError = onError
        self.onSuccess = onSuccess
        self.onComplete = onComplete
        self.button = button
        self.enabled = enabled

    def build(self):

        def loadTap(e):
            self.controls.pop()
            self.controls.append(
                ft.ProgressRing(
                    color="#AE445A"
                )
            )
            self.update()
            try:
                self.onTap()
                if self.onSuccess is not None: self.onSuccess()
            except Exception as e:
                print(e)
                if self.onError is not None: self.onError()
            finally:
                if self.onComplete is not None: self.onComplete()
                self.controls.pop()
                self.controls.append(child)
                self.update()

        child = self.button(text=self.btnText, on_click=loadTap,
                            disabled=not self.enabled) if self.button is not None else AppButton(
            btnText=self.btnText, onTap=loadTap)

        return child
