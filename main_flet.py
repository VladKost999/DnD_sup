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
    page.title = 'DnD sup'
    page.padding = ft.padding.symmetric(horizontal=30)
    page.window_resizable = True

    def create_custom_textfield(index, attr_name, value):
        return ft.TextField(
            value=str(value),
            on_change=lambda e, idx=index, attr=attr_name: update_character_value(idx, attr, e.control.value),
            height=50,
            fill_color=first_color,
            border_color=first_color,
            border_width=3,
            text_size=25,
            expand=True,
            text_vertical_align=ft.VerticalAlignment.CENTER,
            text_style=ft.TextStyle(height=1),
            border_radius=20,
            filled=False,
        )

    def update_character_value(index, attribute, new_value):
        char = characters_list[index]
        setattr(char, attribute, new_value)  # Универсальный подход для изменения атрибута персонажа

    def create_super_custom_textfield(index, attr_name, value):
        def minus_click(e):
            value = getattr(characters_list[index], attr_name)
            update_character_value(index, attr_name, value - 1)
            text_field.value = str(value - 1)
            text_field.update()

        def plus_click(e):
            value = getattr(characters_list[index], attr_name)
            update_character_value(index, attr_name, value + 1)
            text_field.value = str(value + 1)
            text_field.update()

        text_field = ft.TextField(
            value=str(value),
            on_change=lambda e, idx=index, attr=attr_name: update_character_value(idx, attr, e.control.value),
            width=120,
            fill_color=first_color,
            border_width=0,
            text_size=30,
            text_vertical_align=-0.7,
            text_style=ft.TextStyle(height=1),
            filled=False,
        )

        btn_minus = ft.IconButton(icon=ft.icons.REMOVE, on_click=minus_click)
        btn_plus = ft.IconButton(icon=ft.icons.ADD, on_click=plus_click)

        row = ft.Row(
            controls=[text_field, btn_minus, btn_plus],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=-0.5
        )

        return ft.Container(content=row, alignment=ft.alignment.center,
                            border_radius=15, height=50, border=ft.border.all(3, first_color))

    def row_with_alignment(align: ft.MainAxisAlignment):
        return ft.Column(
            [
                ft.Text(str(align), size=16),
                ft.Container(
                    content=ft.Row(items(3), alignment=align),
                    bgcolor=ft.colors.AMBER_100,
                ),
            ]
        )

    def animate_container(color_on_hover, color_on_leave):
        def on_hover(e):
            e.control.bgcolor = color_on_hover if e.data == "true" else color_on_leave
            e.control.update()

        return on_hover

    def update_character_value(index, attribute, new_value):
        char = characters_list[index]
        if attribute == "name":
            char.name = new_value
        elif attribute == "kd":
            char.kd = int(new_value)
        elif attribute == "hp":
            char.hp = int(new_value)
        elif attribute == "initiative":
            char.initiative = int(new_value)

    def update_ui():
        characters_view.controls.clear()
        names_text = ", ".join([str(char.kd) for char in characters_list])
        page.add(ft.Text(value=names_text))
        for index, char in enumerate(characters_list):
            name_text = create_custom_textfield(index, "name", char.name)
            kd_input = create_super_custom_textfield(index, "kd", char.kd)
            hp_input = create_super_custom_textfield(index, "hp", char.hp)
            initiative_input = create_super_custom_textfield(index, "initiative", char.initiative)
            row_ch = ft.Row(
                controls=[name_text, kd_input, hp_input, initiative_input],
                alignment=ft.alignment.center, spacing=20
            )
            container_ch = ft.Container(content=row_ch, padding=ft.padding.symmetric(horizontal=10),
                                        bgcolor=first_color, height=60,
                                        border_radius=20, animate=ft.animation.Animation(duration=100,
                                                                                         curve=ft.AnimationCurve.EASE_IN_OUT),
                                        on_hover=animate_container(color_on_hover=first_color_hover,
                                                                   color_on_leave=first_color))
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
    first_color_hover = "#313240"
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

    names_col = ['Имя', 'КД', 'ХП', 'Инициатива.']
    text_cols = [ft.Text(value=i, expand=True, text_align=ft.TextAlign.CENTER) for i in names_col]
    page.add(ft.Container(ft.Row(controls=text_cols)))

    characters_view = ft.Column()
    page.add(characters_view)

    update_ui()


if __name__ == "__main__":
    ft.app(target=main)
