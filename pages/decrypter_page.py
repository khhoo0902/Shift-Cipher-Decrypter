import streamlit as st
import decrypter
from time import perf_counter

st.set_page_config(page_title="Decrypter")
st.title("Decrypter :material/lock_open_right:", anchor=False)

#Page init
METHODS = ("Shift Guessing", "Keywords Matching", "Manually Selecting")
LETTERCASES = ("Uppercase", "Lowercase", "Adaptive")
KEYWORDS = ("an", "am", "is", "it", "in", "on", "at", "as", "by", "to", "of", "for", "from", "the", "and")
if "decrypter_method" not in st.session_state:
    st.session_state.decrypter_method = "Keywords Matching"
if "decrypter_encrypted_text" not in st.session_state:
    st.session_state.decrypter_encrypted_text = ""
if "decrypter_lettercase" not in st.session_state:
    st.session_state.decrypter_lettercase = "Adaptive"
if "decrypter_remove_whitespace" not in st.session_state:
    st.session_state.decrypter_remove_whitespace = True
if "decrypter_confirmed_input" not in st.session_state:
    st.session_state.decrypter_confirmed_input = False
if "decrypter_shift" not in st.session_state:
    st.session_state.decrypter_shift = 0
if "decrypter_result_confirmed" not in st.session_state:
    st.session_state.decrypter_result_confirmed = False
if "decrypter_decrypted_text" not in st.session_state:
    st.session_state.decrypter_decrypted_text = ""
if "decrypter_letter_mode" not in st.session_state:
    st.session_state.decrypter_letter_mode = ""
if "decrypter_confidence" not in st.session_state:
    st.session_state.decrypter_confidence = 0
if "decrypter_keywords" not in st.session_state:
    st.session_state.decrypter_keywords = []
if "decrypter_matched_num" not in st.session_state:
    st.session_state.decrypter_matched_num = 0
if "decrypter_process_time" not in st.session_state:
    st.session_state.decrypter_process_time = 0

#functions
def clearOutput():
    st.session_state.decrypter_confirmed_input = False
    st.session_state.decrypter_shift = 0
    st.session_state.decrypter_result_confirmed = False
    st.session_state.decrypter_decrypted_text = ""

def validateInputText():
    isAscii = [ord(char) < 128 for char in st.session_state.decrypter_encrypted_text]
    return all(isAscii)

def haveText():
    return any([True if 65 <= ord(char) <= 90 or 97 <= ord(char) <= 122 else False for char in st.session_state.decrypter_encrypted_text])

#Sidebars
st.sidebar.title("Decrypter Settings")
st.session_state.decrypter_lettercase = st.sidebar.radio("**Lettercase**", options=LETTERCASES, index=LETTERCASES.index(st.session_state.decrypter_lettercase), horizontal=True, on_change=clearOutput)
st.session_state.decrypter_remove_whitespace = st.sidebar.checkbox("Remove Whitespace", value=st.session_state.decrypter_remove_whitespace, on_change=clearOutput)
st.session_state.decrypter_method = st.sidebar.radio("**Decrypt Method**", options=METHODS, index=METHODS.index(st.session_state.decrypter_method), on_change=clearOutput,
                                                        captions=("for long paragraphs, auto, fast, accurate", "for short/long paragraphs, auto, slower, more accurate", "for words/paragraphs, manually, biased"))
st.sidebar.divider()
if st.session_state.decrypter_method == "Keywords Matching":
    st.session_state.decrypter_keywords = st.sidebar.multiselect("**Keywords**", options=KEYWORDS, default=KEYWORDS, placeholder="Select or add keywords", accept_new_options=True, on_change=clearOutput)
if any([True if len(keyword) == 1 else False for keyword in st.session_state.decrypter_keywords]):
    st.sidebar.error("Single-character keywords will be ignored.")
    st.session_state.decrypter_keywords = [keyword for keyword in st.session_state.decrypter_keywords if len(keyword) > 1]

#Input
@st.dialog("Upload a text file")
def upload():
    file = st.file_uploader("Upload a text file", type="txt", accept_multiple_files=False, label_visibility="collapsed")
    if file is not None:
        st.toast("File uploaded!", icon=":material/upload:")
        with st.container(horizontal_alignment="center"):
            if st.button("Confirm :material/check:"):
                st.session_state.decrypter_encrypted_text = file.getvalue().decode().strip("\n")
                clearOutput()
                st.rerun()

st.space("small")
st.write("**Encrypted Text**")
st.session_state.decrypter_encrypted_text = st.text_area("Encrypted Text", value=st.session_state.decrypter_encrypted_text, on_change=clearOutput, height="content", placeholder="Enter the encrypted text here.", label_visibility="collapsed").strip("\n")
col1, col2 = st.columns(2, vertical_alignment="center")
with col1:
    if st.button("Read from text file", icon=":material/article:"):
        upload()
with col2:
    st.markdown(f":grey-background[~ {len(st.session_state.decrypter_encrypted_text.split())} words]", width="stretch", text_alignment="right")
st.space("small")

#Output
if st.button("**:green[Confirm]**" if st.session_state.decrypter_method == "Manually Selecting" else "**:green[Decrypt]**", use_container_width=True, disabled=False if st.session_state.decrypter_encrypted_text != "" and not st.session_state.decrypter_confirmed_input else True):
    if validateInputText():
        if haveText():
            st.session_state.decrypter_confirmed_input = True
            st.rerun()
        else: st.error("No alphabet inside the text!", icon=":material/block:")
    else: st.error("Unsupported languague or characters!", icon=":material/block:")

st.space("small")
if st.session_state.decrypter_confirmed_input:

    if st.session_state.decrypter_method == "Shift Guessing":
        if st.session_state.decrypter_decrypted_text == "":
            start = perf_counter()
            st.session_state.decrypter_letter_mode, st.session_state.decrypter_shift, st.session_state.decrypter_confidence, st.session_state.decrypter_decrypted_text = decrypter.guessShift(st.session_state.decrypter_encrypted_text, st.session_state.decrypter_lettercase)
            if st.session_state.decrypter_remove_whitespace:
                st.session_state.decrypter_decrypted_text = st.session_state.decrypter_decrypted_text.strip()
            st.session_state.decrypter_process_time = (perf_counter() - start) * 1000
        st.success(f"Decrypted with {st.session_state.decrypter_process_time: .3f} ms.")
        st.write("**Analysis**")
        col1, col2, col3 = st.columns(3, border=True)
        with col1:
            st.write(f"**Most frequent letter is :blue-background['{st.session_state.decrypter_letter_mode}']**")
        with col2:
            st.write(f"**:blue-background['E' -> '{st.session_state.decrypter_letter_mode}']**")
        with col3:
            st.write(f"**:blue-background[Shift = {st.session_state.decrypter_shift}]**")
        st.write(f"**:{"green" if st.session_state.decrypter_confidence >= 70 else "red"}-background[Confidence: {st.session_state.decrypter_confidence}%]**")
        st.code(st.session_state.decrypter_decrypted_text, language=None, wrap_lines=True, height="content")
        with st.container(horizontal_alignment="right"):
            st.download_button("Download", icon=":material/download:", data=st.session_state.decrypter_decrypted_text, file_name=f"decrypted_text.txt")

    elif st.session_state.decrypter_method == "Keywords Matching":
        if st.session_state.decrypter_keywords != []:
            if st.session_state.decrypter_decrypted_text == "":
                start = perf_counter()
                st.session_state.decrypter_shift, st.session_state.decrypter_confidence, st.session_state.decrypter_matched_num, st.session_state.decrypter_decrypted_text = decrypter.matchKeywords(st.session_state.decrypter_encrypted_text, st.session_state.decrypter_keywords, st.session_state.decrypter_lettercase)
                if st.session_state.decrypter_remove_whitespace:
                    st.session_state.decrypter_decrypted_text = st.session_state.decrypter_decrypted_text.strip()
                st.session_state.decrypter_process_time = (perf_counter() - start) * 1000
            st.success(f"Decrypted with {st.session_state.decrypter_process_time: .3f} ms.")
            st.write("**Analysis**")
            col1, col2 = st.columns(2, border=True)
            with col1:
                st.write(f"**:blue-background[Shift = {st.session_state.decrypter_shift}]**")
            with col2:
                st.write(f"Matched **:blue-background[{st.session_state.decrypter_matched_num} keywords]**")
            st.write(f"**:{"green" if st.session_state.decrypter_confidence >= 70 else "red"}-background[Confidence: {st.session_state.decrypter_confidence}%]**")
            st.code(st.session_state.decrypter_decrypted_text, language=None, wrap_lines=True, height="content")
            with st.container(horizontal_alignment="right"):
                st.download_button("Download", icon=":material/download:", data=st.session_state.decrypter_decrypted_text, file_name=f"decrypted_text.txt")
        else: st.error("No keywords provided!", icon=":material/back_hand:")

    elif st.session_state.decrypter_method == "Manually Selecting":
        if st.session_state.decrypter_result_confirmed:
            st.success("Decrypted!")
        st.write(f"**:blue-background[Shift = {st.session_state.decrypter_shift}]**")
        st.session_state.decrypter_decrypted_text = decrypter.reverseShiftText(st.session_state.decrypter_encrypted_text, st.session_state.decrypter_shift, st.session_state.decrypter_lettercase)
        if st.session_state.decrypter_remove_whitespace:
            st.session_state.decrypter_decrypted_text = st.session_state.decrypter_decrypted_text.strip()
        st.code(st.session_state.decrypter_decrypted_text, language=None, height="content", wrap_lines=st.session_state.decrypter_result_confirmed)
        if st.session_state.decrypter_result_confirmed: 
            with st.container(horizontal_alignment="right"):
                st.download_button("Download", icon=":material/download:", data=st.session_state.decrypter_decrypted_text, file_name=f"decrypted_text.txt")
        if not st.session_state.decrypter_result_confirmed:
            col1, col2, col3 = st.columns([2,2,1])
            with col1:
                if st.button("⬅️ Previous", use_container_width=True):
                    st.session_state.decrypter_shift = 25 if st.session_state.decrypter_shift == 0 else st.session_state.decrypter_shift - 1
                    st.rerun()
            with col2:
                if st.button("➡️ Next", use_container_width=True):
                    st.session_state.decrypter_shift = (st.session_state.decrypter_shift + 1) % 26
                    st.rerun()
            with col3:
                if st.button("✅ Correct", use_container_width=True):
                    st.session_state.decrypter_result_confirmed = True
                    st.rerun()
