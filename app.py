import pandas as pd
import duckdb
import streamlit as st
import io

csv='''
beverage,price
orange juice,2.5
Expresso,2
Tea,3
'''
beverages=pd.read_csv(io.StringIO(csv))

csv2='''
food_item,food_price
cookie juice,2.5
chocolatine,2
muffin,3
'''
food_items=pd.read_csv(io.StringIO(csv2))

answer = """
SELECT * FROM beverages
CROSS JOIN food_items
"""
solution = duckdb.query(answer).df()

with st.sidebar:
    option=st.selectbox("What would you ike to review ?",
                        ("Joins","GroupBy","Windows Functions"),
                        placeholder='Select a theme...',
                        index=None)
    st.write(f"You selected : {option}")


st.header("entrer votre code : ")
query=st.text_area(label="Votre code SQL ici",key="user_input")

if query:
    result = duckdb.query(query).df()
    st.dataframe(result)

tab2,tab3 = st.tabs(("Tables","Solution"))

with tab2:
    st.write("table: beverages")
    st.dataframe(beverages)
    st.write("table: food_items")
    st.dataframe(food_items)
    st.write("expected : ")
    st.dataframe(solution)


with tab3:
    st.write(answer)
