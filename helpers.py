import re
import socket
import streamlit as st
from datetime import datetime

from db import *


def log_result(conn, palabra_id, falladas):
    db_insert_log(conn, palabra_id, falladas, datetime.now())
