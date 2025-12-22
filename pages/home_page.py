import streamlit as st

#Intro
st.title("Welcome to this :rainbow[Shift Cipher Decrypter]! :unlock:", anchor=False)
st.subheader("This web app is designed to decrypt messages that are encrypted with the Shift Cipher encryption method.", anchor=False)

#Navigate user
st.space("large")
st.header("Would you like to...", anchor=False)
col1, col2 = st.columns(2, gap="small")
with col1:
    st.page_link(page="pages/encrypter_page.py", label="**:blue-background[Try encrypting at the encrypter page]**", width="content")
with col2:
    st.page_link(page="pages/decrypter_page.py", label="**:blue-background[Try decrypting at the decrypter page]**", width="content")

#Remarks
st.divider()
st.markdown("""
            * This decrypter is designed to decrypt ***:red-background[English message only]***.

            * Please note that the ***:red-background[decryption results are reserved]*** because the algorithm must not be 100% accurate.

            * If you don't know what Shift Cipher encryption is, you can find more about it in this [Wikipedia Page](https://en.wikipedia.org/wiki/Caesar_cipher).
            """)

#Sidebar
st.sidebar.success("Get started with the tabs above!", icon=":material/arrow_upward:")