import os
import time
import zipfile
from enum import Enum
import datetime
import flet as ft
from mega import Mega
from cryptography.fernet import Fernet
from ui.widgets.filepicker import AppFilePicker, FileType
from ui.widgets.loadingButton import LoadingButton
from ui.widgets.statusTextTemplate import StatusTextTemplate

testStr = """You can upload any file to your Mega Cloud service account by encrypting it. Please select a folder and 
enter the credentials to upload.\nThe key to decrypt will be saved @share the location to decrypt the folder when you 
want to access files."""

decryptStr = """1. The folder which was encrypted using above service can be decrypted here
2. Make sure that you download the folder from Mega cloud
3. upload the zip file
4. upload the key
5. sit back and relax"""

tmpDir = 'backup_tmp'
key_filename = f"{tmpDir}/fernet_key.key"

folder_to_encrypt = ""


class BackupPage(StatusTextTemplate):

    def __init__(self):
        super().__init__()
        self.dialog = None
        self.email = 'mailuser0102@gmail.com'
        self.password = '20U51A6207'
        self.folder_to_encrypt = None
        self.StatusType = None
        self.key_file = None
        self.zip_file = None
        self.backupStatusBar = ft.Container(
            content=ft.Container(),
        )
        self.retrieveStatusBar = ft.Container(
            content=ft.Container(),
        )

    def backup(self):
        if not os.path.exists(tmpDir):
            os.mkdir(tmpDir)

        if not os.path.exists(key_filename):
            # Generate a Fernet key if it doesn't exist
            key = Fernet.generate_key()
            with open(key_filename, 'wb') as key_file:
                key_file.write(key)
            self.updateStatus("Generating Fernet Key....")
        else:
            # Load the Fernet key if it exists
            with open(key_filename, 'rb') as key_file:
                key = key_file.read()
            self.updateStatus("Loading Fernet Key....")
        self.updateStatus("Creating Zip ....")
        zip_file_name = f"{tmpDir}/encrypted_folder_{datetime.datetime.now()}.zip"
        zipf = zipfile.ZipFile(zip_file_name, 'w', zipfile.ZIP_DEFLATED)
        self.updateStatus("Initialize the Fernet cipher with the key....")
        # Initialize the Fernet cipher with the key
        cipher = Fernet(key)
        self.updateStatus("Adding Files to Zip ....")
        c = 0
        for root, dirs, files in os.walk(self.folder_to_encrypt):
            self.updateStatus(f"Adding Files to Zip \n{c} files added....")
            c = c + 1
            for file in files:
                file_path = os.path.join(root, file)
                with open(file_path, 'rb') as file_to_encrypt:
                    plaintext = file_to_encrypt.read()

                # Encrypt the file using Fernet
                encrypted_data = cipher.encrypt(plaintext)

                # Store the encrypted data in the zip file with the same directory structure
                zip_file_path = os.path.relpath(file_path, self.folder_to_encrypt)
                zipf.writestr(zip_file_path, encrypted_data)
        if c == 0:
            self.updateStatus(f"No files added in {self.folder_to_encrypt}")
        zipf.close()
        self.updateStatus("Zip files added to Zip.....")
        mega = Mega()
        self.updateStatus("Logging in to mega.....")
        m = mega.login(self.email, self.password)
        self.updateStatus("uploading to mega.....")
        m.upload(zip_file_name)

        secure_key_filename = f"{tmpDir}/fernet_key.key"
        self.updateStatus(status=f"files upload successful\nFernet key saved at {secure_key_filename}")
        with open(secure_key_filename, 'wb') as secure_key_file:
            secure_key_file.write(key)
        os.remove(zip_file_name)

    def startBackup(self):
        try:
            self.initStatus()
            self.backupStatusBar.content = self.statusContainer
            self.retrieveStatusBar.content = ft.Container()

            self.backupStatusBar.update()
            self.retrieveStatusBar.update()
            if self.email is not None and self.password is not None and self.folder_to_encrypt is not None:
                self.backup()
            else:
                self.page.snack_bar = ft.SnackBar(ft.Text(f"Please Insert All Fields", color=ft.colors.RED),
                                                  show_close_icon=True)
                self.page.snack_bar.open = True
                self.page.update()
        except Exception as e:
            self.updateStatus(f"Error:{e}")

    def retrieve(self):
        # Load the Fernet key

        self.updateStatus("Loading Fernet Key....")
        with open(self.key_file, 'rb') as key_file:
            key = key_file.read()

        # Initialize the Fernet cipher with the key
        cipher = Fernet(key)

        # Create the decrypted folder if it doesn't exist
        decrypted_folder = f'{tmpDir}/decrypted_folder'
        if not os.path.exists(decrypted_folder):
            os.makedirs(decrypted_folder)

        # Extract and decrypt the files from the zip file

        self.updateStatus("Extracting files from zip....")
        with zipfile.ZipFile(self.zip_file, 'r') as zipf:
            for file_info in zipf.infolist():
                encrypted_data = zipf.read(file_info)
                file_path = os.path.join(decrypted_folder, file_info.filename)

                # Decrypt and write the decrypted data to the file
                decrypted_data = cipher.decrypt(encrypted_data)
                with open(file_path, 'wb') as decrypted_file:
                    decrypted_file.write(decrypted_data)

        self.updateStatus(f"files decrypted successfully\nFiles saved at {decrypted_folder}")

    def startRetrieve(self):
        try:
            self.initStatus()
            self.retrieveStatusBar.content = self.statusContainer
            self.backupStatusBar.content = ft.Container()
            self.retrieveStatusBar.update()
            self.backupStatusBar.update()

            if self.password is not None and self.key_file is not None and self.zip_file is not None:
                self.retrieve()
            else:
                self.page.snack_bar = ft.SnackBar(ft.Text(f"Please Insert All Fields", color=ft.colors.RED),
                                                  show_close_icon=True)
                self.page.snack_bar.open = True
                self.page.update()
        except Exception as e:
            self.updateStatus(f"Error:{e}")

    def build(self):

        def updatePassword(e):
            self.email = e.control.value

        def updateEmail(e):
            self.password = e.control.value

        def onSelected(folder_to_encrypt):
            self.folder_to_encrypt = folder_to_encrypt

        def updateKEYFile(key_file):
            self.key_file = key_file

        def updateZipFile(zip_file):
            self.zip_file = zip_file

        return ft.Column(
            horizontal_alignment=ft.alignment.center,
            scroll=ft.ScrollMode.AUTO,
            controls=[
                ft.Text("Backup your files to a safe place Mega", size=16, weight=ft.FontWeight.W_700,
                        color=ft.colors.WHITE),
                ft.Text(testStr),
                ft.Container(
                    margin=ft.margin.only(top=10),
                    padding=ft.padding.symmetric(horizontal=10),
                    content=ft.Row(
                        controls=[
                            ft.TextField(
                                label="Email",
                                value='mailuser0102@gmail.com',
                                on_change=updateEmail,
                                expand=True,
                                filled=True,
                                label_style=ft.TextStyle(
                                    color=ft.colors.WHITE
                                )
                            ),
                            ft.TextField(
                                label="Password",
                                password=True,
                                value='20U51A6207',
                                on_change=updatePassword,
                                expand=True,
                                filled=True,
                                label_style=ft.TextStyle(
                                    color=ft.colors.WHITE
                                )
                            ),
                        ]
                    )),
                AppFilePicker(onSelected=onSelected, type=FileType.Folder, hint_text="Select Files you want to backup"),
                ft.Container(
                    alignment=ft.alignment.center,
                    content=LoadingButton(onTap=self.startBackup, btnText="Backup")
                ),

                self.backupStatusBar,
                ft.Container(
                    bgcolor=ft.colors.WHITE,

                    height=1,
                    margin=ft.margin.only(top=20)
                ),
                ft.Text("Get you data back here", size=16, weight=ft.FontWeight.W_700,
                        color=ft.colors.WHITE),
                ft.Text(decryptStr),
                AppFilePicker(onSelected=updateZipFile, type=FileType.File, hint_text="Select Encrypted folder "
                                                                                      "downloaded from Mega"),
                AppFilePicker(onSelected=updateKEYFile, type=FileType.File, hint_text="Select Key file generated "
                                                                                      "during backup"),
                ft.Container(
                    alignment=ft.alignment.center,
                    content=LoadingButton(onTap=self.startRetrieve, btnText="Decrypt"),
                    margin=ft.margin.only(bottom=10)
                ),
                self.retrieveStatusBar
            ]
        )
