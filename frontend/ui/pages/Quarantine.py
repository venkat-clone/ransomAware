import flet as ft

from ui.widgets.listText import ListText

title = """In the event of a suspected ransomware infection, understanding how to quarantine affected systems is crucial to prevent further spread. Follow these steps:"""

content = [
    ('1. Disconnect from Network','Immediately disconnect the infected device from the network, including Wi-Fi and Ethernet connections. This helps prevent the ransomware from spreading to other devices.'),
    ('2. Isolate Devices','Quarantine the affected device from other devices on the network to contain the ransomware. This limits its impact on other systems.'),
    ('3. Contact IT Support','Report the incident to your IT support team. Provide details on the suspected infection and actions taken to isolate the affected device.'),
]

class QuarantinePage(ft.UserControl):

    def build(self):
        return ft.ListView(
            controls=[
                ft.Text(title, size=16, weight=ft.FontWeight.W_700, color=ft.colors.WHITE),

                ListText(content)
            ]
        )


