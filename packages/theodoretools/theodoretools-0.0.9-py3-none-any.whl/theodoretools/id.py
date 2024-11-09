import datetime
import random
import os
import streamlit as st


def generate_unique_id():
    current_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    random_number = random.randint(1000, 9999)

    return f"{current_time}{random_number}"


def get_st_session_id():
    if os.getenv('ST_SESSION_ID'):
        return os.getenv('ST_SESSION_ID')
    
    if "id" not in st.session_state:
        id = generate_unique_id()
        st.session_state.id = id
    else:
        id = st.session_state.id

    return id
