from nutrition.nutrition_check import main as nutrition
from model.Model import get_user_id_by_username,
from model.engine.Engine import get_session
import  streamlit as st
def add_gizi(total_gizi, selisih_gzi):
    session = get_session()
    username = st.session_state.username
    user_id = get_user_id_by_username(session, username)
def menu():





