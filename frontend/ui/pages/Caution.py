import flet as ft

from ui.widgets.listText import ListText

title = """Stay vigilant and be cautious about the following:"""


content = [
    ('1. Untrusted Sources',"Avoid downloading software or files from untrusted sources. Use official websites and app stores to minimize the risk of downloading malicious content."),
    ('2. Unexpected Emails',"Exercise caution when receiving unexpected emails, especially those with urgent messages or unsolicited attachments. Verify the sender's authenticity before interacting with the content."),
    ('3. Pop-up Warnings','Be skeptical of pop-up warnings or alerts claiming your system is infected. Legitimate antivirus software rarely uses aggressive pop-ups, and these may be attempts to deceive you into downloading malware.'),
    ('4. Unsafe Links','Hover over links before clicking to preview the destination URL. If the link seems suspicious or directs you to an unexpected site, avoid clicking.'),
]

class CautionPage(ft.UserControl):

    def build(self):
        return ft.ListView(
            controls=[
                ft.Text(title, size=16, weight=ft.FontWeight.W_700, color=ft.colors.WHITE),

                ListText(content)
            ]
        )


