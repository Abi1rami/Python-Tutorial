import streamlit as st

st.title("My First Streamlit App")

name = st.text_input("Enter your name")

if st.button("Submit"):
    if name:
        st.success(f"Hi {name}, Welcome to my page!")
    else:
        st.warning("Please enter your name")