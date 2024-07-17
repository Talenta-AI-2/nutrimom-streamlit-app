import streamlit as st
from model.Model import create_user, verify_user_password
from model.engine.Engine import get_session
from streamlit_extras.switch_page_button import switch_page
from utils.AuthCheck import validate_username, validate_password
from main import main

# st.set_page_config(page_title='UmiMom', page_icon='asset/logo_2.png')


if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""


def login(username, password):
    session = get_session()
    if verify_user_password(session, username, password):
        st.session_state.logged_in = True
        st.session_state.username = username
        return True
    else:
        return False


def login_form():
    with st.form(key='login_form'):
        username = st.text_input('Username')
        password = st.text_input('Password', type='password')
        submit_button = st.form_submit_button(label='Login')

        if submit_button:
            if login(username, password):
                st.success(f"Welcome {username}!")


            else:
                st.error("Invalid username or password")


def signup_form():
    with st.form(key='signup_form'):
        username = st.text_input('New Username')
        password = st.text_input('New Password', type='password')
        check_password = st.text_input('Confirm Password', type='password')

        submit_button = st.form_submit_button(label='Sign Up')

        try:
            if submit_button:
                validate_username(username)
                validate_password(password)
                session = get_session()
                if password != check_password:
                    raise ValueError("Passwords do not match")

                create_user(session, username, password)
                st.success("Signup successful! Please login.")
        except Exception as error:
            st.error(str(error))


if st.session_state.logged_in:
    main()

    # if st.button("Logout"):
    #     st.session_state.logged_in = False
    #     st.session_state.username = ""
else:
    st.title("Login and Signup")
    tab1, tab2 = st.tabs(["Login", "Signup"])
    with tab1:
        st.subheader("Login")
        login_form()

    with tab2:
        st.subheader("Sign Up")
        signup_form()
