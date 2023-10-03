import streamlit as st
import pandas as pd
 
st.write("""
# generate your personalised album!
""")

sentence_input = st.text_input("how was your day?")
print(sentence_input)


st.write(""" 
your input:
""")
st.write(sentence_input)

spotify_link_input = st.text_input("paste your favourite spotify album's link here!")
print(spotify_link_input)


 
# df = pd.read_csv("Datasets/collapsed_spotify_result_2020s.csv")
# df_test = df.head(20)
# st.dataframe(df_test)


