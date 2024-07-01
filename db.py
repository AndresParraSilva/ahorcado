import sqlite3
import streamlit as st
from datetime import date
from os import path


@st.cache_resource
def db_get_connection():
    db_exist = path.isfile('palabras.db')
    conn = sqlite3.connect('palabras.db', check_same_thread=False)
    if not db_exist:
        db_setup(conn)
    return conn


def db_setup(conn):
    conn.execute('''
            CREATE TABLE IF NOT EXISTS palabras (
                palabra_id INTEGER PRIMARY KEY,
                palabra TEXT,
                definicion_ia TEXT,
                definicion_rae TEXT,
                fecha_destacada TIMESTAMP
            )
        ''')
    def_ia = """La palabra "pingüe" es un adjetivo que describe algo muy abundante, fértil, opulento o rico. Se utiliza principalmente para destacar la abundancia o la riqueza de algo, ya sea en términos materiales o cualitativos.

Proviene del latín "pinguis," que significa "graso" o "fértil." Este término se utilizaba en latín clásico para describir tierra grasosa o fértil, y también para referirse a cosas ricas en contenido, ya fuera en términos de nutrientes, riqueza o calidad.

Curiosamente, aunque su uso no es extremadamente común en el lenguaje cotidiano, "pingüe" puede encontrarse en textos literarios o en contextos donde se quiere destacar de manera enfática la opulencia o la riqueza de algo. Se puede emplear, por ejemplo, para describir una cosecha muy abundante, un negocio extremadamente lucrativo o cualquier situación donde la abundancia y la riqueza son notables."""
    def_rae = "1. adj. Craso, gordo, mantecoso. 2. adj. Abundante, copioso, fértil."
    conn.execute(f'INSERT INTO palabras (palabra, definicion_ia, definicion_rae, fecha_destacada) VALUES (?, ?, ?, ?);', ("pingüe", def_ia, def_rae, date.today()))
    conn.commit()

def db_get_m_fechas(conn):
    cursor = conn.cursor()
    return cursor.execute("SELECT MIN(fecha_destacada) AS min_fecha, MAX(fecha_destacada) AS max_fecha FROM palabras").fetchone()

def db_insert_palabra(conn, palabra, definicion_ia, definicion_rae, fecha_destacada):
    cursor = conn.cursor()
    cursor.execute(f'INSERT INTO palabras (palabra, definicion_ia, definicion_rae, fecha_destacada) VALUES (?, ?, ?, ?);', (palabra, definicion_ia, definicion_rae, fecha_destacada))
    conn.commit()
    return cursor.lastrowid

def db_get_palabra_fecha(conn, fecha):
    cursor = conn.cursor()
    return cursor.execute("SELECT palabra_id, palabra, definicion_ia, definicion_rae FROM palabras WHERE fecha_destacada=?", (fecha, )).fetchone()
