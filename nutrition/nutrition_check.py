import streamlit as st
from nutrition.nutrition import calculate_nutritional_needs
from nutrition.database import get_nutritional_info
import sqlite3
from fuzzywuzzy import process
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.transforms as transforms


# Function to fetch all food names from the database
def get_all_food_names():
    conn = sqlite3.connect('nutrition/gizi_indo.db')
    cursor = conn.cursor()
    cursor.execute("SELECT NAMA FROM indonesian_food_composition")
    food_names = [row[0] for row in cursor.fetchall()]
    conn.close()
    return food_names


def main():
    total_nutrition ={}
    selisih_gizi= {}
    st.title('Cek Kebutuhan Gizi')

    # Fetch food names from the database
    food_names = get_all_food_names()

    # Initialize session state for foods list
    if 'foods' not in st.session_state:
        st.session_state.foods = []

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

    # Columns for input
    col1, col2, col3 = st.columns(3)

    # Input for food items
    with col1:
        food_name_input = st.text_input("Masukkan nama makanan:")

        if st.button('Tambahkan') and food_name_input.strip():
            # Use fuzzy matching to find closest match
            best_match, score = process.extractOne(food_name_input, food_names)
            if score >= 60:
                nutrition_info = get_nutritional_info(best_match)
                if nutrition_info:
                    # Convert nutritional values to float
                    nutrition_info = (
                    nutrition_info[0], nutrition_info[1], float(nutrition_info[2]), float(nutrition_info[3]),
                    float(nutrition_info[4]), float(nutrition_info[5]), float(nutrition_info[6]),
                    float(nutrition_info[7]))
                    st.session_state.foods.append(nutrition_info)
                    st.success("Makanan berhasil ditambahkan.")
                    food_name_input = ""  # Clear input after adding food
                else:
                    st.warning("Makanan tidak ditemukan di database.")
            else:
                st.warning("Makanan tidak ditemukan di database. Pastikan nama makanan benar atau coba yang lain.")

    with col2:
        age_group = st.selectbox(
            "Pilih kelompok umur:",
            ["16 - 18 Tahun", "19 - 29 tahun", "30 - 49 tahun"]
        )
        if age_group == "16 - 18 Tahun":
            age_group = 1
        elif age_group == "19 - 29 tahun":
            age_group = 2
        elif age_group == "30 - 49 tahun":
            age_group = 3

    with col3:
        trimester = st.selectbox(
            "Pilih trimester kehamilan:",
            ["Trimester 1", "Trimester 2", "Trimester 3"]
        )
        if trimester == "Trimester 1":
            trimester = 1
        elif trimester == "Trimester 2":
            trimester = 2
        elif trimester == "Trimester 3":
            trimester = 3

    # Button to calculate
    if st.button('Hitung'):
        if not st.session_state.foods:
            st.warning("Tidak ada makanan yang ditambahkan. Silakan tambahkan makanan terlebih dahulu.")
            return

        total_nutrition = {
            "Air": sum(food[2] for food in st.session_state.foods),
            "Energi": sum(food[3] for food in st.session_state.foods),
            "Protein": sum(food[4] for food in st.session_state.foods),
            "Lemak": sum(food[5] for food in st.session_state.foods),
            "Karbohidrat": sum(food[6] for food in st.session_state.foods),
            "Serat": sum(food[7] for food in st.session_state.foods)
        }

        age_group_str, trimester_str, needs = calculate_nutritional_needs(age_group, trimester)

        # Calculate nutritional deficiencies
        selisih_gizi = {
            "Air": needs["Air"] - total_nutrition["Air"],
            "Energi": needs["Energi"] - total_nutrition["Energi"],
            "Protein": needs["Protein"] - total_nutrition["Protein"],
            "Lemak": needs["Lemak"] - total_nutrition["Lemak"],
            "Karbohidrat": needs["Karbohidrat"] - total_nutrition["Karbohidrat"],
            "Serat": needs["Serat"] - total_nutrition["Serat"]
        }

        # Display donut chart for each nutrient
        st.subheader('Perbandingan Total Nilai Gizi dan Selisih Kekurangan Gizi')
        nutrients = ["Energi", "Protein", "Lemak", "Karbohidrat", "Serat", "Air"]
        font_color = '#525252'
        colors = ['#1f77b4', '#aec7e8']

        fig, axes = plt.subplots(2, 3, figsize=(6, 6), subplot_kw=dict(aspect="equal"))
        fig.patch.set_facecolor('#e8f4f0')
        column_metric = st.columns(6)

        for i, nutrient in enumerate(nutrients):

            with column_metric[i]:
                st.metric(nutrient, round(total_nutrition[nutrient], 3), round(-selisih_gizi[nutrient], 3))
    return total_nutrition, selisih_gizi

if __name__ == "__main__":
    main()
