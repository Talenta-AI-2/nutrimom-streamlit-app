from model.Model import (get_tinggi_badan_and_status_by_name, get_user_id_by_username, get_anak_by_user_id)
from model.engine.Engine import get_session
import streamlit as st
import pandas as pd


def data_pertumbuhan_anak(nama):
    data = get_tinggi_badan_and_status_by_name(get_session(), nama)
    tinggi = [data_anak[0] for data_anak in data]
    status = [data_anak[1] for data_anak in data]
    tanggal = [data_anak[2] for data_anak in data]
    df = pd.DataFrame({
        'Tinggi': tinggi,
        'Status': status,
        'Day': tanggal
    })
    return df





def getAnak():
    session = get_session()
    username = st.session_state.username
    user_id = get_user_id_by_username(session, username)
    query = get_anak_by_user_id(session, user_id)
    data = [{str(anak.name): anak.id} for anak in query]
    return data


# def get_data_nutrisi(start_date, end_date):
#     username = st.session_state.username
#     session = get_session()
#     user_id = get_user_id_by_username(session, username)
#     data_nutrisi = get_data_nutrisi(start_date,end_date)
#
#     return data_nutrisi
#
#
# def vizualize_nutrisi_ibu():
#     col1, col2 = st.columns(2)
#     with col1:
#         start_date = st.date_input("Start Date")
#     with col2:
#         end_date = st.date_input("End Date")
#     st.html(f"<h5 style: 'text-align:center'>Nutrisi Harian Ibu ({start_date}~~~~{end_date})</h5>")
#     chart1, chart2 = st.columns(2)
#     data = get_data_nutrisi(start_date,end_date)
#     with chart1:
#         st.write(data)



def main():
    st.html("<h1 style: 'text-align:center'>Selamat Datang Di UmiMom</h1>")
    st.write("""
        ### Aplikasi Kesehatan untuk Ibu Hamil dan Balita
        Aplikasi ini untuk membantu mengatasi stunting dari masa kandungan sampai balita.
        """)

    st.header('Statistic', divider='rainbow')
    anak = getAnak()
    nama_anak = [list(d.keys())[0] for d in anak]
    option = st.selectbox("Pilih anak:", nama_anak)
    data = data_pertumbuhan_anak(option)
    st.html(f"<h5 style: 'text-align:center'>Pertumbuhan Tinggi dan Status Nutrisi {option}</h5>")

    st.bar_chart(data=data, x='Day', y='Tinggi', color='Status')
    st.divider()
    # vizualize_nutrisi_ibu()