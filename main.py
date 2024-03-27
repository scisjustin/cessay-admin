from deta import Deta
import streamlit as st
import io
from streamlit_cookies_manager import EncryptedCookieManager
import os

st.set_page_config(page_title='Check Student\'s Essay', page_icon='✏️')

cookies = EncryptedCookieManager(
    prefix="is_logged_in",
    password=os.environ.get("COOKIES_PASSWORD", "My secret password"),
)

# 쿠키가 로도 될때까지 기다리기
if not cookies.ready():
    st.stop()

def Cookies_Login():
    cookies['is_logged_in'] = 'True'
    cookies.save()
    st.rerun()

def Cookies_Logout():
    cookies['is_logged_in'] = 'False'
    cookies.save()
    st.rerun()

try:
    if 'True' == cookies['is_logged_in']:
        is_logged_in = True
    elif 'False' == cookies['is_logged_in']:
        is_logged_in = False
except:
    Cookies_Logout()

with open('style.css', encoding='UTF-8') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

if 'download' not in st.session_state:
    st.session_state.download = False

if is_logged_in == True:
    st.title('Check Student\'s Essay')
    st.divider()

    if st.session_state.download == False:
        DETA_KEY = 'c0ki5D3avML_gSssDuj33rfuzLDrjwL1gc42oQkbgsHj'
        deta = Deta(DETA_KEY)
        db = deta.Drive("Write_Your_Essay")

        response = db.list()["names"]

        for x in response:
            if st.button(x, use_container_width=1):
                st.session_state.target = x
                st.session_state.download = True
                st.rerun()
                        

    elif st.session_state.download == True:
        DETA_KEY = 'c0ki5D3avML_gSssDuj33rfuzLDrjwL1gc42oQkbgsHj'
        deta = Deta(DETA_KEY)
        db = deta.Drive("Write_Your_Essay")

        response = db.list()["names"]

        file = db.get(st.session_state.target)
        file_stream = io.BytesIO(file.read())
        st.success('Successfully Loaded')
        st.download_button(label=f"**Download :blue[{st.session_state.target}]**",
                        data=file_stream,
                        file_name=st.session_state.target,
                        mime='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        if st.button('Go Back to Main Page'):
            st.session_state.download = False
            st.rerun()
        
else:
    master_password = st.text_input('Stem Class 학생들의 Essay를 확인하시려면 비밀번호를 입력해야 합니다.', type='password')
    if master_password == '강예건은 잘생겼다':
        Cookies_Login()