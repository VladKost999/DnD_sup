import flet as ft
import os
from random import randint


class Character:
    def __init__(self, name, kd, hp, initiative, active):
        self.name = name
        self.kd = kd
        self.hp = hp
        self.initiative = initiative
        self.active = active
        self.btn_visible = True


def main(page: ft.Page):
    def on_window_resize(e):
        current_width = e.control.width
        update_ui()

    page.drawer = ft.NavigationDrawer(
        controls=[
            ft.Container(height=12),
            ft.NavigationDrawerDestination(
                label="Item 1",
                icon=ft.icons.DOOR_BACK_DOOR_OUTLINED,
                selected_icon_content=ft.Icon(ft.icons.DOOR_BACK_DOOR),
            ),
            ft.Divider(thickness=2),
            ft.NavigationDrawerDestination(
                icon_content=ft.Icon(ft.icons.MAIL_OUTLINED),
                label="Item 2",
                selected_icon=ft.icons.MAIL,
            ),
            ft.NavigationDrawerDestination(
                icon_content=ft.Icon(ft.icons.PHONE_OUTLINED),
                label="Item 3",
                selected_icon=ft.icons.PHONE,
            ),
        ],
    )


    page.title = 'DnD sup'
    page.window_resizable = True
    page.scroll = ft.ScrollMode.ADAPTIVE
    page.window_min_width = 550
    page.on_resize = on_window_resize
    page.adaptive = True
    page.padding = ft.padding.symmetric(horizontal=20)
    page.vertical_alignment = ft.alignment.top_center
    page.theme_mode = ft.ThemeMode.DARK
    bg_color = '#0e1117'
    first_color = "#262730"
    first_color_hover = "#313240"
    mini_ui = page.platform == ft.PagePlatform.ANDROID
    if mini_ui:
        page.padding = ft.padding.only(left=20, right=20, top=30)
        spacing_custom = 5
        border_custom = 3
        border_col_custom = first_color_hover
    else:
        spacing_custom = 15
        border_custom = 3
        border_col_custom = first_color

    def create_custom_textfield(index, attr_name, value):
        return ft.TextField(
            value=str(value),
            on_change=lambda e, idx=index, attr=attr_name: update_character_value(idx, attr, e.control.value),
            height=45,
            fill_color=first_color,
            border_color=border_col_custom,
            border_width=border_custom,
            text_size=25,
            expand=2,
            text_vertical_align=ft.VerticalAlignment.CENTER,
            text_style=ft.TextStyle(height=1),
            border_radius=15,
            filled=False,
        )

    def update_character_value(index, attribute, new_value):
        char = characters_list[index]
        setattr(char, attribute, new_value)

    def create_super_custom_textfield(index, attr_name, value, width_bool):
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
            input_filter=ft.NumbersOnlyInputFilter(),
            expand=1,
            width=120,
            fill_color=first_color,
            border_width=0,
            text_size=25,
            text_vertical_align=-0.7,
            text_align=ft.TextAlign.START if width_bool else ft.TextAlign.CENTER,
            text_style=ft.TextStyle(height=1),
            filled=False,
        )

        btn_minus = ft.IconButton(icon=ft.icons.REMOVE, on_click=minus_click,
                                  visible=width_bool, width=25, padding=-20)
        btn_plus = ft.IconButton(icon=ft.icons.ADD, on_click=plus_click,
                                 visible=width_bool, width=25, padding=-20)

        row = ft.Row(
            controls=[text_field, btn_minus, btn_plus],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=-0.5
        )

        return ft.Container(content=row, alignment=ft.alignment.center, expand=True,
                            border_radius=15, height=45, border=ft.border.all(border_custom, border_col_custom))

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

    def deactivate_character(e, index):
        char = characters_list[index]
        char.active = False
        update_ui()

    def close_dlg(e):
        rotate_device_alert.open = False
        page.update()

    rotate_device_alert = ft.AlertDialog(
        modal=True,
        title=ft.Text("Измените ориентацию устройства"),
        content=ft.Text("Для вашего же удобства, пожалуйста, переверните ваше устройство."),
        actions=[
            ft.TextButton(text="OK", on_click=close_dlg),
        ]
    )
    if page.platform == ft.PagePlatform.ANDROID:
        page.dialog = rotate_device_alert
        rotate_device_alert.open = True
        page.update()

    def update_ui():
        characters_view.controls.clear()
        btn_visible = page.width >= 750
        for index, char in enumerate(characters_list):
            if char.active:
                name_text = create_custom_textfield(index, "name", char.name)
                kd_input = create_super_custom_textfield(index, "kd", char.kd, btn_visible)
                hp_input = create_super_custom_textfield(index, "hp", char.hp, btn_visible)
                initiative_input = create_super_custom_textfield(index, "initiative", char.initiative,
                                                                 btn_visible)
                delete_btn = ft.IconButton(icon=ft.icons.DELETE, expand=False, icon_color='red',
                                           on_click=lambda e, idx=index: deactivate_character(e, idx),
                                           width=25, padding=-20)
                row_ch = ft.Row(
                    controls=[name_text, kd_input, hp_input, initiative_input, delete_btn],
                    alignment=ft.alignment.center, spacing=spacing_custom
                )
                container_ch = ft.Container(content=row_ch, padding=ft.padding.symmetric(horizontal=10),
                                            bgcolor=first_color, height=50,
                                            border_radius=20, animate=ft.animation.Animation(duration=100,
                                                                                             curve=ft.AnimationCurve.EASE_IN_OUT),
                                            on_hover=animate_container(color_on_hover=first_color_hover,
                                                                       color_on_leave=first_color))
                characters_view.controls.append(container_ch)
        page.update()

    def add_character(e):
        new_name = name_input.value.strip()
        existing_character = next(
            (char for char in characters_list if char.name.lower() == new_name.lower() and not char.active), None)
        if existing_character:
            existing_character.active = True
            existing_character.initiative = 0
        else:
            character = Character(
                name=new_name,
                kd=15,
                hp=20,
                initiative=0,
                active=True
            )
            characters_list.append(character)
        name_input.value = ""
        name_input.update()
        update_ui()

    def show_drawer(e):
        e.control.icon = ft.icons.MENU_OPEN
        page.drawer.open = True
        page.drawer.update()

    characters_list = []

    menu_button = ft.FloatingActionButton(icon=ft.icons.MENU,
                                          height=50,
                                          elevation=0,
                                          on_click=show_drawer)
    name_input = ft.TextField(label="Имя персонажа",
                              fill_color=first_color,
                              border_color=first_color,
                              border_radius=20,
                              on_submit=add_character,
                              expand=True, height=50)
    add_button = ft.FloatingActionButton(icon=ft.icons.ADD,
                                         height=50,
                                         elevation=0,
                                         on_click=add_character)
    input_row = ft.Row(controls=[menu_button, name_input, add_button])
    input_container = ft.Container(content=input_row, padding=ft.padding.only(top=20))
    page.add(input_container)

    def sort_ini():
        def sort_ini_init(e):
            characters_list.sort(key=lambda char: char.initiative, reverse=True)
            update_ui()

        return sort_ini_init

    def rand_ini(e):
        for char in characters_list:
            char.initiative = randint(1, 20)
        sort_ini()(e)
        update_ui()

    def next_turn(e=None):
        if characters_list:
            char = characters_list.pop(0)
            characters_list.append(char)
            update_ui()

    rand_ini_btn = ft.ElevatedButton(text='Случ.ИНИ', expand=True, bgcolor=first_color, on_click=rand_ini)
    sort_ini_btn = ft.ElevatedButton(text='Сортировать', expand=True, bgcolor=first_color, on_click=sort_ini())
    next_turn_btn = ft.ElevatedButton(text='След. Ход', expand=True, bgcolor=first_color, on_click=next_turn)
    btn_row = ft.Row(controls=[rand_ini_btn, sort_ini_btn, next_turn_btn])
    page.add(ft.Container(content=btn_row))

    name_title = ft.Text(value="Имя", expand=2, text_align=ft.TextAlign.CENTER)
    kd_title = ft.Text(value="КД", expand=1, text_align=ft.TextAlign.CENTER)
    hp_title = ft.Text(value="ХП", expand=1, text_align=ft.TextAlign.CENTER)
    ini_title = ft.Text(value="ИНИ", expand=1, text_align=ft.TextAlign.CENTER)
    text_cols = [name_title, kd_title, hp_title, ini_title]
    page.add(
        ft.Container(ft.Row(controls=text_cols, spacing=spacing_custom), padding=ft.padding.only(left=10, right=60)))

    characters_view = ft.Column()
    page.add(characters_view)

    update_ui()


if __name__ == "__main__":
    ft.app(target=main)
