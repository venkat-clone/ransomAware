import flet as ft

from ui.widgets.listText import ListText

title = """Isolation is a critical step in minimizing the impact of ransomware on your network. Follow these guidelines to isolate affected systems:"""

content =[
    ("1. Segmented Networks","mplement network segmentation to isolate critical systems from less secure areas. This limits the lateral movement of ransomware within the network."),
    ("2. Access Controls","Restrict user access based on the principle of least privilege. Users should have only the access necessary for their roles, reducing the potential impact of ransomware."),
    ("3. Quarantine Policies","Establish and enforce quarantine policies for devices displaying suspicious behavior. This includes temporarily restricting network access for further investigation."),
    ("4. Incident Response Plan","Develop and regularly update an incident response plan. Clearly outline the steps to isolate affected systems and restore normal operations."),
]


class IsolationPage(ft.UserControl):

    def build(self):
        return ft.Column(
            controls=[
                ft.Text(title, size=16, weight=ft.FontWeight.W_700, color=ft.colors.WHITE),

                ListText(content)
            ]
        )

