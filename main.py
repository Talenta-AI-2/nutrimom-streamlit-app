from streamlit_option_menu import option_menu
from menu_anak import menu_anak
from chatbot.chatbot import main as chatbot
import streamlit as st
from search.search import main as search
from menu_nutrition import menu
from Dashboard import  main as dashboard
def main():
    with st.sidebar:
        selected = option_menu(
            menu_title='Nutrimom',
            options=['Home', 'Nutrition', 'Child', 'Consultaton', 'Search']
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
