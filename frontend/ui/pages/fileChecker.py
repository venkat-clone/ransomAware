import hashlib

import flet as ft
import requests
from ui.widgets.filepicker import AppFilePicker, FileType
from ui.widgets.loadingButton import LoadingButton
from ui.widgets.statusTextTemplate import StatusTextTemplate

testStr = """please select the file you want to check whether files are infected with ransomware or not"""


class FileCheckerPage(StatusTextTemplate):

    def __init__(self):
        super().__init__()

        self.link1 = ft.TextSpan("",style=ft.TextStyle(color=ft.colors.BLUE))
        self.link2 = ft.TextSpan("",style=ft.TextStyle(color=ft.colors.BLUE))
        self.snapText = ft.Text(
                    "",
                    color=ft.colors.BLACK,

                )
        self.input_file = None

    def selectFile(self, path):
        self.input_file = path

    def getSHADetails(self,sha):
        url = f"http://127.0.0.1:8000/check-sha?format=json&sha={sha}"
        response = requests.request("GET", url)
        return response.json()

    def checkFile(self):
        if self.input_file is None:
            self.page.snack_bar = ft.SnackBar(content=ft.Text("please select file first!"), open=True,
                                              show_close_icon=True)
            self.page.update()
            return

        self.updateStatus("generating hash....")
        sha256_hash = hashlib.sha256()

        with open(self.input_file, "rb") as f:
            while chunk := f.read(8192):
                sha256_hash.update(chunk)
        sha256_value = sha256_hash.hexdigest()
        # sha256_value = '094fd325049b8a9cf6d3e5ef2a6d4cc6a567d7d49c35f8bb8dd9e3c6acf3d78d'
        self.updateStatus("fetching sha details")
        result = self.getSHADetails(sha256_value)

        if result['found']:
            my_string = "\n".join(["{}: {}".format(key, value) for key, value in result.items()])
            self.updateStatus(my_string)
        else:
            # Provide hyperlinks to external services
            string = f"SHA-256 not found in the database.\nYou can check the file on the following services:"
            self.updateStatus(string)
            self.link1.text = f"https://www.virustotal.com/gui/file/{sha256_value}"
            self.link2.text = "https://id-ransomware.malwarehunterteam.com/"
            self.link1.url = f"https://www.virustotal.com/gui/file/{sha256_value}"
            self.link2.url = f"https://id-ransomware.malwarehunterteam.com/"
            # self.link1.on_click = lambda: self.page.launch_url(f"https://www.virustotal.com/gui/file/{sha256_value}")
            # self.link2.on_click = lambda: self.page.launch_url(f"https://id-ransomware.malwarehunterteam.com/")
            self.snapText.spans =[
                        ft.TextSpan('VirusTotal: '),
                        self.link1,
                        ft.TextSpan('\nID Ransomware: '),
                        self.link2,
                    ]
            self.snapText.update()

    def startCheck(self):
        try:
            self.checkFile()
        except Exception as e:
            self.updateStatus(f"Error:{e}", color=ft.colors.RED)

    def build(self):
        return ft.Column(

            controls=[
                ft.Text("Check your files whether infected or not", size=16, weight=ft.FontWeight.W_700, color=ft.colors.WHITE),
                ft.Text(testStr),
                AppFilePicker(type=FileType.File, onSelected=self.selectFile,
                              hint_text="Select file you want to check"),
                ft.Container(
                    alignment=ft.alignment.center,
                    content=LoadingButton(onTap=self.startCheck, btnText="Check File")
                ),
                self.statusContainer,
                self.snapText


            ]
        )
