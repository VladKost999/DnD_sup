import flet as ft
from random import randint


class Character:
    def __init__(self, name, kd, hp, initiative, active):
        self.name = name
        self.kd = kd
        self.hp = hp
        self.initiative = initiative
        self.active = active


def main(page: ft.Page):
    page.padding = ft.padding.symmetric(horizontal=30)

    def create_custom_textfield(value):
        return ft.TextField(
            value=str(value),
            fill_color=first_color,
            border_width=0,
            text_size=25,
            expand=True,
            text_align=ft.TextAlign.CENTER,
            text_vertical_align=ft.VerticalAlignment.CENTER
        )

    def update_ui():
        characters_view.controls.clear()
        for char in characters_list:
            name_text = ft.Text(value=char.name, expand=True)
            kd_input = create_custom_textfield(char.kd)
            hp_input = create_custom_textfield(char.hp)
            initiative_input = create_custom_textfield(char.initiative)
            row_ch = ft.Row(
                controls=[name_text, kd_input, hp_input, initiative_input],
                alignment=ft.alignment.center
            )
            container_ch = ft.Container(content=row_ch, padding=ft.padding.only(left=20), bgcolor=first_color, height=60)
            container_fin = ft.Container(content=container_ch, padding=ft.padding.symmetric(horizontal=20), bgcolor=first_color)
            characters_view.controls.append(container_ch)
        page.update()

    def add_character(e):
        character = Character(
            name=name_input.value,
            kd=randint(10, 18),
            hp=randint(10, 100),
            initiative=randint(1, 20),
            active=True
        )
        characters_list.append(character)
        update_ui()

    page.vertical_alignment = ft.alignment.top_center
    bg_color = '#0e1117'
    first_color = "#262730"
    page.theme_mode = bg_color
    characters_list = []

    name_input = ft.TextField(label="Имя персонажа",
                              fill_color=first_color,
                              border_color=first_color,
                              border_radius=20,
                              on_submit=add_character,
                              expand=True, height=50)
    add_button = ft.FloatingActionButton(icon=ft.icons.ADD,
                                         height=50,
                                         elevation=0,
                                         bgcolor='#c0392b',
                                         on_click=add_character)
    input_row = ft.Row(controls=[name_input, add_button])
    input_card = ft.Card(content=input_row, elevation=0)
    input_container = ft.Container(content=input_card, padding=ft.padding.only(top=20))
    page.add(input_container)

    names_col = ['Имя','КД', 'ХП', 'Иниц.']
    text_cols = [ft.Text(value=i, expand=True, text_align=ft.TextAlign.CENTER) for i in names_col]
    page.add(ft.Row(controls=text_cols))

    characters_view = ft.Column()
    page.add(characters_view)

    update_ui()


if __name__ == "__main__":
    ft.app(target=main)
