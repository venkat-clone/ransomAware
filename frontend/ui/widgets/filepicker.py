import enum

import flet as ft

from flet_core import UserControl


class FileType(enum.Enum):
    Folder = 1
    File = 2


class AppFilePicker(UserControl):

    def __init__(self, type: FileType, onSelected, hint_text: str = None, helper_text: str = None,
                 icon: str = ft.icons.DRIVE_FOLDER_UPLOAD_ROUNDED):
        super().__init__()
        self.fileType = type
        self.onSelected = onSelected
        self.helper_text = helper_text
        self.hint_text = hint_text
        self.icon = icon

    def build(self):

        textField = ft.TextField(
            hint_text=self.hint_text,
            hint_style=ft.TextStyle(color=ft.colors.GREY_600),
            helper_text=self.helper_text,
            read_only=True,
            text_align=ft.TextAlign.START,
            value="",
            content_padding=ft.padding.symmetric(horizontal=10),
            bgcolor=ft.colors.WHITE,
            filled=True,
            border_radius=ft.border_radius.all(6),
            color="#AE445A",
            icon=self.icon
        )

        def pickFile(e):
            def pick_files_result(e: ft.FilePickerResultEvent):
                if (e.path is not None):
                    self.onSelected(e.path)
                    textField.value = e.path
                else:
                    self.onSelected(e.files[0].path)
                    textField.value = e.files[0].path
                textField.update()

            pick_files_dialog = ft.FilePicker(on_result=pick_files_result)
            self.page.overlay.append(pick_files_dialog)
            self.page.update()
            if self.fileType is FileType.Folder:
                pick_files_dialog.get_directory_path()
            elif self.fileType is FileType.File:
                pick_files_dialog.pick_files()

        return ft.Container(
            padding=ft.padding.all(10),
            content=ft.Row(
                controls=[
                    ft.Container(content=textField, expand=True),
                    ft.TextButton(content=ft.Text("Browse"), on_click=pickFile)
                ]
            )
        )
