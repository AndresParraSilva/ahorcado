import re
import socket
import streamlit as st
from datetime import datetime

from db import *


def log_result(conn, palabra_id, falladas):
    db_insert_log(conn, palabra_id, falladas, datetime.now())


def fecha_formateada(fecha):
    mes = {
        1: "enero",
        2: "febrero",
        3: "marzo",
        4: "abril",
        5: "mayo",
        6: "junio",
        7: "julio",
        8: "agosto",
        9: "septiembre",
        10: "octubre",
        11: "noviembre",
        12: "diciembre"
    }
    return f"{fecha.day} de {mes[fecha.month]} de {fecha.year}"
