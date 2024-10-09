import streamlit as st
import pandas as pd
import duckdb

st.writ("Hello world")
data = {'a' : [1,2,3], 'b' : [4,5,6]}
DF = pd.DataFrame(data)

ong1, ong2, ong3 = st.tabs(["Onglet 1","Onglet 2","Onglet 3"])

with ong1:
    st.write("Voici la table DF :")
    st.dataframe(DF)
    query=st.text_area(label= "Quelle requete souhaitez vous faire ?")
    result = duckdb.query(query)
    st.write(f'voici votre requete : {query}')
    st.dataframe(result)


with ong2:
    st.write("vous etes dans l'onglet 2")

with ong3:
    st.write("vous etes dans l'onglet 3")