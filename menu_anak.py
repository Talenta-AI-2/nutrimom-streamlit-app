import streamlit as st
import sys
from stunting.stunting import main as cek_stunting
from model.Model import (get_user_id_by_username, create_anak, get_anak_by_user_id, get_tanggal_lahir_by_name,
                         get_anak_id_by_name, create_pertumbuhan_anak)
from model.engine.Engine import get_session
from utils.age import age_months


def add_anak(name, tanggal_lahir):
    try:
        session = get_session()
        username = st.session_state.username
        user_id = get_user_id_by_username(session, username)
        # user_id = 1

        create_anak(session, user_id, name, tanggal_lahir)
    except Exception as error:
        st.error(str(error))


def getAnak():
    session = get_session()
    username = st.session_state.username
    user_id = get_user_id_by_username(session, username)
    query = get_anak_by_user_id(session, user_id)
    data = [{str(anak.name): anak.id} for anak in query]
    return data


def add_pertumbuhan_anak(nama_anak, umur, tinggi, prediksi):
    try:
        session = get_session()
        anak_id = get_anak_id_by_name(session, nama_anak)
        create_pertumbuhan_anak(session, anak_id, umur, tinggi, prediksi)
    except Exception as error:
        st.error(str(error))


def getUmurBulan(nama):
    session = get_session()
    tanggal_lahir = get_tanggal_lahir_by_name(session, nama)
    umur_bulan = age_months(tanggal_lahir)
    return umur_bulan, tanggal_lahir


def form_add_anak():
    st.header("Add Anak")
    with st.form(key='add_anak_form'):
        nama = st.text_input("Nama")
        tanggal_lahir = st.date_input("Tanggal Lahir")
        print(tanggal_lahir)
        submit_button = st.form_submit_button(label='Add')
        if submit_button:
            add_anak(nama, tanggal_lahir)
            st.success(f"Berhasil menambah data {nama}")


def menu_anak():
    tab1,tab2 = st.tabs(["Add Anak", 'Cek Kondisi'])
    with tab1:
        form_add_anak()
    with tab2:
        st.header("Prediksi Stunting")

        st.subheader("Masukkan Data", divider='rainbow')
        anak = getAnak()
        nama_anak = [list(d.keys())[0] for d in anak]
        option = st.selectbox("Pilih anak:", nama_anak)
        umur, tanggal = getUmurBulan(option)

        height, prediction = cek_stunting(umur)
        if(prediction):
            print(1)
            add_pertumbuhan_anak(option,umur,height,prediction.title())
