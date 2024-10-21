# pylint: disable=(missing-module-docstring)


import logging
import os
import subprocess

import duckdb
import pandas as pd
import streamlit as st
from datetime import date, timedelta

from pandas import timedelta_range

if "data" not in os.listdir():
    logging.error("Create Folder Data")
    os.mkdir("data")

if "exercises_sql_tables.duckdb" not in os.listdir("data"):
    exec(open("init_db.py").read())

def check_users_solution(user_query: str, df_solution: pd.DataFrame)-> None:
    """
    Checks that the query is correct by :\n\n
    1: checking the columns\n\n
    2: checking the values
    :param user_query: a string containing the query inserted by the user
    :param df_solution: the solution of the exercise in DataFrame type
    """
    result = con.execute(user_query).df()
    st.dataframe(result)
    try:
        result = result[df_solution.columns]
        check_df = result.compare(df_solution)
        if not check_df.empty:
            st.dataframe(check_df)
    except KeyError as e:
        liste = []
        diff_lin = df_solution.shape[0] - result.shape[0]
        for columns in df_solution.columns:
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


con = duckdb.connect(database="data/exercises_sql_tables.duckdb", read_only=False)

with st.sidebar:
    available_themes = con.execute("select * from memory_state").df()["theme"].unique()
    option = st.selectbox(
        "What would you like to review ?",
        (available_themes),
        placeholder="Select a theme...",
        index=None,
    )
    if option:
        st.write(f"You selected : {option}")
    exercise = (
        con.execute(f"SELECT * FROM memory_state where theme = '{option}'")
        .df()
        .sort_values("last_review")
        .reset_index()
    )
    if not exercise.empty:
        st.dataframe(exercise)
        exercise_answer = exercise.loc[0, "answer"]
        with open(f"answer/{exercise_answer}", "r", encoding="utf-8") as f:
            answer = f.read()
            solution_df = con.execute(answer).df()


st.header("entrer votre code : ")
query = st.text_area(label="Votre code SQL ici", key="user_input")

if not exercise.empty :
    exercise_name = exercise.loc[0, "exercise_name"]
if option:
    for nb_days in [2, 7, 21]:
        if st.button(f'Revoir dans {nb_days} jours.'):
            next_review = date.today() + timedelta(days=nb_days)
            con.execute(f"update memory_state set last_review = '{next_review}' where exercise_name = '{exercise_name}'")
            st.rerun()

    if st.button('reset'):
        con.execute("update memory_state set last_review = '1970-01-01'")
        st.rerun()

if query:
    check_users_solution(query, solution_df)

tab2, tab3 = st.tabs(("Tables", "Solution"))

with tab2:
    if not exercise.empty:
        exercise_table = exercise.loc[0, "tables"]
        for table in exercise_table:
            st.write(f"table: {table}")
            tab = con.execute(f"SELECT * from {table}").df()
            st.dataframe(tab)

with tab3:
    if not exercise.empty:
        st.write(answer)
