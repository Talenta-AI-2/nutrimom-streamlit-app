from nutrition.nutrition_check import main as nutrition
from model.Model import get_user_id_by_username, create_gizi_harian_ibu_hamil
from model.engine.Engine import get_session
import streamlit as st
from  nutrition.nutrition_check import main as nutrition_check


def add_gizi(total_gizi, selisih_gizi):
    try:
        session = get_session()
        username = st.session_state.username
        user_id = get_user_id_by_username(session, username)
        create_gizi_harian_ibu_hamil(session, total_gizi, selisih_gizi, user_id)
        return 1
    except Exception as error:
        st.error(str(error))


def menu():
    total_gizi, selisih_gizi = nutrition_check()
    if total_gizi:
        t = add_gizi(total_gizi, selisih_gizi)
        st.write(t)