import os
import io
import shutil
import flet as ft

from requests import request

from logic.decryption import rsa_construct_blob, decrypt_file
from ui.widgets.filepicker import AppFilePicker, FileType
from ui.widgets.loadingButton import LoadingButton
from ui.widgets.statusTextTemplate import StatusTextTemplate

testStr = """Please upload the ransom note from desktop with name DECRYPT-FILES.TXT and the folder/file encrypted 
with the Maze Ransomware:"""

tmpDir = "decryptTmp"


class DecryptionPage(StatusTextTemplate):

    def __init__(self):
        super().__init__()
        self.encryptedFile = None
        self.ransomNote = None

    def decrypt(self):
        if not os.path.exists(tmpDir):
            os.mkdir(tmpDir)
        with io.open(f'assets/files/private.bin', 'rb') as f:
            priv_key_blob = f.read()
        self.updateStatus("Constructing RSA Private Key...", addToStack=True)
        priv_key = rsa_construct_blob(priv_key_blob)
        if (priv_key is None) or not priv_key.has_private():
            self.updateStatus("Error: Invalid RSA private key BLOB", addToStack=True)
        new_filename = self.encryptedFile + '.dec'
        self.updateStatus("Decrypting File...", addToStack=True)
        shutil.copy(self.encryptedFile, new_filename)
        if not decrypt_file(new_filename, priv_key):
            os.remove(new_filename)
            self.updateStatus("Error: Failed to decrypt file", addToStack=True)
        else:
            self.updateStatus(f"File decrypted successfully:\ndecrypted file saved at {new_filename}", addToStack=True)

    def decryptAPI(self):

        url = "http://127.0.0.1:8000/decrypt"

        files = [
            ('ransom_note',
             (self.ransomNote, open(self.ransomNote, 'rb'), 'text/plain')),
            ('file_to_decrypt', (
                self.encryptedFile, open(self.encryptedFile, 'rb'),
                'application/octet-stream'))
        ]
        self.updateStatus('Uploading files to decrypting.....')
        response = request("POST", url, files=files)
        self.updateStatus(f'file decrypted & downloaded at {self.encryptedFile}.dec')
        with open(f"{self.encryptedFile}.dec", 'wb') as file:
            file.write(response.content)

    def startDecrypt(self):
        try:

            if self.encryptedFile is None or self.ransomNote is None:
                self.page.snack_bar = ft.SnackBar(content=ft.Text("Please Select above Files", color=ft.colors.RED))
                self.page.update()
            else:
                self.decryptAPI()
        except Exception as e:
            self.updateStatus(f"Error:{e}", color=ft.colors.RED, addToStack=True)

    def pickEncryptedFile(self, path):
        self.encryptedFile = path

    def pickRansomNote(self, path):
        self.ransomNote = path

    def build(self):

        return ft.Column(

            controls=[
                ft.Text("Decrypt", size=16, weight=ft.FontWeight.W_700, color=ft.colors.WHITE),
                ft.Text(testStr),
                AppFilePicker(onSelected=self.pickEncryptedFile, type=FileType.File, hint_text="select File Wanted to "
                                                                                               "decrypt"),
                AppFilePicker(onSelected=self.pickRansomNote, type=FileType.File, hint_text="select RansomNote"),

                ft.Container(
                    alignment=ft.alignment.center,
                    content=LoadingButton(onTap=self.startDecrypt, btnText="Decrypt")
                ),
                self.statusContainer,
            ]
        )
