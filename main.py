import streamlit as st
from random import randint
import re


def gen_ss():
    for i in ['names', 'continue_access', 'list', 'save', 'dice_visible', 'Vika']:
        if i not in st.session_state:
            st.session_state[i] = {}


def account():
    if st.session_state.Vika:
        Vika = st.radio('Точно-точно Вика?', ['Нет', 'ДА КОНЕЧНО'], horizontal=True)
        if Vika == 'ДА КОНЕЧНО':
            st.title('ЛЮ ТЯ ТОГДА<3')
            st.balloons()


def sidebar():
    with st.sidebar:
        if st.button('Кнопка только для Вики', use_container_width=True):
            st.session_state.Vika = not st.session_state.Vika
        account()
        col1, col2 = st.columns(2)
        with col1:
            dice_multi = st.number_input('Кол-во', min_value=1)
        with col2:
            dice = st.selectbox('Кубик', ['к4', 'к6', 'к8', 'к12', 'к20', 'к100', 'Свой'])
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
        if st.session_state.dice_visible:
            st.code(st.session_state.dice_visible)


def access_continue(bool):
    st.session_state.continue_access = bool
    save_char()


def main():
    gen_ss()
    coll1, coll2 = st.columns([3, 1])
    with coll1:
        names = re.split(r'\s*,\s*|\s*,\s*', st.text_input('', value='1,2,3,4,5,6',
                                                           label_visibility='collapsed', on_change=access_continue,
                                                           args=[False]))
    with coll2:
        st.button('Продолжить', use_container_width=True, on_click=access_continue, args=[True])
    if st.session_state.continue_access and st.session_state.names != ['']:
        text_to_names(names)


def text_to_names(names):
    for name in names:
        if name not in st.session_state.list:
            st.session_state.list[name] = [15, 15, 0, 0]
    return buttons(names)


def r_and_sort(names, bool):
    if bool:
        for i in names:
            st.session_state.list[i][-1] = randint(1, 20)
    st.session_state.names = sorted(names,
                                    key=lambda key: st.session_state.list[key][-1],
                                    reverse=True)
    save_char()


def next_turn():
    st.session_state.names = st.session_state.names[1:] + [st.session_state.names[0]]


def buttons(names):
    if not st.session_state.names or set(st.session_state.names) != set(names):
        st.session_state.names = names
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button('Случайная инициатива', use_container_width=True, on_click=r_and_sort, args=[names, True]):
            r_and_sort(names, True)
    with col2:
        if st.button('Сортировать', use_container_width=True, on_click=r_and_sort, args=[names, False]):
            r_and_sort(names, False)
    with col3:
        if st.button('Следующий ход', use_container_width=True):
            next_turn()
    return add_obj(names)


def num_input(i, columns, place):
    return st.number_input('',
                           key=st.session_state.names[i] + str(columns[place + 1]),
                           value=st.session_state.list[st.session_state.names[i]][place],
                           label_visibility='collapsed')


def save_char():
    for i in st.session_state.save.keys():
        st.session_state.list[i] = st.session_state.save[i]


def add_obj(names):
    columns = ['Имя', 'КД', 'ХП', 'Безумие', 'Инициатива']
    plan = [3, 3, 3, 3, 3]
    cols = st.columns(plan)
    for i in range(len(cols)):
        with cols[i]:
            st.write(columns[i])
    for i in range(len(names)):
        with st.container():
            cols = st.columns(plan)
            with cols[0]:
                st.write(st.session_state.names[i])
            with cols[1]:
                defence = num_input(i, columns, 0)
            with cols[2]:
                life = num_input(i, columns, 1)
            with cols[3]:
                ini = num_input(i, columns, 2)
            with cols[4]:
                mad = num_input(i, columns, 3)

            st.session_state.save[st.session_state.names[i]] = [defence, life, ini, mad]


if __name__ == '__main__':
    main()
    sidebar()
