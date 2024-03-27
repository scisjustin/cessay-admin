from deta import Deta
import streamlit as st
import io

st.set_page_config(page_title='Check Student\'s Essay', page_icon='✏️')

with open('style.css', encoding='UTF-8') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

if 'download' not in st.session_state:
    st.session_state.download = False


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
