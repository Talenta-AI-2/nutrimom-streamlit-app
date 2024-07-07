import sqlite3
from fuzzywuzzy import process

def get_all_food_names():
    conn = sqlite3.connect('nutrition/gizi_indo.db')
    cursor = conn.cursor()
    cursor.execute("SELECT NAMA FROM indonesian_food_composition")
    food_names = [row[0] for row in cursor.fetchall()]
    conn.close()
    return food_names

def get_nutritional_info(food_name):
    all_food_names = get_all_food_names()
    best_match, score = process.extractOne(food_name, all_food_names)
    if score < 60:
        return None

    conn = sqlite3.connect('nutrition/gizi_indo.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM indonesian_food_composition WHERE NAMA=?", (best_match,))
    result = cursor.fetchone()
    conn.close()
    return result