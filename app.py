import streamlit as st
from predict_page import show_predict_page
from explore_page import display_explore_page

page =st.sidebar.selectbox("Explore or Predict",("Explore","Predict"))


if page=="Predict":
    
    show_predict_page()
else:
    
    display_explore_page()
