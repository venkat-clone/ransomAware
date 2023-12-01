import flet as ft


def ListText(dict):
    col = ft.Column()
    col.controls.append(ft.Container(height=10))
    for i, j in dict:
        col.controls.append(ft.Text(i, color="#9E514C", weight=ft.FontWeight.W_800, size=13), )
        col.controls.append(ft.Text(j, color="#9E514C"))
    return col
