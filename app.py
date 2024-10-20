# pylint: disable=(missing-module-docstring)


import duckdb
import streamlit as st

con = duckdb.connect(database="data/exercises_sql_tables.duckdb", read_only=False)

# solution_df = duckdb.query(ANSWER_STR).df()

with st.sidebar:
    option = st.selectbox(
        "What would you ike to review ?",
        ("cross_joins", "group_by", "window_functions"),
        placeholder="Select a theme...",
        index=None,
    )
    if option:
        st.write(f"You selected : {option}")
    exercise = con.execute(f"SELECT * FROM memory_state where theme = '{option}'").df()
    if not exercise.empty:
        st.dataframe(exercise)


st.header("entrer votre code : ")
query = st.text_area(label="Votre code SQL ici", key="user_input")

if query:
    result = con.execute(query)
    st.dataframe(result)
#    try:
#        result = result[solution_df.columns]
#        st.dataframe(result.compare(solution_df))
#    except KeyError as e:
#        st.write(f"Erreur de colonne : {e}")
#        liste = []
#        diff_lin = solution_df.shape[0] - result.shape[0]
#        for columns in solution_df.columns:
#            if columns not in result.columns:
#                liste.append(columns)
#
#        if liste:
#            st.write("il manque les colonnes suivantes : ")
#            for columns in liste:
#                st.write(f"-------{columns}")
#        elif diff_lin != 0:
#            st.write(f"il y a un écart de {diff_lin} lignes")
#
#        else:
#            st.write("Veuillez remonter cette erreur au support : support@support.com ")

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
        exercise_answer = exercise.loc[0, "answer"]
        with open(f"answer/{exercise_answer}", "r", encoding="utf-8") as f:
            answer = f.read()
            st.write(answer)
