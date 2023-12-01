from enum import Enum
from  flet import  UserControl

from ui.pages.Caution import CautionPage
from ui.pages.Isolation import IsolationPage
from ui.pages.Prevention import PrecautionPage
from ui.pages.Quarantine import QuarantinePage
from ui.pages.backup import BackupPage
from ui.pages.decryption import DecryptionPage
from ui.pages.fileChecker import FileCheckerPage


class NavigationItem():
    def __init__(self, label: str, route: str,page:UserControl):
        self.label = label
        self.route = route
        self.page = page




class NavigationItems(Enum):
    Prevention = NavigationItem("Prevention", "Prevention",page=PrecautionPage())
    Quarantine = NavigationItem("Quarantine", "Quarantine",page=QuarantinePage())
    Caution = NavigationItem("Caution", "Caution",page=CautionPage())
    Isolation = NavigationItem("Isolation", "Isolation",page=IsolationPage())
    Backup = NavigationItem("Backup", "Backup",page=BackupPage())
    Decryption = NavigationItem("Decryption", "Decryption",page=DecryptionPage())
    FileChecker = NavigationItem("FileChecker", "FileChecker",page=FileCheckerPage())


