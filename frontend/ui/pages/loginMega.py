import time

import flet as ft
from mega import Mega

from ui.widgets.loadingButton import LoadingButton


class LoginMega(ft.UserControl):

    def __init__(self, onLogin,zip_file_name):
        super().__init__()
        self.onLogin = onLogin
        self.email = ''
        self.password = ''
        self.zip_file_name = zip_file_name

    def login(self):
        time.sleep(3)
        # self.onLogin(self.email, self.password)
        mega = Mega()
        # m = mega.login("mailuser0102@gmail.com", "20U51A6207")
        # self.updateStatus(status=f"loading with email {email}....")
        m = mega.login(self.email, self.password)
        # self.updateStatus(status=f"uploading files to mega....")
        m.upload(self.zip_file_name)





    def build(self):
        loginBtn = LoadingButton(onTap=self.login(), btnText="Login")

        def updatePassword(e):
            self.email = e.control.value
            loginBtn.disabled = not (self.email.__contains__('@') and self.password.__len__() >= 8)
            print(loginBtn.disabled)
            loginBtn.update()

        def updateEmail(e):
            self.password = e.control.value
            loginBtn.disabled = not (self.email.__contains__('@') and self.password.__len__() >= 8)
            print(loginBtn.disabled)
            loginBtn.update()

        return ft.Column(
            expand=True,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[

                ft.Text("Login Meta", size=16, weight=ft.FontWeight.W_700),
                ft.Image(src="ransomwAware/ui/assets/mega-logo.png",
                         width=100,
                         height=100,
                         fit=ft.ImageFit.CONTAIN,

                         ),
                ft.TextField(
                    label="Email",
                    value='mailuser0102@gmail.com',
                    on_change=updateEmail
                ),
                ft.TextField(
                    label="Password",
                    password=True,
                    value='20U51A6207',
                    on_change=updatePassword
                ),
                loginBtn
            ]
        )
