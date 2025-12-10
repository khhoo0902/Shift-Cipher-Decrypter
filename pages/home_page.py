import streamlit as st

st.sidebar.success("Start with the tabs above!")

st.title("Welcome to this :rainbow[Shift Cipher decryptor]! :unlock:", anchor=False)
st.subheader("This web app is designed to decrypt messages that are encrypted with the Shift Cipher encryption method.", anchor=False)

st.space("large")
st.header("Would you like to...", anchor=False)
left, right = st.columns(2, gap="small")
with left:
    st.page_link(page="pages/encryptor_page.py", label="**:blue-background[Try encrypting at the encrypter page]**", width="content")
with right:
    st.page_link(page="pages/decryptor_page.py", label="**:blue-background[Try decrypting at the decrypter page]**", width="content")

st.divider()
st.markdown("""
            * Please note that the *:red-background[decryption results are reserved]* because the algorithm must not be 100% accurate.

            * If you don't know what Shift Cipher encryption is, you can find more about it in this [Wikipedia Page](https://en.wikipedia.org/wiki/Caesar_cipher).
            """)
