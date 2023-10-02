import streamlit as st
import pandas as pd
 
st.write("""
# My first app
Hello *world!*
""")

st.write("""
# testing hehe
    below is our dataset
""")
 
df = pd.read_csv("Datasets/collapsed_spotify_result_2020s.csv")
df_test = df.head(20)
st.dataframe(df_test)