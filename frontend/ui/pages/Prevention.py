import flet as ft

from ui.widgets.listText import ListText

title = """Follow these best practices to minimize the risk of falling victim to ransomware attacks:"""

content = [
    ('1. Regular Backups',
     "Schedule regular backups of your important files to an external and secure location. This ensures that even if "
     "your files are encrypted, you can restore them from a clean backup."),
    ('2. Software Updates',
     'Keep your operating system and all software up to date. Regular updates often include security patches that '
     'protect your system from known vulnerabilities.'),
    ('3. Email Vigilance',
     'Be cautious with email attachments and links, especially from unknown or suspicious sources. Ransomware often '
     'spreads through phishing emails.'),
    ('4. Security Software',
     'Install reputable antivirus and anti-malware software. Keep it updated to ensure it can detect and prevent the '
     'latest ransomware threats.'),
    ('5. User Education',
     'Educate yourself and your team on the signs of phishing attempts and how to identify potentially malicious '
     'emails or websites.'),
]


class PrecautionPage(ft.UserControl):

    def build(self):
        return ft.ListView(
            controls=[
                ft.Text(title, size=16, weight=ft.FontWeight.W_900, color=ft.colors.WHITE),

                ListText(content)
            ]
        )
