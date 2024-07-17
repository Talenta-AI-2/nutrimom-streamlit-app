import streamlit as st
import urllib.request
import json
import os
import ssl
import time
from dotenv import load_dotenv
load_dotenv('.env')
def allowSelfSignedHttps(allowed):
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context


allowSelfSignedHttps(True)


def call_azure_ml_service(age, gender, height):
    data = {
        "input_data": {
            "columns": [
                "Umur (bulan)",
                "Jenis Kelamin",
                "Tinggi Badan (cm)"
            ],
            "index": [0],
            "data": [
                [age, gender, height]
            ]
        }
    }

    body = str.encode(json.dumps(data))

    url =  os.getenv('STUNTING_URL')
    api_key = os.getenv('STUNTING_KEY')

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + api_key,
        'azureml-model-deployment': 'stunting-v1-1'
    }

    req = urllib.request.Request(url, body, headers)

    try:
        response = urllib.request.urlopen(req)
        result = response.read().decode('utf-8')
        return json.loads(result)
    except urllib.error.HTTPError as error:
        st.error(f"The request failed with status code: {error.code}")
        st.error(error.read().decode("utf8", 'ignore'))
        return None


def get_nutrition_recommendations(age_in_months, result):

    recommendations = {
        "severely stunted": {
            (0, 5): {"Energi (kkal)": 550, "Protein (g)": 9, "Lemak Total (g)": 31, "Karbohidrat (g)": 59,
                     "Air (ml)": 700},
            (6, 11): {"Energi (kkal)": 800, "Protein (g)": 15, "Lemak Total (g)": 35, "Karbohidrat (g)": 105,
                      "Air (ml)": 900},
            (12, 35): {"Energi (kkal)": 1350, "Protein (g)": 20, "Lemak Total (g)": 45, "Karbohidrat (g)": 215,
                       "Air (ml)": 1150},
            (36, 71): {"Energi (kkal)": 1400, "Protein (g)": 25, "Lemak Total (g)": 50, "Karbohidrat (g)": 220,
                       "Air (ml)": 1450},
        },
        "stunted": {
            (0, 5): {"Energi (kkal)": 550, "Protein (g)": 9, "Lemak Total (g)": 31, "Karbohidrat (g)": 59,
                     "Air (ml)": 700},
            (6, 11): {"Energi (kkal)": 800, "Protein (g)": 15, "Lemak Total (g)": 35, "Karbohidrat (g)": 105,
                      "Air (ml)": 900},
            (12, 35): {"Energi (kkal)": 1350, "Protein (g)": 20, "Lemak Total (g)": 45, "Karbohidrat (g)": 215,
                       "Air (ml)": 1150},
            (36, 71): {"Energi (kkal)": 1400, "Protein (g)": 25, "Lemak Total (g)": 50, "Karbohidrat (g)": 220,
                       "Air (ml)": 1450},
        }
    }

    age_group = None
    if 0 <= age_in_months <= 5:
        age_group = (0, 5)
    elif 6 <= age_in_months <= 11:
        age_group = (6, 11)
    elif 12 <= age_in_months <= 35:
        age_group = (12, 35)
    elif 36 <= age_in_months <= 71:
        age_group = (36, 71)

    if age_group:
        return recommendations[result].get(age_group, "Tidak ada rekomendasi untuk kelompok umur ini.")
    else:
        return "Umur tidak valid."


def main(umur):
    # st.title("Prediksi Stunting")

    # st.header("Masukkan Data")
    age = st.number_input("Umur (bulan)", umur)
    gender = st.selectbox("Jenis Kelamin", ["Laki-laki", "Perempuan"])
    height = st.number_input("Tinggi Badan (cm)", min_value=0.0)
    hasil = ''
    # Custom CSS for button styling
    st.markdown(
        """
        <style>
        div.stButton > button {
            background-color: white;
            color: black;
            font-weight: bold;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    if st.button("Prediksi"):
        with st.spinner('Memproses...'):
            result = call_azure_ml_service(age, gender, height)
            time.sleep(2)
            if result:
                st.success("Prediksi berhasil!")
                try:
                    prediction = result[0]
                    hasil = prediction
                    st.markdown(
                        f"<h1 style='text-align: center; color: white; font-size: 60px; font-weight: bold;'>{prediction.title()}</h1>",
                        unsafe_allow_html=True)

                    if prediction in ["severely stunted", "stunted"]:
                        if age <= 5:
                            st.markdown(
                                "<p style='background-color: black; color: white; font-size: 20px; font-weight: bold; padding: 10px;'>Buah hatimu kekurangan susu ASI, perhatikan asupan gizimu dan buah hatimu</p>",
                                unsafe_allow_html=True)
                        elif prediction == "severely stunted":
                            st.markdown(
                                "<p style='background-color: black; color: white; font-size: 20px; font-weight: bold; padding: 10px;'>Gizi buah hatimu sangat rendah dari gizi normal, perhatikan kebutuhan gizi buah hatimu!</p>",
                                unsafe_allow_html=True)
                        elif prediction == "stunted":
                            st.markdown(
                                "<p style='background-color: black; color: white; font-size: 20px; font-weight: bold; padding: 10px;'>Gizi buah hatimu kurang dari gizi normal, penuhi kebutuhan gizi buah hatimu!</p>",
                                unsafe_allow_html=True)

                        recommendations = get_nutrition_recommendations(age, prediction)
                        # st.write(recommendations)
                        st.subheader("Rekomendasi Gizi:")
                        recommendation_html = "<div style='background-color: black; padding: 10px;'>"
                        if umur>= 72:
                            recommendation_html += f"<span style='color: white; font-size: 18px; font-weight: bold; padding-right: 100px;'>Segera temui dokter!</span> &nbsp;&nbsp;&nbsp;"
                        else:
                            for nutrient, value in recommendations.items():
                                recommendation_html += f"<span style='color: white; font-size: 18px; font-weight: bold; padding-right: 100px;'>{nutrient}: {value}</span> &nbsp;&nbsp;&nbsp;"
                        recommendation_html += "</div>"
                        st.markdown(recommendation_html, unsafe_allow_html=True)


                except (KeyError, IndexError, TypeError) as e:
                    st.error("Struktur data hasil tidak sesuai.")
            else:
                st.error("Gagal mendapatkan prediksi. Coba lagi.")
    return height, hasil

if __name__ == "__main__":
    main()
