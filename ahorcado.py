import random
import streamlit as st

from base64 import b64decode
from streamlit_js_eval import streamlit_js_eval
from unidecode import unidecode


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


st.header("Ahorcado")

state = st.session_state
if "answer" not in state or state.answer == "":
    # Get a word from the dictionary
    with open("media/dictionary.txt", 'r') as file:
        line = random.choice(file.readlines())
    state["answer"] = line.strip().upper()

    state["known_letters"] = set()
    state.known_letters.add(remove_accents(state.answer[0]))
    state.known_letters.add(remove_accents(state.answer[-1]))
    state["attempted_letters"] = set()
    state["finished"] = False

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

if all_known:
    st.header("¡Acertaste!")
    st.audio("media/win.mp3", loop=False, autoplay=True)
    state.finished = True

attempts = len(state.attempted_letters)

if attempts == 6:
    st.header(f"¡Perdiste! La palabra era {state.answer}")
    st.audio("media/lose.mp3", loop=False, autoplay=True)
    state.finished = True

if attempts > 0:
    with st.sidebar:
        st.image(f"media/hanged_{min(6, attempts)}.png")
        if not state.finished:
            st.audio("media/suspense_low_vol.mp3", loop=True, autoplay=True)

if state.finished and st.button("Volver a jugar"):
    state.answer = ""
    reload()
