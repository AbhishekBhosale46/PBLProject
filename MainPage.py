import streamlit as st
from streamlit_lottie import st_lottie
from bokeh.models.widgets import Div
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
            margin-top: -15px
            }
            h3{
            text-align: center;
            font-size: 1.5rem;
            }
            .css-fg4pbf {
            text-align: center;
            }
            .css-1cpxqw2 {
            border-radius: 0.65rem;
            font-weight: 600;
            font-size: 15px;
            border: 1.5px solid rgba(49, 51, 63, 0.2);
            }
            </style>
            ''', unsafe_allow_html=True)


st.title(' 📈 ALGO ALERT 📉 ')
st.markdown('''
            <p style="text-align:center; marginbottom:10px; margin-top:10px;"> 
            <img src="https://i.postimg.cc/MKxNT9QQ/8432.jpg" class="img-fluid hover-shadow" height="243px" width="432px" alt="Cinque Terre">
            </p>
            ''', unsafe_allow_html=True)

st.info('STRATEGIES')
c1, c2 = st.columns(2)
with c1:
    st.subheader('Strategy 1 ')
    st.markdown('''
            <p style="text-align:center; marginbottom:12px; margin-top:12px;"> 
            <img src="https://i.postimg.cc/Dw2GGjLS/i1.png" class="img-fluid hover-shadow" height="144px" width="256" alt="Cinque Terre">
            </p>
            ''', unsafe_allow_html=True)
    if st.button('Check Strategy', key='b1'):
        #js = "window.open('https://www.streamlit.io/')"  # New tab or window
        js = "window.location.href = 'https://abhishekbhosale46-pblproject-main-strategy1-cih40i.streamlitapp.com/'"  # Current tab
        html = '<img src onerror="{}">'.format(js)
        div = Div(text=html)
        st.bokeh_chart(div)
with c2:
    st.subheader('Strategy 2 ')
    st.markdown('''
            <p style="text-align:center; marginbottom:12px; margin-top:12px;"> 
            <img src="https://i.postimg.cc/1zFy3PXw/i2.png" class="img-fluid hover-shadow" height="144px" width="256" alt="Cinque Terre">
            </p>
            ''', unsafe_allow_html=True)
    if st.button('Check Strategy', key='b2'):
        #js = "window.open('https://abhishekbhosale46-pblproject-main-strategy2-i6prxe.streamlitapp.com/')"  # New tab or window
        js = "window.location.href = 'https://abhishekbhosale46-pblproject-main-strategy2-i6prxe.streamlitapp.com/'"  # Current tab
        html = '<img src onerror="{}">'.format(js)
        div = Div(text=html)
        st.bokeh_chart(div)

st.info('STOCK RECOMMENDATION SYSTEMS')
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

st.info('RETURNS COMPARISON DASHBOARD')
st.subheader('Dashboard')
st.markdown('''
            <p style="text-align:center; marginbottom:12px; margin-top:12px;"> 
            <img src="https://i.postimg.cc/RZsj5YTf/i4.png" class="img-fluid hover-shadow" height="64px" width="64px" alt="Cinque Terre">
            </p>
            ''', unsafe_allow_html=True)
st.button('Show Dashboard', key='b5')
st.write('---')
st.error('Disclaimer : Trading in Stock Market, Currency or Commodity markets is risky and there is every chance of losing money.'
           ' One should only trade with a small portion of his or her money which he can afford to lose.')