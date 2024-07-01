import locale
import streamlit as st
from datetime import date, datetime, timedelta
from streamlit_js_eval import streamlit_js_eval
from unidecode import unidecode

from db import *
from helpers import *

def reload():
    streamlit_js_eval(js_expressions="parent.window.location.reload()")
    

def button(letter):
    if st.button(letter, use_container_width=True, disabled=state.finished or letter in state.known_letters or letter in state.attempted_letters):
        if letter in remove_accents(state.answer):
            state.known_letters.add(letter)
        else:
            state.attempted_letters.add(letter)


def remove_accents(encoded):
    """Removes the accent marks, but not for Ññ"""
    decoded = "".join([c if c in "Ññ" else unidecode(c) for c in encoded])
    return decoded


state = st.session_state
st.header("Ahorcado")

# DB connection
state.conn = db_get_connection()

locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

if "fecha" not in state:
    state["fecha"] = date.today()
    state.answer = ""
    state.finished = False

if not state.answer:
    state.logged = False
    # Get a word from the db
    state.palabra_y_defs = db_get_palabra_fecha(state.conn, state.fecha)
    if not state.palabra_y_defs:
        st.write(f"No hay palabra para la fecha {state.fecha.strftime('%d de %B de %Y')}")
        state.answer = ""
    else:
        state["answer"] = state.palabra_y_defs[1].upper()
        state["known_letters"] = set()
        state.known_letters.add(remove_accents(state.answer[0]))
        state.known_letters.add(remove_accents(state.answer[-1]))
        state["attempted_letters"] = set()
        state["finished"] = False

if state.answer:
    if state.fecha == date.today():
        st.subheader("¡Palabra del día!")
    else:
        st.subheader(f"Palabra del {state.fecha.strftime('%d de %B de %Y')}")

    c0, c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12, c13, c14, c15, c16, c17, c18, c19, c20, c21, c22, c23, c24, c25, c26 = st.columns(27)
    with c0:
        button("A")
    with c1:
        button("B")
    with c2:
        button("C")
    with c3:
        button("D")
    with c4:
        button("E")
    with c5:
        button("F")
    with c6:
        button("G")
    with c7:
        button("H")
    with c8:
        button("I")
    with c9:
        button("J")
    with c10:
        button("K")
    with c11:
        button("L")
    with c12:
        button("M")
    with c13:
        button("N")
    with c14:
        button("Ñ")
    with c15:
        button("O")
    with c16:
        button("P")
    with c17:
        button("Q")
    with c18:
        button("R")
    with c19:
        button("S")
    with c20:
        button("T")
    with c21:
        button("U")
    with c22:
        button("V")
    with c23:
        button("W")
    with c24:
        button("X")
    with c25:
        button("Y")
    with c26:
        button("Z")

    if state.attempted_letters:
        st.write("Intentadas: " + " ".join(sorted(state.attempted_letters, key=lambda x: remove_accents(x))))

    shown_word = ""
    all_known = True
    for i in range(len(state.answer)):
        if remove_accents(state.answer[i]) in state.known_letters:
            shown_word += state.answer[i]
        else:
            shown_word += '_'
            all_known = False

    st.subheader(shown_word)

    attempts = len(state.attempted_letters)

    if all_known:
        st.header("¡Acertaste!")
        st.audio("media/win.mp3", loop=False, autoplay=True)
        state.finished = True

    if attempts == 6:
        st.header(f"¡Perdiste! La palabra era {state.answer}")
        st.audio("media/lose.mp3", loop=False, autoplay=True)
        state.finished = True

    if attempts > 0:
        with st.sidebar:
            st.image(f"media/hanged_{min(6, attempts)}.png")
            if not state.finished:
                st.audio("media/suspense_low_vol.mp3", loop=True, autoplay=True)
            st.page_link("https://github.com/AndresParraSilva/ahorcado", label="© Andrés Parra")

    if state.finished:
        if not state.logged:
            log_result(state.conn, state.palabra_y_defs[0], "".join(sorted(state.attempted_letters)))
            state.logged = True

        st.subheader(f"Acerca de {state.palabra_y_defs[1]}")
        st.write(state.palabra_y_defs[2])
        st.subheader("RAE")
        st.page_link(f"https://dle.rae.es/{state.palabra_y_defs[1]}", label=state.palabra_y_defs[1])
        st.write(state.palabra_y_defs[3])

if state.finished and state.answer and st.button("Jugar con la palabra del día anterior"):
    state.answer = ""
    state.fecha = state.fecha - timedelta(days=1)
    st.rerun()

if not state.answer and st.button("Jugar con la palabra del día"):
    state.fecha = date.today()
    st.rerun()

if state.finished:
    min_fecha, max_fecha = db_get_m_fechas(state.conn)
    min_fecha = datetime.strptime(min_fecha, "%Y-%m-%d").date()
    max_fecha = datetime.strptime(max_fecha, "%Y-%m-%d").date()
    rerun = False
    def update_fecha():
        if "sel_fecha" in state and state.sel_fecha:
            state.fecha = state.sel_fecha
            rerun = True
    st.date_input("O seleccionar día", value=max(state.fecha, min_fecha), min_value=min_fecha, max_value=date.today(), format="DD/MM/YYYY", on_change=update_fecha, key="sel_fecha")
    if rerun:
        state.answer = ""
        st.rerun()
