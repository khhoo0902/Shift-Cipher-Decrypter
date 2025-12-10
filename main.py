import streamlit as st

st.set_page_config(
    page_title="Shift Cipher Decryptor",
    page_icon=":unlock:",
    initial_sidebar_state="expanded",
    menu_items={"About": "This web-based application was developed by :grey-background[Wong Ka Ho] with an open-sourced python library [**Streamlit**](https://github.com/streamlit/streamlit) to provide graphical user interface."}
)

pages = {
    "": [
        st.Page("pages/home_page.py", title="Get Started", icon=":material/home:")],
    "Tools": [
        st.Page("pages/encryptor_page.py", title="Encryptor", icon=":material/lock:"),
        st.Page("pages/decryptor_page.py", title="Decryptor", icon=":material/lock_open_right:")],
    "Other": [
        st.Page("pages/about_page.py", title="About", icon=":material/info:")]
}

pg = st.navigation(pages)
pg.run()