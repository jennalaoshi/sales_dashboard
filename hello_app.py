import streamlit as st

st.title("My First Streamlit Dashboard")

st.write("Hello! This is my first Streamlit app.")

name = st.text_input("Enter your name")

if name:
    st.write(f"Welcome, {name}!")
