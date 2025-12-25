import streamlit as st
from random import randint
import encrypter
from time import sleep

st.set_page_config(page_title="Encrypter")
st.title("Encrypter :material/lock:", anchor=False)

sleep(0.2)

#Page init
lettercases = ("Uppercase", "Lowercase", "Adaptive")
if "encrypter_shift_randomly" not in st.session_state:
    st.session_state.encrypter_shift_randomly = True
if "encrypter_shift_value" not in st.session_state:
    st.session_state.encrypter_shift_value = 1
if "encrypter_lettercase" not in st.session_state:
    st.session_state.encrypter_lettercase = "Adaptive"
if "encrypter_remove_whitespace" not in st.session_state:
    st.session_state.encrypter_remove_whitespace = True
if "encrypter_original_text" not in st.session_state:
    st.session_state.encrypter_original_text = ""
if "encrypter_encrypted_text" not in st.session_state:
    st.session_state.encrypter_encrypted_text = ""

#functions
def clearOutput():
    st.session_state.encrypter_encrypted_text = ""

def validateInputText():
    isAscii = [ord(char) < 128 for char in st.session_state.encrypter_original_text]
    return all(isAscii)

#Sidebar
st.sidebar.title("Encrypter Settings")
st.session_state.encrypter_shift_randomly = st.sidebar.toggle("Shift Randomly :material/shuffle:", value=st.session_state.encrypter_shift_randomly, on_change=clearOutput)
if not st.session_state.encrypter_shift_randomly:
    st.session_state.encrypter_shift_value = st.sidebar.slider("**Shift** :material/swap_horiz:", 0, 25, st.session_state.encrypter_shift_value, on_change=clearOutput)
st.session_state.encrypter_lettercase = st.sidebar.radio("**Lettercase**", options=lettercases, index=lettercases.index(st.session_state.encrypter_lettercase), horizontal=True, on_change=clearOutput)
st.session_state.encrypter_remove_whitespace = st.sidebar.checkbox("Remove Whitespace", value=st.session_state.encrypter_remove_whitespace, on_change=clearOutput)

#Input
@st.dialog("Upload a text file")
def upload():
    file = st.file_uploader("Upload a text file", type="txt", accept_multiple_files=False, label_visibility="collapsed")
    if file is not None:
        st.toast("File uploaded!", icon=":material/upload:")
        with st.container(horizontal_alignment="center"):
            if st.button("Confirm :material/check:"):
                st.session_state.encrypter_original_text = file.getvalue().decode().strip("\n")
                clearOutput()
                st.rerun()

st.space("small")
st.write("**Original Text**")
st.session_state.encrypter_original_text = st.text_area("Oringinal Text", value=st.session_state.encrypter_original_text, on_change=clearOutput, height="content", placeholder="Enter text here.", label_visibility="collapsed").strip("\n")
col1, col2 = st.columns(2, vertical_alignment="center")
with col1:
    if st.button("Read from text file", icon=":material/article:"):
        upload()
with col2:
    st.markdown(f":grey-background[~ {len(st.session_state.encrypter_original_text.split())} words]", width="stretch", text_alignment="right")
st.space("small")

#Output
if st.button("**:green[Encrypt]**", use_container_width=True, disabled=False if st.session_state.encrypter_original_text != "" else True):
    if validateInputText():
        if st.session_state.encrypter_shift_randomly:
            st.session_state.encrypter_shift = randint(1, 25)
        else:
            st.session_state.encrypter_shift = st.session_state.encrypter_shift_value
        st.session_state.encrypter_encrypted_text = encrypter.encrypt(st.session_state.encrypter_original_text, st.session_state.encrypter_shift, st.session_state.encrypter_lettercase)
        if st.session_state.encrypter_remove_whitespace:
            st.session_state.encrypter_encrypted_text = st.session_state.encrypter_encrypted_text.strip()
    else: st.error("Unsupported languague or characters!", icon=":material/block:")
    
st.space("small")
if st.session_state.encrypter_encrypted_text != "":
    st.write(f"**Encrypted Text :blue-background[Shift = {st.session_state.encrypter_shift}]**")
    st.code(st.session_state.encrypter_encrypted_text, language=None, wrap_lines=True, height="content")
    with st.container(horizontal_alignment="right"):

        st.download_button("Download", icon=":material/download:", data=st.session_state.encrypter_encrypted_text, file_name=f"encrypted_text.txt")

