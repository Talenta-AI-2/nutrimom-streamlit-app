from streamlit_option_menu import option_menu
from menu_anak import menu_anak
from chatbot.chatbot import main as chatbot
import streamlit as st
from search.search import main as search
from menu_nutrition import menu
from Dashboard import  main as dashboard



def main():
    st.logo('asset/logo_new.png')
    with st.sidebar:
        selected = option_menu(
            menu_title='Nutrimom',
            options=['Home', 'Nutrition', 'Child', 'Consultaton', 'Search', 'Log Out'],
            icons=['house-fill', 'fire', 'piggy-bank-fill', 'bi-chat-left-text-fill', 'bi-search-heart-fill', 'door-closed-fill'],
            menu_icon="cast",
        )
    if selected == 'Home':
        dashboard()
    if selected == 'Nutrition':
        menu()
    if selected == 'Child':
        menu_anak()
    if selected == 'Consultaton':
        chatbot()
    if selected == 'Search':
        search()
    if selected == 'Log Out':
        st.session_state.logged_in = False
        st.session_state.username = ""
