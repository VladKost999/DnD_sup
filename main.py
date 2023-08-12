import streamlit as st
from random import randint
import re

st.set_page_config(page_title="DnD", page_icon="🧩")
dices = ['к4', 'к6', 'к8', 'к12', 'к20', 'к100', 'Свой']

if "continue_access" not in st.session_state:
    st.session_state.continue_access = False

if "dice_visible" not in st.session_state:
    st.session_state.dice_visible = 0

if "name_list" not in st.session_state:
    st.session_state.name_list = {}

if "save" not in st.session_state:
    st.session_state.save = {}

if "names" not in st.session_state:
    st.session_state.names = ''

if "last_rand" not in st.session_state:
    st.session_state.last_rand = False


def num_input(i, col, place, columns):
    return st.number_input('',
                           key=st.session_state.names[i] + str(columns[col]),
                           value=st.session_state.name_list[st.session_state.names[i]][place],
                           label_visibility='collapsed')


def add_ch():
    # st.session_state.start_val = st.session_state.name_list
    first_names = st.session_state.name_list.keys()
    for name in st.session_state.names:
        if name not in first_names:
            st.session_state.name_list[name] = [15, 15, 0]
    st.code(st.session_state.name_list)

    #     Display charters

    columns = ['Имя', 'Броня', 'ХП', 'Иниц.']
    len_col = len(columns)
    cols = st.columns([3, 2, 2, 2])
    for i in range(len_col):
        with cols[i]:
            st.write(columns[i])
    for i in range(len(st.session_state.names)):
        with st.container():
            with cols[0]:
                st.write(st.session_state.names[i])
            with cols[1]:
                defence = num_input(i, 1, 0, columns)
            with cols[2]:
                life = num_input(i, 2, 1, columns)
            with cols[3]:
                ini = num_input(i, 3, 2, columns)
            st.session_state.save[st.session_state.names[i]] = [defence, life, ini]

    def save_char():
        for i in st.session_state.save.keys():
            st.session_state.name_list[i] = st.session_state.save[i]

    butt = st.button('Сохранить характеристики', use_container_width=True, on_click=save_char)

    st.session_state.last_rand = st.button('Рандом характеристики', use_container_width=True)


with st.sidebar:
    col1, col2 = st.columns(2)
    with col1:
        dice_multi = st.number_input('Кол-во', min_value=1)
    with col2:
        dice = st.selectbox('Кубик', dices)
    if dice != 'Свой':
        if st.button(f'Сгенерировать {dice_multi}{dice}', use_container_width=True):
            if dice_multi > 1:
                random_dices = [randint(1, int(dice.split('к')[1])) for i in range(dice_multi)]
                st.session_state.dice_visible = (' + '.join(map(str, random_dices)) + ' = ' + str(sum(random_dices)))
            else:
                st.session_state.dice_visible = (randint(1, int(dice.split('к')[1])))
    else:
        col1, col2 = st.columns(2)
        with col1:
            ot = st.number_input('От', min_value=0)
        with col2:
            do = st.number_input('До', max_value=100)
        if st.button(f'Сгенерировать x{dice_multi}', use_container_width=True):
            if dice_multi > 1:
                random_dices = [randint(min(ot, do), max(ot, do)) for i in range(dice_multi)]
                st.session_state.dice_visible = (' + '.join(map(str, random_dices)) + ' = ' + str(sum(random_dices)))
            else:
                st.session_state.dice_visible = (randint(min(ot, do), max(ot, do)))
    st.code(st.session_state.dice_visible)

coll1, coll2 = st.columns([3, 1])


def access_continue(bool):
    st.session_state.continue_access = bool


with coll1:
    st.session_state.names = re.split(r'\s*,\s*|\s*,\s*',
                                      st.text_input('', value='Введите имена персонажей через запятую',
                                                    label_visibility='collapsed', on_change=access_continue,
                                                    args=[False]))
with coll2:
    if st.button('Продолжить', use_container_width=True):
        st.session_state.continue_access = True
if st.session_state.continue_access and st.session_state.names != ['']:
    add_ch()
