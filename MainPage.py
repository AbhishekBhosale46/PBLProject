import streamlit as st
from streamlit_lottie import st_lottie
import requests


def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()
lottie_anim = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_gxtah1wp.json")

st.set_page_config(layout="wide")

st.markdown('''
            <style>
            .css-18e3th9 {
            padding-top: 0.8rem;
            padding-right: 6rem;
            }
            .css-1d391kg {
            padding-top: 3rem;
            padding-left: 0rem;
            padding-right: 0rem;
            }
            </style>
            ''', unsafe_allow_html=True)

st.markdown('''
            <style>
            h1{
            text-align: center;
            font-weight: 600;
            font-size: 2.5rem;
            }
            h3{
            text-align: center;
            font-size: 1.5rem;
            }
            .css-fg4pbf {
            text-align: center;
            }
            </style>
            ''', unsafe_allow_html=True)


st.title(' 📈 ALGO ALERT 📉 ')
st.markdown('''
            <p style="text-align:center; marginbottom:0px; margin-top:10px;"> 
            <img src="https://i.postimg.cc/MKxNT9QQ/8432.jpg" class="img-fluid hover-shadow" height="270px" width="480px" alt="Cinque Terre">
            </p>
            ''', unsafe_allow_html=True)
st.write('---')

c1, c2 = st.columns(2)
with c1:
    st.subheader('Strategy 1 ')
    st.markdown('''
            <p style="text-align:center; marginbottom:12px; margin-top:12px;"> 
            <img src="https://i.postimg.cc/Dw2GGjLS/i1.png" class="img-fluid hover-shadow" height="144px" width="256" alt="Cinque Terre">
            </p>
            ''', unsafe_allow_html=True)
    st.button('Check Strategy', key='b1')
with c2:
    st.subheader('Strategy 2 ')
    st.markdown('''
            <p style="text-align:center; marginbottom:12px; margin-top:12px;"> 
            <img src="https://i.postimg.cc/1zFy3PXw/i2.png" class="img-fluid hover-shadow" height="144px" width="256" alt="Cinque Terre">
            </p>
            ''', unsafe_allow_html=True)
    st.button('Check Strategy', key='b2')
st.write('---')

c1, c2 = st.columns(2)
with c1:
    st.subheader('SRS 1')
    st.markdown('''
            <p style="text-align:center; marginbottom:12px; margin-top:12px;"> 
            <img src="https://i.postimg.cc/QtWXmf8b/i3.png" class="img-fluid hover-shadow" height="64px" width="64px" alt="Cinque Terre">
            </p>
            ''', unsafe_allow_html=True)
    st.button('Check Stocks', key='b3')
with c2:
    st.subheader('SRS 2 ')
    st.markdown('''
            <p style="text-align:center; marginbottom:12px; margin-top:12px;"> 
            <img src="https://i.postimg.cc/QtWXmf8b/i3.png" class="img-fluid hover-shadow" height="64px" width="64px" alt="Cinque Terre">
            </p>
            ''', unsafe_allow_html=True)
    st.button('Check Stocks', key='b4')
st.write('---')