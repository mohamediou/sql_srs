# pylint: disable=(missing-module-docstring)

import io

import duckdb
import pandas as pd
import streamlit as st

CSV = """
beverage,price
orange juice,2.5
Expresso,2
Tea,3
"""
beverages = pd.read_csv(io.StringIO(CSV))

CSV2 = """
food_item,food_price
cookie juice,2.5
chocolatine,2
muffin,3
"""
food_items = pd.read_csv(io.StringIO(CSV2))

ANSWER_STR = """
SELECT * FROM beverages
CROSS JOIN food_items
"""
solution_df = duckdb.query(ANSWER_STR).df()

with st.sidebar:
    option = st.selectbox(
        "What would you ike to review ?",
        ("Joins", "GroupBy", "Windows Functions"),
        placeholder="Select a theme...",
        index=None,
    )
    st.write(f"You selected : {option}")

st.header("entrer votre code : ")
query = st.text_area(label="Votre code SQL ici", key="user_input")

if query:
    result = duckdb.query(query).df()
    st.dataframe(result)
    try:
        result = result[solution_df.columns]
        st.dataframe(result.compare(solution_df))
    except KeyError as e:
        st.write(f"Erreur de colonne : {e}")
        liste = []
        diff_lin = solution_df.shape[0] - result.shape[0]
        for columns in solution_df.columns:
            if columns not in result.columns:
                liste.append(columns)

        if liste:
            st.write("il manque les colonnes suivantes : ")
            for columns in liste:
                st.write(f"-------{columns}")
        elif diff_lin != 0:
            st.write(f"il y a un écart de {diff_lin} lignes")

        else:
            st.write("Veuillez remonter cette erreur au support : support@support.com ")


tab2, tab3 = st.tabs(("Tables", "Solution"))

with tab2:
    st.write("table: beverages")
    st.dataframe(beverages)
    st.write("table: food_items")
    st.dataframe(food_items)
    st.write("expected : ")
    st.dataframe(solution_df)

with tab3:
    st.write(ANSWER_STR)
