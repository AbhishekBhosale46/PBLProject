import requests
import streamlit as st
from streamlit_lottie import st_lottie
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go


fig = None


# ---FUNCTION TO LOAD LOTTIE FILES---
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


# ---LOTTIE FILES OBJECTS---
lottie_anim = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_kuhijlvx.json")
lottie_anim1 = load_lottieurl("https://assets7.lottiefiles.com/packages/lf20_pmyyjcm7.json")


# ---WEBPAGE DESIGN---
st.set_page_config(layout="wide")
st.markdown("""
        <style>
               .css-18e3th9 {
                    padding-top: 1rem;
                    
                    padding-right: 6rem;
                    
                }
               .css-1d391kg {
                    padding-top: 3.5rem;
                    padding-left: 0rem;
                    padding-right: 0rem;
                }
        </style>
        """, unsafe_allow_html=True)    # Remove whitespace from the top of the page and sidebar


# ---HEADER SECTION---
c1, c2, c3 = st.columns(3)
with c2:
    st.markdown("<h2 style='text-align: center; font-size:48px; color: #31333f;'>	&#128184; ALGO ALERT !</h2>"
               , unsafe_allow_html=True)
st.write("---")


# ---TOP COLUMN---
l, m, r = st.columns([1, 1, 1])
with l:
    st_lottie(lottie_anim, key="anim", width=270, height=300)

with m:
    st.write("##")
    st.markdown('''<h3 style='text-align: left; font-size:32px; color: #31333f;'>
                    Enter a stock ticker : 
                    </h3>''', unsafe_allow_html=True)
    ticker = st.text_input("")
    st.write("##")
    if st.button(" 👉 GO !") or ticker:
        pass

with r:
    st_lottie(lottie_anim1, key="anim1", width=410, height=310)


st.write("---")


# ---PLOTTING GRAPH---
cl1, cl2, cl3 = st.columns([1, 10, 1])
with cl2:
    if fig != None:
        st.plotly_chart(fig, use_container_width=True)



















