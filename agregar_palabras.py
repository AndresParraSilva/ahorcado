import random
import re
import streamlit as st
from datetime import date, timedelta
from openai import OpenAI, OpenAIError
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from time import sleep

from db import *
from helpers import *


@st.cache_resource
def get_client():
    return OpenAI()


state = st.session_state
st.header("Agregar palabras")

# DB connection
state.conn = db_get_connection()

if "nueva_palabra" not in state or st.button("Siguiente"):
    # Get a word from the dictionary
    with open("media/dictionary.txt", 'r') as file:
        line = random.choice(file.readlines())
    state["nueva_palabra"] = line.strip()
    state["definicion_rae"] = ""
    state["definicion_ia"] = ""

st.subheader(state.nueva_palabra)
if st.button("Tomar definición de la RAE"):
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-extensions')
    options.add_argument("user-data-dir=selenium_work_dir")
    driver = webdriver.Chrome(options=options)

    url = f"https://dle.rae.es/{state.nueva_palabra}"
    driver.get(url)
    # sleep(1)

    elem=driver.find_element(By.XPATH,"//meta[@name='description']")
    state.definicion_rae = elem.get_attribute("content")
    if state.definicion_rae == "Versión electrónica 23.7 del «Diccionario de la lengua española», obra lexicográfica académica por excelencia.":
         state.definicion_rae = "No encontrada"

    pattern = r'(^Definición RAE de «.+» según el Diccionario de la lengua española: )'
    state.definicion_rae = re.sub(pattern, '', state.definicion_rae)
    driver.quit()

if state.definicion_rae:
    st.write(state.definicion_rae)

if st.button("Generar definición IA"):
        message_list = []
        message_list.append({"role": "system", "content": """Eres un catedrático español especialista en diccionarios. Tu tarea es, ante una palabra, responder su definición lo más detalladamente posible, incluyendo su etimología y datos curiosos solo si los hubiera. No menciones "en español", ya que se sobreentiende. No agregues títulos para "etimología" ni para "curiosidad" o "curiosidades". No incluyas el cierre "en resumen...". Si no reconoces la palabra, responde "No conozco esa palabra"."""})
        message_list.append({"role": "user", "content": "desmalazada"})
        message_list.append({"role": "assistant", "content": "No conozco esa palabra."})
        message_list.append({"role": "user", "content": "desmazalado"})
        message_list.append({"role": "assistant", "content": """La palabra "desmazalado" es un adjetivo que significa "falto de maña, habilidad o destreza". Se utiliza para describir a una persona que es torpe o que no tiene la habilidad adecuada para realizar una determinada tarea.

La palabra "desmazalado" proviene del prefijo "des-" que indica negación o privación, y del sustantivo "mazal" que es un término menos común que puede estar relacionado con la maña o la habilidad. Por tanto, "desmazalado" literalmente se refiere a alguien que carece de esas habilidades.
"""})
        message_list.append({"role": "user", "content": "copete"})
        message_list.append({"role": "assistant", "content": """La palabra "copete" tiene varias acepciones según su uso contextual, pero generalmente se refiere a una parte superior prominente o decorativa en diferentes contextos.

1. **En anatomía o zoología:** Se refiere al penacho de plumas que algunos pájaros tienen en la cabeza, como el copete de las gallinas. También puede referirse al pelo elevado o abultado en el peinado de una persona, usualmente en la parte frontal de la cabeza.

2. **En arquitectura:** Se utiliza para nombrar la parte superior de un edificio o construcción que tiene una forma decorativa o destacada.

3. **En imprenta y redacción:** Puede referirse al encabezado de una página o de un documento, donde se colocan títulos, subtítulos o encabezados.

4. **En hostelería y bebidas:** En algunos países de América Latina, "copete" también puede referirse al borde de una bebida espumosa, como el que se forma en la cerveza o en los cócteles.

La palabra "copete" proviene del latín vulgar *cuppa*, que significa "copa", debido a la similitud en la forma abultada y prominente. Aunque no directamente relacionado con la "copa" de beber, sí guarda relación con algo que destaca en forma prominente.

En la cultura popular, especialmente en los años 50 y 60, los peinados con copete eran muy comunes y se han convertido en un ícono de esa época, asociados con figuras como Elvis Presley o el estilo rockabilly."""})
        message_list.append({"role": "user", "content": state.nueva_palabra})
 
        client = get_client()
        with st.chat_message("assistant"):
            stream = client.chat.completions.create(
                model="gpt-4o",
                temperature=1.0,
                messages=message_list,
                stream=True
            )
        state.definicion_ia = st.write_stream(stream)
elif state.definicion_ia:
    st.write(state.definicion_ia)

def update_definicion_ia():
    state.definicion_ia = state.nueva_definicion_ia

if state.definicion_ia and st.button("Editar"):
    st.text_area("Definición IA", on_change=update_definicion_ia, label_visibility="hidden", value=state.definicion_ia, key="nueva_definicion_ia")

def agregar(fecha):
    nuevo_id = db_insert_palabra(state.conn, state.nueva_palabra, state.definicion_ia, state.definicion_rae, fecha)
    st.write(f"{state.nueva_palabra} agregada con id {nuevo_id} con fecha {fecha}")

if state.definicion_rae and state.definicion_ia:
    min_fecha, max_fecha = db_get_m_fechas(state.conn)
    min_fecha = datetime.strptime(min_fecha, "%Y-%m-%d").date()
    max_fecha = datetime.strptime(max_fecha, "%Y-%m-%d").date()
    if st.button(f"Agregar al {min_fecha - timedelta(days=1)}"):
        agregar(min_fecha - timedelta(days=1))
    if st.button(f"Agregar al {max_fecha + timedelta(days=1)}"):
        agregar(max_fecha + timedelta(days=1))
