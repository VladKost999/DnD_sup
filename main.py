import streamlit as st
from random import randint
import re

st.set_page_config(page_title="Story", page_icon="🧩")
st.title('ЛЮБЛЮ ВИКУ<3')
dices = ['к4', 'к6', 'к8', 'к12', 'к20', 'к100', 'Свой']

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
                st.code(' + '.join(map(str, random_dices)) + ' = ' + str(sum(random_dices)))
            else:
                st.code(randint(1, int(dice.split('к')[1])))
    else:
        col1, col2 = st.columns(2)
        with col1:
            ot = st.number_input('От', min_value=0)
        with col2:
            do = st.number_input('До', max_value=100)
        if st.button(f'Сгенерировать x{dice_multi}', use_container_width=True):
            if dice_multi > 1:
                random_dices = [randint(ot, do) for i in range(dice_multi)]
                st.code(' + '.join(map(str, random_dices)) + ' = ' + str(sum(random_dices)))
            else:
                st.code(randint(ot, do))

names = st.text_input('Введите имена персонажей через запятую')
name_list = list(map(lambda x: [x, 15, 15, 0], re.split(r'\s*,\s*|\s*,\s*', names)))
cols = st.columns(2)
with cols[0]:
    rand_button = st.button('Случайная инициатива', use_container_width=True)
    if rand_button:
        st.session_state.story = [[*item[:3], randint(0, 20)] for item in name_list]
        st.session_state.lastClick = 0
    if st.session_state.lastClick != 1:
        st.session_state.lastClick = 0
        name_list = st.session_state.story
        name_list = sorted(name_list, key=lambda x: x[-1], reverse=True)
with cols[1]:
    turn_button = st.button('Следующий ход', use_container_width=True)
    if turn_button:
        st.session_state.story = st.session_state.story[1:] + [st.session_state.story[0]]
        st.session_state.lastClick = 1
    if st.session_state.lastClick != 0:
        st.session_state.lastClick = 1
        name_list = st.session_state.story
columns = ['Имя', 'Броня', 'ХП', 'Инициатива']
len_col = len(columns)
cols = st.columns(len_col)
for i in range(len(columns)):
    with cols[i]:
        st.write(columns[i])
for i in range(len(name_list)):
    with st.container():
        cols = st.columns(len_col)
        with cols[0]:
            st.write(name_list[i][0])
        with cols[1]:
            name_list[i][1] = st.number_input('', key=name_list[i][0] + str(columns[1]),
                                              value=name_list[i][1],
                                              label_visibility='collapsed')
        with cols[2]:
            name_list[i][2] = st.number_input('', key=name_list[i][0] + str(columns[2]),
                                              value=name_list[i][2],
                                              label_visibility='collapsed')
        with cols[3]:
            name_list[i][3] = st.number_input('', key=name_list[i][0] + str(columns[3]),
                                              value=name_list[i][3],
                                              label_visibility='collapsed')
# st.code(name_list)
# st.code(st.session_state.story)
