import re
import streamlit as st
from datetime import datetime
from openai import OpenAI, OpenAIError

from db import *


@st.cache_resource
def get_client():
    return OpenAI()